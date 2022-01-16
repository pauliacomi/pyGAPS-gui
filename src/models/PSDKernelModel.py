import warnings

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
    limits = None
    limit_indices = None

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
        self.view.branchDropdown.addItems(["ads", "des"])
        self.view.branchDropdown.setCurrentText(self.branch)
        self.view.kernelDropdown.addItems(_KERNELS),
        self.view.smoothEdit.setValue(self.bspline_order)

        # plot isotherm
        self.view.isoGraph.branch = self.branch
        self.view.isoGraph.pressure_mode = "relative"
        self.view.isoGraph.set_isotherms([self.isotherm])

        # connect signals
        self.view.autoButton.clicked.connect(self.calc_auto)
        self.view.x_select.slider.rangeChanged.connect(self.calc_with_limits)
        self.view.branchDropdown.currentIndexChanged.connect(self.select_branch)
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
        self.calculate()
        self.output_results()
        self.plot_results()
        self.slider_reset()

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        self.calculate()
        self.output_results()
        self.plot_results()

    def prepare_values(self):
        # Pressure
        self.pressure = self.isotherm.pressure(branch=self.branch)

    def calculate(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            self.branch = self.view.branchDropdown.currentText()
            self.kernel = self.view.kernelDropdown.currentText()
            self.bspline_order = int(self.view.smoothEdit.cleanText())
            try:
                self.results = psd_dft(
                    self.isotherm,
                    branch=self.branch,
                    kernel=self.kernel,
                    bspline_order=self.bspline_order,
                    p_limits=self.limits,
                )
                self.limit_indices = self.results.get('limits')
                self.limits = [
                    self.pressure[self.limit_indices[0]],
                    self.pressure[self.limit_indices[1]],
                ]

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Calculation failed! <br> {e}</font>'
                self.limit_indices = [0, 0]
                self.limits = [self.pressure[0], self.pressure[-1]]

            if warning:
                self.output += '<br>'.join([
                    f'<font color="magenta">Warning: {a.message}</font>' for a in warning
                ])

    def output_results(self):
        if self.output:
            error_dialog(self.output)
            self.output = ""

    def plot_results(self):
        # TODO: if the results are missing this will fail

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
        self.view.isoGraph.draw_isotherms(branch=self.branch)
        self.view.isoGraph.ax.plot(
            self.pressure[self.limit_indices[0]:self.limit_indices[1] + 1],
            self.results['kernel_loading'],
            'r-',
            label="fit",
        )

    def slider_reset(self):
        self.view.x_select.setValues(self.limits, emit=False)
        self.view.isoGraph.draw_limits(self.limits[0], self.limits[1])

    def select_branch(self):
        self.branch = self.view.branchDropdown.currentText()
        self.prepare_values()

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
