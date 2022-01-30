import itertools

import pygaps.graphing as pgg
import pygaps.utilities.exceptions as pge

from src.views.GraphView import GraphView
from src.widgets.IsoGraphToolbar import IsoGraphToolbar
from src.widgets.UtilityWidgets import error_dialog


class IsoGraphView(GraphView):

    isotherms = None
    branch: str = "all"
    logx: bool = False
    logy: bool = False
    data_types: list = ["pressure", "loading"]
    x_data: str = "pressure"
    y1_data: str = "loading"
    y2_data: str = None

    x_range: list = None
    y1_range: list = None

    pressure_mode = None
    pressure_unit = None

    lgd_keys = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # anything less and it looks too cramped
        self.setMinimumSize(400, 400)

    def setupNav(self):
        "Override parent nav to add custom toolbar."
        self.navbar = IsoGraphToolbar(self.canvas, self)
        self.navbar.logx.connect(self.handle_logx)
        self.navbar.logy.connect(self.handle_logy)
        self.navbar.axis_data_sel.connect(self.handle_data_sel)

    def set_isotherms(self, isotherms):

        self.isotherms = isotherms
        if not isotherms:
            return

        # data
        keys = list(iso.other_keys for iso in isotherms)
        self.data_types = ["pressure", "loading"]
        self.y2_data = None
        if any(keys):
            self.data_types = self.data_types + list(set(itertools.chain.from_iterable(keys)))
        if self.y1_data not in self.data_types:
            self.y1_data = "loading"
        if self.x_data not in self.data_types:
            self.x_data = "pressure"

        # range
        self.find_xrange()

    def draw_isotherms(self, branch=None):

        if not branch:
            branch = self.branch
        else:
            self.branch = branch

        self.clear()
        if self.isotherms:
            try:
                pgg.plot_iso(
                    self.isotherms,
                    ax=self.ax,
                    branch=branch,
                    logx=self.logx,
                    logy1=self.logy,
                    x_data=self.x_data,
                    y1_data=self.y1_data,
                    y2_data=self.y2_data,
                    pressure_mode=self.pressure_mode,
                    pressure_unit=self.pressure_unit,
                    lgd_keys=self.lgd_keys,
                )
                self.ax.autoscale()  # auto-scale
            except pge.GraphingError:
                error_dialog(
                    "X-axis and Y1-axis must display data that is shared by all isotherms (i.e. pressure or loading)."
                )
            except pge.CalculationError:
                error_dialog(
                    "Cannot plot multiple isotherms that are impossible to convert to the same units / modes."
                )
        self.canvas.draw_idle()

    def set_branch(self, branch):
        pass

    def find_xrange(self):
        self.x_range = (
            min([min(self.state_pressure(i)) for i in self.isotherms]),
            max([max(self.state_pressure(i)) for i in self.isotherms]),
        )
        if self.x_range_select:
            self.x_range_select.setRange(self.x_range)
            self.x_range_select.setValues(self.x_range, emit=False)
            self.low.set_xdata([self.x_range[0], self.x_range[0]])
            self.high.set_xdata([self.x_range[1], self.x_range[1]])

    def state_pressure(self, iso):
        return iso.pressure(
            branch=self.branch,
            pressure_mode=self.pressure_mode,
            pressure_unit=self.pressure_unit,
        )

    def handle_logx(self, is_set: bool):
        self.logx = is_set
        if self.x_range_select:
            self.x_range_select.setLogScale(is_set)
            self.x_range_select.setRange(self.x_range)

    def handle_logy(self, is_set: bool):
        self.logy = is_set
        if self.y_range_select:
            self.y_range_select.setLogScale(is_set)

    def handle_data_sel(self):
        from src.widgets.IsoGraphDataSel import IsoGraphDataSel
        dialog = IsoGraphDataSel(
            self.data_types,
            self.x_data,
            self.y1_data,
            self.y2_data,
            parent=self,
        )
        if dialog.exec():
            if dialog.changed:
                self.x_data = dialog.x_data
                self.y1_data = dialog.y1_data
                self.y2_data = dialog.y2_data
                self.draw_isotherms()


class IsoListGraphView(IsoGraphView):
    """IsoGraphView sublass which adds the ability to connect to a IsoListModel"""

    model = None

    def setModel(self, model):
        self.model = model
        self.model.checked_changed.connect(self.update)

    def update(self):
        self.set_isotherms(self.model.get_checked())
        self.draw_isotherms()


class IsoModelGraphView(IsoGraphView):

    model_isotherm = None
    branch: str = "ads"

    def draw_isotherms(self, branch=None):

        if not branch:
            branch = self.branch
        else:
            self.branch = branch

        self.clear()
        if self.isotherms:
            pgg.plot_iso(
                self.isotherms,
                ax=self.ax,
                branch=self.branch,
                logx=self.logx,
                logy1=self.logy,
                lgd_pos=None,
            )
            if self.model_isotherm:
                pgg.plot_iso(
                    self.model_isotherm,
                    ax=self.ax,
                    branch=self.branch,
                    logx=self.logx,
                    logy1=self.logy,
                    lgd_pos=None,
                    color="r",
                    # TODO does not work if model calculates pressure
                    x_points=self.isotherms[0].pressure(
                        branch=self.branch,
                        limits=self.model_isotherm.model.pressure_range,
                    )
                )
            self.ax.autoscale()  # auto-scale
        self.canvas.draw_idle()
