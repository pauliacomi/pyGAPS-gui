import warnings

from pygaps.characterisation.area_lang import (area_langmuir_raw, langmuir_transform)
from pygaps.graphing.calc_graphs import langmuir_plot


class AreaLangModel():
    def __init__(self, isotherm):

        self.isotherm = isotherm

        # Properties
        self.cross_section = self.isotherm.adsorbate.get_prop("cross_sectional_area")

        # Loading and pressure
        self.loading = self.isotherm.loading(
            branch='ads', loading_unit='mol', loading_basis='molar'
        )
        self.pressure = self.isotherm.pressure(branch='ads', pressure_mode='relative')

        self.limits = None
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

        # connect signals
        self.view.auto_button.clicked.connect(self.calc_auto)
        self.view.pSlider.rangeChanged.connect(self.calc_with_limits)

        # run
        self.view.isoGraph.set_isotherms([self.isotherm])
        self.view.isoGraph.draw_isotherms()
        self.calc_auto()

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        self.calculate()
        self.output_results()
        self.plot_calc()
        self.slider_reset()

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        self.calculate()
        self.output_results()
        self.plot_calc()

    def calculate(self):
        with warnings.catch_warnings(record=True) as warning:

            warnings.simplefilter("always")

            try:
                (
                    self.lang_area,
                    self.k_const,
                    self.n_monolayer,
                    self.slope,
                    self.intercept,
                    self.minimum,
                    self.maximum,
                    self.corr_coef,
                ) = area_langmuir_raw(
                    self.pressure,
                    self.loading,
                    self.cross_section,
                    limits=self.limits,
                )

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output = f'<font color="red">Calculation failed! <br> {e}</font>'
                return

            if warning:
                self.output = '<br>'.join([
                    f'<font color="red">Warning: {a.message}</font>' for a in warning
                ])
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

    def slider_reset(self):
        self.view.pSlider.setValues([self.pressure[self.minimum], self.pressure[self.maximum]],
                                    emit=False)

    def plot_calc(self):

        # Clear plots
        self.view.langGraph.clear()

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
        self.view.langGraph.canvas.draw()
