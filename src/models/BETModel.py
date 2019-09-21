from PySide2 import QtCore

import pygaps
from pygaps.characterisation.area_bet import (area_BET_raw,
                                              bet_transform,
                                              roq_transform)
from pygaps.graphing.calcgraph import bet_plot, roq_plot


class BETModel():

    def __init__(self, isotherm, parent=None):

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

        self.limits = None
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
        self.plotiso()
        self.calcBET()
        self.resetSlider()
        self.plotBET()

    def set_limits(self, left, right):
        self.limits = [left, right]
        self.calcBET()
        self.plotBET()

    def calcBET(self):

        # use the BET function
        (
            self.bet_area,
            self.c_const,
            self.n_monolayer,
            self.p_monolayer,
            self.slope, self.intercept,
            self.minimum, self.maximum,
            self.corr_coef
        ) = area_BET_raw(self.pressure, self.loading,
                         self.cross_section, limits=self.limits)

    def resetSlider(self):
        self.view.pSlider.range_slider.setValues(
            [self.pressure[self.minimum],
             self.pressure[self.maximum]])

    def plotiso(self):
        # Generate plot of the isotherm
        pygaps.plot_iso(
            self._isotherm,
            ax=self.view.isoGraph.ax
        )
        # Draw figure
        self.view.isoGraph.ax.figure.canvas.draw()

    def plotBET(self):

        # Clear plots
        self.view.betGraph.ax.clear()
        self.view.rouqGraph.ax.clear()

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
        self.view.betGraph.ax.figure.canvas.draw()
        self.view.rouqGraph.ax.figure.canvas.draw()
