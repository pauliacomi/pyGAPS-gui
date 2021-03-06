
import pygaps
import pygaps.utilities.unit_converter as pg_units

from src.models.IsoModel import IsoModel
from src.models.IsoDataTableModel import IsoDataTableModel
from src.models.IsoInfoTableModel import IsoInfoTableModel


class IsoListController():

    def __init__(self, widget, model):
        """Connect the MVC architecture."""

        self.widget = widget
        self.list_view = widget.isoExplorer
        self.graph_view = widget.isoGraph

        self.iso_list_model = model
        self.iso_prop_model = None

        # Connect signals for list view
        self.list_view.setModel(self.iso_list_model)
        self.list_view.selectionModel().currentChanged.connect(self.selection_changed)
        self.list_view.delete_current.connect(self.delete_current)

        self.widget.selectAllButton.clicked.connect(
            self.iso_list_model.tick_all)
        self.widget.deselectAllButton.clicked.connect(
            self.iso_list_model.untick_all)
        self.widget.removeButton.clicked.connect(self.delete_current)

        # Create isotherm data view
        self.widget.materialEdit.editingFinished.connect(self.modify_iso)
        self.widget.adsorbateEdit.insertItems(
            0, [ads.name for ads in pygaps.ADSORBATE_LIST])
        self.widget.adsorbateEdit.lineEdit().editingFinished.connect(self.modify_iso)
        self.widget.temperatureEdit.editingFinished.connect(self.modify_iso)
        self.widget.dataButton.clicked.connect(self.iso_data)

        # Connect signals for graph view
        self.graph_view.setModel(self.iso_list_model)
        self.list_view.selectionModel().currentChanged.connect(
            self.iso_list_model.check_selected)
        self.iso_list_model.checkedChanged.connect(self.graph_view.plot)

    ########################################################
    # Display functionality
    ########################################################

    def selection_changed(self, index, **kwargs):
        """What to do when the isotherm selected was changed."""
        isotherm = self.iso_list_model.get_iso_index(index)

        # Reset if nothing to display
        self.reset_iso_info()
        if not isotherm:
            return

        # Essential properties
        self.widget.materialEdit.setText(isotherm.material)
        self.widget.adsorbateEdit.setCurrentText(str(isotherm.adsorbate))
        self.widget.temperatureEdit.setText(str(isotherm.temperature))

        # Units here
        self.widget.pressureMode.addItems(list(pg_units._PRESSURE_MODE.keys()))
        self.widget.pressureUnit.addItems(
            list(pg_units._PRESSURE_UNITS.keys()))
        if isotherm.pressure_mode == "relative":
            self.widget.pressureUnit.setEnabled(False)

        self.widget.loadingBasis.addItems(list(pg_units._MATERIAL_MODE.keys()))
        self.widget.adsorbentBasis.addItems(
            list(pg_units._MATERIAL_MODE.keys()))

        self.widget.loadingUnit.addItems(
            list(pg_units._MATERIAL_MODE[isotherm.loading_basis].keys()))
        self.widget.adsorbentUnit.addItems(
            list(pg_units._MATERIAL_MODE[isotherm.adsorbent_basis].keys()))

        # Display other properties of the isotherm
        self.extraPropTableModel = IsoInfoTableModel(isotherm)
        self.widget.extraPropTableView.setModel(self.extraPropTableModel)
        self.widget.extraPropButtonAdd.clicked.connect(self.extraPropAdd)
        self.widget.extraPropButtonEdit.clicked.connect(self.extraPropEdit)
        self.widget.extraPropButtonDelete.clicked.connect(self.extraPropDelete)

    def reset_iso_info(self):
        """Reset all the display."""
        # self.widget.blockSignals(True)
        # Essential properties
        self.widget.materialEdit.clear()
        self.widget.adsorbateEdit.lineEdit().clear()
        self.widget.temperatureEdit.clear()

        # Units here
        self.widget.pressureMode.clear()
        self.widget.pressureUnit.clear()

        self.widget.loadingBasis.clear()
        self.widget.adsorbentBasis.clear()

        self.widget.loadingUnit.clear()
        self.widget.adsorbentUnit.clear()
        # self.widget.blockSignals(False)

    def iso_data(self):
        from src.widgets.DataDialog import DataDialog
        index = self.list_view.selectionModel().currentIndex()
        isotherm = self.iso_list_model.get_iso_index(index)
        if isotherm:
            dialog = DataDialog()
            dialog.tableView.setModel(IsoDataTableModel(isotherm.data()))
            dialog.exec_()

    ########################################################
    # Model editing functionality
    ########################################################

    def load(self, path, name, ext):
        """Load isotherm from disk."""
        if ext == '.csv':
            isotherm = pygaps.isotherm_from_csv(path)
        elif ext == '.json':
            isotherm = pygaps.isotherm_from_jsonf(path)
        elif ext == '.xls' or ext == '.xlsx':
            isotherm = pygaps.isotherm_from_xl(path)

        # Create the model to store the isotherm
        iso_model = IsoModel(name)
        # store data
        iso_model.setData(isotherm)
        # make checkable (default unchecked)
        iso_model.setCheckable(True)
        # Add to the list model
        self.iso_list_model.appendRow(iso_model)

    def select_last(self):
        """Select last isotherm"""
        last_iso = self.iso_list_model.index(
            self.iso_list_model.rowCount() - 1, 0)
        self.list_view.setCurrentIndex(last_iso)

    def save(self, path, ext):
        """Save isotherm to disk."""
        isotherm = self.iso_list_model.get_iso_index(
            self.list_view.currentIndex())

        if ext == '.csv':
            pygaps.isotherm_to_csv(isotherm, path)
        elif ext == '.json':
            pygaps.isotherm_to_jsonf(isotherm, path)
        elif ext == '.xls' or ext == '.xlsx':
            pygaps.isotherm_to_xl(isotherm, path)

    def delete_current(self):
        """Remove current isotherm from model."""
        self.iso_list_model.delete(self.list_view.currentIndex())

    def modify_iso(self):
        index = self.list_view.selectionModel().currentIndex()
        isotherm = self.iso_list_model.get_iso_index(index)
        if isotherm.material != self.widget.materialEdit.text():
            isotherm.material = self.widget.materialEdit.text()
            self.widget.statusbar.showMessage(
                'Material modified to ' + isotherm.material, 2000)

        if isotherm.adsorbate != self.widget.adsorbateEdit.lineEdit().text():
            isotherm.adsorbate = self.widget.adsorbateEdit.lineEdit().text()
            self.widget.statusbar.showMessage(
                'Adsorbate modified to ' + isotherm.adsorbate, 2000)

        if isotherm.temperature != float(self.widget.temperatureEdit.text()):
            isotherm.temperature = float(self.widget.temperatureEdit.text())
            self.widget.statusbar.showMessage(
                'Temperature modified to ' + str(isotherm.temperature), 2000)

    def extraPropAdd(self):
        propName = self.widget.extraPropLineEditAdd.text()
        if not propName:
            self.widget.statusbar.showMessage("Fill property name!", 2000)
            return
        self.extraPropTableModel.insertRows(
            self.extraPropTableModel.rowCount(), val=propName)
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
