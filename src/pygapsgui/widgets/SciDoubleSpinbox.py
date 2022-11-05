"""Scientific spin box
Adapted from https://gist.github.com/jdreaver/0be2e44981159d0854f5
"""

import re

import numpy as np
from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

# Regular expression to find floats. Match groups are the whole string, the
# whole coefficient, the decimal part of the coefficient, and the exponent
# part.
_float_re = re.compile(r'(([+-]?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)')


def valid_float_string(string):
    """Check if a string contains a valid sci-format float."""
    match = _float_re.search(string)
    return match.groups()[0] == string if match else False


def format_float(value):
    """Format float as sci-float, modified form of the 'g' format specifier."""
    if not isinstance(value, float):
        return str(value)
    string = f"{value:.5g}".replace("e+", "e")
    string = re.sub(r"e(-?)0*(\d+)", r"e\1\2", string)
    return string


class FloatValidator(QG.QValidator):
    """QValidator for float numbers."""
    def validate(self, string, position):
        """Called to check if input is valid."""
        if valid_float_string(string):
            return self.State.Acceptable, string, position
        if string == "" or string[position - 1] in 'e.-+':
            return self.State.Intermediate, string, position
        return self.State.Invalid, string, position

    def fixup(self, text):
        """Can repair some basic errors."""
        match = _float_re.search(text)
        return match.groups()[0] if match else ""


class ScientificDoubleSpinBox(QW.QDoubleSpinBox):
    """A QDoubleSpinbox which shows numbers in scientific format."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimum(-np.inf)
        self.setMaximum(np.inf)
        self.validator = FloatValidator()
        self.setDecimals(1000)
        self.setAlignment(QC.Qt.AlignCenter)

    def validate(self, text, position):
        """Passthrough to validator."""
        return self.validator.validate(text, position)

    def fixup(self, text):
        """Passthrough to validator."""
        return self.validator.fixup(text)

    def valueFromText(self, text):
        """Convert the text to the real value."""
        return float(text)

    def textFromValue(self, value):
        """Nicely display a scientific float."""
        return format_float(value)


class SciFloatSpinDelegate(QW.QStyledItemDelegate):
    """A StyledItemDelegate that displays a ScientificDoubleSpinBox"""
    def createEditor(self, parent, option, index):
        """Give an instance of the SciDoubleSpinbox"""
        return ScientificDoubleSpinBox(parent)

    def setEditorData(self, editor: QW.QWidget, index: QC.QModelIndex) -> None:
        """Transfer the item value to the editor."""
        editor.setValue(index.data())

    def displayText(self, value, locale):
        """Called when the underlying text is displayed."""
        return format_float(value)


class SciFloatDelegate(QW.QStyledItemDelegate):
    """A StyledItemDelegate that displays scientific formatted floats."""
    def createEditor(self, parent, option, index):
        """Give an instance of the SciDoubleSpinbox"""
        if isinstance(index.data(), float):
            return ScientificDoubleSpinBox(parent)
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor: QW.QWidget, index: QC.QModelIndex) -> None:
        """Transfer the item value to the editor."""
        if isinstance(index.data(), float):
            editor.setValue(index.data())
        return super().setEditorData(editor, index)

    def displayText(self, value, locale):
        """Called when the underlying text is displayed."""
        return format_float(value)
