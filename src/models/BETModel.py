from PySide2 import QtCore

import pygaps
from pygaps.characterisation.area_bet import (area_BET_raw,
                                              bet_transform,
                                              roq_transform)
from pygaps.graphing.calcgraph import bet_plot, roq_plot


class BETModel(QtCore.QObject):

    bet_calculated = QtCore.Signal()

    def __init__(self, isotherm, parent=None):
        super().__init__(parent)
        self._isotherm = isotherm

        # Properties
        adsorbate = pygaps.Adsorbate.find(self._isotherm.adsorbate)
        self.cross_section = adsorbate.get_prop("cross_sectional_area")

        # Loading and pressure
        self.loading = self._isotherm.loading(branch='ads',
                                              loading_unit='mol',
                                              loading_basis='molar')
        self.pressure = self._isotherm.pressure(branch='ads',
                                                pressure_mode='relative')

        self.minimum = None
        self.maximum = None

        self.bet_area = None
        self.c_const = None
        self.n_monolayer = None
        self.p_monolayer = None
        self.slope = None
        self.intercept = None
        self.corr_coef = None

    def set_view(self, view):
        self.view = view
        self.bet_calculated.connect(self.plotBET)
        self.calcBET()

    def calcBET(self):

        # use the bet function
        (
            self.bet_area,
            self.c_const,
            self.n_monolayer,
            self.p_monolayer,
            self.slope, self.intercept,
            self.minimum, self.maximum,
            self.corr_coef
        ) = area_BET_raw(self.pressure, self.loading,
                         self.cross_section, limits=None)

        self.bet_calculated.emit()

    def plotBET(self):

        # Clear plots
        self.view.isoGraph.ax.clear()
        self.view.betGraph.ax.clear()
        self.view.rouqGraph.ax.clear()

        # Generate plot of the isotherm
        pygaps.plot_iso(
            self._isotherm,
            ax=self.view.isoGraph.ax
        )

        # Generate plot of the BET points chosen
        bet_plot(self.pressure,
                 bet_transform(self.pressure, self.loading),
                 self.minimum, self.maximum,
                 self.slope, self.intercept,
                 self.p_monolayer,
                 bet_transform(self.p_monolayer, self.n_monolayer),
                 ax=self.view.betGraph.ax)

        # Generate plot of the Rouquerol points chosen
        roq_plot(self.pressure,
                 roq_transform(self.pressure, self.loading),
                 self.minimum, self.maximum,
                 self.p_monolayer,
                 roq_transform(self.p_monolayer, self.n_monolayer),
                 ax=self.view.rouqGraph.ax)

        # Draw figures
        self.view.isoGraph.ax.figure.canvas.draw()
        self.view.betGraph.ax.figure.canvas.draw()
        self.view.rouqGraph.ax.figure.canvas.draw()
