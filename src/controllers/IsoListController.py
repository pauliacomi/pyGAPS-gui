import pygaps
from pygaps.utilities.converter_mode import _PRESSURE_MODE, _LOADING_MODE, _MATERIAL_MODE

from src.models.IsoModel import IsoModel
from src.models.IsoDataTableModel import IsoDataTableModel
from src.models.IsoInfoTableModel import IsoInfoTableModel


class IsoListController():
    """
    Interface between the Isotherm List Model and main window Isotherm views.

    The Isotherm List Model is the collection of isotherms that have been loaded
    in memory, which are stored in a custom QT QStandardItemModel.

    The main window has various views into this collection, such as:

        - displaying a list of all isotherms (IsoExplorer)
        - displaying metadata and unit for a selected isotherm (IsoDetails)
        - plotting one or more selected isotherms (IsoGraph)

    This is also the only place where the pygaps package is imported and used
    for the main window.

    """
    def __init__(self, widget, model):
        """Connect the MVC architecture."""

        self.widget = widget
        self.unit_widget = widget.unitPropButtonWidget
        self.list_view = widget.isoExplorer
        self.graph_view = widget.isoGraph

        self.iso_list_model = model

        # Connect signals for list view
        self.list_view.setModel(self.iso_list_model)
        self.list_view.selectionModel().currentChanged.connect(self.selection_changed)
        self.list_view.delete_current_iso.connect(self.delete_current_iso)

        self.widget.selectAllButton.clicked.connect(self.iso_list_model.tick_all)
        self.widget.deselectAllButton.clicked.connect(self.iso_list_model.untick_all)
        self.widget.removeButton.clicked.connect(self.delete_current_iso)

        # Create isotherm data view
        self.widget.materialEdit.insertItems(0, [mat.name for mat in pygaps.MATERIAL_LIST])
        self.widget.materialEdit.lineEdit().editingFinished.connect(self.modify_iso_baseprops)
        self.widget.adsorbateEdit.insertItems(0, [ads.name for ads in pygaps.ADSORBATE_LIST])
        self.widget.adsorbateEdit.lineEdit().editingFinished.connect(self.modify_iso_baseprops)
        self.widget.temperatureEdit.editingFinished.connect(self.modify_iso_baseprops)
        self.widget.dataButton.clicked.connect(self.display_iso_data)

        # Setup unit view
        self.unit_widget.init_boxes(_PRESSURE_MODE, _LOADING_MODE, _MATERIAL_MODE)

        # Setup property signals
        self.widget.extraPropButtonAdd.clicked.connect(self.extraPropAdd)
        self.widget.extraPropButtonEdit.clicked.connect(self.extraPropEdit)
        self.widget.extraPropButtonDelete.clicked.connect(self.extraPropDelete)

        # Connect signals for graph view
        self.graph_view.setModel(self.iso_list_model)
        self.list_view.selectionModel().currentChanged.connect(self.iso_list_model.check_selected)
        self.iso_list_model.checkedChanged.connect(self.graph_view.plot)
        self.unit_widget.unitsChanged.connect(self.graph_view.plot)

    def refresh_material_edit(self):
        self.widget.materialEdit.clear()
        self.widget.materialEdit.insertItems(0, [mat.name for mat in pygaps.MATERIAL_LIST])

    ########################################################
    # Display functionality
    ########################################################

    def selection_changed(self, index, **kwargs):
        """What to do when the selected isotherm has changed."""
        isotherm = self.iso_list_model.get_iso_index(index)

        # Reset if nothing to display
        self.clear_iso_views()
        if not isotherm:
            return

        # Essential metadata
        self.widget.materialEdit.setCurrentText(str(isotherm.material))
        self.widget.adsorbateEdit.setCurrentText(str(isotherm.adsorbate))
        self.widget.temperatureEdit.setText(str(isotherm.temperature))

        # Units setup
        self.unit_widget.init_units(isotherm)

        # Other isotherm metadata
        self.extraPropTableModel = IsoInfoTableModel(isotherm)
        self.widget.extraPropTableView.setModel(self.extraPropTableModel)

    def clear_iso_views(self):
        """Reset all the display."""
        # self.widget.blockSignals(True)

        # Essential metadata
        self.widget.materialEdit.lineEdit().clear()
        self.widget.adsorbateEdit.lineEdit().clear()
        self.widget.temperatureEdit.clear()

        # Units
        self.unit_widget.clear()
        # self.widget.blockSignals(False)

    def display_iso_data(self):
        from src.widgets.DataDialog import DataDialog
        index = self.list_view.selectionModel().currentIndex()
        isotherm = self.iso_list_model.get_iso_index(index)
        if isotherm:
            dialog = DataDialog()
            dialog.tableView.setModel(IsoDataTableModel(isotherm.data()))
            dialog.exec_()

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
        elif ext == '.xls' or ext == '.xlsx':
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
            # TODO implement
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
    # Selecting, modifying and deleting isotherms
    ########################################################

    def select_last_iso(self):
        """Select last isotherm"""
        last_iso = self.iso_list_model.index(self.iso_list_model.rowCount() - 1, 0)
        self.list_view.setCurrentIndex(last_iso)

    def delete_current_iso(self):
        """Remove current isotherm from model."""
        self.iso_list_model.delete(self.list_view.currentIndex())

    def modify_iso_baseprops(self):
        index = self.list_view.selectionModel().currentIndex()
        isotherm = self.iso_list_model.get_iso_index(index)
        modified = False

        if isotherm.material != self.widget.materialEdit.lineEdit().text():
            isotherm.material = self.widget.materialEdit.lineEdit().text()
            self.widget.statusbar.showMessage(f'Material modified to {isotherm.material}', 2000)
            modified = True

        if isotherm.adsorbate != self.widget.adsorbateEdit.lineEdit().text():
            isotherm.adsorbate = self.widget.adsorbateEdit.lineEdit().text()
            self.widget.statusbar.showMessage(f'Adsorbate modified to {isotherm.adsorbate}', 2000)
            modified = True

        if isotherm.temperature != float(self.widget.temperatureEdit.text()):
            isotherm.temperature = float(self.widget.temperatureEdit.text())
            self.widget.statusbar.showMessage(f'Temperature modified to {isotherm.temperature}', 2000)
            modified = True

        if modified:
            self.graph_view.plot()

    def extraPropAdd(self):
        propName = self.widget.extraPropLineEditAdd.text()
        if not propName:
            self.widget.statusbar.showMessage("Fill property name!", 2000)
            return
        self.extraPropTableModel.insertRows(self.extraPropTableModel.rowCount(), val=propName)
        self.widget.statusbar.showMessage(f"Added property named {propName}")
        self.widget.extraPropLineEditAdd.clear()

    def extraPropEdit(self):
        index = self.widget.extraPropTableView.selectionModel().currentIndex()
        if index:
            self.widget.extraPropTableView.edit(index)

    def extraPropDelete(self):
        index = self.widget.extraPropTableView.selectionModel().currentIndex()
        self.widget.statusbar.showMessage(f"Deleted property named {index}")
        self.extraPropTableModel.removeRow(index.row())
