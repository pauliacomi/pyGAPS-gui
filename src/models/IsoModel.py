from qtpy import QtCore as QC
from qtpy import QtGui as QG


class IsoModel(QG.QStandardItem):
    """Overloading a standard item to store an isotherm."""
    userCheckState = QC.Qt.Unchecked

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDropEnabled(False)
        self.setDragEnabled(True)
        self.setCheckable(True)
        self.setCheckState(QC.Qt.Unchecked)

    def clone(self):
        clone = IsoModel()
        clone.userCheckState = self.userCheckState
        if clone.userCheckState == QC.Qt.Unchecked:
            clone.setCheckState(QC.Qt.Unchecked)
        return clone
