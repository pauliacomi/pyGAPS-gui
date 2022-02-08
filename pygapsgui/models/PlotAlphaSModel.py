from qtpy import QtWidgets as QW

from pygaps.characterisation.alphas_plots import alpha_s_raw
from pygaps.characterisation.area_bet import area_BET
from pygaps.characterisation.area_lang import area_langmuir
from pygaps.graphing.calc_graphs import tp_plot
from pygaps.utilities.exceptions import CalculationError
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.widgets.UtilityWidgets import error_dialog


class PlotAlphaSModel():

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
        self.view.refarea_dropdown.currentIndexChanged.connect(self.select_area)
        self.view.refarea_input.editingFinished.connect(self.select_area)
        self.view.branch_dropdown.currentIndexChanged.connect(self.select_branch)
        self.view.refbranch_dropdown.currentIndexChanged.connect(self.select_refbranch)
        self.view.pressure_input.editingFinished.connect(self.select_redpressure)
        self.view.calc_auto_button.clicked.connect(self.calc_auto)
        self.view.x_select.slider.rangeChanged.connect(self.calc_with_limits)
        self.view.button_box.accepted.connect(self.export_results)
        self.view.button_box.rejected.connect(self.view.reject)

        # Calculation
        # static parameters
        self.molar_mass = self.isotherm.adsorbate.molar_mass()
        self.liquid_density = self.isotherm.adsorbate.liquid_density(isotherm.temperature)

        self.reference_area = area_BET(self.ref_isotherm).get('area')
        # dynamic parameters
        if self.prepare_values():
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

        with log_hook:
            try:
                self.alpha_s_point = self.ref_isotherm.loading_at(
                    self.reducing_pressure,
                    branch=self.ref_branch,
                    loading_unit='mol',
                    loading_basis='molar',
                    pressure_mode='relative',
                )
                self.reference_loading = self.ref_isotherm.loading_at(
                    self.pressure,
                    branch=self.ref_branch,
                    pressure_unit=self.isotherm.pressure_unit,
                    loading_unit='mol',
                )
                if self.ref_branch == 'des':
                    self.reference_loading = self.reference_loading[::-1]
            except Exception as err:
                self.output += f'<font color="red">Error: The reference isotherm does not cover the same pressure range! <br></font>'
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
        tp_plot(
            self.alphas_curve,
            self.loading,
            self.results,
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

    def select_area(self):
        area_type = self.view.refarea_dropdown.currentText().lower()
        with log_hook:
            if area_type == "bet":
                self.reference_area = area_BET(self.ref_isotherm).get('area')
                self.view.refarea_input.setEnabled(False)
            elif area_type == "langmuir":
                self.reference_area = area_langmuir(self.ref_isotherm).get('area')
                self.view.refarea_input.setEnabled(False)
            else:
                self.view.refarea_input.setEnabled(True)
                ref_area_str = self.view.refarea_input.text()
                if not ref_area_str:
                    return
                self.reference_area = float(ref_area_str)
            self.output += log_hook.get_logs()

        if self.prepare_values():
            self.calc_auto()

    def select_branch(self):
        """Handle isotherm branch selection."""
        self.branch = self.view.branch_dropdown.currentText()
        if self.prepare_values():
            self.calc_auto()

    def select_refbranch(self):
        self.ref_branch = self.view.refbranch_dropdown.currentText()
        if self.prepare_values():
            self.calc_auto()

    def select_redpressure(self):
        self.reducing_pressure = float(self.view.pressure_input.text())
        if self.prepare_values():
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
        if serialize(results, parent=self.view):
            self.view.accept()
