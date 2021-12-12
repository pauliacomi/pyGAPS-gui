import itertools

import pygaps.graphing as pgg
import pygaps.utilities.exceptions as pge

from src.views.GraphView import GraphView
from src.widgets.IsoGraphToolbar import IsoGraphToolbar
from src.widgets.UtilityWidgets import error_dialog


class IsoGraphView(GraphView):

    isotherms = None
    branch = "all"
    logx = False
    logy = False
    data_types = ["pressure", "loading"]
    x_data = "pressure"
    y1_data = "loading"
    y2_data = None

    def setupNav(self):
        self.navbar = IsoGraphToolbar(self.canvas, self)
        self.navbar.logx.connect(self.handle_logx)
        self.navbar.logy.connect(self.handle_logy)
        self.navbar.axis_data_sel.connect(self.handle_data_sel)

    def set_isotherms(self, isotherms):
        self.isotherms = isotherms
        keys = list(getattr(iso, "other_keys", []) for iso in isotherms)
        self.data_types = ["pressure", "loading"]
        self.y2_data = None
        if any(keys):
            self.data_types = self.data_types + list(set(itertools.chain.from_iterable(keys)))
            self.y2_data = self.data_types[-1]
        if self.y1_data not in self.data_types:
            self.y1_data = "loading"
        if self.x_data not in self.data_types:
            self.x_data = "pressure"

    def draw_isotherms(self, branch="all"):
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
                )
            except pge.GraphingError as ex:
                error_dialog(
                    "X-axis and Y1-axis must display data that is shared by all isotherms (i.e. pressure or loading)."
                )
        self.canvas.draw_idle()

    def handle_logx(self, is_set: bool):
        self.logx = is_set
        if self.selector:
            self.selector.setRange(self.ax.get_xlim())
            self.selector.setLogScale(is_set)

    def handle_logy(self, is_set: bool):
        self.logy = is_set

    def handle_data_sel(self):
        from src.widgets.IsoGraphDataSel import IsoGraphDataSel
        dialog = IsoGraphDataSel(
            self.data_types, self.x_data, self.y1_data, self.y2_data, parent=self
        )
        if dialog.exec_():
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

    def update(self):
        self.set_isotherms(self.model.get_iso_checked())
        self.draw_isotherms()
