from qtpy import QtWidgets as QW

from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas)
from matplotlib.figure import Figure

from ..widgets.IsoGraphToolbar import IsoGraphToolbar

import pygaps


class IsoGraphView(QW.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()
        self.isotherms = None

    def setupUi(self):
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.navBar = IsoGraphToolbar(self.canvas, self)

        layout = QW.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addWidget(self.navBar)

        self._static_ax = self.canvas.figure.subplots()

    def setIsotherms(self, isotherms):
        self.isotherms = isotherms

    def plot(self):
        self._static_ax.clear()
        if self.isotherms:
            pygaps.plot_iso(self.isotherms, ax=self._static_ax)
        self._static_ax.figure.canvas.draw()
