import os

from qtpy import QtWidgets as QW

from src.controllers.IsoController import IsoController
from src.models.IsoListModel import IsoListModel
from src.widgets.MainWindowUI import MainWindowUI
from src.widgets.UtilityWidgets import (error_dialog, open_files_dialog, save_file_dialog)


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
        self.ui.action_t_plot.triggered.connect(self.t_plot)
        self.ui.action_alpha_s_plot.triggered.connect(self.alphas_plot)
        self.ui.action_dr_plot.triggered.connect(self.dr_plot)
        self.ui.action_da_plot.triggered.connect(self.da_plot)
        self.ui.actionMicroporous_PSD.triggered.connect(self.psd_micro)
        self.ui.actionMesoporous_PSD.triggered.connect(self.psd_meso)
        self.ui.actionDFT_Kernel_PSD.triggered.connect(self.psd_kernel)
        self.ui.action_isosteric.triggered.connect(self.isosteric)

        self.ui.actionModel_By.triggered.connect(self.model_by)

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
                    error_dialog(str(e))
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
                    error_dialog(str(e))
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
                error_dialog(str(e))

    def BETarea(self):
        index = self.ui.isoExplorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_iso_index(index)

        from src.models.AreaBETModel import AreaBETModel
        from src.views.AreaBETDialog import AreaBETDialog
        dialog = AreaBETDialog()
        model = AreaBETModel(isotherm)
        model.set_view(dialog)
        dialog.exec_()

    def langmuirarea(self):
        index = self.ui.isoExplorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_iso_index(index)

        from src.models.AreaLangModel import AreaLangModel
        from src.views.AreaLangDialog import AreaLangDialog
        dialog = AreaLangDialog()
        model = AreaLangModel(isotherm)
        model.set_view(dialog)
        dialog.exec_()

    def t_plot(self):
        index = self.ui.isoExplorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_iso_index(index)

        from src.models.PlotTModel import PlotTModel
        from src.views.PlotTDialog import PlotTDialog
        dialog = PlotTDialog()
        model = PlotTModel(isotherm)
        model.set_view(dialog)
        dialog.exec_()

    def alphas_plot(self):
        index = self.ui.isoExplorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_iso_index(index)

        isotherms = self.iso_model.get_iso_checked()
        if len(isotherms) != 2:
            error_dialog("Select two isotherms")
            return
        isotherms.remove(isotherm)
        if len(isotherms) != 1:
            error_dialog("Unexpected isotherm selection error")
            return
        ref_isotherm = isotherms[0]

        from src.models.PlotAlphaSModel import PlotAlphaSModel
        from src.views.PlotAlphaSDialog import PlotAlphaSDialog
        dialog = PlotAlphaSDialog()
        model = PlotAlphaSModel(isotherm, ref_isotherm)
        model.set_view(dialog)
        dialog.exec_()

    def dr_plot(self):
        self.dadr_plot(ptype="DR")

    def da_plot(self):
        self.dadr_plot(ptype="DA")

    def dadr_plot(self, ptype):
        index = self.ui.isoExplorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_iso_index(index)

        from src.models.DADRModel import DADRModel
        from src.views.DADRDialog import DADRDialog
        dialog = DADRDialog(ptype=ptype)
        model = DADRModel(isotherm, ptype=ptype)
        model.set_view(dialog)
        dialog.exec_()

    def psd_micro(self):
        index = self.ui.isoExplorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_iso_index(index)

        from src.models.PSDMicroModel import PSDMicroModel
        from src.views.PSDMicroDialog import PSDMicroDialog
        dialog = PSDMicroDialog()
        model = PSDMicroModel(isotherm)
        model.set_view(dialog)
        dialog.exec_()

    def psd_meso(self):
        index = self.ui.isoExplorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_iso_index(index)

        from src.models.PSDMesoModel import PSDMesoModel
        from src.views.PSDMesoDialog import PSDMesoDialog
        dialog = PSDMesoDialog()
        model = PSDMesoModel(isotherm)
        model.set_view(dialog)
        dialog.exec_()

    def psd_kernel(self):
        index = self.ui.isoExplorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_iso_index(index)

        from src.models.PSDKernelModel import PSDKernelModel
        from src.views.PSDKernelDialog import PSDKernelDialog
        dialog = PSDKernelDialog()
        model = PSDKernelModel(isotherm)
        model.set_view(dialog)
        dialog.exec_()

    def isosteric(self):
        isotherms = self.iso_model.get_iso_checked()
        if len(isotherms) < 2:
            error_dialog("Select two or more isotherms")
            return

        from src.models.IsostericModel import IsostericModel
        from src.views.IsostericDialog import IsostericDialog
        dialog = IsostericDialog()
        model = IsostericModel(isotherms)
        model.set_view(dialog)
        dialog.exec_()

    def model_by(self):
        index = self.ui.isoExplorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_iso_index(index)

        from src.models.IsoModelByModel import IsoModelByModel
        from src.views.IsoModelByDialog import IsoModelByDialog
        dialog = IsoModelByDialog()
        model = IsoModelByModel(isotherm)
        model.set_view(dialog)
        dialog.exec_()

    def about(self):
        """Show Help/About message box."""
        QW.QMessageBox.about(self, 'application', 'iacomi.paul@gmail.com')
