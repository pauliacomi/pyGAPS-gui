import pathlib

from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from pygapsgui.widgets.UtilityWidgets import CollapsibleBox


def open_files_dialog(parent, caption, directory, filter=None) -> "list[pathlib.Path]":
    """Abstract dialog for file opening."""
    filenames = QW.QFileDialog.getOpenFileNames(
        parent=parent,
        caption=caption,
        dir=directory,
        filter=filter,
    )
    if isinstance(filenames, tuple):  # PyQt5 returns a tuple...
        filenames = filenames[0]
    return tuple(map(pathlib.Path, filenames))


def save_file_dialog(parent, caption, directory, filter=None) -> "list[pathlib.Path]":
    """Abstract dialog for file saving."""
    filename = QW.QFileDialog.getSaveFileName(
        parent=parent,
        caption=caption,
        dir=directory,
        filter=filter,
    )
    if isinstance(filename, tuple):  # PyQt5 returns a tuple...
        filename = filename[0]
    if filename:
        return pathlib.Path(filename)


def error_dialog(error: str):
    """Call general error/warning dialog."""
    errorbox = ErrorMessageBox(error)
    errorbox.exec_()


def error_detail_dialog(error: str, trace: str):
    """In-depth (with traceback) error dialog."""
    errorbox = ErrorMessageBox(error, trace)
    errorbox.exec_()


class ErrorMessageBox(QW.QDialog):
    """General error/warning dialog."""
    trace = False

    def __init__(self, text: str, trace: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trace = trace
        self.setWindowTitle("An error occurred!")

        self.text_label = QW.QLabel()
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(QC.Qt.AlignCenter | QC.Qt.AlignVCenter)
        self.text_label.setText(text)

        self.scroll_area = QW.QScrollArea()
        self.scroll_area.setWidget(self.text_label)
        self.scroll_area.setFrameShape(QW.QFrame.NoFrame)
        self.scroll_area.setWidgetResizable(True)

        if trace:
            self.details_box = CollapsibleBox("Debug information.")
            self.details_label = QW.QLabel()
            self.details_label.setText(trace)
            self.copy_button = QW.QPushButton()
            self.copy_button.setText("Copy to clipboard")
            self.copy_button.clicked.connect(
                lambda: QG.QGuiApplication.clipboard().setText(self.details_label.text())
            )
            details_layout = QW.QVBoxLayout()
            details_layout.addWidget(self.copy_button)
            details_layout.addWidget(self.details_label)
            self.details_box.setContentLayout(details_layout)

        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.close)

        _layout = QW.QVBoxLayout(self)
        _layout.addWidget(self.scroll_area)
        if trace:
            _layout.addWidget(self.details_box)
        _layout.addWidget(self.button_box)


def help_dialog(url: str):
    """Display a dialog with online help."""
    help = HelpDialog(url)
    help.exec_()


class HelpDialog(QW.QDialog):
    """General help dialog, actually just a browser window."""
    def __init__(self, url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Help Dialog")

        from qtpy import QtWebEngineWidgets as QWW
        self.browser = QWW.QWebEngineView()
        self.browser.setUrl(QC.QUrl(url))

        _layout = QW.QVBoxLayout(self)
        _layout.addWidget(self.browser)
