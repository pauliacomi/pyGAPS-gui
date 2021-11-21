import warnings

from pygaps.characterisation.psd_micro import psd_microporous
from pygaps.characterisation.psd_micro import _MICRO_PSD_MODELS
from pygaps.characterisation.psd_micro import _PORE_GEOMETRIES
from pygaps.characterisation.models_hk import _ADSORBENT_MODELS
from pygaps.graphing.calc_graphs import psd_plot

from qtpy import QtWidgets as QW

from src.widgets.UtilityWidgets import error_dialog


class PSDMicroModel():
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
        self.view.modelDropdown.addItems(_MICRO_PSD_MODELS),
        self.view.geometryDropdown.addItems(_PORE_GEOMETRIES),
        self.view.amodelDropdown.addItems(_ADSORBENT_MODELS),

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
                self.results = psd_microporous(
                    self.isotherm,
                    branch=self.view.branchDropdown.currentText(),
                    psd_model=self.view.modelDropdown.currentText(),
                    pore_geometry=self.view.geometryDropdown.currentText(),
                    material_model=self.view.amodelDropdown.currentText(),
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
