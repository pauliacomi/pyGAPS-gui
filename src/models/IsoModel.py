from qtpy import QtCore as QC
from qtpy import QtGui as QG


class IsoModel(QG.QStandardItem):
    """Overloading a standard item to store an isotherm."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDropEnabled(False)
        self.setCheckable(True)
        self.oldCheckState = QC.Qt.Unchecked
        self.userCheckState = QC.Qt.Unchecked
