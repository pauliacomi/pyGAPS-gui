from matplotlib.figure import Figure

from PySide2 import QtCore
from PySide2.QtWidgets import (QVBoxLayout, QWidget)

import matplotlib.backends.qt_compat
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


class GraphView(QWidget):

    def __init__(self):
        super().__init__()

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.navBar = NavigationToolbar(self.canvas, self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.navBar)
        self.setLayout(self.layout)

        self._static_ax = self.canvas.figure.subplots()

    @property
    def ax(self):
        """Get main ax."""
        return self._static_ax
