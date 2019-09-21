import os
import sys
from PySide2.QtWidgets import QMainWindow, QMessageBox
import PySide2.QtCore as QtCore

from src.dialogs.MainWindowUI import MainWindowUI
from src.dialogs.UtilityDialogs import open_files_dialog, save_file_dialog, ErrorMessageBox

from src.models.IsothermListModel import IsothermListModel
from src.models.IsothermDataTableModel import IsothermDataTableModel

from src.views.ConsoleView import ConsoleView


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
        self.isotherms_model = IsothermListModel()

        # Create isotherm explorer view
        self.ui.isoExplorer.setModel(self.isotherms_model)
        self.ui.isoExplorer.clicked.connect(self.isotherms_model.select)

        # Create isotherm info view
        self.isotherms_model.iso_sel_change.connect(self.iso_info)

        # Create isotherm data view
        self.ui.dataButton.clicked.connect(self.iso_data)

        # Connect to graph
        self.ui.isoGraph.setModel(self.isotherms_model)
        self.isotherms_model.iso_sel_change.connect(self.ui.isoGraph.plot)

    ########################################################
    # Display functionality
    ########################################################

    def iso_info(self):
        isotherm = self.isotherms_model.get_iso_current()

        self.ui.materialNameLineEdit.setText(isotherm.material)
        self.ui.materialBatchLineEdit.setText(isotherm.material_batch)
        self.ui.adsorbateLineEdit.setText(str(isotherm.adsorbate))
        self.ui.temperatureLineEdit.setText(str(isotherm.temperature))
        self.ui.textInfo.setText(str(isotherm))

    def iso_data(self):
        from src.dialogs.DataDialog import DataDialog
        if self.isotherms_model.current_iso_index:
            isotherm = self.isotherms_model.get_iso_current()
            dialog = DataDialog()
            dialog.tableView.setModel(IsothermDataTableModel(isotherm.data()))
            dialog.exec_()

    ########################################################
    # Menu functionality
    ########################################################

    def connect_menu(self):
        """Connect signals and slots of the menu."""
        self.ui.actionOpen.triggered.connect(self.load)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionQuit.triggered.connect(self.quit_app)
        self.ui.actionAbout.triggered.connect(self.about)
        # self.ui.actionConsole.triggered.connect(self.console)

        self.ui.actionBET_Surface_Area.triggered.connect(self.BETarea)

    def quit_app(self):
        """Close application."""
        self.close()

    def load(self):
        """Open isotherm from file."""
        filenames = open_files_dialog(self, "Load an isotherm", '.',
                                      filter='pyGAPS isotherms (*.json *.csv *.xls)')

        if filenames is not None and filenames != '':
            for filepath in filenames:
                dirpath, filename = os.path.split(filepath)
                filetitle, fileext = os.path.splitext(filename)
                try:
                    self.isotherms_model.load(filepath, filename, fileext)
                except Exception as e:
                    errorbox = ErrorMessageBox()
                    errorbox.setText(str(e))
                    errorbox.exec_()

    def save(self):
        """Save isotherm to file."""
        if self.isotherms_model.current_iso_index is None:
            return

        filename = save_file_dialog(self, "Save an isotherm", '.',
                                    filter=";;".join(
                                        ['pyGAPS JSON Isotherm (*.json)',
                                         'pyGAPS CSV Isotherm (*.csv)',
                                         'pyGAPS Excel Isotherm (*.xls)']))

        if filename is not None and filename != '':
            _, ext = os.path.splitext(filename)
            try:
                self.isotherms_model.save(filename, ext)
            except Exception as e:
                errorbox = ErrorMessageBox()
                errorbox.setText(str(e))
                errorbox.exec_()

    def BETarea(self):
        from src.dialogs.BETDialog import BETDialog
        from src.models.BETModel import BETModel
        index = self.isotherms_model.current_iso_index
        if index:
            isotherm = self.isotherms_model.itemFromIndex(index).data()
            dialog = BETDialog()
            model = BETModel(isotherm)
            model.set_view(dialog)
            dialog.pSlider.rangeChanged.connect(model.set_limits)
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
