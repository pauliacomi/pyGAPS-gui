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

    # for range_select
    x_range_select = None  # can be selector
    low = None  # can be plt.ax
    high = None  # can be plt.ax

    def __init__(
        self,
        x_range_select=False,
        y_range_select=False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.x_range_select = x_range_select
        self.setup_UI()

    def setup_UI(self):
        self.figure = Figure(figsize=(5, 5), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.subplots()

        _layout = QW.QVBoxLayout(self)
        _layout.addWidget(self.canvas)

        if self.x_range_select:
            self.setupRangeSelect()
            _layout.addWidget(self.x_range_select)

        self.setupNav()
        _layout.addWidget(self.navbar)

    def setupNav(self):
        self.navbar = NavigationToolbar(self.canvas, self)

    def setupRangeSelect(self):
        self.x_range_select = HSelectorToolbar("XRangeSelect", ax=self.ax)
        self.x_range_select.slider.rangeChanged.connect(self.draw_limits)
        self.low = self.ax.axvline(0, c="r", ls="--")
        self.high = self.ax.axvline(1, c="r", ls="--")

    def draw_limits(self, low, high):
        self.low.set_xdata([low, low])
        self.high.set_xdata([high, high])
        self.canvas.draw_idle()

    def clear(self):
        # TODO: figure out why some of the clears don't work (like isosteric enthalpy)
        for ax in self.figure.axes:
            if ax == self.ax:
                for line in ax.get_lines():
                    if line not in [self.low, self.high]:
                        line.remove()
                ax.relim()  # make sure all the data fits
                ax.autoscale()  # auto-scale
            else:
                self.figure.delaxes(ax)
