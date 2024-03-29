from pygaps.characterisation.models_kelvin import _KELVIN_MODELS
from pygaps.characterisation.models_thickness import _THICKNESS_MODELS
from pygaps.characterisation.psd_meso import _MENISCUS_GEOMETRIES
from pygaps.characterisation.psd_meso import _MESO_PSD_MODELS
from pygaps.characterisation.psd_meso import _PORE_GEOMETRIES
from pygaps.characterisation.psd_meso import psd_mesoporous
from pygaps.graphing.calc_graphs import psd_plot
from pygaps.utilities.exceptions import CalculationError
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.widgets.UtilityDialogs import error_dialog


class PSDMesoModel():
    """Pore size distribution calculations with Kelvin-based theory: QT MVC Model."""

    # Refs
    isotherm = None
    view = None

    # Settings
    branch = "des"
    psd_model = None
    pore_geometry = None
    meniscus_geometry = None
    thickness_model = None
    kelvin_model = None
    limit_indices = None
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
        self.view.setWindowTitle(
            self.view.windowTitle() +
            f" '{isotherm.material} - {isotherm.adsorbate} - {isotherm._temperature:.2g} {isotherm.temperature_unit}'"
        )
        self.view.branch_dropdown.addItems(["ads", "des"])
        self.view.branch_dropdown.setCurrentText(self.branch)
        self.view.tmodel_dropdown.addItems(_MESO_PSD_MODELS)
        self.view.geometry_dropdown.addItems(_PORE_GEOMETRIES)
        self.view.mgeometry_dropdown.addItems(["auto"] + _MENISCUS_GEOMETRIES)
        self.view.thickness_dropdown.addItems(_THICKNESS_MODELS)
        self.view.kmodel_dropdown.addItems(_KELVIN_MODELS)

        # plot setup
        self.view.iso_graph.branch = self.branch
        self.view.iso_graph.lgd_keys = ["material"]
        self.view.iso_graph.pressure_mode = "relative"
        self.view.iso_graph.set_isotherms([self.isotherm])

        # connect signals
        self.view.calc_auto_button.clicked.connect(self.calc_auto)
        self.view.x_select.slider.rangeChanged.connect(self.calc_with_limits)
        self.view.branch_dropdown.currentIndexChanged.connect(self.select_branch)
        self.view.export_btn.clicked.connect(self.export_results)
        self.view.button_box.accepted.connect(self.view.accept)
        self.view.button_box.rejected.connect(self.view.reject)
        self.view.button_box.helpRequested.connect(self.help_dialog)

        # Calculation
        # run calculation
        self.calc_auto()

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        if self.calculate():
            pressure = self.isotherm.pressure(branch=self.branch, pressure_mode="relative")
            if self.branch == 'des':
                pressure = pressure[::-1]
            self.limits = (pressure[self.limit_indices[0]], pressure[self.limit_indices[1]])
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
            self.psd_model = self.view.tmodel_dropdown.currentText()
            self.pore_geometry = self.view.geometry_dropdown.currentText()
            self.meniscus_geometry = self.view.mgeometry_dropdown.currentText()
            if self.meniscus_geometry == "auto":
                self.meniscus_geometry = None
            self.thickness_model = self.view.thickness_dropdown.currentText()
            self.kelvin_model = self.view.kmodel_dropdown.currentText()
            try:
                self.results = psd_mesoporous(
                    self.isotherm,
                    branch=self.branch,
                    psd_model=self.psd_model,
                    pore_geometry=self.pore_geometry,
                    meniscus_geometry=self.meniscus_geometry,
                    thickness_model=self.thickness_model,
                    kelvin_model=self.kelvin_model,
                    p_limits=self.limits,
                )
                self.limit_indices = self.results.get('limits')

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Calculation failed! <br> {e}</font>'
                return False
            self.output += log_hook.get_logs()
            return True

    def output_results(self):
        """Fill in any GUI text output with results"""
        pass

    def output_log(self):
        """Output text or dialog error/warning/info."""
        if self.output:
            error_dialog(self.output)
            self.output = ""

    def plot_results(self):
        """Fill in any GUI plots with results."""

        # Isotherm plot update
        self.view.iso_graph.draw_isotherms()
        self.view.iso_graph.ax.autoscale(enable=False)

        from pygaps.units.converter_mode import c_loading
        model_pressure = self.isotherm.pressure(
            pressure_mode="relative",
            branch=self.branch,
        )
        if self.branch == "des":
            model_pressure = model_pressure[::-1]
        model_pressure = model_pressure[self.results["limits"][0]:self.results["limits"][1] + 1]
        model_pressure = (model_pressure[:-1] + model_pressure[1:]) / 2
        model_loading = c_loading(
            self.results["pore_volume_cumulative"],
            basis_from="volume_liquid",
            unit_from="cm3",
            basis_to=self.isotherm.loading_basis,
            unit_to=self.isotherm.loading_unit,
            adsorbate=self.isotherm.adsorbate,
            temp=self.isotherm.temperature,
        )

        self.view.iso_graph.ax.plot(
            model_pressure,
            model_loading,
            c='yellow',
            label="fit",
        )

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
        self.view.res_graph.canvas.draw_idle()

    def plot_clear(self):
        """Reset plots to default values."""
        self.view.iso_graph.draw_isotherms()
        self.view.res_graph.clear()
        self.view.res_graph.canvas.draw_idle()

    def slider_reset(self):
        """Resets the GUI selection sliders."""
        self.view.x_select.setValues(self.limits, emit=False)
        self.view.iso_graph.draw_xlimits(self.limits[0], self.limits[1])

    def select_branch(self):
        """Handle isotherm branch selection."""
        self.branch = self.view.branch_dropdown.currentText()
        self.view.iso_graph.branch = self.branch
        self.plot_clear()

    def result_dict(self):
        """Return a dictionary of results."""
        return {
            "Pore widths [nm]":
            self.results.get("pore_widths"),
            "Pore distribution [dV/dW]":
            self.results.get("pore_distribution"),
            "Pore cumulative volume [cm3/{self.isotherm.material_unit}]":
            self.results.get("pore_volume_cumulative"),
        }

    def export_results(self):
        """Save results as a file."""
        if not self.results:
            error_dialog("No results to export.")
            return
        from pygapsgui.utilities.result_export import serialize
        results = self.result_dict()
        serialize(results, how="V", parent=self.view)

    def help_dialog(self):
        """Display a dialog with the pyGAPS help."""
        from pygapsgui.widgets.UtilityDialogs import help_dialog
        help_dialog(psd_mesoporous)
