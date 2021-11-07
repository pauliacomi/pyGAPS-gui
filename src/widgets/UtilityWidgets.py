from qtpy import QtCore as QC
from qtpy import QtWidgets as QW


def open_file_dialog(parent_widget, caption, directory, filter=None):
    filename = QW.QFileDialog.getOpenFileName(parent_widget, caption=caption, directory=directory, filter=filter)
    if isinstance(filename, tuple):  # PyQt5 returns a tuple...
        return str(filename[0])
    return str(filename)


def open_files_dialog(parent_widget, caption, directory, filter=None):
    filenames = QW.QFileDialog.getOpenFileNames(parent_widget, caption=caption, directory=directory, filter=filter)
    if isinstance(filenames, tuple):  # PyQt5 returns a tuple...
        filenames = filenames[0]
    return filenames


def save_file_dialog(parent_widget, caption, directory, filter=None):
    filename = QW.QFileDialog.getSaveFileName(parent_widget, caption=caption, directory=directory, filter=filter)
    if isinstance(filename, tuple):  # PyQt5 returns a tuple...
        return str(filename[0])
    return str(filename)


def error_dialog(error: str):
    errorbox = ErrorMessageBox()
    errorbox.setText(error)
    errorbox.exec_()


class ErrorMessageBox(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super(ErrorMessageBox, self).__init__(*args, **kwargs)
        self.setWindowTitle("An error occurred!")

        self.text_lbl = QW.QLabel()
        self.text_lbl.setTextInteractionFlags(QC.Qt.TextSelectableByMouse)
        self.scroll_area = QW.QScrollArea()

        self.scroll_area.setWidget(self.text_lbl)
        self.scroll_area.setWidgetResizable(True)
        self.ok_btn = QW.QPushButton('OK')

        _layout = QW.QGridLayout()
        _layout.addWidget(self.scroll_area, 0, 0, 1, 10)
        _layout.addWidget(self.ok_btn, 1, 9)

        self.setLayout(_layout)
        self.ok_btn.clicked.connect(self.close)

    def setText(self, text_str):
        self.text_lbl.setText(text_str)


class EditAlignRight(QW.QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(QC.Qt.AlignRight | QC.Qt.AlignVCenter)


class LabelAlignRight(QW.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(QC.Qt.AlignRight | QC.Qt.AlignVCenter)


class LabelResult(QW.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFrameStyle(QW.QFrame.Panel | QW.QFrame.Sunken)
        self.setAlignment(QC.Qt.AlignHCenter | QC.Qt.AlignVCenter)


class LabelOutput(QW.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFrameStyle(QW.QFrame.Panel | QW.QFrame.Sunken)
        self.setAlignment(QC.Qt.AlignLeft | QC.Qt.AlignTop)
        self.setWordWrap(True)
        self.setMinimumSize(50, 100)
