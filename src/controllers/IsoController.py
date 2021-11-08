import pygaps
from pygaps.utilities.converter_mode import _PRESSURE_MODE, _LOADING_MODE, _MATERIAL_MODE
from pygaps.utilities.converter_unit import _TEMPERATURE_UNITS

from qtpy import QtWidgets as QW

from src.models.IsoModel import IsoModel
from src.models.IsoPropTableModel import IsoPropTableModel
from src.widgets.UtilityWidgets import ErrorMessageBox


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
        self.current_isotherm = None  # nothing here

        self.list_view.setModel(self.iso_list_model)
        self.graph_view.setModel(self.iso_list_model)

        # populate adsorbates and materials
        self.mw_widget.materialEdit.insertItems(0, [mat.name for mat in pygaps.MATERIAL_LIST])
        self.mw_widget.adsorbateEdit.insertItems(0, [ads.name for ads in pygaps.ADSORBATE_LIST])

        # populate units view
        self.unit_widget.init_boxes(_PRESSURE_MODE, _LOADING_MODE, _MATERIAL_MODE, _TEMPERATURE_UNITS)

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
        self.mw_widget.dataButton.clicked.connect(self.display_iso_data)

        # Setup property signals
        self.mw_widget.extraPropButtonWidget.propButtonSave.clicked.connect(self.extra_prop_save)
        self.mw_widget.extraPropButtonWidget.propButtonDelete.clicked.connect(self.extra_prop_delete)
        self.mw_widget.materialDetails.clicked.connect(self.material_detail)
        self.mw_widget.adsorbateDetails.clicked.connect(self.adsorbate_detail)

        # Connect signals for graph view
        self.list_view.selectionModel().currentChanged.connect(self.iso_list_model.check_selected)
        self.iso_list_model.checkedChanged.connect(self.graph_view.update)
        self.unit_widget.unitsChanged.connect(self.update_isotherm)

    ########################################################
    # Display functionality
    ########################################################

    def selection_changed(self, index, **kwargs):
        """What to do when the selected isotherm has changed."""
        self.current_isotherm = self.iso_list_model.get_iso_index(index)

        # Just reset if nothing to display
        self.clear_isotherm()
        if not self.current_isotherm:
            return

        # Otherwise detail all the isotherm
        self.display_isotherm()

    def display_isotherm(self):

        # Essential metadata
        self.mw_widget.materialEdit.setCurrentText(str(self.current_isotherm.material))
        self.mw_widget.adsorbateEdit.setCurrentText(str(self.current_isotherm.adsorbate))
        self.mw_widget.temperatureEdit.setText(str(self.current_isotherm._temperature))

        # Units setup
        self.unit_widget.init_units(self.current_isotherm)

        # Other isotherm metadata
        self.extraPropTableModel = IsoPropTableModel(self.current_isotherm)
        self.mw_widget.extraPropTableView.setModel(self.extraPropTableModel)
        self.mw_widget.extraPropTableView.selectionModel().selectionChanged.connect(self.extra_prop_select)

    def update_isotherm(self):
        self.display_isotherm()
        self.graph_view.update()

    def clear_isotherm(self):
        """Reset all the display."""

        # Essential metadata
        self.mw_widget.materialEdit.lineEdit().clear()
        self.mw_widget.adsorbateEdit.lineEdit().clear()
        self.mw_widget.temperatureEdit.clear()

        # Units
        self.unit_widget.clear()

        # Other metadata
        self.mw_widget.extraPropButtonWidget.clear()

    def modify_iso_baseprops(self):
        isotherm = self.current_isotherm
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
            self.update_isotherm()

    def material_detail(self):
        from src.views.MaterialView import MaterialDialog

        if self.current_isotherm:
            dialog = MaterialDialog(self.current_isotherm.material)
            ret = dialog.exec()
            if ret == QW.QDialog.Accepted:
                self.update_isotherm()

    def adsorbate_detail(self):
        from src.views.AdsorbateView import AdsorbateDialog

        if self.current_isotherm:
            dialog = AdsorbateDialog(self.current_isotherm.adsorbate)
            ret = dialog.exec()
            if ret == QW.QDialog.Accepted:
                self.update_isotherm()

    def extra_prop_select(self):
        index = self.mw_widget.extraPropTableView.selectionModel().currentIndex()
        if index:
            data = self.extraPropTableModel.rowData(index)
            if data:
                self.mw_widget.extraPropButtonWidget.display(*data)
            else:
                self.mw_widget.extraPropButtonWidget.clear()

    def extra_prop_save(self):

        propName = self.mw_widget.extraPropButtonWidget.nameEdit.text()
        propValue = self.mw_widget.extraPropButtonWidget.valueEdit.text()
        propType = self.mw_widget.extraPropButtonWidget.typeEdit.currentText()
        if not propName:
            self.mw_widget.statusbar.showMessage("Fill property name!", 2000)
            return

        if propType == "number":
            try:
                propValue = float(propValue)
            except ValueError:
                errorbox = ErrorMessageBox()
                errorbox.setText("Could not convert metadata value to number.")
                errorbox.exec()
                return

        self.extraPropTableModel.setOrInsertRow(data=[propName, propValue, propType])
        self.mw_widget.statusbar.showMessage(f"Added property named {propName}")
        self.mw_widget.extraPropTableView.resizeColumns()

    def extra_prop_delete(self):
        index = self.mw_widget.extraPropTableView.selectionModel().currentIndex()
        self.mw_widget.statusbar.showMessage(f"Deleted property named {index}")
        self.extraPropTableModel.removeRow(index.row())

    def display_iso_data(self):
        from src.views.IsoDataDialog import IsoDataDialog
        from src.models.IsoDataTableModel import IsoDataTableModel

        if self.current_isotherm:
            dialog = IsoDataDialog()
            dialog.tableView.setModel(IsoDataTableModel(self.current_isotherm.data()))
            ret = dialog.exec()
            if ret == QW.QDialog.Accepted:
                self.update_isotherm()

    def refresh_material_edit(self):
        self.mw_widget.materialEdit.clear()
        self.mw_widget.materialEdit.insertItems(0, [mat.name for mat in pygaps.MATERIAL_LIST])

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

    def loadImport(self, path, name, iso_type):
        isotherm = None

        if iso_type == 0:  # bel raw
            isotherm = pygaps.isotherm_from_bel(path)
        elif iso_type == 1:  # bel report
            isotherm = pygaps.isotherm_from_xl(path, fmt='bel')
        elif iso_type == 2:  # mic report
            isotherm = pygaps.isotherm_from_xl(path, fmt='mic')
        elif iso_type == 3:  # qnt report
            isotherm = pygaps.isotherm_from_xl(fmt='qnt')
            # TODO implement Quantachrome report
        elif iso_type == 4:  # 3P report:
            isotherm = pygaps.isotherm_from_xl(fmt='3p')
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
