import warnings

from pygaps.characterisation.dr_da_plots import da_plot_raw, log_p_exp, log_v_adj
from pygaps.graphing.calc_graphs import dra_plot

from qtpy import QtWidgets as QW

from src.widgets.UtilityWidgets import error_dialog


class DADRModel():
    def __init__(self, isotherm, ptype="DR"):

        self.isotherm = isotherm
        self.ptype = ptype

        self.exponent = None
        if self.ptype == "DR":
            self.exponent = 2

        # Properties
        self.molar_mass = self.isotherm.adsorbate.molar_mass()
        self.liquid_density = self.isotherm.adsorbate.liquid_density(isotherm.temperature)
        self.temperature = self.isotherm.temperature

        # Loading and pressure
        self.loading = isotherm.loading(branch='ads', loading_unit='mol', loading_basis='molar')
        try:
            self.pressure = isotherm.pressure(
                branch='ads',
                pressure_mode='relative',
            )
        except Exception:
            error_dialog("The isotherm cannot be converted to a relative basis. Is your isotherm supercritical?")

        self.limits = None
        self.minimum = None
        self.maximum = None

        self.microp_volume = None
        self.potential = None
        self.exp = None
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
        self.calc_auto()

    def save_exp(self):
        exp = self.view.DRExponent.cleanText()
        if exp:
            self.exponent = float(exp)

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        if self.ptype == "DA" and self.exponent:
            self.save_exp()
        self.calculate()
        self.output_results()
        self.plot()
        self.resetSlider()

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        if self.ptype == "DA" and self.exponent:
            self.save_exp()
        self.calculate()
        self.output_results()
        self.plot()

    def calculate(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            # Check consistency of exponent
            if self.exponent and self.exponent < 0:
                raise Exception("Exponent cannot be negative.")

            try:
                (
                    self.microp_volume,
                    self.potential,
                    exp,
                    self.slope,
                    self.intercept,
                    self.minimum,
                    self.maximum,
                    self.corr_coef,
                ) = da_plot_raw(
                    self.pressure,
                    self.loading,
                    self.isotherm.temperature,
                    self.molar_mass,
                    self.liquid_density,
                    self.exponent,
                    self.limits,
                )
                if self.ptype == "DA":
                    self.exponent = exp

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output = f'<font color="red">Calculation failed! <br> {e}</font>'
                return

            if warning:
                self.output = '<br>'.join([f'<font color="red">Warning: {a.message}</font>' for a in warning])
            else:
                self.output = None

    def output_results(self):

        self.view.result_microporevol.setText(f"{self.microp_volume:g}")
        self.view.result_adspotential.setText(f"{self.potential:g}")
        if self.ptype == "DA":
            self.view.DRExponent.setValue(self.exponent)
        # self.view.result_adspotential.setText(f"{self.corr_coef:g}")

    def plot(self):

        # Clear plots
        self.view.graph.clear()

        # Generate plot
        dra_plot(
            log_v_adj(self.loading, self.molar_mass, self.liquid_density),
            log_p_exp(self.pressure, self.exponent),
            self.minimum,
            self.maximum,
            self.slope,
            self.intercept,
            self.exponent,
            ax=self.view.graph.ax
        )

        # Draw figures
        self.view.graph.canvas.draw()

    def resetSlider(self):
        self.view.pSlider.setValues([self.pressure[self.minimum], self.pressure[self.maximum - 1]], emit=False)
