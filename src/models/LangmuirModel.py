import warnings

import pygaps
from pygaps.characterisation.area_langmuir import (area_langmuir_raw, langmuir_transform)
from pygaps.graphing.calc_graphs import langmuir_plot


class LangmuirModel():
    def __init__(self, isotherm, parent=None):

        self._isotherm = isotherm

        # Properties
        adsorbate = pygaps.Adsorbate.find(self._isotherm.adsorbate)
        self.cross_section = adsorbate.get_prop("cross_sectional_area")

        # Loading and pressure
        self.loading = self._isotherm.loading(branch='ads', loading_unit='mol', loading_basis='molar')
        self.pressure = self._isotherm.pressure(branch='ads', pressure_mode='relative')

        self.minimum = None
        self.maximum = None

        self.lang_area = None
        self.k_const = None
        self.n_monolayer = None
        self.slope = None
        self.intercept = None
        self.corr_coef = None

        self.output = None

    def set_view(self, view):
        """Initial actions on view connect."""
        self.view = view
        self.view.auto_button.clicked.connect(self.calc_auto)
        self.view.pSlider.rangeChanged.connect(self.calc_with_limits)
        self.plot_iso()
        self.calc_auto()

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        self.calculate()
        self.output_results()
        self.plot_calc()
        self.resetSlider()

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        self.calculate()
        self.output_results()
        self.plot_calc()

    def calculate(self):

        # use the function
        with warnings.catch_warnings(record=True) as warning:

            warnings.simplefilter("always")

            try:
                (
                    self.lang_area, self.k_const, self.n_monolayer, self.slope, self.intercept, self.minimum,
                    self.maximum, self.corr_coef
                ) = area_langmuir_raw(self.pressure, self.loading, self.cross_section, limits=self.limits)

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output = f'<font color="red">Calculation failed! <br> {e}</font>'
                return

            if warning:
                self.output = '<br>'.join([f'<font color="red">Warning: {a.message}</font>' for a in warning])
            else:
                self.output = None

    def output_results(self):
        self.view.result_lang.setText(f'{self.lang_area:.4}')
        self.view.result_k.setText(f'{self.k_const:.4}')
        self.view.result_mono_n.setText(f'{self.n_monolayer:.4}')
        self.view.result_slope.setText(f'{self.slope:.4}')
        self.view.result_intercept.setText(f'{self.intercept:.4}')
        self.view.result_r.setText(f'{self.corr_coef:.4}')

        self.view.output.setText(self.output)

    def resetSlider(self):
        self.view.pSlider.setValues([self.pressure[self.minimum], self.pressure[self.maximum]], emit=False)

    def plot_iso(self):
        # Generate plot of the isotherm
        pygaps.plot_iso(self._isotherm, ax=self.view.isoGraph.ax)
        # Draw figure
        self.view.isoGraph.ax.figure.canvas.draw()

    def plot_calc(self):

        # Clear plots
        self.view.langGraph.ax.clear()

        # Generate plot of the BET points chosen
        langmuir_plot(
            self.pressure,
            langmuir_transform(self.pressure, self.loading),
            self.minimum,
            self.maximum,
            self.slope,
            self.intercept,
            ax=self.view.langGraph.ax
        )

        # Draw figures
        self.view.langGraph.ax.figure.canvas.draw()
