from qtpy import QtWidgets as QW

from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas)
from matplotlib.figure import Figure

from ..widgets.IsoGraphToolbar import IsoGraphToolbar

import pygaps


class IsoGraphView(QW.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()

    def setupUi(self):
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.navBar = IsoGraphToolbar(self.canvas, self)

        layout = QW.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addWidget(self.navBar)

        self._static_ax = self.canvas.figure.subplots()

    def setModel(self, model):
        self.model = model

    def plot(self, sel_index=None, **kwargs):
        self._static_ax.clear()
        selection = self.model.get_iso_checked()
        if any(selection):
            pygaps.plot_iso(selection, ax=self._static_ax)
        self._static_ax.figure.canvas.draw()
