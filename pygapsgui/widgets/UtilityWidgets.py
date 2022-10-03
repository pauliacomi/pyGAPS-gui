from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from pygapsgui.widgets.SciDoubleSpinbox import ScientificDoubleSpinBox


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
    """A QSpinbox with a large upper bound."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximum(999999999)


class FloatStandardItem(QG.QStandardItem):
    """A QStandardItem which can store floats."""
    val = None

    def type(self) -> int:
        """Expects custom type."""
        return QG.QStandardItem.UserType + 1

    def setData(self, value, role: int = QC.Qt.DisplayRole) -> None:
        """Just store data as float."""
        if role in [QC.Qt.DisplayRole, QC.Qt.EditRole]:
            self.val = value
        self.emitDataChanged()

    def data(self, role: int = QC.Qt.DisplayRole):
        """Get back same float."""
        if role in [QC.Qt.DisplayRole, QC.Qt.EditRole]:
            return self.val


class LimitEdit(QW.QWidget):
    """Allows two numbers intended as limits to be set/read."""

    lower_changed = QC.Signal(float)
    upper_changed = QC.Signal(float)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.lower_edit = ScientificDoubleSpinBox()
        self.upper_edit = ScientificDoubleSpinBox()
        self.lower_edit.valueChanged.connect(self.lower_changed)
        self.upper_edit.valueChanged.connect(self.upper_changed)
        _layout = QW.QHBoxLayout(self)
        _layout.addWidget(self.lower_edit)
        _layout.addWidget(self.upper_edit)

    def set_values(self, values):
        """Individually set upper/lower values."""
        self.lower_edit.setValue(values[0])
        self.upper_edit.setValue(values[1])

    def set_limits_lower(self, low, high):
        """Set lower box limits."""
        if low:
            self.lower_edit.setMinimum(low)
        if high:
            self.lower_edit.setMaximum(high)

    def set_limits_upper(self, low, high):
        """Set lower box limits."""
        if low:
            self.upper_edit.setMinimum(low)
        if high:
            self.upper_edit.setMaximum(high)

    def values(self):
        """Get tuple of the upper/lower values."""
        return self.lower_edit.value(), self.upper_edit.value()


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
        """Animate and toggle open/closed."""
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(QC.Qt.DownArrow if checked else QC.Qt.RightArrow)
        self.toggle_animation.setDirection(
            QC.QAbstractAnimation.Forward if checked else QC.QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        """Populate the box layout."""
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
    """A table QHeaderView which wraps and adapts to text height."""
    def __init__(self, parent=None):
        super().__init__(QC.Qt.Horizontal, parent=parent)
        self.setSectionResizeMode(QW.QHeaderView.Stretch)
        self.setStretchLastSection(True)
        self.setDefaultAlignment(QC.Qt.AlignCenter | QC.Qt.Alignment(QC.Qt.TextWordWrap))

    def sectionSizeFromContents(self, logicalIndex):
        """Tweak bounding rectangle based on data."""
        text = self.model().headerData(logicalIndex, self.orientation(), QC.Qt.DisplayRole)
        alignment = self.defaultAlignment()
        metrics = QG.QFontMetrics(self.fontMetrics())
        rect = metrics.boundingRect(QC.QRect(), alignment, text)
        return rect.size()
