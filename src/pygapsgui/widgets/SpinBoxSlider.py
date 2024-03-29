import math

from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from pygapsgui.widgets.SciDoubleSpinbox import ScientificDoubleSpinBox
from pygapsgui.widgets.UtilityWidgets import LabelAlignRight


class QSpinBoxSlider(QW.QWidget):
    """Slider connected to a SpinBox acting as a whole. A label is included."""

    name = None  # A name for the value it is tracing, useful for identification
    changed = QC.Signal(float)
    changed_named = QC.Signal(str, float)
    minv = 0
    maxv = 100
    step = 1

    def __init__(self, value=0, *args, **kwargs):
        """Initial init."""
        super().__init__(*args, **kwargs)

        self.value = value

        # label
        self.label = LabelAlignRight(self)
        self.label.setMinimumSize(5, 2)
        self.label.setMaximumSize(50, 10)

        # spinbox
        self.spin_box = ScientificDoubleSpinBox()
        self.spin_box.setDecimals(3)
        self.spin_box.setValue(value)
        self.spin_box.valueChanged.connect(self.handleSpinBox)

        # slider
        self.slider = QW.QSlider(self)
        self.slider.setRange(self.minv, self.maxv)
        self.slider.setSingleStep(self.step)
        self.slider.setOrientation(QC.Qt.Horizontal)
        self.slider.setTracking(False)
        self.slider.valueChanged.connect(self.handleSlider)

    def setText(self, text):
        """Pass-through to label."""
        self.label.setText(text)

    def scaleTo(self, value):
        """Convert to slider domain from range domain."""
        return round(value / (self.maxv - self.minv) * 100)

    def scaleFrom(self, value):
        """Convert from slider domain to range domain."""
        return value / 100 * (self.maxv - self.minv)

    def setRange(self, minv=0, maxv=100, step=None):
        """Set the range of the component."""

        if not step:
            step = abs(maxv - minv) / 100

        self.minv = minv
        self.maxv = maxv
        self.step = step

        self.spin_box.setRange(minv, maxv)
        self.spin_box.setSingleStep(step)

        # dec_pnts = 2
        # exp = math.log10(step)
        # if exp > 2:
        #     dec_pnts = 0
        # elif exp < 0:
        #     dec_pnts = round(abs(exp)) + 2
        # self.spin_box.setDecimals(dec_pnts)

    def setValue(self, value, emit=True):
        """Set a value for the slider/spinbox."""
        # value
        if not emit:
            self.slider.blockSignals(True)
            self.spin_box.blockSignals(True)
        self.spin_box.setValue(value)
        self.slider.setValue(self.scaleTo(value))
        if not emit:
            self.slider.blockSignals(False)
            self.spin_box.blockSignals(False)

    def getValue(self) -> float:
        """Pass-through to spinbox value."""
        return self.spin_box.value()

    def handleSpinBox(self, value, emit=True):
        """Make sure value is changed in known increments."""
        value = self.adjustValue(value)

        if emit:
            self.emitValueChange()

    def handleSlider(self, value):
        """When slider is moved we set the spinbox value."""
        self.spin_box.setValue(self.scaleFrom(value))

    def adjustValue(self, new_value):
        """
        Check that the value is a multiple of the step size, rounds to the
        nearest step if it is not.
        """
        step = self.step
        adj = round(new_value / step)
        adj = adj * step
        return adj

    def emitValueChange(self):
        """
        Emit range signal, but only if it actually changed.
        This also updates the slider.
        """
        should_emit = False
        if self.value != self.spin_box.value():
            self.value = self.spin_box.value()
            should_emit = True
        if should_emit:
            self.slider.blockSignals(True)
            self.slider.setValue(self.scaleTo(self.value))
            self.slider.blockSignals(False)
            self.changed.emit(self.value)
            if self.name is not None:
                self.changed_named.emit(self.name, self.value)


class QHSpinBoxSlider(QSpinBoxSlider):
    """Horizontal implementation of the QSpinBoxSlider."""
    def __init__(self, value=0, parent=None, **kwargs):
        super().__init__(value=value, parent=parent, **kwargs)

        _layout = QW.QGridLayout(self)
        _layout.addWidget(self.label, 0, 0, 1, 1)
        _layout.addWidget(self.slider, 0, 1, 1, 2)
        _layout.addWidget(self.spin_box, 0, 3, 1, 1)
