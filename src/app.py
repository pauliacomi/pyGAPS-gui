#!/usr/bin/env python3

import os
import sys
from PySide2.QtWidgets import QMainWindow, QApplication, QMessageBox
from PySide2.QtCore import QCoreApplication, Signal, QThread, QFile, Qt

from src.views.mainwindow import MainWindow
from src.views.data_dialog import DataDialog
from src.views.utility import open_files_dialog, save_file_dialog
from src.models.main_model import MainModel
from src.models.isotherm_data_model import IsothermDataModel

import pygaps

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)


class ApplicationWindow(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create models
        self.model = MainModel()

        # Create views
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.data_dialog = DataDialog()

        # Connect views and models
        self.ui.isoExplorer.setModel(self.model.explorer_model)
        self.ui.isoExplorer.clicked.connect(self.model.select)
        self.model.iso_selected.connect(self.iso_info)
        self.model.iso_selected.connect(self.iso_plot)
        self.ui.dataButton.clicked.connect(self.iso_data)

        # Create and connect signals
        self.connect_signals()

        # Start thread
        self.worker = Worker()
        self.worker.send_text.connect(self.receive_text)
        self.worker.start()

    def connect_signals(self):
        """Connect signals and slots."""
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(self.save_content)
        self.ui.actionQuit.triggered.connect(self.quit_app)
        self.ui.actionAbout.triggered.connect(self.about)

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
        self.ui.materialNameLineEdit.setText(isotherm.material_name)
        self.ui.materialBatchLineEdit.setText(isotherm.material_batch)
        self.ui.adsorbateLineEdit.setText(isotherm.adsorbate)
        self.ui.temperatureLineEdit.setText(str(isotherm.t_iso))
        self.ui.textInfo.setText(str(isotherm))

    def iso_data(self):
        index = self.model.current_iso_index
        isotherm = self.model.explorer_model.itemFromIndex(index).data()
        model = IsothermDataModel(isotherm.data())
        self.data_dialog.tableView.setModel(model)
        self.data_dialog.exec_()

    def receive_text(self, some_string):
        """Add some_string at the end of textInfo."""
        self.ui.textInfo.append(some_string)

    def about(self):
        """Show Help/About message box."""
        QMessageBox.about(self, 'application', 'iacomi.paul@gmail.com')


class Worker(QThread):
    """
    Worker thread.Runs work method, and create signals.

    finished
        No data
    error
        `tuple` (exctype, value, traceback.format_exc() )
    result
        `object` data returned from processing, anything
    progress
        `int` indicating % progress
    send_text
        'str' send text to textInfo
    """
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)
    send_text = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        """Start work method and take care about run-time errors in thread"""
        self.result.emit(self.work())

    def work(self):
        """Emit program arguments as 'send_text' signal."""
        arguments = QCoreApplication.arguments()
        if len(arguments) > 1:
            for arg in arguments[1:]:
                self.send_text.emit(arg)


def main(args=sys.argv):
    app = QApplication(args)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())
