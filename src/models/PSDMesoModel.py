import warnings

from pygaps.characterisation.psd_meso import psd_mesoporous
from pygaps.characterisation.psd_meso import _MESO_PSD_MODELS
from pygaps.characterisation.psd_meso import _PORE_GEOMETRIES
from pygaps.characterisation.models_thickness import _THICKNESS_MODELS
from pygaps.characterisation.models_kelvin import _KELVIN_MODELS
from pygaps.graphing.calc_graphs import psd_plot
from pygaps.utilities.exceptions import CalculationError

from src.widgets.UtilityWidgets import error_dialog


class PSDMesoModel():

    # Refs
    isotherm = None
    view = None

    # Settings
    branch = "des"
    psd_model = None
    pore_geometry = None
    thickness_model = None
    kelvin_model = None
    limits = None

    # Results
    results = None
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
                "PSD cannot be calculated for supercritical "
                "adsorbates or those with an unknown saturation pressure. If "
                "your adsorbate does not have a thermodynamic backend add a "
                "'saturation_pressure' metadata to it."
            )
            self.success = False
            return

        # View actions
        # view setup
        self.view.branchDropdown.addItems(["ads", "des"])
        self.view.branchDropdown.setCurrentText(self.branch)
        self.view.tmodelDropdown.addItems(_MESO_PSD_MODELS)
        self.view.geometryDropdown.addItems(_PORE_GEOMETRIES)
        self.view.thicknessDropdown.addItems(_THICKNESS_MODELS)
        self.view.kmodelDropdown.addItems(_KELVIN_MODELS)

        # plot isotherm
        self.view.isoGraph.branch = self.branch
        self.view.isoGraph.pressure_mode = "relative"
        self.view.isoGraph.set_isotherms([self.isotherm])

        # connect signals
        self.view.autoButton.clicked.connect(self.calc_auto)
        self.view.x_select.slider.rangeChanged.connect(self.calc_with_limits)
        self.view.button_box.accepted.connect(self.export_results)
        self.view.button_box.rejected.connect(self.view.reject)

        # Calculation
        # run calculation
        self.calc_auto()

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        self.calculate()
        pressure = self.isotherm.pressure(branch=self.branch, pressure_mode="relative")
        if self.branch == 'des':
            pressure = pressure[::-1]
        self.limits = [pressure[self.limits[0]], pressure[self.limits[1]]]
        self.output_results()
        self.plot_results()
        self.slider_reset()

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        self.calculate()
        self.output_results()
        self.plot_results()

    def calculate(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            self.branch = self.view.branchDropdown.currentText()
            self.psd_model = self.view.tmodelDropdown.currentText()
            self.pore_geometry = self.view.geometryDropdown.currentText()
            self.thickness_model = self.view.thicknessDropdown.currentText()
            self.kelvin_model = self.view.kmodelDropdown.currentText()
            try:
                self.results = psd_mesoporous(
                    self.isotherm,
                    branch=self.branch,
                    psd_model=self.psd_model,
                    pore_geometry=self.pore_geometry,
                    thickness_model=self.thickness_model,
                    kelvin_model=self.kelvin_model,
                    p_limits=self.limits,
                )
                self.limits = self.results.get('limits')

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Calculation failed! <br> {e}</font>'
                self.limits = [0, 0]

            if warning:
                self.output += '<br>'.join([
                    f'<font color="magenta">Warning: {a.message}</font>' for a in warning
                ])

    def output_results(self):
        if self.output:
            error_dialog(self.output)
            self.output = ""

    def plot_results(self):

        # Isotherm plot update
        self.view.isoGraph.draw_isotherms(branch=self.branch)

        # PSD plot
        self.view.res_graph.clear()
        psd_plot(
            self.results['pore_widths'],
            self.results['pore_distribution'],
            self.results['pore_volume_cumulative'],
            method=self.thickness_model,
            left=1.5,
            ax=self.view.res_graph.ax
        )
        self.view.res_graph.canvas.draw()

    def slider_reset(self):
        self.view.x_select.setValues(self.limits, emit=False)
        self.view.isoGraph.draw_limits(self.limits[0], self.limits[1])

    def export_results(self):
        if not self.results:
            error_dialog("No results to export.")
            return
        from src.utilities.result_export import serialize
        results = {
            "Pore widths [nm]": self.results.get("pore_widths").tolist(),
            "Pore distribution [dV/dW]": self.results.get("pore_distribution").tolist(),
            "Pore cumulative volume [cm3/g]": self.results.get("pore_volume_cumulative").tolist(),
        }
        if serialize(results, parent=self.view):
            self.view.accept()
