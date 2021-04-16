from qtpy import QtWidgets, QtCore


def open_file_dialog(parent_widget, caption, directory, filter=None):
    filename = QtWidgets.QFileDialog.getOpenFileName(
        parent_widget, caption=caption, directory=directory, filter=filter
    )
    if isinstance(filename, tuple):  # PyQt5 returns a tuple...
        return str(filename[0])
    return str(filename)


def open_files_dialog(parent_widget, caption, directory, filter=None):
    filenames = QtWidgets.QFileDialog.getOpenFileNames(
        parent_widget, caption=caption, directory=directory, filter=filter
    )
    if isinstance(filenames, tuple):  # PyQt5 returns a tuple...
        filenames = filenames[0]
    return filenames


def save_file_dialog(parent_widget, caption, directory, filter=None):
    filename = QtWidgets.QFileDialog.getSaveFileName(
        parent_widget, caption=caption, directory=directory, filter=filter
    )
    if isinstance(filename, tuple):  # PyQt5 returns a tuple...
        return str(filename[0])
    return str(filename)


class ErrorMessageBox(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(ErrorMessageBox, self).__init__(*args, **kwargs)
        self.setWindowTitle("An error occurred!")

        self.text_lbl = QtWidgets.QLabel()
        self.text_lbl.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.scroll_area = QtWidgets.QScrollArea()

        self.scroll_area.setWidget(self.text_lbl)
        self.scroll_area.setWidgetResizable(True)
        self.ok_btn = QtWidgets.QPushButton('OK')

        _layout = QtWidgets.QGridLayout()
        _layout.addWidget(self.scroll_area, 0, 0, 1, 10)
        _layout.addWidget(self.ok_btn, 1, 9)

        self.setLayout(_layout)
        self.ok_btn.clicked.connect(self.close)

    def setText(self, text_str):
        self.text_lbl.setText(text_str)


class LabelAlignRight(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)


class LabelResult(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


class LabelOutput(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setWordWrap(True)


class LabelOnChange(QtWidgets.QLabel):

    changed = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
