import pygaps as pg

from qtpy import QtCore as QC
from qtpy import QtGui as QG


class IsoModel(QG.QStandardItem):
    """Overloading a standard item to store an isotherm."""

    # Whether the user has checked it purposefully
    userCheckState = QC.Qt.Unchecked

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # dragdrop
        self.setDropEnabled(False)
        self.setDragEnabled(True)
        # checkable
        self.setCheckable(True)
        self.setCheckState(QC.Qt.Unchecked)
        # bg
        self.setBackground(QG.QColor('#beaed4'))

    def setData(self, isotherm, *args, **kwargs):
        if isinstance(isotherm, pg.ModelIsotherm):
            self.setBackground(QG.QColor('#7fc97f'))
        super().setData(isotherm, *args, **kwargs)
