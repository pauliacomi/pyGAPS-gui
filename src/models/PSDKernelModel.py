import warnings

from pygaps.characterisation.psd_kernel import psd_dft
from pygaps.characterisation.psd_kernel import _KERNELS
from pygaps.graphing.calc_graphs import psd_plot

from qtpy import QtWidgets as QW

from src.widgets.UtilityWidgets import error_dialog


class PSDKernelModel():
    def __init__(self, isotherm):

        self.isotherm = isotherm

        self.limits = None
        self.minimum = None
        self.maximum = None

        self.results = None
        self.output = None

    def set_view(self, view):
        """Initial actions on view connect."""
        self.view = view

        # view setup
        self.view.branchDropdown.addItems(["ads", "des"]),
        self.view.kernelDropdown.addItems(_KERNELS),
        self.view.smoothEdit.setValue(2)

        # plot isotherm
        self.view.isoGraph.setIsotherms([self.isotherm])
        self.view.isoGraph.plot()

        # connect signals
        self.view.autoButton.clicked.connect(self.calc_auto)
        self.view.pSlider.rangeChanged.connect(self.calc_with_limits)

        # first run
        self.calc_auto()

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        self.calculate()
        self.output_results()
        self.plot()
        self.resetSlider()

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        self.calculate()
        self.output_results()
        self.plot()

    def calculate(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            try:
                self.results = psd_dft(
                    self.isotherm,
                    branch=self.view.branchDropdown.currentText(),
                    kernel=self.view.kernelDropdown.currentText(),
                    bspline_order=self.view.smoothEdit.cleanText(),
                    p_limits=self.limits,
                )

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                error_dialog(f'<font color="red">Calculation failed! <br> {e}</font>')
                return

            if warning:
                error_dialog('<br>'.join([f'<font color="red">Warning: {a.message}</font>' for a in warning]))
                self.output = None

    def output_results(self):
        pass

    def plot(self):

        # Clear plots
        self.view.resGraph.clear()

        # Generate plot
        psd_plot(
            self.results['pore_widths'],
            self.results['pore_distribution'],
            self.results['pore_volume_cumulative'],
            method=self.view.modelDropdown.currentText(),
            log=False,
            right=5,
            ax=self.view.resGraph.ax
        )

        # Draw figures
        self.view.resGraph.canvas.draw()

    def resetSlider(self):
        self.view.pSlider.setValues([0, 1], emit=False)
