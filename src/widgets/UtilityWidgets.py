from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtGui as QG


def open_files_dialog(parent, caption, directory, filter=None):
    """Abstract dialog for file opening."""
    filenames = QW.QFileDialog.getOpenFileNames(
        parent=parent,
        caption=caption,
        dir=directory,
        filter=filter,
    )
    if isinstance(filenames, tuple):  # PyQt5 returns a tuple...
        filenames = filenames[0]
    return filenames


def save_file_dialog(parent, caption, directory, filter=None):
    """Abstract dialog for file saving."""
    filename = QW.QFileDialog.getSaveFileName(
        parent=parent,
        caption=caption,
        dir=directory,
        filter=filter,
    )
    if isinstance(filename, tuple):  # PyQt5 returns a tuple...
        return str(filename[0])
    return str(filename)


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


class EditAlignRight(QW.QLineEdit):
    """Right-aligned LineEdit."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(QC.Qt.AlignRight | QC.Qt.AlignVCenter)


class LabelAlignRight(QW.QLabel):
    """Right-aligned Label."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(QC.Qt.AlignRight | QC.Qt.AlignVCenter)


class LabelResult(QW.QLabel):
    """Label used for results (selectable)."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFrameStyle(QW.QFrame.Panel | QW.QFrame.Sunken)
        self.setAlignment(QC.Qt.AlignHCenter | QC.Qt.AlignVCenter)
        self.setTextInteractionFlags(QC.Qt.TextSelectableByMouse)


class LabelOutput(QW.QTextEdit):
    """An output area."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFrameStyle(QW.QFrame.Panel | QW.QFrame.Sunken)
        self.setAlignment(QC.Qt.AlignLeft | QC.Qt.AlignTop)
        self.setReadOnly(True)
        self.setMinimumSize(50, 80)


class CollapsibleBox(QW.QWidget):
    """
    Collapsible box.

    Adapted from https://stackoverflow.com/a/52617714/8331027
    """
    def __init__(self, title="", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.toggle_button = QW.QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setToolButtonStyle(QC.Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QC.Qt.RightArrow)
        self.toggle_button.toggled.connect(self.on_pressed)

        self.toggle_animation = QC.QParallelAnimationGroup(self)

        self.content_area = QW.QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setWidgetResizable(True)
        self.content_area.setSizePolicy(QW.QSizePolicy.Expanding, QW.QSizePolicy.Expanding)

        _layout = QW.QVBoxLayout(self)
        _layout.setSpacing(0)
        _layout.setContentsMargins(0, 0, 0, 0)
        _layout.addWidget(self.toggle_button)
        _layout.addWidget(self.content_area)

        self.setMaximumWidth(150)

        self.toggle_animation.addAnimation(QC.QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QC.QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QC.QPropertyAnimation(self, b"minimumWidth"))
        self.toggle_animation.addAnimation(QC.QPropertyAnimation(self, b"maximumWidth"))
        self.toggle_animation.addAnimation(
            QC.QPropertyAnimation(self.content_area, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QC.QPropertyAnimation(self.content_area, b"maximumWidth")
        )

    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(QC.Qt.DownArrow if checked else QC.Qt.RightArrow)
        self.toggle_animation.setDirection(
            QC.QAbstractAnimation.Forward if checked else QC.QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        self.content_area.setLayout(layout)
        collapsed_height = (self.sizeHint().height() - self.content_area.maximumHeight())
        collapsed_width = self.sizeHint().width()
        content_height = layout.sizeHint().height()
        content_width = layout.sizeHint().width()
        max_height = min(content_height, 400)
        max_width = min(content_width, 700)

        animation = self.toggle_animation.animationAt(0)
        animation.setDuration(60)
        animation.setStartValue(collapsed_height)
        animation.setEndValue(collapsed_height + max_height)

        animation = self.toggle_animation.animationAt(1)
        animation.setDuration(60)
        animation.setStartValue(collapsed_height)
        animation.setEndValue(collapsed_height + max_width)

        animation = self.toggle_animation.animationAt(2)
        animation.setDuration(60)
        animation.setStartValue(collapsed_width)
        animation.setEndValue(max_width)

        animation = self.toggle_animation.animationAt(3)
        animation.setDuration(60)
        animation.setStartValue(collapsed_width)
        animation.setEndValue(max_width)

        animation = self.toggle_animation.animationAt(4)
        animation.setDuration(60)
        animation.setStartValue(0)
        animation.setEndValue(max_height)

        animation = self.toggle_animation.animationAt(5)
        animation.setDuration(60)
        animation.setStartValue(0)
        animation.setEndValue(max_width)
