#!/usr/bin/env python3

import os
import sys
from PySide2.QtWidgets import QMainWindow, QApplication, QMessageBox
from PySide2.QtCore import QCoreApplication, Signal, QThread, QFile, Qt

from src.views.mainwindow import Ui_MainWindow
from src.views.utility import open_files_dialog, save_file_dialog
from src.models.mainmodel import MainModel
from src.controllers.graphcontroller import GraphController
from src.controllers.textinfocontroller import TextInfoController

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)


class ApplicationWindow(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create models
        self.model = MainModel()

        # Create views
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create controllers
        self.explorer_controller = GraphController(
            self.ui.graphView, self.model)
        self.graph_controller = GraphController(
            self.ui.graphView, self.model)
        self.textinfo_controller = TextInfoController(
            self.ui.textInfo, self.model)

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

        self.ui.okButton.clicked.connect(self.quit_app)
        self.ui.cancelButton.clicked.connect(self.quit_app)

    def quit_app(self):
        """Close application."""
        # answer = QMessageBox.question(self, 'Quit program', 'Are you sure?',
        #                               QMessageBox.Yes | QMessageBox.No)
        # if answer == QMessageBox.Yes:
        #     self.close()
        self.close()

    def open_file(self):
        """Open isotherm from file."""
        default_file_name = '.'
        filename = open_files_dialog(self, "Load an isotherm",
                                     default_file_name,
                                     filter='pyGAPS isotherms (*.json)')

        if filename is not None and filename != '':
            self.model.load(filename)

    def save_content(self):
        """Save isotherm to file."""
        default_file_name = '.'
        filename = save_file_dialog(self, "Save an isotherm",
                                    default_file_name,
                                    filter='pyGAPS Isotherm (*.json)')

        if filename is not None and filename != '':
            self.model.save(filename)

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
        super(Worker, self).__init__(parent)

    def run(self):
        """Start work method and take care about run-time errors in thread"""
        result = self.work()
        self.result.emit(result)

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
