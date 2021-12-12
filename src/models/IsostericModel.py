import warnings

from pygaps.characterisation.isosteric_enth import isosteric_enthalpy, isosteric_enthalpy_raw
from pygaps.graphing.calc_graphs import isosteric_enthalpy_plot


class IsostericModel():
    def __init__(self, isotherms):

        self.isotherms = isotherms

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

        # plot isotherm
        self.view.isoGraph.set_isotherms([self.isotherm])
        self.view.isoGraph.draw_isotherms()

        # connect signals
        self.view.autoButton.clicked.connect(self.calc_auto)
        self.view.pSlider.rangeChanged.connect(self.calc_with_limits)

        # run
        self.calc_auto()

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        if self.calculate():
            self.output_results()
            self.plot()
            self.slider_reset()

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        if self.calculate():
            self.calculate()
            self.output_results()
            self.plot()

    def calculate(self):
        with warnings.catch_warnings(record=True) as warning:

            warnings.simplefilter("always")

            try:
                self.results = isosteric_enthalpy(
                    self.isotherms,
                    branch=self.view.branchDropdown.currentText(),
                    # loading_points=,
                )

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output = f'<font color="red">Calculation failed! <br> {e}</font>'
                return False

            if warning:
                self.output = '<br>'.join([
                    f'<font color="red">Warning: {a.message}</font>' for a in warning
                ])
            else:
                self.output = None
            return True

    def output_results(self):
        pass

    def slider_reset(self):
        self.view.pSlider.setValues([0, 1], emit=False)

    def plot(self):

        # Clear plots
        self.view.resGraph.clear()

        # Generate plot of the BET points chosen
        isosteric_enthalpy_plot(
            self.results["loading"],
            self.results["isosteric_enthalpy"],
            self.results["std_errs"],
            ax=self.view.resGraph.ax,
        )

        # Draw figures
        self.view.resGraph.canvas.draw()
