from qtpy import QtWidgets as QW

import pygaps
from pygaps.graphing.iast_graphs import plot_iast_svp
from pygaps.graphing.labels import label_units_iso
from pygaps.iast import iast_binary_svp
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.widgets.UtilityDialogs import error_dialog


class IASTSVPModel():
    """IAST selectivity versus pressure prediction: QT MVC Model."""

    isotherms = None
    view = None

    # Settings
    main_adsorbate = None
    mole_fractions = None
    pressure_points = None
    branch = "ads"

    # Results
    results = None
    output = ""
    success = True

    def __init__(self, isotherms, view):
        """First init"""
        # Save refs
        self.isotherms = isotherms
        self.view = view

        if any(isinstance(i, pygaps.PointIsotherm) for i in isotherms):
            self.output = '<font color="magenta">Careful, using PointIsotherms interpolates then numerically calculates spreading pressure.</font>'
            self.view.output.setText(self.output)

        if not all(i.temperature == isotherms[0].temperature for i in isotherms):
            self.output = '<font color="magenta">Isotherms do not seem to have the same temperature. Is this correct?</font>'
            self.view.output.setText(self.output)

        # View actions
        # view setup
        self.view.adsorbate_input.addItems([i.adsorbate.name for i in isotherms])
        self.view.adsorbate_input.setCurrentText(isotherms[0].adsorbate.name)
        self.view.branch_dropdown.addItems(["ads", "des"])
        self.view.branch_dropdown.setCurrentText(self.branch)

        # connect signals
        self.view.branch_dropdown.currentIndexChanged.connect(self.select_branch)
        self.view.data_table.set_data(props=["Pressure"], data=self.pressure_points)
        self.view.calc_button.clicked.connect(self.calc_auto)
        self.view.button_box.accepted.connect(self.export_results)
        self.view.button_box.rejected.connect(self.view.reject)

        # Calculation

    def calc_auto(self):
        """Automatic calculation."""
        if self.calculate():
            self.output_log()
            self.output_results()
            self.plot_results()
        else:
            self.output_log()
            self.plot_clear()

    def calculate(self):
        """Call pyGAPS to perform main calculation."""
        self.pressure_points = self.view.data_table.data["Pressure"].to_numpy()
        if self.pressure_points is None:
            error_dialog("First specify pressure points.")
            return
        slider = float(self.view.fraction_slider.getValue())
        self.mole_fractions = [slider, 1 - slider]
        self.main_adsorbate = self.view.adsorbate_input.currentText()
        self.isotherms = sorted(
            self.isotherms,
            key=lambda x: x.adsorbate == self.main_adsorbate,
            reverse=True,
        )

        with log_hook:
            try:
                self.results = iast_binary_svp(
                    self.isotherms,
                    mole_fractions=self.mole_fractions,
                    pressures=self.pressure_points,
                    branch=self.branch,
                    warningoff=False,
                )
            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Model failed! <br> {e}</font>'
                return False
            self.output += log_hook.get_logs()
            return True

    def output_results(self):
        """Fill in any GUI text output with results"""
        pass

    def output_log(self):
        """Output text or dialog error/warning/info."""
        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):
        """Fill in any GUI plots with results."""
        self.view.res_graph.clear()
        plot_iast_svp(
            self.results['pressure'],
            self.results['selectivity'],
            self.isotherms[0].adsorbate,
            self.isotherms[1].adsorbate,
            self.mole_fractions[0],
            self.isotherms[0].pressure_unit,
            ax=self.view.res_graph.ax,
        )
        self.view.res_graph.canvas.draw()

    def plot_clear(self):
        """Reset plots to default values."""
        self.view.res_graph.clear()
        self.view.res_graph.canvas.draw()

    def select_branch(self):
        """Handle isotherm branch selection."""
        self.branch = self.view.branch_dropdown.currentText()
        self.plot_clear()

    def export_results(self):
        """Save results as a file."""
        if not self.results:
            error_dialog("No results to export.")
            return
        from pygapsgui.utilities.result_export import serialize
        p_units = label_units_iso(self.isotherms[0], "pressure")
        results = {
            f"Total {p_units}": self.results['pressure'],
            f"Selectivity for {self.main_adsorbate}": self.results['selectivity'],
        }
        serialize(results, how="V", parent=self.view)
