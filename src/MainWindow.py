import os
import sys
from PySide2.QtWidgets import QMainWindow, QMessageBox
import PySide2.QtCore as QtCore

from src.views.mainwindow_ui import MainWindowUI
from src.views.UtilityWidgets import open_files_dialog, save_file_dialog, ErrorMessageBox
from src.models.bet_model import BETModel

from src.models.IsothermModel import IsothermModel
from src.models.IsothermListModel import IsothermListModel
from src.models.IsothermDataTableModel import IsothermDataTableModel

import pygaps


class MainWindow(QMainWindow):
    """Main Window for isotherm explorer and plotting."""

    current_iso_index = None
    selected_iso_indices = []

    iso_sel_change = QtCore.Signal()

    def __init__(self, parent=None):

        # Initial init
        super().__init__(parent)

        # Create and attach UI
        self.ui = MainWindowUI()
        self.ui.setupUi(self)

        # Create isotherm explorer
        self.explorer_init()

        self.iso_sel_change.connect(self.iso_info)
        self.iso_sel_change.connect(self.iso_plot)

        # Create isotherm data link
        self.ui.dataButton.clicked.connect(self.iso_data)

        # Create and connect menu
        self.connect_menu()

        # Display state
        self.ui.statusbar.showMessage('Ready', 5000)

    def explorer_init(self):
        """Create the isotherm explorer model and connect it to UI."""
        self.explorer_model = IsothermListModel()

        self.ui.isoExplorer.setModel(self.explorer_model)
        self.ui.isoExplorer.clicked.connect(self.select)
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
                try:
                    if fileext == '.csv':
                        isotherm = pygaps.isotherm_from_csv(filepath)
                    elif fileext == '.json':
                        isotherm = pygaps.isotherm_from_jsonf(filepath)
                    elif fileext == '.xls' or fileext == '.xlsx':
                        isotherm = pygaps.isotherm_from_xl(filepath)

                    # Create the model to store the isotherm
                    iso_model = IsothermModel(filetitle)
                    # store data
                    iso_model.setData(isotherm)
                    # make checkable and set unchecked
                    iso_model.setCheckable(True)
                    iso_model.setCheckState(QtCore.Qt.Unchecked)
                    # Add to the explorer model
                    self.explorer_model.appendRow(iso_model)
                except Exception as e:
                    errorbox = ErrorMessageBox()
                    errorbox.setText(str(e))
                    errorbox.exec_()

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
                errorbox = ErrorMessageBox()
                errorbox.setText(str(e))
                errorbox.exec_()

    def iso_plot(self):
        selected_iso = [
            self.explorer_model.itemFromIndex(index).data()
            for index in self.selected_iso_indices
        ]
        if self.current_iso_index not in self.selected_iso_indices:
            selected_iso.append(
                self.explorer_model.itemFromIndex(
                    self.current_iso_index).data())
        self.ui.graphicsView.ax.clear()
        pygaps.plot_iso(
            selected_iso,
            ax=self.ui.graphicsView.ax
        )
        self.ui.graphicsView.ax.figure.canvas.draw()

    def iso_info(self):
        isotherm = self.explorer_model.itemFromIndex(
            self.current_iso_index).data()

        self.ui.materialNameLineEdit.setText(isotherm.material)
        self.ui.materialBatchLineEdit.setText(isotherm.material_batch)
        self.ui.adsorbateLineEdit.setText(str(isotherm.adsorbate))
        self.ui.temperatureLineEdit.setText(str(isotherm.temperature))
        self.ui.textInfo.setText(str(isotherm))

    def iso_data(self):
        from src.views.data_dialog import DataDialog
        if self.current_iso_index:
            isotherm = self.explorer_model.itemFromIndex(
                self.current_iso_index).data()
            dialog = DataDialog()
            dialog.tableView.setModel(IsothermDataTableModel(isotherm.data()))
            dialog.exec_()

    def select(self, index):
        self.current_iso_index = index
        self.iso_sel_change.emit()

    def checked(self, index):
        self.current_iso_index = index
        if index not in self.selected_iso_indices:
            self.selected_iso_indices.append(index)
        self.iso_sel_change.emit()

    def unchecked(self, index):
        self.selected_iso_indices.remove(index)
        self.iso_sel_change.emit()

    def explorer_changed(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            self.checked(item.index())
        if item.checkState() == QtCore.Qt.Unchecked:
            self.unchecked(item.index())

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
