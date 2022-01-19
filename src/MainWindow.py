import os

from qtpy import QtWidgets as QW
from qtpy import QtCore as QC

from src.controllers.IsoController import IsoController
from src.models.IsoListModel import IsoListModel
from src.MainWindowUI import MainWindowUI
from src.widgets.UtilityWidgets import (
    error_dialog, error_detail_dialog, open_files_dialog, save_file_dialog
)


class MainWindow(QW.QMainWindow):
    """Main Window for isotherm explorer and plotting."""
    def __init__(self, parent=None):

        # Initial init
        super().__init__(parent=parent)

        # Create and attach UI
        self.ui = MainWindowUI()
        self.ui.setup_UI(self)

        # Create isotherm list mvc
        self.iso_model = IsoListModel(parent=self)
        self.iso_controller = IsoController(self.ui, self.iso_model)

        # Create and connect menu
        self.connect_menu()

        # Allow drops
        self.setAcceptDrops(True)

        # last directory
        self.last_dir = None

        # Display state
        self.ui.statusbar.showMessage('Ready', 5000)

    ########################################################
    # Drag & Drop functionality
    ########################################################

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        filepaths = [u.toLocalFile() for u in event.mimeData().urls()]
        self.open_iso(filepaths)

    ########################################################
    # Menu functionality
    ########################################################

    def connect_menu(self):
        """Connect signals and slots of the menu."""
        self.ui.action_new.triggered.connect(self.new_iso)
        self.ui.action_open.triggered.connect(self.open_iso)
        self.ui.action_import.triggered.connect(self.import_iso)
        self.ui.action_save.triggered.connect(self.save_iso)
        self.ui.action_quit.triggered.connect(self.close)
        self.ui.action_about.triggered.connect(self.about)

        self.ui.action_area_bet.triggered.connect(self.area_bet)
        self.ui.action_area_lang.triggered.connect(self.area_langmuir)
        self.ui.action_t_plot.triggered.connect(self.t_plot)
        self.ui.action_alpha_s_plot.triggered.connect(self.alpha_s_plot)
        self.ui.action_dr_plot.triggered.connect(self.dr_plot)
        self.ui.action_da_plot.triggered.connect(self.da_plot)
        self.ui.action_psd_micro.triggered.connect(self.psd_micro)
        self.ui.action_psd_meso.triggered.connect(self.psd_meso)
        self.ui.action_psd_kernel.triggered.connect(self.psd_kernel)
        self.ui.action_isosteric.triggered.connect(self.isosteric)

        self.ui.action_model_by.triggered.connect(self.model_by)
        self.ui.action_model_guess.triggered.connect(self.model_guess)
        self.ui.action_model_manual.triggered.connect(self.model_manual)

        self.ui.action_iast_binary_vle.triggered.connect(self.iast_binary_vle)
        self.ui.action_iast_binary_svp.triggered.connect(self.iast_binary_svp)
        self.ui.action_iast_multi_lvp.triggered.connect(self.iast_multi_lvp)

        self.ui.action_adsorbates.triggered.connect(self.adsorbate_explorer)
        self.ui.action_materials.triggered.connect(self.material_explorer)

    ########################################################
    # Isotherm creation / load / import / save
    ########################################################

    def new_iso(self):
        # TODO dialog for new isotherm
        from pygaps import PointIsotherm
        isotherm = PointIsotherm(
            pressure=[0, 1],
            loading=[0, 1],
            m="New material",
            a="N2",
            t=77,
        )
        self.iso_controller.add_isotherm("new isotherm", isotherm)
        self.iso_controller.select_last_iso()

    def open_iso(self, filepaths=None):
        """Open isotherm from file."""
        if not filepaths:
            filepaths = open_files_dialog(
                self,
                "Load an isotherm",
                str(self.last_dir) if self.last_dir else '.',
                filter='pyGAPS isotherms (*.aif *.json *.csv *.xls)'
            )
            if not filepaths:
                return

        for fp in filepaths:
            self.last_dir = fp.parent
            self.iso_controller.load(fp, fp.stem, fp.suffix)
        self.iso_controller.select_last_iso()

    def import_iso(self, filepaths=None, ftype=None):
        """Import isotherm from manufacturer files."""
        from src.views.ImportDialog import ImportDialog

        if not filepaths:
            dialog = ImportDialog(parent=self)
            dialog.last_dir = self.last_dir
            dialog.exec()
            filepaths = dialog.filepaths
            ftype = dialog.ftype
            if not filepaths:
                return

        for fp in filepaths:
            self.last_dir = fp.parent
            self.iso_controller.loadImport(fp, fp.stem, ftype)
        self.iso_controller.select_last_iso()

    def save_iso(self, filepath=None):
        """Save isotherm to file."""
        index = self.ui.iso_explorer.currentIndex()
        if not index.isValid():
            return

        if not filepath:
            filepath = save_file_dialog(
                self,
                "Save an isotherm",
                str(self.last_dir) if self.last_dir else '.',
                filter=";;".join([
                    'pyGAPS JSON Isotherm (*.json)',
                    'pyGAPS CSV Isotherm (*.csv)',
                    'pyGAPS Excel Isotherm (*.xls)',
                ])
            )
            if not filepath:
                return

        self.last_dir = filepath.parent
        self.iso_controller.save(filepath, filepath.ext)

    ########################################################
    # Characterisation / modelling / etc
    ########################################################

    def area_bet(self):
        index = self.ui.iso_explorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_item_index(index)

        from src.models.AreaBETModel import AreaBETModel
        from src.views.AreaBETDialog import AreaBETDialog
        dialog = AreaBETDialog(parent=self)
        model = AreaBETModel(isotherm, dialog)
        if model.success:
            dialog.exec()

    def area_langmuir(self):
        index = self.ui.iso_explorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_item_index(index)

        from src.models.AreaLangModel import AreaLangModel
        from src.views.AreaLangDialog import AreaLangDialog
        dialog = AreaLangDialog(parent=self)
        model = AreaLangModel(isotherm, dialog)
        if model.success:
            dialog.exec()

    def t_plot(self):
        index = self.ui.iso_explorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_item_index(index)

        from src.models.PlotTModel import PlotTModel
        from src.views.PlotTDialog import PlotTDialog
        dialog = PlotTDialog(parent=self)
        model = PlotTModel(isotherm, dialog)
        if model.success:
            dialog.exec()

    def alpha_s_plot(self):
        index = self.ui.iso_explorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_item_index(index)

        isotherms = self.iso_model.get_item_checked()
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
        dialog = PlotAlphaSDialog(parent=self)
        model = PlotAlphaSModel(isotherm, ref_isotherm, dialog)
        if model.success:
            dialog.exec()

    def dr_plot(self):
        self.dadr_plot(ptype="DR")

    def da_plot(self):
        self.dadr_plot(ptype="DA")

    def dadr_plot(self, ptype):
        index = self.ui.iso_explorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_item_index(index)

        from src.models.DADRModel import DADRModel
        from src.views.DADRDialog import DADRDialog
        dialog = DADRDialog(ptype=ptype, parent=self)
        model = DADRModel(isotherm, dialog, ptype=ptype)
        if model.success:
            dialog.exec()

    def psd_micro(self):
        index = self.ui.iso_explorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_item_index(index)

        from src.models.PSDMicroModel import PSDMicroModel
        from src.views.PSDMicroDialog import PSDMicroDialog
        dialog = PSDMicroDialog(parent=self)
        model = PSDMicroModel(isotherm, dialog)
        if model.success:
            dialog.exec()

    def psd_meso(self):
        index = self.ui.iso_explorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_item_index(index)

        from src.models.PSDMesoModel import PSDMesoModel
        from src.views.PSDMesoDialog import PSDMesoDialog
        dialog = PSDMesoDialog(parent=self)
        model = PSDMesoModel(isotherm, dialog)
        if model.success:
            dialog.exec()

    def psd_kernel(self):
        index = self.ui.iso_explorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_item_index(index)

        from src.models.PSDKernelModel import PSDKernelModel
        from src.views.PSDKernelDialog import PSDKernelDialog
        dialog = PSDKernelDialog(parent=self)
        model = PSDKernelModel(isotherm, dialog)
        if model.success:
            dialog.exec()

    def isosteric(self):
        isotherms = self.iso_model.get_item_checked()
        if len(isotherms) < 2:
            error_dialog("Select two or more isotherms")
            return

        from src.models.IsostericModel import IsostericModel
        from src.views.IsostericDialog import IsostericDialog
        dialog = IsostericDialog(parent=self)
        model = IsostericModel(isotherms, dialog)
        if model.success:
            dialog.exec()

    def model_by(self):
        index = self.ui.iso_explorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_item_index(index)

        from src.models.IsoModelByModel import IsoModelByModel
        from src.views.IsoModelByDialog import IsoModelByDialog
        dialog = IsoModelByDialog(parent=self)
        model = IsoModelByModel(isotherm, dialog)
        if not model.success:
            return
        ret = dialog.exec()

        if ret == QW.QDialog.Accepted and model.model_isotherm:
            name = self.iso_model.itemFromIndex(index).text() + " model"
            self.iso_controller.add_isotherm(name, model.model_isotherm)
            self.iso_controller.select_last_iso()

    def model_guess(self):
        index = self.ui.iso_explorer.currentIndex()
        if not index.isValid():
            return
        isotherm = self.iso_model.get_item_index(index)

        from src.models.IsoModelGuessModel import IsoModelGuessModel
        from src.views.IsoModelGuessDialog import IsoModelGuessDialog
        dialog = IsoModelGuessDialog(parent=self)
        model = IsoModelGuessModel(isotherm, dialog)
        if not model.success:
            return
        ret = dialog.exec()

        if ret == QW.QDialog.Accepted and model.model_isotherm:
            name = self.iso_model.itemFromIndex(index).text() + " model"
            self.iso_controller.add_isotherm(name, model.model_isotherm)
            self.iso_controller.select_last_iso()

    def model_manual(self):
        from src.models.IsoModelManualModel import IsoModelManualModel
        from src.views.IsoModelManualDialog import IsoModelManualDialog
        dialog = IsoModelManualDialog(parent=self)
        model = IsoModelManualModel(dialog)
        if not model.success:
            return
        ret = dialog.exec()

        if ret == QW.QDialog.Accepted and model.model_isotherm:
            name = model.model_isotherm.model.name + " custom model"
            self.iso_controller.add_isotherm(name, model.model_isotherm)
            self.iso_controller.select_last_iso()

    def iast_binary_vle(self):
        """Start IAST procedures."""
        isotherms = self.iso_model.get_item_checked()
        if len(isotherms) != 2:
            error_dialog("Select two isotherms.")
            return

        from src.models.IASTVLEModel import IASTVLEModel
        from src.views.IASTVLEDialog import IASTVLEDialog
        dialog = IASTVLEDialog(parent=self)
        model = IASTVLEModel(isotherms, dialog)
        if not model.success:
            return
        dialog.exec()

    def iast_binary_svp(self):
        """Start IAST procedures."""
        isotherms = self.iso_model.get_item_checked()
        if len(isotherms) != 2:
            error_dialog("Select two isotherms.")
            return

        from src.models.IASTSVPModel import IASTSVPModel
        from src.views.IASTSVPDialog import IASTSVPDialog
        dialog = IASTSVPDialog(parent=self)
        model = IASTSVPModel(isotherms, dialog)
        if not model.success:
            return
        dialog.exec()

    def iast_multi_lvp(self):
        """Start IAST procedures."""
        isotherms = self.iso_model.get_item_checked()
        if len(isotherms) < 2:
            error_dialog("Select at least two isotherms.")
            return

        from src.models.IASTModel import IASTModel
        from src.views.IASTDialog import IASTDialog
        dialog = IASTDialog(parent=self)
        model = IASTModel(isotherms, dialog)
        if not model.success:
            return
        dialog.exec()

    def adsorbate_explorer(self):
        """Explore/modify pyGAPS adsorbates."""
        from src.views.AdsorbateView import AdsorbateListDialog
        dialog = AdsorbateListDialog(parent=self)
        dialog.exec()

    def material_explorer(self):
        """Explore/modify pyGAPS materials."""
        from src.views.MaterialView import MaterialListDialog
        dialog = MaterialListDialog(parent=self)
        dialog.exec()

    ########################################################
    # About
    ########################################################

    def about(self):
        """Show Help/About message box."""
        QW.QMessageBox.about(
            self, "About pyGAPS-GUI", "Main author <i>Paul Iacomi</i><br>"
            "<a href='mailto:iacomi.paul@gmail.com'>iacomi.paul@gmail.com</a><br>"
            "Open source at<br>"
            "<a href='https://github.com/pauliacomi/pyGAPS-gui'>github.com/pauliacomi/pyGAPS-gui</a><br>"
            "Under AGPL License<br>"
        )
