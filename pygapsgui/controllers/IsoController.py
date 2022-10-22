from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

import pygaps
from pygaps.units.converter_mode import _LOADING_MODE
from pygaps.units.converter_mode import _MATERIAL_MODE
from pygaps.units.converter_mode import _PRESSURE_MODE
from pygaps.units.converter_unit import _TEMPERATURE_UNITS
from pygaps.utilities import exceptions as pge
from pygapsgui.models.IsoModel import IsoModel
from pygapsgui.widgets.UtilityDialogs import error_dialog


class IsoController():
    """
    Interface between Isotherms loaded in memory and main window Isotherm views.

    The Isotherm List Model is the collection of isotherms that have been loaded
    in memory, which are stored in a custom QT QStandardItemModel.

    The main window has various views into this collection, such as:

        - displaying a list of all isotherms (iso_explorer)
        - displaying metadata and unit for a selected isotherm (iso_details)
        - plotting one or more selected isotherms (iso_graph)

    """
    iso_current = None

    def __init__(self, main_window, iso_list_model):
        """Connect the MVC architecture."""

        # Store refs to main widgets
        self.mw_widget = main_window
        self.unit_widget = main_window.prop_unit_widget
        self.list_view = main_window.iso_explorer
        self.graph_view = main_window.iso_graph

        # Store ref to model and define other models
        self.iso_list_model = iso_list_model
        self.metadata_table_model = None

        # Connect model/view
        self.list_view.setModel(self.iso_list_model)
        self.graph_view.setModel(self.iso_list_model)

        # populate adsorbates and materials
        self.mw_widget.material_input.insertItems(0, [mat.name for mat in pygaps.MATERIAL_LIST])
        self.mw_widget.adsorbate_input.insertItems(0, [ads.name for ads in pygaps.ADSORBATE_LIST])

        # populate units view
        self.unit_widget.init_boxes(
            _PRESSURE_MODE,
            _LOADING_MODE,
            _MATERIAL_MODE,
            _TEMPERATURE_UNITS,
        )

        # signals between all model/views
        self.connect_signals()

    def connect_signals(self):
        """Connect permanent signals."""

        # Connect signals for iso explorer
        selection_model = self.list_view.selectionModel()
        selection_model.currentChanged.connect(self.selection_changed)
        selection_model.currentChanged.connect(self.iso_list_model.handle_item_select)
        self.mw_widget.exp_select_button.clicked.connect(self.iso_list_model.check_all)
        self.mw_widget.exp_deselect_button.clicked.connect(self.iso_list_model.uncheck_all)
        self.mw_widget.exp_remove_button.clicked.connect(self.delete_current_iso)

        # Connect signals for iso details
        self.mw_widget.material_input.lineEdit().editingFinished.connect(self.modify_iso_baseprops)
        self.mw_widget.adsorbate_input.lineEdit().editingFinished.connect(self.modify_iso_baseprops)
        self.mw_widget.temperature_input.editingFinished.connect(self.modify_iso_baseprops)
        self.mw_widget.data_button.clicked.connect(self.iso_display_data)
        self.mw_widget.material_details.clicked.connect(self.material_detail)
        self.mw_widget.adsorbate_details.clicked.connect(self.adsorbate_detail)
        self.mw_widget.prop_extra_edit_widget.changed.connect(self.handle_metadata_changed)

        # Connect signals for iso graph
        self.unit_widget.pressure_changed.connect(self.modify_iso_p_units)
        self.unit_widget.loading_changed.connect(self.modify_iso_l_units)
        self.unit_widget.material_changed.connect(self.modify_iso_m_units)
        self.unit_widget.temperature_changed.connect(self.modify_iso_t_units)

    ########################################################
    # Display functionality
    ########################################################

    def selection_changed(self, current, previous):
        """Do when selected isotherm has changed."""
        if not current.isValid():
            self.iso_current = None
            self.clear_iso_display()
            return

        # Otherwise save and display the isotherm
        self.iso_current = self.iso_list_model.itemFromIndex(current).data()
        self.iso_display_properties()

    def iso_display_properties(self):
        """Populate widgets with the selected isotherm data."""
        if self.iso_current is None:
            return

        # Essential metadata
        self.mw_widget.material_input.setCurrentText(str(self.iso_current.material))
        self.mw_widget.adsorbate_input.setCurrentText(str(self.iso_current.adsorbate))
        self.mw_widget.temperature_input.setValue(self.iso_current._temperature)

        # Units setup
        self.unit_widget.init_units(self.iso_current)

        # Other isotherm metadata
        self.mw_widget.prop_extra_edit_widget.set_model(self.iso_current)

        # Model/Point specific
        if isinstance(self.iso_current, pygaps.ModelIsotherm):
            self.mw_widget.data_button.setText("Isotherm Parameters")
        elif isinstance(self.iso_current, pygaps.PointIsotherm):
            self.mw_widget.data_button.setText("Isotherm Points")

    def iso_display_update(self):
        """Update all the isotherm display."""
        self.iso_display_properties()
        self.graph_view.update()

    def clear_iso_display(self):
        """Reset all the display."""
        # Essential metadata
        self.mw_widget.material_input.lineEdit().clear()
        self.mw_widget.adsorbate_input.lineEdit().clear()
        self.mw_widget.temperature_input.clear()

        # Units
        self.unit_widget.clear()

        # Other metadata
        self.mw_widget.prop_extra_edit_widget.clear()
        self.metadata_table_model.deleteLater()

        # Graph
        self.graph_view.update()

    def modify_iso_p_units(self, mode_to, unit_to):
        """Convert current isotherm pressure."""
        if not self.iso_current:
            return
        try:
            self.iso_current.convert_pressure(mode_to=mode_to, unit_to=unit_to)
        except Exception as err:
            error_dialog(
                "Cannot convert relative pressure. Common causes are supercritical "
                "adsorbates or those without a thermodynamic backend. If "
                "the isotherm adsorbate does not have a thermodynamic backend, "
                "add a metadata named 'saturation_pressure' with a known value."
            )
        self.iso_display_update()  # not efficient but guarantees a full refresh

    def modify_iso_l_units(self, basis_to, unit_to):
        """Convert current isotherm loading."""
        if not self.iso_current:
            return
        try:
            self.iso_current.convert_loading(basis_to=basis_to, unit_to=unit_to)
        except Exception as err:
            if basis_to == "volume":
                error_dialog(
                    "Cannot convert loading. Common causes are supercritical "
                    "adsorbates or those without a thermodynamic backend. If "
                    "the isotherm adsorbate does not have a thermodynamic backend, "
                    "add a metadata named 'gas_density' with a known value."
                )
            elif basis_to == "molar":
                error_dialog(
                    "Cannot convert loading. Common causes are without a "
                    "thermodynamic backend. If "
                    "the isotherm adsorbate does not have a thermodynamic backend, "
                    "add a metadata named 'molar_mass' with a known value."
                )
            else:
                raise Exception from err
        self.iso_display_update()  # not efficient but guarantees a full refresh

    def modify_iso_m_units(self, basis_to, unit_to):
        """Convert current isotherm material basis/unit."""
        if not self.iso_current:
            return
        try:
            self.iso_current.convert_material(basis_to=basis_to, unit_to=unit_to)
        except Exception as err:
            if basis_to == "volume":
                msg = "Could not convert material to a volume basis. Does it have a density set?"
            elif basis_to == "molar":
                msg = "Could not convert material to a molar basis. Does it have a molar_mass set?"
            else:
                raise Exception from err
            error_dialog(msg)
        self.iso_display_update()  # not efficient but guarantees a full refresh

    def modify_iso_t_units(self, unit_to):
        """Convert current isotherm temperature."""
        if not self.iso_current:
            return
        self.iso_current.convert_temperature(unit_to=unit_to)
        self.iso_display_update()  # not efficient but guarantees a full refresh

    def modify_iso_baseprops(self):
        """Modify one of the current isotherm base properties (material/adsorbate/temperature)."""
        if not self.iso_current:
            return
        isotherm = self.iso_current
        modified = False

        if isotherm.material != self.mw_widget.material_input.lineEdit().text():
            isotherm.material = self.mw_widget.material_input.lineEdit().text()
            self.mw_widget.statusbar.showMessage(f'Material modified to {isotherm.material}', 2000)
            self.refresh_material_edit(isotherm.material.name)
            modified = True

        if isotherm.adsorbate != self.mw_widget.adsorbate_input.lineEdit().text():
            isotherm.adsorbate = self.mw_widget.adsorbate_input.lineEdit().text()
            self.mw_widget.statusbar.showMessage(
                f'Adsorbate modified to {isotherm.adsorbate}', 2000
            )
            modified = True

        if isotherm.temperature != self.mw_widget.temperature_input.value():
            isotherm.temperature = self.mw_widget.temperature_input.value()
            self.mw_widget.statusbar.showMessage(
                f'Temperature modified to {isotherm.temperature}', 2000
            )
            modified = True

        if modified:
            # We need to recalculate units
            self.unit_widget.init_units(self.iso_current)
            # And refresh graph
            self.graph_view.update()

    def material_detail(self):
        """Bring up widget with current isotherm material details."""
        if not self.iso_current:
            return
        from pygapsgui.views.MaterialView import MaterialDialog
        dialog = MaterialDialog(
            self.iso_current.material,
            parent=self.mw_widget.central_widget,
        )
        dialog.material_changed.connect(self.handle_material_changed)
        dialog.exec()

    def handle_material_changed(self, material):
        """Ensure refreshes when material changes."""
        self.iso_display_update()
        self.refresh_material_edit(material)

    def refresh_material_edit(self, material=None):
        """Reload material list from database."""
        self.mw_widget.material_input.clear()
        self.mw_widget.material_input.insertItems(0, [mat.name for mat in pygaps.MATERIAL_LIST])
        if material:
            self.mw_widget.material_input.setCurrentText(material)

    def adsorbate_detail(self):
        """Bring up widget with current isotherm adsorbate details."""
        if not self.iso_current:
            return
        from pygapsgui.views.AdsorbateView import AdsorbateDialog
        dialog = AdsorbateDialog(
            self.iso_current.adsorbate,
            parent=self.mw_widget.central_widget,
        )
        dialog.adsorbate_changed.connect(self.handle_adsorbate_changed)
        dialog.exec()

    def handle_adsorbate_changed(self, adsorbate):
        """Ensure refreshes when adsorbate changes."""
        self.iso_display_update()

    def handle_metadata_changed(self):
        """Save a metadata point."""
        self.mw_widget.statusbar.showMessage("Metadata changed successfully.", 2000)

    def metadata_save_bulk(self, results: dict):
        """Save multiple metadatas from a dictionary."""
        self.mw_widget.prop_extra_edit_widget.metadata_save_bulk(results)
        self.mw_widget.statusbar.showMessage("Saved results as metadata.")

    def iso_display_data(self):
        """Bring up widget with current isotherm data."""
        if not self.iso_current:
            return

        if isinstance(self.iso_current, pygaps.PointIsotherm):
            from pygapsgui.views.IsoEditPointDialog import IsoEditPointDialog
            dialog = IsoEditPointDialog(self.iso_current, parent=self.mw_widget.central_widget)
        elif isinstance(self.iso_current, pygaps.ModelIsotherm):
            from pygapsgui.views.IsoEditModelDialog import IsoEditModelDialog
            dialog = IsoEditModelDialog(self.iso_current, parent=self.mw_widget.central_widget)

        dialog.exec()
        self.iso_display_update()

    ########################################################
    # Add and remove functionality
    ########################################################

    def load(self, path, name, ext):
        """Use pygaps parsing to load an isotherm and add it to the model."""

        isotherm = None

        import pygaps.parsing as pgp
        if ext == '.csv':
            isotherm = pgp.isotherm_from_csv(path)
        elif ext == '.json':
            isotherm = pgp.isotherm_from_json(path)
        elif ext == '.xls':
            isotherm = pgp.isotherm_from_xl(path)
        elif ext == '.aif':
            isotherm = pgp.isotherm_from_aif(path)
        else:
            raise Exception(f"Unknown isotherm type '{ext}'.")

        if not isotherm:
            return

        self.add_isotherm(name, isotherm)

    def load_import(self, path, name, settings):
        """Use pygaps parsing to import an isotherm and add it to the model."""
        isotherm = None

        import pygaps.parsing as pgp
        try:
            isotherm = pgp.isotherm_from_commercial(path=path, **settings)
        except pge.ParsingError as exc:
            error_dialog(str(exc))
        except BaseException as exc:
            error_dialog(str(exc))

        if not isotherm:
            return

        self.add_isotherm(name, isotherm)

    def add_isotherm(self, name, isotherm):
        """Wrap an isotherm in an IsoModel and add to the IsothermListModel."""

        # Add adsorbates to the list
        if isotherm.material not in pygaps.MATERIAL_LIST:
            pygaps.MATERIAL_LIST.append(isotherm.material)
            self.refresh_material_edit(isotherm.material.name)

        # Create the model to store the isotherm
        iso_model = IsoModel(name)
        # store data
        iso_model.setData(isotherm)
        # Add to the list model
        self.iso_list_model.appendRow(iso_model)

    def save(self, path, ext):
        """Save isotherm to disk."""
        isotherm = self.iso_current

        import pygaps.parsing as pgp
        if ext == '.csv':
            pgp.isotherm_to_csv(isotherm, path)
        elif ext == '.json':
            pgp.isotherm_to_json(isotherm, path)
        elif ext in ['.xls', '.xlsx']:
            pgp.isotherm_to_xl(isotherm, path)
        elif ext == '.aif':
            pgp.isotherm_to_aif(isotherm, path)
        else:
            raise Exception("Unknown file save format.")

    ########################################################
    # Selecting, deleting, isotherms from list
    ########################################################

    def select_last_iso(self):
        """Select last isotherm"""
        last_iso = self.iso_list_model.index(self.iso_list_model.rowCount() - 1, 0)
        self.list_view.setCurrentIndex(last_iso)

    def delete_current_iso(self):
        """Remove current isotherm from model."""
        self.iso_list_model.removeRow(self.list_view.currentIndex().row())
