import os

from qtpy import QtWidgets as QW

from src.controllers.IsoController import IsoController
from src.models.IsoListModel import IsoListModel
from src.widgets.MainWindowUI import MainWindowUI
from src.widgets.UtilityWidgets import (ErrorMessageBox, open_files_dialog, save_file_dialog)


class MainWindow(QW.QMainWindow):
    """Main Window for isotherm explorer and plotting."""
    def __init__(self, parent=None):

        # Initial init
        super().__init__(parent)

        # Create and attach UI
        self.ui = MainWindowUI()
        self.ui.setupUi(self)

        # Create isotherm list mvc
        self.iso_model = IsoListModel(parent=self)
        self.iso_controller = IsoController(self.ui, self.iso_model)

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

        self.ui.actionBET_SA.triggered.connect(self.BETarea)
        self.ui.actionLangmuir_SA.triggered.connect(self.langmuirarea)

    def load(self, filepaths=None):
        """Open isotherm from file."""
        if not filepaths:
            filepaths = open_files_dialog(
                self, "Load an isotherm", '.', filter='pyGAPS isotherms (*.aif *.json *.csv *.xls)'
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
            self.iso_controller.select_last_iso()

    def importIso(self, filepaths=None):
        """Import isotherm from manufacturer files."""
        from src.views.ImportDialog import ImportDialog

        dialog = ImportDialog()
        dialog.exec_()

        if dialog.filepaths and dialog.filepaths != '':
            for filepath in dialog.filepaths:
                dirpath, filename = os.path.split(filepath)
                try:
                    self.iso_controller.loadImport(filepath, filename, dialog.ftype)
                except Exception as e:
                    errorbox = ErrorMessageBox()
                    errorbox.setText(str(e))
                    errorbox.exec_()
            self.iso_controller.select_last_iso()

    def save(self, filepath=None):
        """Save isotherm to file."""
        index = self.ui.isoExplorer.currentIndex()
        if not index.isValid():
            return

        if not filepath:
            filename = save_file_dialog(
                self,
                "Save an isotherm",
                '.',
                filter=";;".join([
                    'pyGAPS JSON Isotherm (*.json)', 'pyGAPS CSV Isotherm (*.csv)', 'pyGAPS Excel Isotherm (*.xls)'
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
        from src.models.AreaBETModel import AreaBETModel
        from src.views.AreaBETDialog import AreaBETDialog
        index = self.ui.isoExplorer.currentIndex()
        if index.isValid():
            isotherm = self.iso_model.get_iso_index(index)
            dialog = AreaBETDialog()
            model = AreaBETModel(isotherm)
            model.set_view(dialog)
            dialog.exec_()

    def langmuirarea(self):
        from src.models.AreaLangModel import AreaLangModel
        from src.views.AreaLangDialog import AreaLangDialog
        index = self.ui.isoExplorer.currentIndex()
        if index.isValid():
            isotherm = self.iso_model.get_iso_index(index)
            dialog = AreaLangDialog()
            model = AreaLangModel(isotherm)
            model.set_view(dialog)
            dialog.exec_()

    def about(self):
        """Show Help/About message box."""
        QW.QMessageBox.about(self, 'application', 'iacomi.paul@gmail.com')
