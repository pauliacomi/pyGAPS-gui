import warnings

from pygaps.characterisation.area_bet import (area_BET_raw, bet_transform, roq_transform)
from pygaps.graphing.calc_graphs import bet_plot, roq_plot
from pygaps.utilities.exceptions import CalculationError

from src.widgets.UtilityWidgets import error_dialog


class AreaBETModel():

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
        self.view.label_area.setText(f"BET area [m2/{self.isotherm.material_unit}]:")
        self.view.label_n_mono.setText(f"Monolayer uptake [mmol/{self.isotherm.material_unit}]:")
        self.view.branchDropdown.addItems(["ads", "des"])
        self.view.branchDropdown.setCurrentText(self.branch)
        self.view.isoGraph.branch = self.branch
        self.view.isoGraph.pressure_mode = "relative"
        self.view.isoGraph.set_isotherms([self.isotherm])

        # connect signals
        self.view.branchDropdown.currentIndexChanged.connect(self.select_branch)
        self.view.auto_button.clicked.connect(self.calc_auto)
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
            self.limits = [self.pressure[self.min_point], self.pressure[self.max_point]]
            self.slider_reset()
            self.output_results()
            self.plot_results()
        # if we can't calculate, we just display the isotherm and error
        else:
            self.view.isoGraph.draw_isotherms(branch=self.branch)
            self.view.output.setText(self.output)
            self.output = ""

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        if self.calculate():
            self.output_results()
            self.plot_results()
        # if we can't calculate, we just display the isotherm and error
        else:
            self.view.isoGraph.draw_isotherms(branch=self.branch)
            self.view.output.setText(self.output)
            self.output = ""

    def calculate(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
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

            if warning:
                self.output += '<br>'.join([
                    f'<font color="magenta">Warning: {a.message}</font>' for a in warning
                ])
            return True

    def output_results(self):
        self.view.result_bet.setText(f'{self.bet_area:g}')
        self.view.result_c.setText(f'{self.c_const:.4}')
        self.view.result_mono_n.setText(f'{self.n_monolayer * 1000:.4}')
        self.view.result_mono_p.setText(f'{self.p_monolayer:.4}')
        self.view.result_slope.setText(f'{self.slope:.4}')
        self.view.result_intercept.setText(f'{self.intercept:.4}')
        self.view.result_r.setText(f'{self.corr_coef:.4}')

        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):

        # Isotherm plot update
        self.view.isoGraph.draw_isotherms(branch=self.branch)

        # Generate plot of the BET points chosen
        self.view.betGraph.clear()
        bet_plot(
            self.pressure,
            bet_transform(self.pressure, self.loading),
            self.min_point,
            self.max_point,
            self.slope,
            self.intercept,
            self.p_monolayer,
            bet_transform(self.p_monolayer, self.n_monolayer),
            ax=self.view.betGraph.ax
        )
        self.view.betGraph.canvas.draw()

        # Generate plot of the Rouquerol points chosen
        self.view.rouqGraph.clear()
        roq_plot(
            self.pressure,
            roq_transform(self.pressure, self.loading),
            self.min_point,
            self.max_point,
            self.p_monolayer,
            roq_transform(self.p_monolayer, self.n_monolayer),
            ax=self.view.rouqGraph.ax
        )
        self.view.rouqGraph.canvas.draw()

    def slider_reset(self):
        self.view.x_select.setValues(self.limits, emit=False)
        self.view.isoGraph.draw_limits(self.limits[0], self.limits[1])

    def select_branch(self):
        self.branch = self.view.branchDropdown.currentText()
        self.prepare_values()
        self.calc_auto()

    def export_results(self):
        from src.utilities.result_export import serialize

        results = {
            'BET Area [m2/g]': self.bet_area,
            'R^2': self.corr_coef,
            'C constant': self.c_const,
            'n_monolayer [mmol/g]': self.n_monolayer * 1000,
            'p_monolayer [p/p0]': self.p_monolayer,
            'BET slope': self.slope,
            'BET intercept': self.intercept,
            'Pressure limits': self.limits
        }
        if serialize(results, parent=self.view):
            self.view.accept()
