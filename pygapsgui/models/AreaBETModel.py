from pygaps.characterisation.area_bet import area_BET_raw
from pygaps.characterisation.area_bet import bet_transform
from pygaps.characterisation.area_bet import roq_transform
from pygaps.graphing.calc_graphs import bet_plot
from pygaps.graphing.calc_graphs import roq_plot
from pygaps.utilities.exceptions import CalculationError
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.widgets.UtilityDialogs import error_dialog


class AreaBETModel():
    """BET specific area calculations: QT MVC Model."""

    isotherm = None
    view = None

    # Settings
    branch = "ads"
    limits = None

    # Calculated
    loading = None
    pressure = None
    cross_section = None

    # Results
    bet_area = None
    c_const = None
    n_monolayer = None
    p_monolayer = None
    slope = None
    intercept = None
    corr_coef = None
    min_point = None
    max_point = None

    output = ""
    success = True

    def __init__(self, isotherm, view):
        """First init"""
        # Save refs
        self.isotherm = isotherm
        self.view = view

        # Fail condition
        try:
            self.isotherm.pressure(pressure_mode="relative")
        except CalculationError:
            error_dialog(
                "BET area cannot be calculated for supercritical "
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
        self.view.label_area.setText(f"BET area [m2/{self.isotherm.material_unit}]:")
        self.view.label_n_mono.setText(f"Monolayer uptake [mmol/{self.isotherm.material_unit}]:")
        self.view.branch_dropdown.addItems(["ads", "des"])
        self.view.branch_dropdown.setCurrentText(self.branch)

        # view graph
        self.view.iso_graph.branch = self.branch
        self.view.iso_graph.lgd_keys = ["adsorbate", "key"]
        self.view.iso_graph.pressure_mode = "relative"
        self.view.iso_graph.y2_data = None
        self.view.iso_graph.set_isotherms([self.isotherm])  # always last

        # connect signals
        self.view.branch_dropdown.currentIndexChanged.connect(self.select_branch)
        self.view.calc_auto_button.clicked.connect(self.calc_auto)
        self.view.x_select.slider.rangeChanged.connect(self.calc_with_limits)
        self.view.button_box.accepted.connect(self.export_results)
        self.view.button_box.rejected.connect(self.view.reject)

        # Calculation
        # static parameters
        self.cross_section = self.isotherm.adsorbate.get_prop("cross_sectional_area")
        # dynamic parameters
        self.prepare_values()
        # run calculation
        self.calc_auto()

    def prepare_values(self):
        """Preliminary calculation of values that rarely change."""
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
            self.plot_clear()
            self.output_log()

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
        """Call pyGAPS to perform main calculation."""
        with log_hook:
            # TODO Should put all these into a dictionary
            try:
                (
                    self.bet_area,
                    self.c_const,
                    self.n_monolayer,
                    self.p_monolayer,
                    self.slope,
                    self.intercept,
                    self.min_point,
                    self.max_point,
                    self.corr_coef,
                ) = area_BET_raw(
                    self.pressure,
                    self.loading,
                    self.cross_section,
                    p_limits=self.limits,
                )
            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Calculation failed! <br> {e}</font>'
                return False
            self.output += log_hook.get_logs()
            return True

    def output_results(self):
        """Fill in any GUI text output with results"""
        self.view.result_bet.setText(f'{self.bet_area:g}')
        self.view.result_c.setText(f'{self.c_const:.4}')
        self.view.result_mono_n.setText(f'{self.n_monolayer * 1000:.4}')
        self.view.result_mono_p.setText(f'{self.p_monolayer:.4}')
        self.view.result_slope.setText(f'{self.slope:.4}')
        self.view.result_intercept.setText(f'{self.intercept:.4}')
        self.view.result_r.setText(f'{self.corr_coef:.4}')

    def output_log(self):
        """Output text or dialog error/warning/info."""
        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):
        """Fill in any GUI plots with results."""

        # Isotherm plot update
        self.view.iso_graph.draw_isotherms()

        # Generate plot of the BET points chosen
        self.view.bet_graph.clear()
        bet_plot(
            self.pressure,
            bet_transform(self.pressure, self.loading),
            self.min_point,
            self.max_point,
            self.slope,
            self.intercept,
            self.p_monolayer,
            bet_transform(self.p_monolayer, self.n_monolayer),
            ax=self.view.bet_graph.ax
        )
        self.view.bet_graph.canvas.draw_idle()

        # Generate plot of the Rouquerol points chosen
        self.view.rouq_graph.clear()
        roq_plot(
            self.pressure,
            roq_transform(self.pressure, self.loading),
            self.min_point,
            self.max_point,
            self.p_monolayer,
            roq_transform(self.p_monolayer, self.n_monolayer),
            ax=self.view.rouq_graph.ax
        )
        self.view.rouq_graph.canvas.draw_idle()

    def plot_clear(self):
        """Reset plots to default values."""
        self.view.iso_graph.draw_isotherms()
        self.view.bet_graph.clear()
        self.view.bet_graph.canvas.draw_idle()
        self.view.rouq_graph.clear()
        self.view.rouq_graph.canvas.draw_idle()

    def slider_reset(self):
        """Resets the GUI selection sliders."""
        self.view.x_select.setValues(self.limits, emit=False)
        self.view.iso_graph.draw_xlimits(self.limits[0], self.limits[1])

    def select_branch(self):
        """Handle isotherm branch selection."""
        self.branch = self.view.branch_dropdown.currentText()
        self.view.iso_graph.set_branch(self.branch)
        self.prepare_values()
        self.calc_auto()

    def export_results(self):
        """Save results as a file."""
        if not self.bet_area:
            error_dialog("No results to export.")
            return
        from pygapsgui.utilities.result_export import serialize

        results = {
            f"BET area [m2/{self.isotherm.material_unit}]": self.bet_area,
            'R^2': self.corr_coef,
            'C constant': self.c_const,
            f"Monolayer uptake [mmol/{self.isotherm.material_unit}]": self.n_monolayer * 1000,
            'p_monolayer [p/p0]': self.p_monolayer,
            'BET slope': self.slope,
            'BET intercept': self.intercept,
            'Pressure limits': self.limits
        }
        serialize(results, parent=self.view)
