import pathlib
from functools import partial

from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from pygapsgui.controllers.IsoController import IsoController
from pygapsgui.MainWindowUI import MainWindowUI
from pygapsgui.models.IsoListModel import IsoListModel
from pygapsgui.widgets.UtilityDialogs import error_dialog
from pygapsgui.widgets.UtilityDialogs import open_files_dialog
from pygapsgui.widgets.UtilityDialogs import save_file_dialog


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

        # Recent file actions
        self.recent_files_no = 8
        self.recent_file_actions = []
        self.load_recent_files()

        # Display state
        self.ui.statusbar.showMessage('Ready', 5000)

    ########################################################
    # Drag & Drop functionality
    ########################################################

    def dragEnterEvent(self, event):
        """Happens when a file is dragged on top of the window."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """We try to parse the dropped file as an isotherm."""
        filepaths = [pathlib.Path(u.toLocalFile()) for u in event.mimeData().urls()]
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
        self.ui.action_examples.triggered.connect(self.examples)
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

        self.ui.action_iast_binary_vle.triggered.connect(self.iast_binary_vle)
        self.ui.action_iast_binary_svp.triggered.connect(self.iast_binary_svp)
        self.ui.action_iast_multi_lvp.triggered.connect(self.iast_multi_lvp)

        self.ui.action_adsorbates.triggered.connect(self.adsorbate_explorer)
        self.ui.action_materials.triggered.connect(self.material_explorer)

    def load_recent_files(self):
        """Get recent files from the settings, and place them in the menu."""
        settings = QC.QSettings()
        recent_paths = settings.value("recentFiles", [])

        for ind in range(self.recent_files_no):
            recent_file_action = QW.QAction()
            recent_file_action.setVisible(False)
            recent_file_action.triggered.connect(partial(self.open_recent, ind))
            self.recent_file_actions.append(recent_file_action)

        for recent_file_action in self.recent_file_actions:
            self.ui.menu_recent.addAction(recent_file_action)

        cutoff = min(self.recent_files_no, len(recent_paths))

        for ind in range(cutoff):
            self.recent_file_actions[ind].setText(recent_paths[ind].name)
            self.recent_file_actions[ind].setData(recent_paths[ind])
            self.recent_file_actions[ind].setVisible(True)

    def update_recent_files(self, filepaths):
        """Update the recent files with the argument filepaths."""
        settings = QC.QSettings()
        recent_paths = settings.value("recentFiles", [])

        for filepath in filepaths:
            if filepath in recent_paths:
                recent_paths.remove(filepath)
            recent_paths.insert(0, filepath)

        recent_paths = recent_paths[:self.recent_files_no]

        settings.setValue("recentFiles", recent_paths)

        self.load_recent_files()

    ########################################################
    # Isotherm creation / load / import / save
    ########################################################

    def new_iso(self):
        """Create an empty isotherm."""
        """Start a manual manual creation dialog."""
        from pygapsgui.models.IsoCreateModel import IsoCreateModel
        from pygapsgui.views.IsoCreateDialog import IsoCreateDialog
        dialog = IsoCreateDialog(parent=self)
        model = IsoCreateModel(dialog)
        if not model.success:
            return
        ret = dialog.exec()

        if ret == QW.QDialog.Accepted and model.full_isotherm:
            iso = model.full_isotherm
            name = f"{iso.material} {iso.adsorbate} {iso.temperature}"
            self.iso_controller.add_isotherm(name, iso)
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

        # Update in recent files
        self.update_recent_files(filepaths)

    def open_recent(self, index=None):
        """Open the recent file in memory."""
        if index is not None:
            self.open_iso([self.recent_file_actions[index].data()])

    def import_iso(self, filepaths=None, ftype=None):
        """Import isotherm from manufacturer files."""
        from pygapsgui.views.ImportDialog import ImportDialog

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
            self.iso_controller.load_import(fp, fp.stem, ftype)
        self.iso_controller.select_last_iso()

    def save_iso(self, filepath=None):
        """Save isotherm to file."""
        index = self.ui.iso_explorer.currentIndex()
        if not index.isValid():
            return

        suggested_name = str(self.last_dir) if self.last_dir else '.'
        suggested_name += "/" + index.data()

        if not filepath:
            filepath = save_file_dialog(
                self,
                "Save an isotherm",
                suggested_name,
                filter=";;".join([
                    'AIF Isotherm (*.aif)',
                    'pyGAPS JSON Isotherm (*.json)',
                    'pyGAPS CSV Isotherm (*.csv)',
                    'pyGAPS Excel Isotherm (*.xls)',
                ])
            )
            if not filepath:
                return

        self.last_dir = filepath.parent
        self.iso_controller.save(filepath, filepath.suffix)

    ########################################################
    # Characterisation / modelling / etc
    ########################################################

    def area_bet(self):
        """Start BET area dialog."""
        isotherm = self.iso_controller.iso_current
        if not isotherm:
            return
        from pygapsgui.models.AreaBETModel import AreaBETModel
        from pygapsgui.views.AreaBETDialog import AreaBETDialog
        dialog = AreaBETDialog(parent=self)
        model = AreaBETModel(isotherm, dialog)
        if model.success:
            ret = dialog.exec()
            if ret == QW.QDialog.Accepted:
                # TODO There may be no results!!!
                results = model.result_dict()
                self.iso_controller.metadata_save_bulk(results)

    def area_langmuir(self):
        """Start Langmuir area dialog."""
        isotherm = self.iso_controller.iso_current
        if not isotherm:
            return
        from pygapsgui.models.AreaLangModel import AreaLangModel
        from pygapsgui.views.AreaLangDialog import AreaLangDialog
        dialog = AreaLangDialog(parent=self)
        model = AreaLangModel(isotherm, dialog)
        if model.success:
            ret = dialog.exec()
            if ret == QW.QDialog.Accepted:
                results = model.result_dict()
                self.iso_controller.metadata_save_bulk(results)

    def t_plot(self):
        """Start t-plot dialog."""
        isotherm = self.iso_controller.iso_current
        if not isotherm:
            return
        from pygapsgui.models.PlotTModel import PlotTModel
        from pygapsgui.views.PlotTDialog import PlotTDialog
        dialog = PlotTDialog(parent=self)
        model = PlotTModel(isotherm, dialog)
        if model.success:
            ret = dialog.exec()
            if ret == QW.QDialog.Accepted:
                results = model.result_dict()
                self.iso_controller.metadata_save_bulk(results)

    def alpha_s_plot(self):
        """Start alpha-s plot dialog."""
        isotherm = self.iso_controller.iso_current
        if not isotherm:
            return
        isotherms = self.iso_model.get_checked()
        if len(isotherms) != 2:
            error_dialog("Select two isotherms: one to characterize and one for reference.")
            return
        isotherms.remove(isotherm)
        if len(isotherms) != 1:
            error_dialog("Unexpected isotherm selection error")
            return
        ref_isotherm = isotherms[0]

        from pygapsgui.models.PlotAlphaSModel import PlotAlphaSModel
        from pygapsgui.views.PlotAlphaSDialog import PlotAlphaSDialog
        dialog = PlotAlphaSDialog(parent=self)
        model = PlotAlphaSModel(isotherm, ref_isotherm, dialog)
        if model.success:
            ret = dialog.exec()
            if ret == QW.QDialog.Accepted:
                results = model.result_dict()
                self.iso_controller.metadata_save_bulk(results)

    def dr_plot(self):
        """Start DR dialog. Calls a generic function."""
        self.dadr_plot(ptype="DR")

    def da_plot(self):
        """Start DA dialog. Calls a generic function."""
        self.dadr_plot(ptype="DA")

    def dadr_plot(self, ptype):
        """Start DA dialog."""
        isotherm = self.iso_controller.iso_current
        if not isotherm:
            return
        from pygapsgui.models.DADRModel import DADRModel
        from pygapsgui.views.DADRDialog import DADRDialog
        dialog = DADRDialog(ptype=ptype, parent=self)
        model = DADRModel(isotherm, dialog, ptype=ptype)
        if model.success:
            ret = dialog.exec()
            if ret == QW.QDialog.Accepted:
                results = model.result_dict()
                self.iso_controller.metadata_save_bulk(results)

    def psd_micro(self):
        """Start microporous PSD dialog."""
        isotherm = self.iso_controller.iso_current
        if not isotherm:
            return
        from pygapsgui.models.PSDMicroModel import PSDMicroModel
        from pygapsgui.views.PSDMicroDialog import PSDMicroDialog
        dialog = PSDMicroDialog(parent=self)
        model = PSDMicroModel(isotherm, dialog)
        if model.success:
            ret = dialog.exec()
            if ret == QW.QDialog.Accepted:
                results = model.result_dict()
                self.iso_controller.metadata_save_bulk(results)

    def psd_meso(self):
        """Start mesoporous PSD dialog."""
        isotherm = self.iso_controller.iso_current
        if not isotherm:
            return
        from pygapsgui.models.PSDMesoModel import PSDMesoModel
        from pygapsgui.views.PSDMesoDialog import PSDMesoDialog
        dialog = PSDMesoDialog(parent=self)
        model = PSDMesoModel(isotherm, dialog)
        if model.success:
            ret = dialog.exec()
            if ret == QW.QDialog.Accepted:
                results = model.result_dict()
                self.iso_controller.metadata_save_bulk(results)

    def psd_kernel(self):
        """Start kernel fitting PSD dialog."""
        isotherm = self.iso_controller.iso_current
        if not isotherm:
            return
        from pygapsgui.models.PSDKernelModel import PSDKernelModel
        from pygapsgui.views.PSDKernelDialog import PSDKernelDialog
        dialog = PSDKernelDialog(parent=self)
        model = PSDKernelModel(isotherm, dialog)
        if model.success:
            ret = dialog.exec()
            if ret == QW.QDialog.Accepted:
                results = model.result_dict()
                self.iso_controller.metadata_save_bulk(results)

    def isosteric(self):
        """Start isosteric enthalpy dialog."""
        isotherms = self.iso_model.get_checked()
        if len(isotherms) < 2:
            error_dialog("Select two or more isotherms")
            return

        from pygapsgui.models.IsostericModel import IsostericModel
        from pygapsgui.views.IsostericDialog import IsostericDialog
        dialog = IsostericDialog(parent=self)
        model = IsostericModel(isotherms, dialog)
        if model.success:
            dialog.exec()

    def model_by(self):
        """Start modellling by a specific model dialog."""
        isotherm = self.iso_controller.iso_current
        if not isotherm:
            return
        from pygapsgui.models.IsoModelByModel import IsoModelByModel
        from pygapsgui.views.IsoModelByDialog import IsoModelByDialog
        dialog = IsoModelByDialog(parent=self)
        model = IsoModelByModel(isotherm, dialog)
        if not model.success:
            return
        ret = dialog.exec()

        if ret == QW.QDialog.Accepted and model.model_isotherm:
            name = f"{isotherm.material} {isotherm.adsorbate} {model.model_isotherm.model.name}"
            self.iso_controller.add_isotherm(name, model.model_isotherm)
            self.iso_controller.select_last_iso()

    def model_guess(self):
        """Start guess fit model dialog."""
        isotherm = self.iso_controller.iso_current
        if not isotherm:
            return
        from pygapsgui.models.IsoModelGuessModel import IsoModelGuessModel
        from pygapsgui.views.IsoModelGuessDialog import IsoModelGuessDialog
        dialog = IsoModelGuessDialog(parent=self)
        model = IsoModelGuessModel(isotherm, dialog)
        if not model.success:
            return
        ret = dialog.exec()

        if ret == QW.QDialog.Accepted and model.model_isotherm:
            name = f"{isotherm.material} {isotherm.adsorbate} {model.model_isotherm.model.name}"
            self.iso_controller.add_isotherm(name, model.model_isotherm)
            self.iso_controller.select_last_iso()

    def iast_binary_vle(self):
        """Start binary vapour-liquid equilibrium IAST procedure."""
        isotherms = self.iso_model.get_checked()
        if len(isotherms) != 2:
            error_dialog("Select two isotherms.")
            return
        if isotherms[0].adsorbate == isotherms[1].adsorbate:
            error_dialog("IAST predicts multicomponent adsorption, select different adsorbates.")
            return

        from pygapsgui.models.IASTVLEModel import IASTVLEModel
        from pygapsgui.views.IASTVLEDialog import IASTVLEDialog
        dialog = IASTVLEDialog(parent=self)
        model = IASTVLEModel(isotherms, dialog)
        if not model.success:
            return
        dialog.exec()

    def iast_binary_svp(self):
        """Start selectivity-pressure IAST procedure."""
        isotherms = self.iso_model.get_checked()
        if len(isotherms) != 2:
            error_dialog("Select two isotherms.")
            return
        if isotherms[0].adsorbate == isotherms[1].adsorbate:
            error_dialog("IAST predicts multicomponent adsorption, select different adsorbates.")
            return

        from pygapsgui.models.IASTSVPModel import IASTSVPModel
        from pygapsgui.views.IASTSVPDialog import IASTSVPDialog
        dialog = IASTSVPDialog(parent=self)
        model = IASTSVPModel(isotherms, dialog)
        if not model.success:
            return
        dialog.exec()

    def iast_multi_lvp(self):
        """Start generic IAST procedures."""
        isotherms = self.iso_model.get_checked()
        if len(isotherms) < 2:
            error_dialog("Select at least two isotherms.")
            return

        from pygapsgui.models.IASTModel import IASTModel
        from pygapsgui.views.IASTDialog import IASTDialog
        dialog = IASTDialog(parent=self)
        model = IASTModel(isotherms, dialog)
        if not model.success:
            return
        dialog.exec()

    def adsorbate_explorer(self):
        """Explore/modify pyGAPS adsorbates."""
        from pygapsgui.views.AdsorbateView import AdsorbateListDialog
        dialog = AdsorbateListDialog(parent=self)
        dialog.adsorbate_changed.connect(self.iso_controller.handle_adsorbate_changed)
        dialog.exec()

    def material_explorer(self):
        """Explore/modify pyGAPS materials."""
        from pygapsgui.views.MaterialView import MaterialListDialog
        dialog = MaterialListDialog(parent=self)
        dialog.material_changed.connect(self.iso_controller.handle_material_changed)
        dialog.exec()

    ########################################################
    # About / examples
    ########################################################

    def examples(self):
        """Load example data."""
        qm = QW.QMessageBox()
        ret = qm.question(
            self,
            'Question',
            "Do you want to load some example data?",
            qm.Yes | qm.No,
        )
        if ret == qm.Yes:
            import pygapsgui.resources.sample_data as sd
            folder = pathlib.Path(sd.__file__).parent
            filepaths = tuple(folder.glob("*.json"))
            self.open_iso(filepaths)

    def about(self):
        """Show Help/About message box."""
        from importlib.metadata import version
        pgv = version("pygaps")
        pggv = version("pygapsgui")
        QW.QMessageBox.about(
            self, f"About pyGAPS-GUI v{pggv}", f"Built with pyGAPS v{pgv}<br>"
            "<a href='https://github.com/pauliacomi/pyGAPS'>github.com/pauliacomi/pyGAPS</a><br>"
            "Open source at<br>"
            "<a href='https://github.com/pauliacomi/pyGAPS-gui'>github.com/pauliacomi/pyGAPS-gui</a><br>"
            "Main author <i>Paul Iacomi</i><br>"
            "<a href='mailto:iacomi.paul@gmail.com'>iacomi.paul@gmail.com</a><br>"
            "Under AGPL License<br>"
        )
