import os

from qtpy import QtWidgets as QW

from src.widgets.MainWindowUI import MainWindowUI
from src.widgets.UtilityWidgets import open_files_dialog, save_file_dialog, ErrorMessageBox

from src.models.IsoListModel import IsoListModel
from src.models.IsoDataTableModel import IsoDataTableModel
from src.models.IsoInfoTableModel import IsoInfoTableModel

from src.views.ConsoleView import ConsoleView

from src.controllers.IsoListController import IsoListController


class MainWindow(QW.QMainWindow):
    """Main Window for isotherm explorer and plotting."""
    def __init__(self, kernel, parent=None):

        # Initial init
        super().__init__(parent)

        # save kernel
        self.kernel = kernel

        # Create and attach UI
        self.ui = MainWindowUI()
        self.ui.setupUi(self)

        # Create isotherm list mvc
        self.iso_model = IsoListModel(parent=self)
        self.iso_controller = IsoListController(self.ui, self.iso_model)

        # Create and connect menu
        self.connect_menu()

        # Display state
        self.ui.statusbar.showMessage('Ready', 5000)

    ########################################################
    # Menu functionality
    ########################################################

    def connect_menu(self):
        """Connect signals and slots of the menu."""
        self.ui.actionOpen.triggered.connect(self.load)
        self.ui.actionImport.triggered.connect(self.importIso)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.about)
        # self.ui.actionConsole.triggered.connect(self.console)

        self.ui.actionBET_SA.triggered.connect(self.BETarea)
        self.ui.actionLangmuir_SA.triggered.connect(self.langmuirarea)

    def load(self, filepaths=None):
        """Open isotherm from file."""
        if not filepaths:
            filepaths = open_files_dialog(
                self,
                "Load an isotherm",
                '.',
                filter='pyGAPS isotherms (*.json *.csv *.xls *.aif)'
            )

        if filepaths and filepaths != '':
            for filepath in filepaths:
                dirpath, filename = os.path.split(filepath)
                filetitle, fileext = os.path.splitext(filename)
                try:
                    self.iso_controller.load(filepath, filename, fileext)
                except Exception as e:
                    errorbox = ErrorMessageBox()
                    errorbox.setText(str(e))
                    errorbox.exec_()
            self.iso_controller.select_last()

    def importIso(self, filepaths=None):
        """Import isotherm from manufacturer files."""
        from src.widgets.ImportDialog import ImportDialog

        dialog = ImportDialog()
        dialog.exec_()

        if dialog.filepaths and dialog.filepaths != '':
            for filepath in dialog.filepaths:
                dirpath, filename = os.path.split(filepath)
                try:
                    self.iso_controller.loadImport(
                        filepath, filename, dialog.ftype
                    )
                except Exception as e:
                    errorbox = ErrorMessageBox()
                    errorbox.setText(str(e))
                    errorbox.exec_()
            self.iso_controller.select_last()

    def save(self, filepath=None):
        """Save isotherm to file."""
        # if self.iso_model.current_iso_index is None:
        #     return

        if not filepath:
            filename = save_file_dialog(
                self,
                "Save an isotherm",
                '.',
                filter=";;".join([
                    'pyGAPS JSON Isotherm (*.json)',
                    'pyGAPS CSV Isotherm (*.csv)',
                    'pyGAPS Excel Isotherm (*.xls)'
                ])
            )

        if filename and filename != '':
            _, ext = os.path.splitext(filename)
            try:
                self.iso_controller.save(filename, ext)
            except Exception as e:
                errorbox = ErrorMessageBox()
                errorbox.setText(str(e))
                errorbox.exec_()

    def BETarea(self):
        from src.widgets.BETDialog import BETDialog
        from src.models.BETModel import BETModel
        index = self.ui.isoExplorer.currentIndex()
        if index:
            isotherm = self.iso_model.get_iso_index(index)
            dialog = BETDialog()
            model = BETModel(isotherm)
            model.set_view(dialog)
            dialog.exec_()

    def langmuirarea(self):
        from src.widgets.LangmuirDialog import LangmuirDialog
        from src.models.LangmuirModel import LangmuirModel
        index = self.ui.isoExplorer.currentIndex()
        if index:
            isotherm = self.iso_model.get_iso_index(index)
            dialog = LangmuirDialog()
            model = LangmuirModel(isotherm)
            model.set_view(dialog)
            dialog.exec_()

    def about(self):
        """Show Help/About message box."""
        QW.QMessageBox.about(self, 'application', 'iacomi.paul@gmail.com')

    def console(self):
        """Display console."""

        kernel_client = self.kernel.client()
        kernel_client.start_channels()

        global ipython_widget  # Prevent from being garbage collected
        ipython_widget = ConsoleView(self.kernel, kernel_client)
        ipython_widget.show()
