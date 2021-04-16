from qtpy import QtGui, QtCore


class IsoModel(QtGui.QStandardItem):
    """Overloading a standard item to store an isotherm."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDropEnabled(False)
        self.oldCheckState = QtCore.Qt.Unchecked
        self.userCheckState = QtCore.Qt.Unchecked
