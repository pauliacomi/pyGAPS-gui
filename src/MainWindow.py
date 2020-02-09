import os
import sys
from PySide2.QtWidgets import QMainWindow, QMessageBox
import PySide2.QtCore as QtCore

from src.dialogs.MainWindowUI import MainWindowUI
from src.dialogs.UtilityDialogs import open_files_dialog, save_file_dialog, ErrorMessageBox

from src.models.IsoListModel import IsoListModel
from src.models.IsoDataTableModel import IsoDataTableModel
from src.models.IsoInfoTableModel import IsoInfoTableModel

from src.views.ConsoleView import ConsoleView

import pygaps.utilities.unit_converter as pg_units


class MainWindow(QMainWindow):
    """Main Window for isotherm explorer and plotting."""

    def __init__(self, kernel, parent=None):

        # Initial init
        super().__init__(parent)

        # save kernel
        self.kernel = kernel

        # Create and attach UI
        self.ui = MainWindowUI()
        self.ui.setupUi(self)

        # Create isotherm model-views
        self.isotherm_model_init()

        # Create and connect menu
        self.connect_menu()

        # Display state
        self.ui.statusbar.showMessage('Ready', 5000)

    def isotherm_model_init(self):
        """Create the isotherm explorer model and connect it to views."""

        # Create isotherm list model
        self.iso_model = IsoListModel()

        # Create isotherm explorer view
        self.ui.isoExplorer.setModel(self.iso_model)

        self.ui.isoExplorer.selectionModel().currentChanged.connect(self.iso_model.select)
        self.ui.isoExplorer.delete_current.connect(
            self.iso_model.remove_iso_current)

        self.ui.selectAllButton.clicked.connect(self.iso_model.check_all)
        self.ui.deselectAllButton.clicked.connect(self.iso_model.uncheck_all)
        self.ui.removeButton.clicked.connect(self.iso_model.remove_iso_current)

        # Create isotherm info view
        self.iso_model.layoutChanged.connect(self.iso_info)

        # Create isotherm data view
        self.ui.dataButton.clicked.connect(self.iso_data)

        # Connect to graph
        self.ui.isoGraph.setModel(self.iso_model)
        self.iso_model.layoutChanged.connect(self.ui.isoGraph.plot)

    ########################################################
    # Display functionality
    ########################################################

    def iso_info(self):
        isotherm = self.iso_model.get_iso_current()

        # Reset if nothing to display
        if not isotherm:
            self.reset_iso_info()
            return

        # Essential properties
        self.ui.materialNameLineEdit.setText(isotherm.material)
        self.ui.adsorbateLineEdit.setText(str(isotherm.adsorbate))
        self.ui.temperatureLineEdit.setText(str(isotherm.temperature))

        # Units here
        self.ui.pressureMode.addItems(list(pg_units._PRESSURE_MODE.keys()))
        self.ui.pressureUnit.addItems(list(pg_units._PRESSURE_UNITS.keys()))
        if isotherm.pressure_mode == "relative":
            self.ui.pressureUnit.setEnabled(False)

        self.ui.loadingBasis.addItems(list(pg_units._MATERIAL_MODE.keys()))
        self.ui.adsorbentBasis.addItems(list(pg_units._MATERIAL_MODE.keys()))

        self.ui.loadingUnit.addItems(
            list(pg_units._MATERIAL_MODE[isotherm.loading_basis].keys()))
        self.ui.adsorbentUnit.addItems(
            list(pg_units._MATERIAL_MODE[isotherm.adsorbent_basis].keys()))

        # Display other properties of the isotherm
        self.ui.otherIsoInfoTable.setModel(IsoInfoTableModel(isotherm))
        # self.ui.textInfo.setText(str(isotherm))

    def reset_iso_info(self):
        """Reset all the display."""

        # Essential properties
        self.ui.materialNameLineEdit.clear()
        self.ui.adsorbateLineEdit.clear()
        self.ui.temperatureLineEdit.clear()

        # Units here
        self.ui.pressureMode.clear()
        self.ui.pressureUnit.clear()

        self.ui.loadingBasis.clear()
        self.ui.adsorbentBasis.clear()

        self.ui.loadingUnit.clear()
        self.ui.adsorbentUnit.clear()

    def iso_data(self):
        from src.dialogs.DataDialog import DataDialog
        if self.iso_model.current_iso_index:
            isotherm = self.iso_model.get_iso_current()
            dialog = DataDialog()
            dialog.tableView.setModel(IsoDataTableModel(isotherm.data()))
            dialog.exec_()

    ########################################################
    # Menu functionality
    ########################################################

    def connect_menu(self):
        """Connect signals and slots of the menu."""
        self.ui.actionOpen.triggered.connect(self.load)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.about)
        # self.ui.actionConsole.triggered.connect(self.console)

        self.ui.actionBET_Surface_Area.triggered.connect(self.BETarea)
        self.ui.actionLangmuir_Surface_Area.triggered.connect(
            self.langmuirarea)

    def load(self, filepaths=None):
        """Open isotherm from file."""
        if not filepaths:
            filepaths = open_files_dialog(self, "Load an isotherm", '.',
                                          filter='pyGAPS isotherms (*.json *.csv *.xls)')

        if filepaths and filepaths != '':
            for filepath in filepaths:
                dirpath, filename = os.path.split(filepath)
                filetitle, fileext = os.path.splitext(filename)
                try:
                    self.iso_model.load(filepath, filename, fileext)
                except Exception as e:
                    errorbox = ErrorMessageBox()
                    errorbox.setText(str(e))
                    errorbox.exec_()
            first_iso = self.iso_model.index(0, 0)
            self.ui.isoExplorer.setCurrentIndex(first_iso)

    def save(self, filepath=None):
        """Save isotherm to file."""
        if self.iso_model.current_iso_index is None:
            return

        if not filepath:
            filename = save_file_dialog(self, "Save an isotherm", '.',
                                        filter=";;".join(
                                            ['pyGAPS JSON Isotherm (*.json)',
                                             'pyGAPS CSV Isotherm (*.csv)',
                                             'pyGAPS Excel Isotherm (*.xls)']))

        if filename and filename != '':
            _, ext = os.path.splitext(filename)
            try:
                self.iso_model.save(filename, ext)
            except Exception as e:
                errorbox = ErrorMessageBox()
                errorbox.setText(str(e))
                errorbox.exec_()

    def BETarea(self):
        from src.dialogs.BETDialog import BETDialog
        from src.models.BETModel import BETModel
        index = self.iso_model.current_iso_index
        if index:
            isotherm = self.iso_model.itemFromIndex(index).data()
            dialog = BETDialog()
            model = BETModel(isotherm)
            model.set_view(dialog)
            dialog.exec_()

    def langmuirarea(self):
        from src.dialogs.LangmuirDialog import LangmuirDialog
        from src.models.LangmuirModel import LangmuirModel
        index = self.iso_model.current_iso_index
        if index:
            isotherm = self.iso_model.itemFromIndex(index).data()
            dialog = LangmuirDialog()
            model = LangmuirModel(isotherm)
            model.set_view(dialog)
            dialog.exec_()

    def about(self):
        """Show Help/About message box."""
        QMessageBox.about(self, 'application', 'iacomi.paul@gmail.com')

    def console(self):
        """Display console."""

        kernel_client = self.kernel.client()
        kernel_client.start_channels()

        global ipython_widget  # Prevent from being garbage collected
        ipython_widget = ConsoleView(self.kernel, kernel_client)
        ipython_widget.show()
