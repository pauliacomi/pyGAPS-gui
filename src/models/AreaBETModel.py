import warnings

import pygaps
from pygaps.characterisation.area_bet import (area_BET_raw, bet_transform, roq_transform)
from pygaps.graphing.calc_graphs import bet_plot, roq_plot


class AreaBETModel():
    def __init__(self, isotherm):

        self._isotherm = isotherm

        # Properties
        adsorbate = pygaps.Adsorbate.find(self._isotherm.adsorbate)
        self.cross_section = adsorbate.get_prop("cross_sectional_area")

        # Loading and pressure
        self.loading = self._isotherm.loading(branch='ads', loading_unit='mol', loading_basis='molar')
        self.pressure = self._isotherm.pressure(branch='ads', pressure_mode='relative')

        self.minimum = None
        self.maximum = None

        self.bet_area = None
        self.c_const = None
        self.n_monolayer = None
        self.p_monolayer = None
        self.slope = None
        self.intercept = None
        self.corr_coef = None

        self.output = None

    def set_view(self, view):
        """Initial actions on view connect."""
        self.view = view
        self.view.auto_button.clicked.connect(self.calc_auto)
        self.view.pSlider.rangeChanged.connect(self.calc_with_limits)
        self.plotiso()
        self.calc_auto()

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        self.calculate()
        self.output_results()
        self.plotBET()
        self.resetSlider()

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        self.calculate()
        self.output_results()
        self.plotBET()

    def calculate(self):

        # use the function
        with warnings.catch_warnings(record=True) as warning:

            warnings.simplefilter("always")

            try:
                (
                    self.bet_area, self.c_const, self.n_monolayer, self.p_monolayer, self.slope, self.intercept,
                    self.minimum, self.maximum, self.corr_coef
                ) = area_BET_raw(self.pressure, self.loading, self.cross_section, limits=self.limits)

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output = f'<font color="red">Calculation failed! <br> {e}</font>'
                return

            if warning:
                self.output = '<br>'.join([f'<font color="red">Warning: {a.message}</font>' for a in warning])
            else:
                self.output = None

    def output_results(self):
        self.view.result_bet.setText(f'{self.bet_area:.4}')
        self.view.result_c.setText(f'{self.c_const:.4}')
        self.view.result_mono_n.setText(f'{self.n_monolayer:.4}')
        self.view.result_mono_p.setText(f'{self.p_monolayer:.4}')
        self.view.result_slope.setText(f'{self.slope:.4}')
        self.view.result_intercept.setText(f'{self.intercept:.4}')
        self.view.result_r.setText(f'{self.corr_coef:.4}')

        self.view.output.setText(self.output)

    def resetSlider(self):
        self.view.pSlider.setValues([self.pressure[self.minimum], self.pressure[self.maximum]], emit=False)

    def plotiso(self):
        # Generate plot of the isotherm
        pygaps.plot_iso(self._isotherm, ax=self.view.isoGraph.ax)
        # Draw figure
        self.view.isoGraph.ax.figure.canvas.draw()

    def plotBET(self):

        # Clear plots
        self.view.betGraph.ax.clear()
        self.view.rouqGraph.ax.clear()

        # Generate plot of the BET points chosen
        bet_plot(
            self.pressure,
            bet_transform(self.pressure, self.loading),
            self.minimum,
            self.maximum,
            self.slope,
            self.intercept,
            self.p_monolayer,
            bet_transform(self.p_monolayer, self.n_monolayer),
            ax=self.view.betGraph.ax
        )

        # Generate plot of the Rouquerol points chosen
        roq_plot(
            self.pressure,
            roq_transform(self.pressure, self.loading),
            self.minimum,
            self.maximum,
            self.p_monolayer,
            roq_transform(self.p_monolayer, self.n_monolayer),
            ax=self.view.rouqGraph.ax
        )

        # Draw figures
        self.view.betGraph.ax.figure.canvas.draw()
        self.view.rouqGraph.ax.figure.canvas.draw()
