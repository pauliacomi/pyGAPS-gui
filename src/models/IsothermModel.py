from PySide2 import QtGui


class IsothermModel(QtGui.QStandardItem):
    """Overloading a standard item to store an isotherm."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
