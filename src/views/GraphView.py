from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from qtpy import QtWidgets as QW

from src.widgets.GraphSelectorToolbar import HSelectorToolbar


class GraphView(QW.QWidget):

    canvas = None
    figure = None
    ax = None
    navbar = None

    # for selector
    low = None
    high = None
    selector = None

    def __init__(self, selector=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_selector = selector
        self.setupUi()

    def setupUi(self):
        self.figure = Figure(figsize=(5, 5), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.subplots()

        layout = QW.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        if self.has_selector:
            self.selector = HSelectorToolbar("Selector", ax=self.ax, parent=self)
            self.selector.slider.rangeChanged.connect(self.draw_limits)
            self.low = self.ax.axvline(0, c="r", ls="--")
            self.high = self.ax.axvline(1, c="r", ls="--")
            layout.addWidget(self.selector)

        self.setupNav()
        layout.addWidget(self.navbar)

    def setupNav(self):
        self.navbar = NavigationToolbar(self.canvas, self)

    def draw_limits(self, low, high):
        self.low.set_xdata([low, low])
        self.high.set_xdata([high, high])
        self.canvas.draw_idle()

    def clear(self):
        for ax in self.figure.axes:
            if ax == self.ax:
                for line in ax.get_lines():
                    if line not in [self.low, self.high]:
                        line.remove()
                    # TODO reset selector lines if needed
                ax.relim()  # make sure all the data fits
                ax.autoscale()  # auto-scale
                # if self.selector:
                #     self.selector.setRange(self.ax.get_xlim())
            else:
                self.figure.delaxes(ax)
