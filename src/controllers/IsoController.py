import pygaps
from pygaps.utilities.converter_mode import _PRESSURE_MODE, _LOADING_MODE, _MATERIAL_MODE
from pygaps.utilities.converter_unit import _TEMPERATURE_UNITS

from qtpy import QtWidgets as QW

from src.models.IsoModel import IsoModel
from src.models.IsoPropTableModel import IsoPropTableModel
from src.widgets.UtilityWidgets import error_dialog


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
        self.mw_widget.prop_extra_edit_widget.save_button.clicked.connect(self.metadata_save)
        self.mw_widget.prop_extra_edit_widget.delete_button.clicked.connect(self.metadata_delete)
        self.mw_widget.material_details.clicked.connect(self.material_detail)
        self.mw_widget.adsorbate_details.clicked.connect(self.adsorbate_detail)

        # Connect signals for iso graph
        self.unit_widget.pressure_changed.connect(self.modify_iso_pressure)
        self.unit_widget.loading_changed.connect(self.modify_iso_loading)
        self.unit_widget.material_changed.connect(self.modify_iso_materialunit)
        self.unit_widget.temperature_changed.connect(self.modify_iso_temperature)

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
        self.mw_widget.temperature_input.setText(f"{self.iso_current._temperature:g}")

        # Units setup
        self.unit_widget.init_units(self.iso_current)

        # Other isotherm metadata
        self.metadata_table_model = IsoPropTableModel(self.iso_current)
        self.mw_widget.metadata_table_view.setModel(self.metadata_table_model)
        self.mw_widget.metadata_table_view.selectionModel().selectionChanged.connect(
            self.metadata_select
        )

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

    def modify_iso_pressure(self, mode_to, unit_to):
        """Convert current isotherm pressure."""
        if not self.iso_current:
            return
        try:
            self.iso_current.convert_pressure(mode_to=mode_to, unit_to=unit_to)
        except Exception as ex:
            error_dialog(
                "Cannot convert relative pressure. Common causes are supercritical "
                "adsorbates or those without a thermodynamic backend. If "
                "the isotherm adsorbate does not have a thermodynamic backend, "
                "add a metadata named 'saturation_pressure' with a known value."
            )
        self.iso_display_update()  # not efficient but guarantees a full refresh

    def modify_iso_loading(self, basis_to, unit_to):
        """Convert current isotherm loading."""
        if not self.iso_current:
            return
        try:
            self.iso_current.convert_loading(basis_to=basis_to, unit_to=unit_to)
        except Exception as ex:
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
                raise Exception from ex
        self.iso_display_update()  # not efficient but guarantees a full refresh

    def modify_iso_materialunit(self, basis_to, unit_to):
        """Convert current isotherm material basis/unit."""
        if not self.iso_current:
            return
        try:
            self.iso_current.convert_material(basis_to=basis_to, unit_to=unit_to)
        except Exception as ex:
            if basis_to == "volume":
                msg = "Could not convert material to a volume basis. Does it have a density set?"
            elif basis_to == "molar":
                msg = "Could not convert material to a molar basis. Does it have a molar_mass set?"
            else:
                raise Exception from ex
            error_dialog(msg)
        self.iso_display_update()  # not efficient but guarantees a full refresh

    def modify_iso_temperature(self, unit_to):
        """Convert current isotherm temperature."""
        if not self.iso_current:
            return
        self.iso_current.convert_temperature(unit_to=unit_to)
        self.iso_display_update()  # not efficient but guarantees a full refresh

    def modify_iso_baseprops(self):
        """Modify one of the current isotherm base properties (material/adsorbate/temperature)."""
        isotherm = self.iso_current
        modified = False

        if isotherm.material != self.mw_widget.material_input.lineEdit().text():
            isotherm.material = self.mw_widget.material_input.lineEdit().text()
            self.mw_widget.statusbar.showMessage(f'Material modified to {isotherm.material}', 2000)
            self.refresh_material_edit()
            modified = True

        if isotherm.adsorbate != self.mw_widget.adsorbate_input.lineEdit().text():
            isotherm.adsorbate = self.mw_widget.adsorbate_input.lineEdit().text()
            self.mw_widget.statusbar.showMessage(
                f'Adsorbate modified to {isotherm.adsorbate}', 2000
            )
            modified = True

        if isotherm.temperature != float(self.mw_widget.temperature_input.text()):
            isotherm.temperature = float(self.mw_widget.temperature_input.text())
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
        from src.views.MaterialView import MaterialDialog
        dialog = MaterialDialog(
            self.iso_current.material,
            parent=self.mw_widget.central_widget,
        )
        ret = dialog.exec()
        if ret == QW.QDialog.Accepted:
            self.iso_display_update()

    def adsorbate_detail(self):
        """Bring up widget with current isotherm adsorbate details."""
        if not self.iso_current:
            return
        from src.views.AdsorbateView import AdsorbateDialog
        dialog = AdsorbateDialog(
            self.iso_current.adsorbate,
            parent=self.mw_widget.central_widget,
        )
        ret = dialog.exec()
        if ret == QW.QDialog.Accepted:
            self.iso_display_update()

    def metadata_select(self):
        """Update display when a metadata point is selected."""
        index = self.mw_widget.metadata_table_view.selectionModel().currentIndex()
        if not index.isValid():
            return
        data = self.metadata_table_model.rowData(index)
        self.mw_widget.prop_extra_edit_widget.display(*data)

    def metadata_save(self):
        """Save a metadata point."""
        meta_name = self.mw_widget.prop_extra_edit_widget.name_input.text()
        meta_value = self.mw_widget.prop_extra_edit_widget.value_input.text()
        meta_type = self.mw_widget.prop_extra_edit_widget.type_input.currentText()
        if not meta_name:
            self.mw_widget.statusbar.showMessage("Fill property name!", 2000)
            return
        if not meta_value:
            self.mw_widget.statusbar.showMessage("Fill property value!", 2000)
            return

        if meta_type == "number":
            try:
                meta_value = float(meta_type)
            except ValueError:
                error_dialog("Could not convert metadata value to number.")
                return

        self.metadata_table_model.setOrInsertRow(data=[meta_name, meta_value, meta_type])
        self.mw_widget.statusbar.showMessage(f"Added property named {meta_name}")
        self.mw_widget.metadata_table_view.resizeColumns()

    def metadata_delete(self):
        """Delete a metadata point."""
        index = self.mw_widget.metadata_table_view.selectionModel().currentIndex()
        if not index.isValid():
            return
        self.metadata_table_model.removeRow(index.row())
        self.mw_widget.statusbar.showMessage(f"Deleted property named {index}")

    def iso_display_data(self):
        """Bring up widget with current isotherm data."""
        if not self.iso_current:
            return
        ret = 0

        if isinstance(self.iso_current, pygaps.PointIsotherm):
            from src.views.IsoDataDialog import IsoDataDialog
            from src.models.IsoDataTableModel import IsoDataTableModel
            model = IsoDataTableModel(self.iso_current.data())
            dialog = IsoDataDialog(parent=self.mw_widget.central_widget)
            dialog.table_view.setModel(model)
            ret = dialog.exec()
        elif isinstance(self.iso_current, pygaps.ModelIsotherm):
            #TODO implement viewer for modelisotherms
            pass

        if ret == QW.QDialog.Accepted:
            self.iso_display_update()

    def refresh_material_edit(self):
        # TODO change how materials are handled and updated
        # due to errors in editing during isotherm edits
        self.mw_widget.material_input.clear()
        self.mw_widget.material_input.insertItems(0, [mat.name for mat in pygaps.MATERIAL_LIST])

    ########################################################
    # Add and remove functionality
    ########################################################

    def load(self, path, name, ext):
        """Load isotherm from disk."""

        isotherm = None

        import pygaps.parsing as pgp
        if ext == '.csv':
            isotherm = pgp.isotherm_from_csv(path)
        elif ext == '.json':
            isotherm = pgp.isotherm_from_json(path)
        elif ext in ['.xls', '.xlsx']:
            isotherm = pgp.isotherm_from_xl(path)
        elif ext == '.aif':
            isotherm = pgp.isotherm_from_aif(path)
        else:
            raise Exception(f"Unknown isotherm type '{ext}'.")

        if not isotherm:
            return

        self.add_isotherm(name, isotherm)

    def load_import(self, path, name, iso_type):
        isotherm = None

        import pygaps.parsing as pgp
        if iso_type == 0:  # bel raw
            isotherm = pgp.isotherm_from_bel(path)
        elif iso_type == 1:  # bel report
            isotherm = pgp.isotherm_from_xl(path, fmt='bel')
        elif iso_type == 2:  # mic report
            isotherm = pgp.isotherm_from_xl(path, fmt='mic')
        elif iso_type == 3:  # qnt report
            isotherm = pgp.isotherm_from_xl(path, fmt='qnt')
            # TODO implement Quantachrome report
        elif iso_type == 4:  # 3P report:
            isotherm = pgp.isotherm_from_xl(path, fmt='3p')
            # TODO implement 3p report
        else:
            raise Exception(f"Could not determine import type '{iso_type}'.")

        if not isotherm:
            return

        self.add_isotherm(name, isotherm)

    def add_isotherm(self, name, isotherm):

        # Add adsorbates to the list
        if isotherm.material not in pygaps.MATERIAL_LIST:
            pygaps.MATERIAL_LIST.append(isotherm.material)
            self.refresh_material_edit()

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
