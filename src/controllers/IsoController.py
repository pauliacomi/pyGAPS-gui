import pygaps
from pygaps.utilities.converter_mode import _PRESSURE_MODE, _LOADING_MODE, _MATERIAL_MODE
from pygaps.utilities.converter_unit import _TEMPERATURE_UNITS

from src.models.IsoModel import IsoModel
from src.models.IsoPropTableModel import IsoPropTableModel


class IsoController():
    """
    Interface between the Isotherm Models (list, single) and main window Isotherm views.

    The Isotherm List Model is the collection of isotherms that have been loaded
    in memory, which are stored in a custom QT QStandardItemModel.

    The main window has various views into this collection, such as:

        - displaying a list of all isotherms (IsoExplorer)
        - displaying metadata and unit for a selected isotherm (IsoDetails)
        - plotting one or more selected isotherms (IsoGraph)

    This is also the only place where the pygaps package is imported and used
    for the main window.

    """
    def __init__(self, mainWindowWidget, listModel):
        """Connect the MVC architecture."""

        self.mw_widget = mainWindowWidget
        self.unit_widget = mainWindowWidget.unitPropButtonWidget
        self.list_view = mainWindowWidget.isoExplorer
        self.graph_view = mainWindowWidget.isoGraph

        self.iso_list_model = listModel

        self.list_view.setModel(self.iso_list_model)
        self.graph_view.setModel(self.iso_list_model)

        # populate
        self.mw_widget.materialEdit.insertItems(0, [mat.name for mat in pygaps.MATERIAL_LIST])
        self.mw_widget.adsorbateEdit.insertItems(0, [ads.name for ads in pygaps.ADSORBATE_LIST])
        # populate unit view
        self.unit_widget.temperatureUnit = self.mw_widget.temperatureUnit
        self.unit_widget.init_boxes(_PRESSURE_MODE, _LOADING_MODE, _MATERIAL_MODE)

        # signals between all model/views
        self.connectSignals()

    def connectSignals(self):

        # Connect signals for list view
        self.list_view.selectionModel().currentChanged.connect(self.selection_changed)
        self.list_view.delete_current_iso.connect(self.delete_current_iso)

        self.mw_widget.selectAllButton.clicked.connect(self.iso_list_model.tick_all)
        self.mw_widget.deselectAllButton.clicked.connect(self.iso_list_model.untick_all)
        self.mw_widget.removeButton.clicked.connect(self.delete_current_iso)

        # Create isotherm data view
        self.mw_widget.materialEdit.lineEdit().editingFinished.connect(self.modify_iso_baseprops)
        self.mw_widget.adsorbateEdit.lineEdit().editingFinished.connect(self.modify_iso_baseprops)
        self.mw_widget.temperatureEdit.editingFinished.connect(self.modify_iso_baseprops)
        self.mw_widget.temperatureUnit.currentIndexChanged.connect(self.modify_iso_baseprops)
        self.mw_widget.dataButton.clicked.connect(self.display_iso_data)

        # Setup property signals
        self.mw_widget.extraPropButtonWidget.propButtonAdd.clicked.connect(self.extra_prop_add)
        self.mw_widget.extraPropButtonWidget.propButtonEdit.clicked.connect(self.extra_prop_edit)
        self.mw_widget.extraPropButtonWidget.propButtonDelete.clicked.connect(self.extra_prop_delete)
        self.mw_widget.materialDetails.clicked.connect(self.material_detail)
        self.mw_widget.adsorbateDetails.clicked.connect(self.adsorbate_detail)

        # Connect signals for graph view
        # TODO: would it be better to centralize everything when an isotherm needs plotting/modifying?
        self.list_view.selectionModel().currentChanged.connect(self.iso_list_model.check_selected)
        self.iso_list_model.checkedChanged.connect(self.graph_view.plot)
        self.unit_widget.unitsChanged.connect(self.graph_view.plot)

    ########################################################
    # Display functionality
    ########################################################

    def selection_changed(self, index, **kwargs):
        """What to do when the selected isotherm has changed."""
        isotherm = self.iso_list_model.get_iso_index(index)

        # Just reset if nothing to display
        self.clear_iso_views()
        if not isotherm:
            return

        # Otherwise detail all the isotherm
        self.display_isotherm(isotherm)

    def display_isotherm(self, isotherm):

        # Essential metadata
        self.mw_widget.materialEdit.setCurrentText(str(isotherm.material))
        self.mw_widget.adsorbateEdit.setCurrentText(str(isotherm.adsorbate))
        self.mw_widget.temperatureEdit.setText(str(isotherm.temperature))

        # Units setup
        self.unit_widget.init_units(isotherm)

        # Other isotherm metadata
        self.extraPropTableModel = IsoPropTableModel(isotherm)
        self.mw_widget.extraPropTableView.setModel(self.extraPropTableModel)

    def clear_iso_views(self):
        """Reset all the display."""

        # Essential metadata
        self.mw_widget.materialEdit.lineEdit().clear()
        self.mw_widget.adsorbateEdit.lineEdit().clear()
        self.mw_widget.temperatureEdit.clear()

        # Units
        self.unit_widget.clear()

    def modify_iso_baseprops(self):
        index = self.list_view.selectionModel().currentIndex()
        isotherm = self.iso_list_model.get_iso_index(index)
        modified = False

        if isotherm.material != self.mw_widget.materialEdit.lineEdit().text():
            isotherm.material = self.mw_widget.materialEdit.lineEdit().text()
            self.mw_widget.statusbar.showMessage(f'Material modified to {isotherm.material}', 2000)
            self.refresh_material_edit()
            modified = True

        if isotherm.adsorbate != self.mw_widget.adsorbateEdit.lineEdit().text():
            isotherm.adsorbate = self.mw_widget.adsorbateEdit.lineEdit().text()
            self.mw_widget.statusbar.showMessage(f'Adsorbate modified to {isotherm.adsorbate}', 2000)
            modified = True

        if isotherm.temperature != float(self.mw_widget.temperatureEdit.text()):
            isotherm.temperature = float(self.mw_widget.temperatureEdit.text())
            self.mw_widget.statusbar.showMessage(f'Temperature modified to {isotherm.temperature}', 2000)
            modified = True

        if modified:
            self.display_isotherm(isotherm)
            self.graph_view.plot()

    def material_detail(self):
        from src.views.MaterialView import MaterialView

        index = self.list_view.selectionModel().currentIndex()
        isotherm = self.iso_list_model.get_iso_index(index)
        if isotherm:
            dialog = MaterialView(isotherm.material)
            dialog.exec_()

    def adsorbate_detail(self):
        from src.views.AdsorbateView import AdsorbateView

        index = self.list_view.selectionModel().currentIndex()
        isotherm = self.iso_list_model.get_iso_index(index)
        if isotherm:
            view = AdsorbateView(isotherm.adsorbate)
            view.exec_()

    def extra_prop_add(self):
        propName = self.mw_widget.extraPropButtonWidget.propLineEditAdd.text()
        if not propName:
            self.mw_widget.statusbar.showMessage("Fill property name!", 2000)
            return
        self.extraPropTableModel.insertRows(self.extraPropTableModel.rowCount(), val=propName)
        self.mw_widget.statusbar.showMessage(f"Added property named {propName}")
        self.mw_widget.extraPropButtonWidget.propLineEditAdd.clear()

    def extra_prop_edit(self):
        index = self.mw_widget.extraPropTableView.selectionModel().currentIndex()
        if index:
            self.mw_widget.extraPropTableView.edit(index)

    def extra_prop_delete(self):
        index = self.mw_widget.extraPropTableView.selectionModel().currentIndex()
        self.mw_widget.statusbar.showMessage(f"Deleted property named {index}")
        self.extraPropTableModel.removeRow(index.row())

    def display_iso_data(self):
        from src.views.IsoDataDialog import IsoDataDialog
        from src.models.IsoDataTableModel import IsoDataTableModel

        index = self.list_view.selectionModel().currentIndex()
        isotherm = self.iso_list_model.get_iso_index(index)
        if isotherm:
            dialog = IsoDataDialog()
            dialog.tableView.setModel(IsoDataTableModel(isotherm.data()))
            dialog.exec_()

    def refresh_material_edit(self):
        self.mw_widget.materialEdit.clear()
        self.mw_widget.materialEdit.insertItems(0, [mat.name for mat in pygaps.MATERIAL_LIST])

    ########################################################
    # Add and remove functionality
    ########################################################

    def load(self, path, name, ext):
        """Load isotherm from disk."""

        isotherm = None

        if ext == '.csv':
            isotherm = pygaps.isotherm_from_csv(path)
        elif ext == '.json':
            isotherm = pygaps.isotherm_from_json(path)
        elif ext in ['.xls', '.xlsx']:
            isotherm = pygaps.isotherm_from_xl(path)
        elif ext == '.aif':
            isotherm = pygaps.isotherm_from_aif(path)
        else:
            raise Exception(f"Unknown isotherm type '{ext}'.")

        if not isotherm:
            return

        self.add_isotherm(name, isotherm)

    def loadImport(self, path, name, iso_type):
        isotherm = None

        if iso_type == 0:  # bel raw
            isotherm = pygaps.isotherm_from_bel(path)
        elif iso_type == 1:  # bel report
            isotherm = pygaps.isotherm_from_xl(path, fmt='bel')
        elif iso_type == 2:  # mic report
            isotherm = pygaps.isotherm_from_xl(path, fmt='mic')
        elif iso_type == 3:  # qnt report
            pygaps.isotherm_from_xl()
            # TODO implement Quantachrome report
            pass
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
        isotherm = self.iso_list_model.get_iso_index(self.list_view.currentIndex())

        if ext == '.csv':
            pygaps.isotherm_to_csv(isotherm, path)
        elif ext == '.json':
            pygaps.isotherm_to_json(isotherm, path)
        elif ext == '.xls' or ext == '.xlsx':
            pygaps.isotherm_to_xl(isotherm, path)
        elif ext == '.aif':
            pygaps.isotherm_to_aif(isotherm, path)
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
        self.iso_list_model.delete(self.list_view.currentIndex())
