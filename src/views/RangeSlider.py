#
# The MIT License
#
# Copyright (c) 2009 Zhuang Lab, Harvard University
# Copyright (c) 2016 Sean Yeh
#   (Porting to qtpy, Python3 compatibility, and some trivial modifications)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import decimal
from qtpy import QtCore, QtGui
import sys

from qtpy.QtWidgets import (
    QDoubleSpinBox,
    QWidget,
    QDialog,
    QSizePolicy,
    QHBoxLayout,
    QGridLayout,
    QDialogButtonBox,
)


class QRangeSlider(QWidget):
    """
    Range Slider super class.

    @param slider_range [min, max, step size].
    @param values [initial minimum setting, initial maximum setting].
    @param parent (Optional) The PyQt parent of this widget.
    """
    doubleClick = QtCore.Signal(bool)
    rangeChanged = QtCore.Signal(float, float)

    def __init__(self, slider_range, values, parent=None):
        QWidget.__init__(self, parent)
        self.bar_width = 10
        self.emit_while_moving = False
        self.moving = "none"
        self.old_min_val = 0.0
        self.old_max_val = 0.0
        self.scale = 0
        self.setMouseTracking(False)
        self.single_step = 0.0

        if slider_range:
            self.setRange(slider_range)
        else:
            self.setRange([0.0, 1.0, 0.01])
        if values:
            self.setValues(values)
        else:
            self.setValues([0.3, 0.6])

        self.setFocusPolicy(QtCore.Qt.ClickFocus)

    def emitRange(self):
        """Emits the rangeChanged signal, if the range has actually changed."""
        if (self.old_min_val !=
            self.min_val) or (self.old_max_val != self.max_val):
            self.rangeChanged.emit(self.min_val, self.max_val)
            self.old_min_val = self.min_val
            self.old_max_val = self.max_val
            if 0:
                print("Range change:", self.min_val, self.max_val)

    def getValues(self):
        """@return [current minimum, current maximum]."""
        return [self.min_val, self.max_val]

    def keyPressEvent(self, event):
        """@param event A PyQt key press event."""
        key = event.key()

        # move bars based on arrow keys
        moving_max = False
        if key == QtCore.Qt.Key_Up:
            self.max_val += self.single_step
            moving_max = True
        elif key == QtCore.Qt.Key_Down:
            self.max_val -= self.single_step
            moving_max = True
        elif key == QtCore.Qt.Key_Left:
            self.min_val -= self.single_step
        elif key == QtCore.Qt.Key_Right:
            self.min_val += self.single_step

        # update (if necessary) based on allowed range
        if moving_max:
            if (self.max_val < self.min_val):
                self.min_val = self.max_val
        else:
            if (self.min_val > self.max_val):
                self.max_val = self.min_val

        if (self.min_val < self.start):
            self.min_val = self.start
        if (self.max_val < self.start):
            self.max_val = self.start

        slider_max = self.start + self.scale
        if (self.min_val > slider_max):
            self.min_val = slider_max
        if (self.max_val > slider_max):
            self.max_val = slider_max

        self.emitRange()
        self.updateDisplayValues()
        self.update()

    def mouseDoubleClickEvent(self, event):
        """
        Emits a doubleClick signal when the user double clicks on the slider.

        @param event A PyQt double click event.
        """
        self.doubleClick.emit(True)

    def mouseMoveEvent(self, event):
        """
        Handles moving the slider bars if necessary.

        @param event A PyQt mouse motion event.
        """
        size = self.rangeSliderSize()
        diff = self.start_pos - self.getPos(event)
        if self.moving == "min":
            temp = self.start_display_min - diff
            if (temp >= self.bar_width) and (temp < size - self.bar_width):
                self.display_min = temp
                if self.display_max < self.display_min:
                    self.display_max = self.display_min
                self.updateScaleValues()
                if self.emit_while_moving:
                    self.emitRange()
        elif self.moving == "max":
            temp = self.start_display_max - diff
            if (temp >= self.bar_width) and (temp < size - self.bar_width):
                self.display_max = temp
                if self.display_max < self.display_min:
                    self.display_min = self.display_max
                self.updateScaleValues()
                if self.emit_while_moving:
                    self.emitRange()
        elif self.moving == "bar":
            temp = self.start_display_min - diff
            if (temp >= self.bar_width) and (
                temp < size - self.bar_width -
                (self.start_display_max - self.start_display_min)
            ):
                self.display_min = temp
                self.display_max = self.start_display_max - diff
                self.updateScaleValues()
                if self.emit_while_moving:
                    self.emitRange()

    def mousePressEvent(self, event):
        """
        If the mouse is pressed down when the cursor is over one of the slider
        bars then we need to move the slider bar as the mouse moves.

        @param event A PyQt event.
        """
        pos = self.getPos(event)
        if abs(self.display_min - 0.5 * self.bar_width -
               pos) < (0.5 * self.bar_width):
            self.moving = "min"
        elif abs(self.display_max + 0.5 * self.bar_width -
                 pos) < (0.5 * self.bar_width):
            self.moving = "max"
        elif (pos > self.display_min) and (pos < self.display_max):
            self.moving = "bar"
        self.start_display_min = self.display_min
        self.start_display_max = self.display_max
        self.start_pos = pos

    def mouseReleaseEvent(self, event):
        """
        Stop moving the slider bar when the mouse is released.

        @param event A PyQt event.
        """
        if not (self.moving == "none"):
            self.emitRange()
        self.moving = "none"

    def resizeEvent(self, event):
        """
        Handles adusting the (displayed) scroll bars positions when the slider
        is resized.

        @param event A PyQt event.
        """
        QWidget.resizeEvent(self, event)
        self.updateDisplayValues()

    def setEmitWhileMoving(self, flag):
        """
       Set whether or not to emit rangeChanged signal while the slider is 
       being moved with the mouse.

       @param flag True/False emit while moving.
        """
        if flag:
            self.emit_while_moving = True
        else:
            self.emit_while_moving = False

    def setRange(self, slider_range):
        """
        @param slider_range [min, max, step size].
        """
        self.start = slider_range[0]
        # seanyeh: I added this to keep track of max
        self.end = slider_range[1]
        self.scale = slider_range[1] - slider_range[0]
        self.single_step = slider_range[2]

        # Check that the range is a multiple of the step size.
        steps = self.scale / self.single_step
        if (abs(steps - round(steps)) > 0.01 * self.single_step):
            raise Exception("Slider range is not a multiple of the step size!")

    def setValues(self, values, emit=True):
        """
        @param values [position of minimum slider, position of maximum slider].
        """
        self.min_val = values[0]
        self.max_val = values[1]
        if emit:
            self.emitRange()
        self.updateDisplayValues()
        self.update()

    def updateDisplayValues(self):
        """
        This updates the display value, i.e. the real location in the widgets 
        where the bars are drawn.
        """
        size = float(self.rangeSliderSize() - 2 * self.bar_width - 1)
        self.display_min = int(
            size * (self.min_val - self.start) / self.scale
        ) + self.bar_width
        self.display_max = int(
            size * (self.max_val - self.start) / self.scale
        ) + self.bar_width

    def updateScaleValues(self):
        """
        This updates the internal / real values that correspond to the 
        current slider positions.
        """
        size = float(self.rangeSliderSize() - 2 * self.bar_width - 1)
        if (self.moving == "min") or (self.moving == "bar"):
            self.min_val = self.start + \
                (self.display_min - self.bar_width)/float(size) * self.scale
            self.min_val = float(
                round(self.min_val / self.single_step)
            ) * self.single_step
        if (self.moving == "max") or (self.moving == "bar"):
            self.max_val = self.start + \
                (self.display_max - self.bar_width)/float(size) * self.scale
            self.max_val = float(
                round(self.max_val / self.single_step)
            ) * self.single_step
        self.updateDisplayValues()
        self.update()


# QHRangeSlider
#
#
class QHRangeSlider(QRangeSlider):
    """
    Horizontal Range Slider.

    @param slider_range (Optional) [min, max, step size].
    @param values (Optional) [initial minimum setting, initial maximum setting].
    @param parent (Optional) The PyQt parent of this widget.
    """
    def __init__(self, slider_range=None, values=None, parent=None):
        QRangeSlider.__init__(self, slider_range, values, parent)
        if parent is not None:
            self.setGeometry(200, 200, 200, 100)

    def getPos(self, event):
        """
        @param event A PyQt event.

        @return The location in x of the event.
        """
        return event.x()

    def paintEvent(self, event):
        """
        Draw the horizontal slider.

        @param event A PyQt event.
        """
        painter = QtGui.QPainter(self)
        w = self.width()
        h = self.height()

        # background
        painter.setPen(QtCore.Qt.gray)
        painter.setBrush(QtCore.Qt.lightGray)
        painter.drawRect(2, 2, w - 4, h - 4)

        # range bar
        painter.setPen(QtCore.Qt.darkGray)
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawRect(
            self.display_min - 1, 5, self.display_max - self.display_min + 2,
            h - 10
        )

        # min & max tabs
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.gray)
        painter.drawRect(
            self.display_min - self.bar_width, 1, self.bar_width, h - 2
        )

        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.gray)
        painter.drawRect(self.display_max, 1, self.bar_width, h - 2)

    def rangeSliderSize(self):
        """
        @return The current width of the slider widget.
        """
        return self.width()


class QVRangeSlider(QRangeSlider):
    """
    Vertical Range Slider.

    @param slider_range (Optional) [min, max, step size].
    @param values (Optional) [initial minimum setting, initial maximum setting].
    @param parent (Optional) The PyQt parent of this widget.
    """
    def __init__(self, slider_range=None, values=None, parent=None):
        QRangeSlider.__init__(self, slider_range, values, parent)
        if parent is not None:
            self.setGeometry(200, 200, 100, 200)

    def getPos(self, event):
        """
        @param event A PyQt event.

        @return The location in x of the event.
        """
        return self.height() - event.y()

    def paintEvent(self, event):
        """
        Draw the vertical slider.

        @param event A PyQt event.
        """
        painter = QtGui.QPainter(self)
        w = self.width()
        h = self.height()

        # background
        painter.setPen(QtCore.Qt.gray)
        painter.setBrush(QtCore.Qt.lightGray)
        painter.drawRect(2, 2, w - 4, h - 4)

        # range bar
        painter.setPen(QtCore.Qt.darkGray)
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawRect(
            5, h - self.display_max - 1, w - 10,
            self.display_max - self.display_min + 1
        )

        # min & max tabs
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.gray)
        painter.drawRect(
            1, h - self.display_max - self.bar_width - 1, w - 2, self.bar_width
        )

        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.gray)
        painter.drawRect(1, h - self.display_min - 1, w - 2, self.bar_width)

    def rangeSliderSize(self):
        """
        @return The current height of the slider widget.
        """
        return self.height()


class QSpinBoxRangeSlider(QWidget):
    """
    Range slider with two double spin boxes super class.

    @param slider_range [min, max, step size].
    @param values [initial minimum setting, initial maximum setting].
    @param parent (Optional) The PyQt parent of this widget.
    """

    doubleClick = QtCore.Signal(bool)
    rangeChanged = QtCore.Signal(float, float)

    def __init__(self, slider_range, values, parent=None, **kwargs):
        QWidget.__init__(self, parent)
        self.max_val = values[1]
        self.min_val = values[0]
        self.range_slider = False

        if 'dec_pnts' in kwargs:
            dec_pnts = kwargs['dec_pnts']
        else:
            # Attempt to calculate the appropriate number of decimal points.
            dec_pnts = abs(
                decimal.Decimal(slider_range[2]).as_tuple().exponent
            )

        self.min_spin_box = QDoubleSpinBox()
        self.min_spin_box.setDecimals(dec_pnts)
        self.min_spin_box.setMinimum(slider_range[0])
        self.min_spin_box.setMaximum(slider_range[1])
        self.min_spin_box.setSingleStep(slider_range[2])
        self.min_spin_box.setValue(values[0])
        self.min_spin_box.valueChanged.connect(self.handleMinSpinBox)

        self.max_spin_box = QDoubleSpinBox()
        self.max_spin_box.setDecimals(dec_pnts)
        self.max_spin_box.setMinimum(slider_range[0])
        self.max_spin_box.setMaximum(slider_range[1])
        self.max_spin_box.setSingleStep(slider_range[2])
        self.max_spin_box.setValue(values[1])
        self.max_spin_box.valueChanged.connect(self.handleMaxSpinBox)

    def addRangeSlider(self, range_slider):
        """
        Add the range slider element and connects it's signals.

        @param range_slider
        """
        self.range_slider = range_slider

        # Make range slider take as much of the space as possible.
        size_policy = QSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        self.range_slider.setSizePolicy(size_policy)

        # Connect signals/
        self.range_slider.doubleClick.connect(self.handleDoubleClick)
        self.range_slider.rangeChanged.connect(self.handleRangeChange)

    def adjustValue(self, new_value):
        """
        Check that the value is a multiple of the step size, rounds to the
        nearest step if it is not.

        @param a_value.
        @return [The adjusted value, True / False if it was adjusted].
        """
        adj = round(new_value / self.range_slider.single_step)
        adj = adj * self.range_slider.single_step
        return adj

    def emitRangeChange(self):
        """
        Emit range changed signal, but only if it actually changed.
        This also updates the range slider.
        """
        should_emit = False
        if (self.min_val != self.min_spin_box.value()):
            self.min_val = self.min_spin_box.value()
            should_emit = True
        if (self.max_val != self.max_spin_box.value()):
            self.max_val = self.max_spin_box.value()
            should_emit = True
        if should_emit:
            if 0:
                print(self.min_val, self.max_val)
            self.range_slider.setValues([self.min_val, self.max_val])
            self.rangeChanged.emit(self.min_val, self.max_val)

    def getValues(self):
        """
        @return [current minimum, current maximum].
        """
        return [self.min_spin_box.value(), self.max_spin_box.value()]

    def setValues(self, values, emit=True):
        """
        @param values [position of minimum slider, position of maximum slider].
        """
        self.range_slider.setValues(values, emit)
        if not emit:
            self.min_spin_box.blockSignals(True)
            self.max_spin_box.blockSignals(True)
        self.handleRangeChange(values[0], values[1])
        if not emit:
            self.min_spin_box.blockSignals(False)
            self.max_spin_box.blockSignals(False)

    def handleDoubleClick(self, boolean):
        """
        This just passes on the double click signal from the range slider.

        @param boolean A dummy parameter.
        """
        self.doubleClick.emit(boolean)

    def handleMaxSpinBox(self, new_value, emit=True):
        """
        @param new_value The new value of the spin box.
        """
        self.max_spin_box.setValue(self.adjustValue(new_value))
        if (new_value < self.min_spin_box.value()):
            self.min_spin_box.setValue(new_value)

        if emit:
            self.emitRangeChange()

    def handleMinSpinBox(self, new_value, emit=True):
        """
        @param new_value The new value of the spin box.
        """
        self.min_spin_box.setValue(self.adjustValue(new_value))
        if (new_value > self.max_spin_box.value()):
            self.max_spin_box.setValue(new_value)

        if emit:
            self.emitRangeChange()

    def handleRangeChange(self, min_val, max_val):
        """
        Handle the range changed signal from the range slider.

        @param min_val, max_val
        """
        self.min_spin_box.setValue(min_val)
        self.max_spin_box.setValue(max_val)

    def setEmitWhileMoving(self, flag):
        """
        Set whether or not to emit rangeChanged signal while the slider
        is being moved with the mouse.

        @param flag True/False emit while moving.
        """
        self.range_slider.setEmitWhileMoving(flag)


class QHSpinBoxRangeSlider(QSpinBoxRangeSlider):
    """
    Horizontal range slider with two double spin boxes.

    @param slider_range [min, max, step size].
    @param values [initial minimum setting, initial maximum setting].
    @param parent (Optional) The PyQt parent of this widget.
    """
    def __init__(self, slider_range, values, parent=None, **kwargs):
        QSpinBoxRangeSlider.__init__(
            self, slider_range, values, parent, **kwargs
        )
        self.addRangeSlider(QHRangeSlider(slider_range, values, self))

        if (not parent):
            self.setGeometry(200, 200, 300, 100)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.min_spin_box)
        self.layout.addWidget(self.range_slider)
        self.layout.addWidget(self.max_spin_box)


class QVSpinBoxRangeSlider(QSpinBoxRangeSlider):
    """
    Vertical range slider with two double spin boxes.

    @param slider_range [min, max, step size].
    @param values [initial minimum setting, initial maximum setting].
    @param parent (Optional) The PyQt parent of this widget.
    """
    def __init__(self, slider_range, values, parent=None, **kwargs):
        QSpinBoxRangeSlider.__init__(
            self, slider_range, values, parent, **kwargs
        )
        self.addRangeSlider(QVRangeSlider(slider_range, values, self))

        if (not parent):
            self.setGeometry(200, 200, 100, 300)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.max_spin_box)
        self.layout.addWidget(self.range_slider)
        self.layout.addWidget(self.min_spin_box)
