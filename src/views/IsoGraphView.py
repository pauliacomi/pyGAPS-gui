import pygaps

from src.views.GraphView import GraphView
from src.widgets.IsoGraphToolbar import IsoGraphToolbar


class IsoGraphView(GraphView):

    isotherms = None
    logx = False
    logy = False

    def setupNav(self):
        self.navbar = IsoGraphToolbar(self.canvas, self)
        self.navbar.logx.connect(self.handle_logx)
        self.navbar.logy.connect(self.handle_logy)

    def setIsotherms(self, isotherms):
        self.isotherms = isotherms

    def plot(self, branch="all"):
        self.ax.clear()
        if self.isotherms:
            pygaps.plot_iso(
                self.isotherms,
                ax=self.ax,
                branch=branch,
                logx=self.logx,
                logy=self.logy,
            )
        self.canvas.draw()

    def handle_logx(self, is_set: bool):
        self.logx = is_set

    def handle_logy(self, is_set: bool):
        self.logy = is_set
