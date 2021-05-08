from qtpy import QtWidgets as QW

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as
    NavigationToolbar
)
from matplotlib.figure import Figure


class GraphView(QW.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.navBar = NavigationToolbar(self.canvas, self)

        self.layout = QW.QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.navBar)
        self.setLayout(self.layout)

        self._static_ax = self.canvas.figure.subplots()

    @property
    def ax(self):
        return self._static_ax
