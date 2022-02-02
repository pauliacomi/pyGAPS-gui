from pygaps.characterisation.dr_da_plots import da_plot_raw
from pygaps.characterisation.dr_da_plots import log_p_exp
from pygaps.characterisation.dr_da_plots import log_v_adj
from pygaps.graphing.calc_graphs import dra_plot
from pygaps.utilities.exceptions import CalculationError
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.widgets.UtilityWidgets import error_dialog


class DADRModel():

    isotherm = None
    view = None

    # Settings
    branch = "ads"
    limits = None
    exponent = None

    # Results
    microp_volume = None
    potential = None
    exp = None
    slope = None
    intercept = None
    corr_coef = None
    min_point = None
    max_point = None

    output = ""
    success = True

    def __init__(self, isotherm, view, ptype="DR"):
        """First init"""
        # Save refs
        self.isotherm = isotherm
        self.view = view
        self.ptype = ptype

        if self.ptype == "DR":
            self.exponent = 2

        # Fail condition
        try:
            self.isotherm.pressure(pressure_mode="relative")
        except CalculationError:
            error_dialog(
                "Plot cannot be calculated for supercritical "
                "adsorbates or those with an unknown saturation pressure. If "
                "your adsorbate does not have a thermodynamic backend add a "
                "'saturation_pressure' metadata to it."
            )
            self.success = False
            return

        # View actions
        # view setup
        self.view.setWindowTitle(
            self.view.windowTitle() +
            f" '{isotherm.material} - {isotherm.adsorbate} - {isotherm._temperature:.2g} {isotherm.temperature_unit}'"
        )
        self.view.label_vol.setText(f"Micropore Volume [cm3/{self.isotherm.material_unit}]")
        self.view.branch_dropdown.addItems(["ads", "des"])
        self.view.branch_dropdown.setCurrentText(self.branch)

        # plot setup
        self.view.iso_graph.branch = self.branch
        self.view.iso_graph.pressure_mode = "relative"
        self.view.iso_graph.set_isotherms([self.isotherm])

        # connect signals
        self.view.calc_auto_button.clicked.connect(self.calc_auto)
        self.view.x_select.slider.rangeChanged.connect(self.calc_with_limits)
        if self.ptype == "DA":
            self.view.dr_exp_input.valueChanged.connect(self.select_exp)
        self.view.branch_dropdown.currentIndexChanged.connect(self.select_branch)
        self.view.button_box.accepted.connect(self.export_results)
        self.view.button_box.rejected.connect(self.view.reject)

        # Calculation
        # static parameters
        self.molar_mass = self.isotherm.adsorbate.molar_mass()
        self.liquid_density = self.isotherm.adsorbate.liquid_density(isotherm.temperature)
        self.temperature = self.isotherm.temperature
        # dynamic parameters
        self.prepare_values()
        # run calculation
        self.calc_auto()

    def prepare_values(self):
        # Loading and pressure
        self.loading = self.isotherm.loading(
            branch=self.branch,
            loading_basis='molar',
            loading_unit='mol',
        )
        self.pressure = self.isotherm.pressure(
            branch=self.branch,
            pressure_mode="relative",
        )
        if self.branch == 'des':
            self.loading = self.loading[::-1]
            self.pressure = self.pressure[::-1]

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        if self.calculate():
            self.limits = (self.pressure[self.min_point], self.pressure[self.max_point])
            self.slider_reset()
            self.output_log()
            self.output_results()
            self.plot_results()
        else:
            self.output_log()
            self.plot_clear()

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        if self.calculate():
            self.output_log()
            self.output_results()
            self.plot_results()
        else:
            self.output_log()
            self.plot_clear()

    def calculate(self):
        with log_hook:
            try:
                (
                    self.microp_volume,
                    self.potential,
                    exp,
                    self.slope,
                    self.intercept,
                    self.min_point,
                    self.max_point,
                    self.corr_coef,
                ) = da_plot_raw(
                    self.pressure,
                    self.loading,
                    self.isotherm.temperature,
                    self.molar_mass,
                    self.liquid_density,
                    self.exponent,
                    p_limits=self.limits,
                )
                if self.ptype == "DA":
                    self.exponent = exp
            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Calculation failed! <br> {e}</font>'
                return False
            self.output += log_hook.getLogs()
            return True

    def output_results(self):
        self.view.result_r.setText(f'{self.corr_coef:.4}')
        self.view.result_microporevol.setText(f"{self.microp_volume:g}")
        self.view.result_adspotential.setText(f"{self.potential:g}")
        if self.ptype == "DA":
            self.view.dr_exp_input.blockSignals(True)
            self.view.dr_exp_input.setValue(self.exponent)
            self.view.dr_exp_input.blockSignals(False)
        self.view.result_slope.setText(f'{self.slope:.4}')
        self.view.result_intercept.setText(f'{self.intercept:.4}')

    def output_log(self):
        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):
        # Isotherm plot update
        self.view.iso_graph.draw_isotherms()
        # DR/DA plot
        self.view.rgraph.clear()
        dra_plot(
            log_v_adj(self.loading, self.molar_mass, self.liquid_density),
            log_p_exp(self.pressure, self.exponent),
            self.min_point,
            self.max_point,
            self.slope,
            self.intercept,
            self.exponent,
            ax=self.view.rgraph.ax
        )
        self.view.rgraph.canvas.draw_idle()

    def plot_clear(self):
        self.view.iso_graph.draw_isotherms()
        self.view.res_graph.clear()
        self.view.res_graph.canvas.draw_idle()

    def select_exp(self):
        exp = self.view.dr_exp_input.cleanText()
        # Check consistency of exponent
        if exp:
            exp = float(exp)
            if exp < 0:
                raise Exception("Exponent cannot be negative.")
            self.exponent = exp
        self.prepare_values()
        self.calc_auto()

    def slider_reset(self):
        self.view.x_select.setValues(self.limits, emit=False)
        self.view.iso_graph.draw_xlimits(self.limits[0], self.limits[1])

    def select_branch(self):
        self.branch = self.view.branch_dropdown.currentText()
        self.view.iso_graph.set_branch(self.branch)
        self.prepare_values()
        self.calc_auto()

    def export_results(self):
        if not self.microp_volume:
            error_dialog("No results to export.")
            return
        from pygapsgui.utilities.result_export import serialize

        results = {
            f'Mircropore Volume [cm3/{self.isotherm.material_unit}]': self.microp_volume * 1000,
            'Effective potential [kJ/mol]': self.potential,
            'R^2': self.corr_coef,
            'Slope': self.slope,
            'Intercept': self.intercept,
            'Pressure limits': self.limits
        }
        if self.ptype != "DR":
            results['DR Exponent'] = self.exp

        serialize(results, parent=self.view)
