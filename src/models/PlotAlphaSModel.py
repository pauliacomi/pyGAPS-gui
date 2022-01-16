import warnings

from pygaps.characterisation.area_bet import area_BET
from pygaps.characterisation.area_lang import area_langmuir
from pygaps.characterisation.alphas import alpha_s_raw
from pygaps.graphing.calc_graphs import tp_plot
from pygaps.utilities.exceptions import CalculationError

from src.widgets.UtilityWidgets import error_dialog

from qtpy import QtWidgets as QW


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
        self.view.branchDropdown.addItems(["ads", "des"])
        self.view.branchDropdown.setCurrentText(self.branch)
        self.view.refbranchDropdown.addItems(["ads", "des"])
        self.view.refbranchDropdown.setCurrentText(self.ref_branch)

        # connect signals
        self.view.areaDropdown.currentIndexChanged.connect(self.select_area)
        self.view.areaInput.editingFinished.connect(self.select_area)
        self.view.branchDropdown.currentIndexChanged.connect(self.select_branch)
        self.view.refbranchDropdown.currentIndexChanged.connect(self.select_refbranch)
        self.view.pressure_input.editingFinished.connect(self.select_redpressure)
        self.view.auto_button.clicked.connect(self.calc_auto)
        self.view.x_select.slider.rangeChanged.connect(self.calc_with_limits)
        self.view.button_box.accepted.connect(self.export_results)
        self.view.button_box.rejected.connect(self.view.reject)

        # Calculation
        # static parameters
        self.molar_mass = self.isotherm.adsorbate.molar_mass()
        self.liquid_density = self.isotherm.adsorbate.liquid_density(isotherm.temperature)

        self.reference_area = area_BET(self.ref_isotherm).get('area')
        # dynamic parameters
        self.prepare_values()
        # run calculation
        self.calc_auto()

    def prepare_values(self):
        # Loading and pressure
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            try:
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

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Calculation failed! <br> {e}</font>'

            if warning:
                self.output += '<br>'.join([
                    f'<font color="magenta">Warning: {a.message}</font>' for a in warning
                ])

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        self.calculate()
        self.slider_reset()
        self.output_results()
        self.plot_results()

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        self.calculate()
        self.output_results()
        self.plot_results()

    def calculate(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
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

            if warning:
                self.output += '<br>'.join([
                    f'<font color="magenta">Warning: {a.message}</font>' for a in warning
                ])

    def output_results(self):
        self.view.resultsTable.setRowCount(0)
        self.view.resultsTable.setRowCount(len(self.results))
        for index, result in enumerate(self.results):
            self.view.resultsTable.setItem(
                index, 0, QW.QTableWidgetItem(f"{result.get('adsorbed_volume'):g}")
            )
            self.view.resultsTable.setItem(index, 1, QW.QTableWidgetItem(f"{result.get('area'):g}"))
            self.view.resultsTable.setItem(
                index, 2, QW.QTableWidgetItem(f"{result.get('corr_coef'):g}")
            )
            self.view.resultsTable.setItem(
                index, 3, QW.QTableWidgetItem(f"{result.get('slope'):g}")
            )
            self.view.resultsTable.setItem(
                index, 4, QW.QTableWidgetItem(f"{result.get('intercept'):g}")
            )

        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):

        # Generate alphas plot
        self.view.tGraph.clear()
        tp_plot(
            self.alphas_curve,
            self.loading,
            self.results,
            ax=self.view.tGraph.ax,
            alpha_s=True,
            alpha_reducing_p=self.reducing_pressure
        )
        self.view.tGraph.canvas.draw()

    def slider_reset(self):
        self.view.x_select.setRange((0, self.alphas_curve[-1]))
        self.view.x_select.setValues((self.alphas_curve[0], self.alphas_curve[-1]), emit=False)
        self.view.tGraph.draw_limits(self.alphas_curve[0], self.alphas_curve[-1])

    def select_area(self):
        area_type = self.view.areaDropdown.currentText().lower()
        if area_type == "bet":
            self.reference_area = area_BET(self.ref_isotherm).get('area')
            self.view.areaInput.setEnabled(False)
        elif area_type == "langmuir":
            self.reference_area = area_langmuir(self.ref_isotherm).get('area')
            self.view.areaInput.setEnabled(False)
        else:
            self.view.areaInput.setEnabled(True)
            ref_area_str = self.view.areaInput.text()
            if not ref_area_str:
                return
            self.reference_area = float(ref_area_str)

        self.prepare_values()
        self.calc_auto()

    def select_branch(self):
        self.branch = self.view.branchDropdown.currentText()
        self.prepare_values()
        self.calc_auto()

    def select_refbranch(self):
        self.ref_branch = self.view.refbranchDropdown.currentText()
        self.prepare_values()
        self.calc_auto()

    def select_redpressure(self):
        self.reducing_pressure = float(self.view.pressure_input.text())
        self.prepare_values()
        self.calc_auto()

    def export_results(self):
        if not self.results:
            error_dialog("No results to export.")
            return
        from src.utilities.result_export import serialize
        results = {
            e: {
                "Pore volume [cm3/g]": result.get("adsorbed_volume"),
                "Area [m2/g]": result.get("area"),
                "R^2": result.get("corr_coef"),
                "Slope": result.get("slope"),
                "Intercept": result.get("intercept"),
            }
            for e, result in enumerate(self.results)
        }
        if serialize(results, parent=self.view):
            self.view.accept()
