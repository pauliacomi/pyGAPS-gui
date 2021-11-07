from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from qtpy import QtWidgets as QW


class GraphView(QW.QWidget):

    canvas = None
    figure = None
    ax = None
    navbar = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()

    def setupUi(self):
        self.figure = Figure(figsize=(5, 5), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.setupNav()
        self.ax = self.figure.subplots()

        layout = QW.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addWidget(self.navbar)

    def setupNav(self):
        self.navbar = NavigationToolbar(self.canvas, self)

    def clear(self):
        for ax in self.figure.axes:
            if ax == self.ax:
                ax.clear()
            else:
                self.figure.delaxes(ax)
