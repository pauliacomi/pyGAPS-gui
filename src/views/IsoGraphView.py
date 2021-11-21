import itertools

import pygaps.graphing as pgg

from src.views.GraphView import GraphView
from src.widgets.IsoGraphToolbar import IsoGraphToolbar


class IsoGraphView(GraphView):

    isotherms = None
    logx = False
    logy = False
    data_types = None
    x_data = "pressure"
    y1_data = "loading"
    y2_data = None

    def setupNav(self):
        self.navbar = IsoGraphToolbar(self.canvas, self)
        self.navbar.logx.connect(self.handle_logx)
        self.navbar.logy.connect(self.handle_logy)

    def setIsotherms(self, isotherms):
        self.isotherms = isotherms
        keys = list(getattr(iso, "other_keys", None) for iso in isotherms)
        self.data_types = None
        self.y2_data = None
        if any(keys):
            self.data_types = list(set(itertools.chain.from_iterable(keys)))
            self.y2_data = self.data_types[0]

    def plot(self, branch="all"):
        self.clear()
        if self.isotherms:
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
        self.canvas.draw()

    def handle_logx(self, is_set: bool):
        self.logx = is_set
        self.canvas.draw()

    def handle_logy(self, is_set: bool):
        self.logy = is_set
        self.canvas.draw()
