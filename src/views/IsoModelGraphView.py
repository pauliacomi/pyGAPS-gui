import pygaps.graphing as pgg

from src.views.IsoGraphView import IsoGraphView


class IsoModelGraphView(IsoGraphView):

    model_isotherm = None

    def set_isotherms(self, isotherm, model_isotherm=None):
        self.isotherms = isotherm
        if model_isotherm:
            self.model_isotherm = model_isotherm

    def plot(self, branch="all"):
        self.ax.clear()
        if self.isotherms:
            pgg.plot_iso(
                self.isotherms,
                ax=self.ax,
                branch=branch,
                logx=self.logx,
                logy=self.logy,
                lgd_pos=None,
            )
            if self.model_isotherm:
                pgg.plot_iso(
                    self.model_isotherm,
                    ax=self.ax,
                    branch=branch,
                    logx=self.logx,
                    logy=self.logy,
                    lgd_pos=None,
                    color="r",
                    x_points=self.isotherms.pressure(branch=branch)
                )
        self.canvas.draw()
