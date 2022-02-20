from qtpy import QtWidgets as QW

from pygaps.characterisation.models_thickness import _THICKNESS_MODELS
from pygaps.characterisation.models_thickness import get_thickness_model
from pygaps.characterisation.t_plots import t_plot_raw
from pygaps.graphing.calc_graphs import tp_plot
from pygaps.utilities.exceptions import CalculationError
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.widgets.UtilityDialogs import error_dialog


class PlotTModel():

    isotherm = None
    view = None

    # Settings
    branch = "ads"
    limits = None
    thickness_model = None
    molar_mass = None
    liquid_density = None

    # Results
    t_curve = None
    results = None

    output = ""
    success = True

    def __init__(self, isotherm, view):
        # Save refs
        self.isotherm = isotherm
        self.view = view

        # Fail condition
        try:
            self.isotherm.pressure(pressure_mode="relative")
        except CalculationError:
            error_dialog(
                "T-plots cannot be defined for supercritical "
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
        self.view.res_table.setHorizontalHeaderLabels((
            f"V [cm3/{self.isotherm.material_unit}]",
            f"A [m2/{self.isotherm.material_unit}]",
            "R^2",
            "Slope",
            "Intercept",
        ))
        self.view.branch_dropdown.addItems(["ads", "des"])
        self.view.branch_dropdown.setCurrentText(self.branch)
        models = list(_THICKNESS_MODELS.keys())
        models.remove("Zero thickness")  # Not an option
        self.view.thickness_dropdown.addItems(models)

        # connect signals
        self.view.branch_dropdown.currentIndexChanged.connect(self.select_branch)
        # TODO: add the ability for custom callable models
        self.view.thickness_dropdown.currentIndexChanged.connect(self.select_tmodel)
        self.view.calc_auto_button.clicked.connect(self.calc_auto)
        self.view.x_select.slider.rangeChanged.connect(self.calc_with_limits)
        self.view.button_box.accepted.connect(self.export_results)
        self.view.button_box.rejected.connect(self.view.reject)

        # Calculation
        # static parameters
        self.molar_mass = self.isotherm.adsorbate.molar_mass()
        self.liquid_density = self.isotherm.adsorbate.liquid_density(isotherm.temperature)
        self.thickness_model = get_thickness_model(models[0])
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
            self.limits = (0, self.t_curve[-1])
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
        """Call pyGAPS to perform main calculation."""
        with log_hook:
            try:
                self.results, self.t_curve = t_plot_raw(
                    self.loading,
                    self.pressure,
                    self.thickness_model,
                    self.liquid_density,
                    self.molar_mass,
                    t_limits=self.limits,
                )
            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Calculation failed! <br> {e}</font>'
                return False
            self.output += log_hook.get_logs()
            return True

    def output_results(self):
        """Fill in any GUI text output with results"""
        self.view.res_table.setRowCount(0)
        self.view.res_table.setRowCount(len(self.results))
        for index, result in enumerate(self.results):
            self.view.res_table.setItem(
                index, 0, QW.QTableWidgetItem(f"{result.get('adsorbed_volume'):g}")
            )
            self.view.res_table.setItem(index, 1, QW.QTableWidgetItem(f"{result.get('area'):g}"))
            self.view.res_table.setItem(
                index, 2, QW.QTableWidgetItem(f"{result.get('corr_coef'):g}")
            )
            self.view.res_table.setItem(index, 3, QW.QTableWidgetItem(f"{result.get('slope'):g}"))
            self.view.res_table.setItem(
                index, 4, QW.QTableWidgetItem(f"{result.get('intercept'):g}")
            )

    def output_log(self):
        """Output text or dialog error/warning/info."""
        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):
        """Fill in any GUI plots with results."""
        # Generate tplot
        self.view.res_graph.clear()
        tp_plot(
            self.t_curve,
            self.loading,
            self.results,
            ax=self.view.res_graph.ax,
        )
        self.view.res_graph.ax.set_title("")
        self.view.res_graph.canvas.draw_idle()

    def plot_clear(self):
        """Reset plots to default values."""
        self.view.res_graph.clear()
        self.view.res_graph.canvas.draw_idle()

    def slider_reset(self):
        """Resets the GUI selection sliders."""
        self.view.x_select.setRange(self.limits)
        self.view.x_select.setValues((self.t_curve[0], self.t_curve[-1]), emit=False)
        self.view.res_graph.draw_xlimits(self.t_curve[0], self.t_curve[-1])

    def select_tmodel(self):
        tmodel_text = self.view.thickness_dropdown.currentText()
        self.thickness_model = get_thickness_model(tmodel_text)
        self.calc_auto()

    def select_branch(self):
        """Handle isotherm branch selection."""
        self.branch = self.view.branch_dropdown.currentText()
        self.prepare_values()
        self.calc_auto()

    def export_results(self):
        """Save results as a file."""
        if not self.results:
            error_dialog("No results to export.")
            return
        from pygapsgui.utilities.result_export import serialize
        results = {
            e: {
                f"Pore volume [cm3/{self.isotherm.material_unit}]": result.get("adsorbed_volume"),
                f"Area [m2/{self.isotherm.material_unit}]": result.get("area"),
                "R^2": result.get("corr_coef"),
                "Slope": result.get("slope"),
                "Intercept": result.get("intercept"),
            }
            for e, result in enumerate(self.results)
        }
        serialize(results, parent=self.view)
