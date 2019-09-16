import os
import sys
from PySide2.QtWidgets import QMainWindow, QMessageBox
import PySide2.QtCore as QtCore

from src.views.mainwindow_ui import MainWindowUI
from src.views.utility import open_files_dialog, save_file_dialog
from src.models.bet_model import BETModel
from src.models.explorer_model import ExplorerModel
from src.models.isotherm_model import IsothermModel
from src.models.isotherm_data_model import IsothermDataModel

import pygaps


class MainWindow(QMainWindow):
    """Main Window for isotherm explorer and plotting."""

    current_iso_index = None
    selected_iso_indices = []

    iso_selected = QtCore.Signal()
    iso_deselected = QtCore.Signal()

    def __init__(self, parent=None):

        # Initial init
        super().__init__(parent)

        # Create and attach UI
        self.ui = MainWindowUI()
        self.ui.setupUi(self)

        # Create isotherm explorer
        self.explorer_init()

        self.iso_selected.connect(self.iso_info)
        self.iso_selected.connect(self.iso_plot)

        # Create isotherm data link
        self.ui.dataButton.clicked.connect(self.iso_data)

        # Create and connect menu
        self.connect_menu()

        # Display state
        self.ui.statusbar.showMessage('Ready', 5000)

    def explorer_init(self):
        """Create the isotherm explorer model and connect it to UI."""
        self.explorer_model = ExplorerModel()

        self.ui.isoExplorer.setModel(self.explorer_model)
        # self.ui.isoExplorer.clicked.connect(self.select)
        self.explorer_model.itemChanged.connect(self.explorer_changed)

    def connect_menu(self):
        """Connect signals and slots of the menu."""
        self.ui.actionOpen.triggered.connect(self.load)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionQuit.triggered.connect(self.quit_app)
        self.ui.actionAbout.triggered.connect(self.about)

        self.ui.actionBET_Surface_Area.triggered.connect(self.BETarea)

    def load(self):
        """Open isotherm from file."""
        default_file_name = '.'
        filenames = open_files_dialog(self, "Load an isotherm",
                                      default_file_name,
                                      filter='pyGAPS isotherms (*.json *.csv *.xls)')

        if filenames is not None and filenames != '':
            for filepath in filenames:
                dirpath, filename = os.path.split(filepath)
                filetitle, fileext = os.path.splitext(filename)
                new_iso_model = IsothermModel(filetitle)
                try:
                    if fileext == '.csv':
                        new_iso_model.setData(
                            pygaps.isotherm_from_csv(filepath))
                    elif fileext == '.json':
                        new_iso_model.setData(
                            pygaps.isotherm_from_jsonf(filepath))
                    elif fileext == '.xls' or fileext == '.xlsx':
                        new_iso_model.setData(
                            pygaps.isotherm_from_xl(filepath))

                    # It should be checkable, but not checked
                    new_iso_model.setCheckable(True)
                    check = QtCore.Qt.Unchecked
                    new_iso_model.setCheckState(check)
                    # TODO need to make them checkable later

                    self.explorer_model.appendRow(new_iso_model)
                except Exception as e:
                    # TODO Print out error details
                    print(e)

    def save(self):
        """Save isotherm to file."""
        default_file_name = '.'
        filename = save_file_dialog(self, "Save an isotherm",
                                    default_file_name,
                                    filter=";;".join(
                                        ['pyGAPS JSON Isotherm (*.json)',
                                         'pyGAPS CSV Isotherm (*.csv)',
                                         'pyGAPS Excel Isotherm (*.xls)']))

        if filename is not None and filename != '':
            isotherm = self.explorer_model.itemFromIndex(
                self.current_iso_index).data()
            fileroot, fileext = os.path.splitext(filename)
            try:
                if fileext == '.csv':
                    pygaps.isotherm_to_csv(isotherm, filename)
                elif fileext == '.json':
                    pygaps.isotherm_to_jsonf(isotherm, filename)
                elif fileext == '.xls' or fileext == '.xlsx':
                    pygaps.isotherm_to_xl(isotherm, filename)
            except Exception as e:
                # TODO Print error details
                print(e)
                pass

    def iso_plot(self):
        selected_iso = [
            self.explorer_model.itemFromIndex(index).data()
            for index in self.selected_iso_indices
        ]
        self.ui.graphicsView.ax.clear()
        pygaps.plot_iso(
            selected_iso,
            ax=self.ui.graphicsView.ax
        )
        self.ui.graphicsView.ax.figure.canvas.draw()

    def iso_info(self):
        index = self.current_iso_index
        isotherm = self.explorer_model.itemFromIndex(index).data()
        self.ui.materialNameLineEdit.setText(isotherm.material)
        self.ui.materialBatchLineEdit.setText(isotherm.material_batch)
        self.ui.adsorbateLineEdit.setText(str(isotherm.adsorbate))
        self.ui.temperatureLineEdit.setText(str(isotherm.temperature))
        self.ui.textInfo.setText(str(isotherm))

    def iso_data(self):
        from src.views.data_dialog import DataDialog
        index = self.current_iso_index
        if index:
            isotherm = self.explorer_model.itemFromIndex(index).data()
            dialog = DataDialog()
            dialog.tableView.setModel(IsothermDataModel(isotherm.data()))
            dialog.exec_()

    def select(self, index):
        self.current_iso_index = index
        self.selected_iso_indices.append(index)
        self.iso_selected.emit()

    def deselect(self, index):
        self.selected_iso_indices.remove(index)
        self.iso_selected.emit()

    def explorer_changed(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            self.select(item.index())
        if item.checkState() == QtCore.Qt.Unchecked:
            self.deselect(item.index())

    def quit_app(self):
        """Close application."""
        self.close()

    ########################################################
    # Menu functionality
    ########################################################

    def BETarea(self):
        from src.views.bet_dialog import BETDialog
        index = self.current_iso_index
        if index:
            isotherm = self.explorer_model.itemFromIndex(index).data()
            dialog = BETDialog()
            # TODO is it a model or a controller??
            controller = BETModel(isotherm)
            controller.set_view(dialog)
            dialog.exec_()

    def about(self):
        """Show Help/About message box."""
        QMessageBox.about(self, 'application', 'iacomi.paul@gmail.com')
