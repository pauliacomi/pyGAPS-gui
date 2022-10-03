from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from qtpy import QtWidgets as QW

from pygapsgui.widgets.GraphSelectorToolbar import HSelectorToolbar
from pygapsgui.widgets.GraphSelectorToolbar import VSelectorToolbar


class GraphView(QW.QWidget):
    """A widget that extends the matplotlib canvas with some useful functionality."""

    canvas = None
    figure = None
    ax = None
    navbar = None

    # for range_select
    x_range_select = None  # can be selector
    y_range_select = None  # can be selector
    x_lower = None  # can be plt.ax
    x_upper = None  # can be plt.ax
    ylow = None  # can be plt.ax
    yhigh = None  # can be plt.ax

    def __init__(
        self,
        x_range_select=False,
        y_range_select=False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        # Ensure some minimum height
        self.setMinimumSize(300, 300)
        self.x_range_select = x_range_select
        self.y_range_select = y_range_select
        self.setup_UI()

    def setup_UI(self):
        """Create and set-up static UI elements."""
        self.figure = Figure(figsize=(5, 5), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot()

        _layout = QW.QGridLayout(self)
        row = 0
        col = 0

        if self.y_range_select:
            self.setupYRangeSelect()
            _layout.addWidget(self.y_range_select, 0, 0, 1, 1)
            col = 1

        if self.x_range_select:
            self.setupXRangeSelect()
            _layout.addWidget(self.x_range_select, 1, col, 1, 1)
            row = 1

        self.setupNav()

        _layout.addWidget(self.canvas, 0, col, 1, 1)
        _layout.addWidget(self.navbar, row + 1, col, 1, 1)

    def setupNav(self):
        """Creates the navbar."""
        self.navbar = NavigationToolbar(self.canvas, self)

    def setupXRangeSelect(self):
        """Creates and connects a selector for the x-axis."""
        self.x_range_select = HSelectorToolbar("HRangeSelect", ax=self.ax)
        self.x_range_select.slider.rangeChanged.connect(self.draw_xlimits)
        self.x_lower = self.ax.axvline(0, c="r", ls="--")
        self.x_upper = self.ax.axvline(1, c="r", ls="--")

    def setupYRangeSelect(self):
        """Creates and connects a selector for the y-axis."""
        self.y_range_select = VSelectorToolbar("VRangeSelect", ax=self.ax)
        self.y_range_select.slider.rangeChanged.connect(self.draw_ylimits)
        self.ylow = self.ax.axhline(0, c="r", ls="--")
        self.yhigh = self.ax.axhline(1, c="r", ls="--")

    def draw_xlimits(self, low, high):
        """Sets the selector limits for the x axis."""
        self.x_lower.set_xdata([low, low])
        self.x_upper.set_xdata([high, high])
        self.canvas.draw_idle()

    def draw_ylimits(self, low, high):
        """Sets the selector limits for the y axis."""
        self.ylow.set_ydata([low, low])
        self.yhigh.set_ydata([high, high])
        self.canvas.draw_idle()

    def clear(self):
        """Custom clear function that only removes what's needed."""
        for ax in self.figure.axes:
            if ax == self.ax:
                ax.set_prop_cycle(None)
                for line in ax.get_lines():
                    if line not in [self.x_lower, self.x_upper, self.ylow, self.yhigh]:
                        line.remove()
                lgd = ax.get_legend()
                if lgd:
                    lgd.remove()
                ax.relim()  # make sure all the data fits
                ax.autoscale()  # auto-scale
            else:
                self.figure.delaxes(ax)
