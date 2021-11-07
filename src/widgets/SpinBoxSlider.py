import math

from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from src.widgets.UtilityWidgets import LabelAlignRight


class QSpinBoxSlider(QW.QWidget):

    changed = QC.Signal(float)
    minv = 0
    maxv = 100
    step = 1
    """
    Range slider with label and spinbox.
    """
    def __init__(self, value=0, parent=None, **kwargs):
        super().__init__(parent)

        self.value = value

        layout = QW.QGridLayout(self)

        # label
        self.label = LabelAlignRight(self)
        self.label.setMinimumSize(5, 2)

        # spinbox
        self.spin_box = QW.QDoubleSpinBox(self)
        self.spin_box.setDecimals(2)
        # self.spin_box.setMinimum(slider_range[0])
        # self.spin_box.setMaximum(slider_range[1])
        # self.spin_box.setSingleStep(slider_range[2])
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
        self.label.setText(text)

    def scaleTo(self, value):
        return round(value / (self.maxv - self.minv) * 100)

    def scaleFrom(self, value):
        return value / 100 * (self.maxv - self.minv)

    def setRange(self, minv=0, maxv=100, step=None):

        if not step:
            step = abs(maxv - minv) / 100

        self.minv = minv
        self.maxv = maxv
        self.step = step

        self.spin_box.setRange(minv, maxv)
        self.spin_box.setSingleStep(step)

        dec_pnts = 2
        exp = math.log10(step)
        if exp > 2:
            dec_pnts = 0
        elif exp < 0:
            dec_pnts = round(abs(exp)) + 2
        self.spin_box.setDecimals(dec_pnts)

    def setValue(self, value, emit=True):
        self.setRange(maxv=value * 2)

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
        return self.spin_box.value()

    def handleSpinBox(self, value, emit=True):
        if value > self.maxv:
            self.setRange(maxv=value * 2)
        self.spin_box.setValue(self.adjustValue(value))

        if emit:
            self.emitValueChange()

    def handleSlider(self, value):
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


class QHSpinBoxSlider(QSpinBoxSlider):
    def __init__(self, value=0, parent=None, **kwargs):
        super().__init__(value=value, parent=parent, **kwargs)

        layout = self.layout()
        layout.addWidget(self.label, 0, 0, 1, 1)
        layout.addWidget(self.spin_box, 0, 1, 1, 1)
        layout.addWidget(self.slider, 1, 0, 1, 2)
