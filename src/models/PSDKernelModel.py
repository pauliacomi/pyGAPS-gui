from src.utilities.log_hook import log_hook

from pygaps.characterisation.psd_kernel import psd_dft
from pygaps.characterisation.psd_kernel import _KERNELS
from pygaps.graphing.calc_graphs import psd_plot
from pygaps.utilities.exceptions import CalculationError

from src.widgets.UtilityWidgets import error_dialog


class PSDKernelModel():

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
        self.view.kernel_dropdown.addItems(_KERNELS),
        self.view.smooth_input.setValue(self.bspline_order)

        # plot isotherm
        self.view.iso_graph.branch = self.branch
        self.view.iso_graph.lgd_keys = ["material"]
        self.view.iso_graph.pressure_mode = "relative"
        self.view.iso_graph.set_isotherms([self.isotherm])

        # connect signals
        self.view.calc_auto_button.clicked.connect(self.calc_auto)
        self.view.x_select.slider.rangeChanged.connect(self.calc_with_limits)
        self.view.branch_dropdown.currentIndexChanged.connect(self.select_branch)
        self.view.button_box.accepted.connect(self.export_results)
        self.view.button_box.rejected.connect(self.view.reject)

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
            self.view.iso_graph.draw_isotherms(branch=self.branch)
            self.output_log()

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        if self.calculate():
            self.output_log()
            self.output_results()
            self.plot_results()
        else:
            self.view.iso_graph.draw_isotherms(branch=self.branch)
            self.output_log()

    def prepare_values(self):
        # Pressure
        self.pressure = self.isotherm.pressure(branch=self.branch)

    def calculate(self):
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
            self.output += log_hook.getLogs()
            return True

    def output_results(self):
        pass

    def output_log(self):
        if self.output:
            error_dialog(self.output)
            self.output = ""

    def plot_results(self):
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
        self.view.res_graph.canvas.draw()

        # Isotherm plot
        self.view.iso_graph.draw_isotherms(branch=self.branch)
        self.view.iso_graph.ax.plot(
            self.pressure[self.limit_indices[0]:self.limit_indices[1] + 1],
            self.results['kernel_loading'],
            'r-',
            label="fit",
        )

    def slider_reset(self):
        self.view.x_select.setValues(self.limits, emit=False)
        self.view.iso_graph.draw_xlimits(self.limits[0], self.limits[1])

    def select_branch(self):
        self.branch = self.view.branch_dropdown.currentText()
        self.prepare_values()

    def export_results(self):
        if not self.results:
            error_dialog("No results to export.")
            return
        from src.utilities.result_export import serialize
        results = {
            "Pore widths [nm]": self.results.get("pore_widths"),
            "Pore distribution [dV/dW]": self.results.get("pore_distribution"),
            "Pore cumulative volume [cm3/g]": self.results.get("pore_volume_cumulative"),
        }
        serialize(results, how="V", parent=self.view)
