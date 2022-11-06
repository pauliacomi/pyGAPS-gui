from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from pygapsgui.widgets.SciDoubleSpinbox import ScientificDoubleSpinBox
from pygapsgui.widgets.SpinBoxSlider import QSpinBoxSlider
from pygapsgui.widgets.UtilityWidgets import LabelAlignCenter


class QSpinBoxLimitSlider(QSpinBoxSlider):
    """Spinbox slider with added limit labels."""
    def __init__(self, value=0, *args, **kwargs):
        super().__init__(value, *args, **kwargs)

        # max/min spinboxes
        self.max_spin_box = ScientificDoubleSpinBox()
        self.max_spin_box.setDecimals(3)
        self.max_spin_box.setValue(self.maxv)
        self.max_spin_box.valueChanged.connect(self.handleMaxSpinBox)

        self.min_spin_box = ScientificDoubleSpinBox()
        self.min_spin_box.setDecimals(3)
        self.min_spin_box.setValue(self.minv)
        self.min_spin_box.valueChanged.connect(self.handleMinSpinBox)

    def setRange(self, minv=0, maxv=100, step=None):
        super().setRange(minv, maxv, step)
        self.min_spin_box.setValue(minv)
        self.min_spin_box.setSingleStep(self.step)
        self.max_spin_box.setValue(maxv)
        self.max_spin_box.setSingleStep(self.step)

    def handleMaxSpinBox(self, value):
        """Expand range based on limit spinbox."""
        self.setRange(self.minv, value)
        self.slider.blockSignals(True)
        self.slider.setValue(self.scaleTo(self.value))
        self.slider.blockSignals(False)

    def handleMinSpinBox(self, value):
        """Expand range based on limit spinbox."""
        self.setRange(value, self.maxv)
        self.slider.blockSignals(True)
        self.slider.setValue(self.scaleTo(self.value))
        self.slider.blockSignals(False)


class QHSpinBoxLimitSlider(QSpinBoxLimitSlider):
    """Horizontal implementation of the QSpinBoxLimitSlider."""
    def __init__(self, value=0, parent=None, **kwargs):
        super().__init__(value=value, parent=parent, **kwargs)

        _layout = QW.QGridLayout(self)
        _layout.addWidget(LabelAlignCenter("min"), 0, 0, 1, 1)
        _layout.addWidget(self.label, 0, 2, 1, 1)
        _layout.addWidget(LabelAlignCenter("max"), 0, 5, 1, 1)
        _layout.addWidget(self.spin_box, 0, 3, 1, 1)
        _layout.addWidget(self.min_spin_box, 1, 0, 1, 1)
        _layout.addWidget(self.slider, 1, 1, 1, 4)
        _layout.addWidget(self.max_spin_box, 1, 5, 1, 1)

        self.setMaximumHeight(70)
