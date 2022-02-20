from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW


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


class LabelAlignCenter(QW.QLabel):
    """Center-aligned Label."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(QC.Qt.AlignCenter | QC.Qt.AlignVCenter)


class LabelResult(QW.QLabel):
    """Label used for results (selectable)."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFrameStyle(QW.QFrame.Panel | QW.QFrame.Sunken)
        self.setAlignment(QC.Qt.AlignHCenter | QC.Qt.AlignVCenter)
        self.setTextInteractionFlags(QC.Qt.TextSelectableByMouse)


class LabelOutput(QW.QTextEdit):
    """An output area for large amount of text."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFrameStyle(QW.QFrame.Panel | QW.QFrame.Sunken)
        self.setAlignment(QC.Qt.AlignLeft | QC.Qt.AlignTop)
        self.setReadOnly(True)
        self.setMinimumSize(50, 80)


class FreeSpinBox(QW.QSpinBox):
    #TODO implement
    pass


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


class HeightHeaderView(QW.QHeaderView):
    def __init__(self, parent=None):
        super().__init__(QC.Qt.Horizontal, parent=parent)
        self.setSectionResizeMode(QW.QHeaderView.Stretch)
        self.setStretchLastSection(True)
        self.setDefaultAlignment(QC.Qt.AlignCenter | QC.Qt.Alignment(QC.Qt.TextWordWrap))

    def sectionSizeFromContents(self, logicalIndex):
        text = self.model().headerData(logicalIndex, self.orientation(), QC.Qt.DisplayRole)
        alignment = self.defaultAlignment()
        metrics = QG.QFontMetrics(self.fontMetrics())
        rect = metrics.boundingRect(QC.QRect(), alignment, text)
        return rect.size()
