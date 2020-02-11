from PySide2 import QtWidgets

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

import pygaps


class IsoGraphView(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.navBar = NavigationToolbar(self.canvas, self)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.navBar)
        self.setLayout(self.layout)

        self._static_ax = self.canvas.figure.subplots()

    def setModel(self, model):
        self.model = model

    def plot(self, sel_index=None, **kwargs):
        selection = self.model.get_iso_checked()
        self._static_ax.clear()
        if any(selection):
            pygaps.plot_iso(
                selection,
                ax=self._static_ax
            )
            self._static_ax.figure.canvas.draw()
