import os
import sys
from PySide2.QtWidgets import QMainWindow, QMessageBox
from PySide2.QtCore import QCoreApplication, Signal, QThread, QFile, Slot

from src.views.mainwindow_ui import MainWindowUI
from src.views.utility import open_files_dialog, save_file_dialog
from src.models.main_model import MainModel
from src.models.bet_model import BETModel
from src.models.isotherm_data_model import IsothermDataModel

import pygaps


class MainWindow(QMainWindow):
    """Main Window for the entire application"""

    def __init__(self, parent=None):

        # Initial init
        super().__init__(parent)

        # Create and attach UI
        self.ui = MainWindowUI()
        self.ui.setupUi(self)

        # Create model
        self.model = MainModel()

        # Connect views and models
        self.ui.isoExplorer.setModel(self.model.explorer_model)
        self.ui.isoExplorer.clicked.connect(self.model.select)
        self.model.iso_selected.connect(self.iso_info)
        self.model.iso_selected.connect(self.iso_plot)
        self.ui.dataButton.clicked.connect(self.iso_data)

        # Create and connect signals
        self.connect_signals()

        # Display state
        self.ui.statusbar.showMessage('Ready', 5000)

    def connect_signals(self):
        """Connect signals and slots."""
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(self.save_content)
        self.ui.actionQuit.triggered.connect(self.quit_app)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionBET_Surface_Area.triggered.connect(self.BETarea)

    def quit_app(self):
        """Close application."""
        self.close()

    def open_file(self):
        """Open isotherm from file."""
        default_file_name = '.'
        filename = open_files_dialog(self, "Load an isotherm",
                                     default_file_name,
                                     filter='pyGAPS isotherms (*.json *.csv *.xls)')

        if filename is not None and filename != '':
            self.model.load(filename)

    def save_content(self):
        """Save isotherm to file."""
        default_file_name = '.'
        filename = save_file_dialog(self, "Save an isotherm",
                                    default_file_name,
                                    filter=";;".join(
                                        ['pyGAPS JSON Isotherm (*.json)',
                                         'pyGAPS CSV Isotherm (*.csv)',
                                         'pyGAPS Excel Isotherm (*.xls)']))

        if filename is not None and filename != '':
            self.model.save(filename)

    def iso_plot(self):
        indices = self.model.selected_iso_indices
        selected_iso = [
            self.model.explorer_model.itemFromIndex(index).data() for index in indices]
        self.ui.graphicsView.ax.clear()
        pygaps.plot_iso(
            selected_iso,
            ax=self.ui.graphicsView.ax
        )
        self.ui.graphicsView.ax.figure.canvas.draw()

    def iso_info(self):
        index = self.model.current_iso_index
        isotherm = self.model.explorer_model.itemFromIndex(index).data()
        self.ui.materialNameLineEdit.setText(isotherm.material)
        self.ui.materialBatchLineEdit.setText(isotherm.material_batch)
        self.ui.adsorbateLineEdit.setText(str(isotherm.adsorbate))
        self.ui.temperatureLineEdit.setText(str(isotherm.temperature))
        self.ui.textInfo.setText(str(isotherm))

    def iso_data(self):
        from src.views.data_dialog import DataDialog
        index = self.model.current_iso_index
        if index:
            isotherm = self.model.explorer_model.itemFromIndex(index).data()
            dialog = DataDialog()
            dialog.tableView.setModel(IsothermDataModel(isotherm.data()))
            dialog.exec_()

    # Menu functionality

    def BETarea(self):
        from src.views.bet_dialog import BETDialog
        index = self.model.current_iso_index
        if index:
            isotherm = self.model.explorer_model.itemFromIndex(index).data()
            dialog = BETDialog()
            # TODO is it a model or a controller??
            controller = BETModel(isotherm)
            controller.set_view(dialog)
            dialog.exec_()

    def about(self):
        """Show Help/About message box."""
        QMessageBox.about(self, 'application', 'iacomi.paul@gmail.com')
