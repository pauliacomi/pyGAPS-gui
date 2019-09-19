from matplotlib.figure import Figure

from PySide2 import QtCore
from PySide2.QtWidgets import (QVBoxLayout, QWidget)

from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

import pygaps


class GraphView(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.navBar = NavigationToolbar(self.canvas, self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.navBar)
        self.setLayout(self.layout)

        self._static_ax = self.canvas.figure.subplots()

    def setModel(self, model):
        self.model = model

    def plot(self):
        selected_iso = [
            self.model.data_from_iso(index)
            for index in self.model.selected_iso_indices
        ]
        if self.model.current_iso_index not in self.model.selected_iso_indices:
            selected_iso.append(self.model.current_iso())
        self._static_ax.clear()
        pygaps.plot_iso(
            selected_iso,
            ax=self._static_ax
        )
        self._static_ax.figure.canvas.draw()
