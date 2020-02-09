
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
        # self.info_table_view = widget.isoGraph
        self.model = model

        # Connect signals for list view
        self.list_view.setModel(self.model)
        self.list_view.selectionModel().currentChanged.connect(self.selection_changed)
        self.list_view.delete_current.connect(self.delete_current)

        self.widget.selectAllButton.clicked.connect(self.model.check_all)
        self.widget.deselectAllButton.clicked.connect(self.model.uncheck_all)
        self.widget.removeButton.clicked.connect(self.delete_current)

        # Create isotherm data view
        self.widget.dataButton.clicked.connect(self.iso_data)

        # Connect signals for graph view
        self.graph_view.setModel(self.model)
        self.list_view.selectionModel().currentChanged.connect(self.model.check)
        self.model.checkedChanged.connect(self.graph_view.plot)

    ########################################################
    # Display functionality
    ########################################################

    def selection_changed(self, index, **kwargs):
        """What to do when the isotherm selected was changed."""
        isotherm = self.model.get_iso_index(index)

        # Reset if nothing to display
        if not isotherm:
            self.reset_iso_info()
            return

        # Essential properties
        self.widget.materialNameLineEdit.setText(isotherm.material)
        self.widget.adsorbateLineEdit.setText(str(isotherm.adsorbate))
        self.widget.temperatureLineEdit.setText(str(isotherm.temperature))

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
        self.widget.otherIsoInfoTable.setModel(IsoInfoTableModel(isotherm))
        # self.model.textInfo.setText(str(isotherm))

    def reset_iso_info(self):
        """Reset all the display."""

        # Essential properties
        self.widget.materialNameLineEdit.clear()
        self.widget.adsorbateLineEdit.clear()
        self.widget.temperatureLineEdit.clear()

        # Units here
        self.widget.pressureMode.clear()
        self.widget.pressureUnit.clear()

        self.widget.loadingBasis.clear()
        self.widget.adsorbentBasis.clear()

        self.widget.loadingUnit.clear()
        self.widget.adsorbentUnit.clear()

    def iso_data(self):
        from src.dialogs.DataDialog import DataDialog
        if self.iso_model.current_iso_index:
            isotherm = self.iso_model.get_iso_current()
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
        self.model.appendRow(iso_model)

    def select_last(self):
        """Select last isotherm"""
        last_iso = self.model.index(self.model.rowCount() - 1, 0)
        self.list_view.setCurrentIndex(last_iso)

    def save(self, path, ext):
        """Save isotherm to disk."""
        isotherm = self.model.get_iso_index(self.list_view.currentIndex())

        if ext == '.csv':
            pygaps.isotherm_to_csv(isotherm, path)
        elif ext == '.json':
            pygaps.isotherm_to_jsonf(isotherm, path)
        elif ext == '.xls' or ext == '.xlsx':
            pygaps.isotherm_to_xl(isotherm, path)

    def delete(self, index):
        """Remove isotherm from model."""
        row = index.row()
        if row < 0:
            return
        self.model.removeRow(row)  # LayoutChanged called automatically

    def delete_current(self):
        """Remove current isotherm from model."""
        self.delete(self.list_view.currentIndex())
