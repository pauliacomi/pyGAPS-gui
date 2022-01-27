import warnings

from pygaps.characterisation.isosteric_enth import isosteric_enthalpy, isosteric_enthalpy_raw
from pygaps.graphing.calc_graphs import isosteric_enthalpy_plot

from src.widgets.UtilityWidgets import error_dialog

import numpy


class IsostericModel():
    # Refs
    isotherms = None
    view = None

    # Settings
    branch = "ads"
    limits = None
    loading_points = None
    loading_point_no = 50

    # Results
    results = None
    output = ""
    success = True

    # TODO finish implementation
    def __init__(self, isotherms, view):
        """First init"""
        # Save refs
        self.isotherms = isotherms
        self.view = view

        # view setup
        self.view.branch_dropdown.addItems(["ads", "des"])
        self.view.branch_dropdown.setCurrentText(self.branch)

        # plot isotherm
        self.view.iso_graph.branch = self.branch
        self.view.iso_graph.set_isotherms(self.isotherms)

        # connect signals
        self.view.branch_dropdown.currentIndexChanged.connect(self.select_branch)
        self.view.calc_auto_button.clicked.connect(self.calc_auto)
        # self.view.x_select.slider.rangeChanged.connect(self.calc_with_limits)
        self.view.button_box.accepted.connect(self.export_results)
        self.view.button_box.rejected.connect(self.view.reject)

        # Calculation
        # run calculation
        self.calc_auto()

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        self.loading_points = None
        self.calculate()
        self.slider_reset()
        self.output_results()
        self.plot_results()

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        self.loading_points = numpy.linspace(left, right, self.loading_point_no)
        self.calculate()
        self.output_results()
        self.plot_results()

    def calculate(self):
        with warnings.catch_warnings(record=True) as warning:

            warnings.simplefilter("always")

            try:
                self.results = isosteric_enthalpy(
                    self.isotherms,
                    branch=self.branch,
                    loading_points=self.loading_points,
                )

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
        if not self.results:
            return

        # Isotherm plot update
        self.view.iso_graph.draw_isotherms(branch=self.branch)

        # Generate plot of the points chosen
        self.view.res_graph.clear()
        # TODO: there's a new legend every time...
        isosteric_enthalpy_plot(
            self.results["loading"],
            self.results["isosteric_enthalpy"],
            self.results["std_errs"],
            ax=self.view.res_graph.ax,
        )
        self.view.res_graph.canvas.draw()

    def slider_reset(self):
        if self.limits:
            self.view.x_select.setValues(self.limits, emit=False)
            self.view.iso_graph.draw_limits(self.limits[0], self.limits[1])

    def select_branch(self):
        self.branch = self.view.branch_dropdown.currentText()
        self.calc_auto()

    def export_results(self):
        if not self.results:
            error_dialog("No results to export.")
            return
