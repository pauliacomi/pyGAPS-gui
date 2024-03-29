from qtpy import QtWidgets as QW

from pygaps.characterisation.alphas_plots import alpha_s
from pygaps.characterisation.alphas_plots import alpha_s_raw
from pygaps.characterisation.area_bet import area_BET
from pygaps.characterisation.area_lang import area_langmuir
from pygaps.graphing.calc_graphs import tp_plot
from pygaps.utilities.exceptions import CalculationError
from pygaps.utilities.pygaps_utilities import get_iso_loading_and_pressure_ordered
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.widgets.UtilityDialogs import error_dialog


class PlotAlphaSModel():
    """Alpha-s plot calculations: QT MVC Model."""

    isotherm = None
    ref_isotherm = None
    view = None

    # Settings
    branch = "ads"
    ref_branch = "ads"
    limits = None
    molar_mass = None
    liquid_density = None
    reference_loading = None
    reference_area = None
    reducing_pressure = 0.4

    # Results
    alphas_curve = None
    results = None

    output = ""
    success = True

    def __init__(self, isotherm, ref_isotherm, view):
        # Save refs
        self.isotherm = isotherm
        self.ref_isotherm = ref_isotherm
        self.view = view

        # Fail condition
        try:
            self.isotherm.pressure(pressure_mode="relative")
            self.ref_isotherm.pressure(pressure_mode="relative")
        except CalculationError:
            error_dialog(
                "Alpha-s plots cannot be defined for supercritical "
                "adsorbates or those with an unknown saturation pressure. If "
                "your adsorbate does not have a thermodynamic backend add a "
                "'saturation_pressure' metadata to it."
            )
            self.success = False
            return

        # View setup
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
        self.view.refbranch_dropdown.addItems(["ads", "des"])
        self.view.refbranch_dropdown.setCurrentText(self.ref_branch)

        # connect signals
        self.view.refarea_dropdown.currentTextChanged.connect(self.select_area)
        self.view.refarea_input.editingFinished.connect(self.select_area_specify)
        self.view.branch_dropdown.currentTextChanged.connect(self.select_branch)
        self.view.refbranch_dropdown.currentTextChanged.connect(self.select_refbranch)
        self.view.pressure_input.editingFinished.connect(self.select_redpressure)
        self.view.calc_auto_button.clicked.connect(self.calc_auto)
        self.view.x_select.slider.rangeChanged.connect(self.calc_with_limits)
        self.view.export_btn.clicked.connect(self.export_results)
        self.view.button_box.accepted.connect(self.view.accept)
        self.view.button_box.rejected.connect(self.view.reject)
        self.view.button_box.helpRequested.connect(self.help_dialog)

        # Calculation
        # static parameters
        self.molar_mass = self.isotherm.adsorbate.molar_mass()
        self.liquid_density = self.isotherm.adsorbate.liquid_density(isotherm.temperature)

        # dynamic parameters
        if self.prepare_values():
            # calculate reference area
            self.select_area("BET")
            # run calculation
            self.calc_auto()

    def prepare_values(self):
        """Preliminary calculation of values that rarely change."""
        # Loading and pressure
        self.pressure, self.loading = get_iso_loading_and_pressure_ordered(
            self.isotherm, self.branch, {
                "loading_basis": "molar",
                "loading_unit": "mmol"
            }, {"pressure_mode": "relative"}
        )

        with log_hook:
            try:
                self.alpha_s_point = self.ref_isotherm.loading_at(
                    self.reducing_pressure,
                    branch=self.ref_branch,
                    loading_unit='mmol',
                    loading_basis='molar',
                    pressure_mode='relative',
                )
                self.reference_loading = self.ref_isotherm.loading_at(
                    self.pressure,
                    branch=self.ref_branch,
                    pressure_unit=self.isotherm.pressure_unit,
                    loading_unit='mmol',
                )
                if self.ref_branch == 'des':
                    self.reference_loading = self.reference_loading[::-1]
            except Exception as err:
                self.output += '<font color="red">Error: The reference isotherm does not cover the same pressure range! <br></font>'
                self.output_log()
                return False

            self.output += log_hook.get_logs()
            return True

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        if self.calculate():
            self.limits = (0, self.alphas_curve[-1])
            self.slider_reset()
            self.output_results()
            self.output_log()
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
                self.results, self.alphas_curve = alpha_s_raw(
                    self.loading,
                    self.reference_loading,
                    self.alpha_s_point,
                    self.reference_area,
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
        # Generate alphas plot
        self.view.res_graph.clear()
        units = self.isotherm.units
        units.update({"loading_basis": "molar", "loading_unit": "mmol"})
        tp_plot(
            self.alphas_curve,
            self.loading,
            self.results,
            units,
            ax=self.view.res_graph.ax,
            alpha_s=True,
            alpha_reducing_p=self.reducing_pressure
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
        self.view.x_select.setValues((self.alphas_curve[0], self.alphas_curve[-1]), emit=False)
        self.view.res_graph.draw_xlimits(self.alphas_curve[0], self.alphas_curve[-1])

    def select_area(self, area_type):
        """Handle reference area selection."""
        with log_hook:
            if area_type == "BET":
                self.reference_area = area_BET(self.ref_isotherm).get('area')
                self.view.refarea_input.setReadOnly(True)
                self.view.refarea_input.setText(f"{self.reference_area:.4g}")
            elif area_type == "Langmuir":
                self.reference_area = area_langmuir(self.ref_isotherm).get('area')
                self.view.refarea_input.setReadOnly(True)
                self.view.refarea_input.setText(f"{self.reference_area:.4g}")
            else:
                self.view.refarea_input.setReadOnly(False)
            self.output += log_hook.get_logs()

        if self.prepare_values():
            self.calc_auto()

    def select_area_specify(self):
        """Use area specified by user."""
        ref_area_str = self.view.refarea_input.text()
        if not ref_area_str:
            return
        self.reference_area = float(ref_area_str)
        if self.prepare_values():
            self.calc_auto()

    def select_branch(self, branch):
        """Handle isotherm branch selection."""
        self.branch = branch
        if self.prepare_values():
            self.calc_auto()

    def select_refbranch(self, branch):
        """Handle reference isotherm branch selection."""
        self.ref_branch = branch
        if self.prepare_values():
            self.calc_auto()

    def select_redpressure(self):
        """Handle reducing pressure selection."""
        self.reducing_pressure = float(self.view.pressure_input.text())
        if self.prepare_values():
            self.calc_auto()

    def result_dict(self):
        """Return a dictionary of results."""
        return {
            e: {
                f"Alpha S pore volume [cm3/{self.isotherm.material_unit}]":
                result.get("adsorbed_volume"),
                f"Alpha S area [m2/{self.isotherm.material_unit}]":
                result.get("area"),
                "Alpha S R^2":
                result.get("corr_coef"),
                "Alpha S slope":
                result.get("slope"),
                "Alpha S intercept":
                result.get("intercept"),
            }
            for e, result in enumerate(self.results)
        }

    def export_results(self):
        """Save results as a file."""
        if not self.results:
            error_dialog("No results to export.")
            return
        from pygapsgui.utilities.result_export import serialize
        results = self.result_dict()
        serialize(results, parent=self.view)

    def help_dialog(self):
        """Display a dialog with the pyGAPS help."""
        from pygapsgui.widgets.UtilityDialogs import help_dialog
        help_dialog(alpha_s)
