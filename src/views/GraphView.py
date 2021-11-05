# check deprecations with respect to iso graph view

from qtpy import QtWidgets as QW

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure


class GraphView(QW.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.figure = Figure(figsize=(5, 3), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.navBar = NavigationToolbar(self.canvas, self)
        self.ax = self.figure.subplots()

        layout = QW.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addWidget(self.navBar)

    def clear(self):
        for ax in self.figure.axes:
            if ax == self.ax:
                ax.clear()
            else:
                self.figure.delaxes(ax)
