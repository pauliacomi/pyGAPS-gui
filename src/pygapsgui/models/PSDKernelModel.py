from pygaps.characterisation.psd_kernel import psd_dft
from pygaps.data import KERNELS
from pygaps.graphing.calc_graphs import psd_plot
from pygaps.utilities.exceptions import CalculationError
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.widgets.UtilityDialogs import error_dialog


class PSDKernelModel():
    """Pore size distribution calculations with kernel fitting: QT MVC Model."""

    # Refs
    isotherm = None
    view = None

    # Settings
    branch = "ads"
    kernel = None
    bspline_order = 2
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

        # view setup
        self.view.setWindowTitle(
            self.view.windowTitle() +
            f" '{isotherm.material} - {isotherm.adsorbate} - {isotherm._temperature:.2g} {isotherm.temperature_unit}'"
        )
        self.view.branch_dropdown.addItems(["ads", "des"])
        self.view.branch_dropdown.setCurrentText(self.branch)
        self.view.kernel_dropdown.addItems(KERNELS)
        self.view.smooth_input.setValue(self.bspline_order)

        # plot setup
        self.view.iso_graph.branch = self.branch
        self.view.iso_graph.lgd_keys = ["material"]
        # TODO: this should be derived from the individual kernel units
        self.view.iso_graph.pressure_mode = "relative"
        self.view.iso_graph.loading_basis = "molar"
        self.view.iso_graph.loading_unit = "mmol"
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
        # dynamic parameters
        self.prepare_values()
        # run calculation
        self.calc_auto()

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        if self.calculate():
            self.limits = (
                self.pressure[self.limit_indices[0]],
                self.pressure[self.limit_indices[1]],
            )
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

    def prepare_values(self):
        """Preliminary calculation of values that rarely change."""
        # Pressure
        self.pressure = self.isotherm.pressure(branch=self.branch)

    def calculate(self):
        """Call pyGAPS to perform main calculation."""
        with log_hook:
            self.branch = self.view.branch_dropdown.currentText()
            self.kernel = self.view.kernel_dropdown.currentText()
            self.bspline_order = int(self.view.smooth_input.cleanText())
            try:
                self.results = psd_dft(
                    self.isotherm,
                    branch=self.branch,
                    kernel=self.kernel,
                    bspline_order=self.bspline_order,
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

    def output_log(self):
        """Output text or dialog error/warning/info."""
        if self.output:
            error_dialog(self.output)
            self.output = ""

    def plot_results(self):
        """Fill in any GUI plots with results."""
        # PSD plot
        self.view.res_graph.clear()
        psd_plot(
            self.results['pore_widths'],
            self.results['pore_distribution'],
            self.results['pore_volume_cumulative'],
            method=self.kernel,
            log=False,
            right=5,
            ax=self.view.res_graph.ax
        )
        self.view.res_graph.canvas.draw_idle()

        # Isotherm plot
        self.view.iso_graph.draw_isotherms()
        self.view.iso_graph.ax.plot(
            self.pressure[self.limit_indices[0]:self.limit_indices[1] + 1],
            self.results['kernel_loading'],
            c='yellow',
            label="fit",
        )

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
        self.prepare_values()

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
        help_dialog(psd_dft)
