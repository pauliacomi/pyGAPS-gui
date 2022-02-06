import numpy

from pygaps.characterisation.isosteric_enth import isosteric_enthalpy
from pygaps.characterisation.isosteric_enth import isosteric_enthalpy_raw
from pygaps.graphing.calc_graphs import isosteric_enthalpy_plot
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.widgets.UtilityWidgets import error_dialog


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

    def __init__(self, isotherms, view):
        """First init"""
        # Save refs
        self.isotherms = isotherms
        self.view = view

        # Fail condition

        # view setup
        self.view.setWindowTitle(
            self.view.windowTitle() + f" '{isotherms[0].material} - {isotherms[0].adsorbate}'"
        )
        self.view.branch_dropdown.addItems(["ads", "des"])
        self.view.branch_dropdown.setCurrentText(self.branch)
        self.view.points_input.setValue(self.loading_point_no)

        # plot setup
        self.view.iso_graph.branch = self.branch
        self.view.iso_graph.lgd_keys = ["temperature"]
        self.view.iso_graph.set_isotherms(self.isotherms)

        # connect signals
        self.view.branch_dropdown.currentIndexChanged.connect(self.select_branch)
        self.view.points_input.lineEdit().editingFinished.connect(self.select_points)
        self.view.calc_auto_button.clicked.connect(self.calc_auto)
        self.view.y_select.slider.rangeChanged.connect(self.calc_with_limits)
        self.view.button_box.accepted.connect(self.export_results)
        self.view.button_box.rejected.connect(self.view.reject)

        # Calculation
        # run calculation
        self.calc_auto()

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        self.loading_points = None
        if self.calculate():
            self.limits = (self.results["loading"][0], self.results["loading"][-1])
            self.slider_reset()
            self.output_log()
            self.output_results()
            self.plot_results()
        else:
            self.output_log()
            self.plot_clear()

    def calc_with_limits(self, down, up):
        """Set limits on calculation."""
        self.limits = [down, up]
        self.loading_points = numpy.linspace(down, up, self.loading_point_no)
        if self.calculate():
            self.output_log()
            self.output_results()
            self.plot_results()
        else:
            self.output_log()
            self.plot_clear()

    def calculate(self):
        with log_hook:
            try:
                self.results = isosteric_enthalpy(
                    self.isotherms,
                    branch=self.branch,
                    loading_points=self.loading_points,
                )
            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Calculation failed! <br> {e}</font>'
                self.limits = None
                return False
            self.output += log_hook.getLogs()
            return True

    def output_results(self):
        pass

    def output_log(self):
        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):
        # Isotherm plot update
        self.view.iso_graph.draw_isotherms()

        # Generate plot of the points chosen
        self.view.res_graph.ax.clear()
        isosteric_enthalpy_plot(
            self.results["loading"],
            self.results["isosteric_enthalpy"],
            self.results["std_errs"],
            isotherm=self.isotherms[0],
            ax=self.view.res_graph.ax,
        )
        self.view.res_graph.canvas.draw_idle()

    def plot_clear(self):
        self.view.iso_graph.draw_isotherms()
        self.view.res_graph.clear()
        self.view.res_graph.canvas.draw_idle()

    def slider_reset(self):
        if self.limits:
            self.view.y_select.setRange(self.limits)
            self.view.y_select.setValues(self.limits, emit=False)
            self.view.iso_graph.draw_ylimits(self.limits[0], self.limits[1])

    def select_branch(self, branch):
        self.branch = self.view.branch_dropdown.currentText()
        self.view.iso_graph.set_branch(self.branch)
        self.calc_auto()

    def select_points(self, npoints):
        self.loading_point_no = self.view.points_input.value()
        self.calc_auto()

    def export_results(self):
        if not self.results:
            error_dialog("No results to export.")
            return
        from pygapsgui.utilities.result_export import serialize
        results = {
            f"Loading [{self.isotherms[0].loading_unit}/{self.isotherms[0].material_unit}]":
            self.results.get("loading"),
            "Isosteric Enthalpy [kJ/mol]":
            self.results.get("isosteric_enthalpy"),
            "Standard Error [kJ/mol]":
            self.results.get("std_errs"),
        }
        serialize(results, how="V", parent=self.view)