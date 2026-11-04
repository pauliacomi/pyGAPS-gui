import pygaps as pg
from qtpy import QtCore as QC
from qtpy import QtGui as QG

from pygapsgui.utilities import color_theme


class IsoModel(QG.QStandardItem):
    """Overloading a standard item to store an isotherm."""

    # Whether the user has checked it purposefully
    userCheckState = QC.Qt.CheckState.Unchecked

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # dragdrop
        self.setDropEnabled(False)
        self.setDragEnabled(True)
        # checkable
        self.setCheckable(True)
        self.setCheckState(QC.Qt.CheckState.Unchecked)

    def setData(self, isotherm, *args, **kwargs):
        if isinstance(isotherm, pg.ModelIsotherm):
            self.setForeground(QG.QColor(color_theme.COLORS['primary']))
        super().setData(isotherm, *args, **kwargs)

    def apply_theme(self):
        if isinstance(self.data(), pg.ModelIsotherm):
            self.setForeground(QG.QColor(color_theme.COLORS["primary"]))
