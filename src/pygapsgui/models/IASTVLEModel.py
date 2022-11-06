import pygaps
from pygaps.graphing.iast_graphs import plot_iast_vle
from pygaps.iast import iast_binary_vle
from pygaps.utilities.exceptions import CalculationError
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.widgets.UtilityDialogs import error_dialog


class IASTVLEModel():
    """IAST vapour-liquid equilibrium prediction: QT MVC Model."""

    isotherms = None
    view = None

    # Settings
    main_adsorbate = None
    total_pressure = None
    number_points = None
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

        # Fail condition
        # None

        # Warnings
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
        self.view.calc_button.clicked.connect(self.calc_auto)
        self.view.pressure_input.valueChanged.connect(self.calc_autobox)
        self.view.point_input.valueChanged.connect(self.calc_autobox)
        self.view.button_box.accepted.connect(self.export_results)
        self.view.button_box.rejected.connect(self.view.reject)

    def calc_auto(self):
        """Automatic calculation."""
        if self.calculate():
            self.output_log()
            self.output_results()
            self.plot_results()
        else:
            self.output_log()
            self.plot_clear()

    def calc_autobox(self):
        if self.view.calc_autobox.isChecked():
            self.calc_auto()

    def calculate(self):
        """Call pyGAPS to perform main calculation."""
        self.total_pressure = self.view.pressure_input.value()
        self.number_points = self.view.point_input.value()
        self.main_adsorbate = self.view.adsorbate_input.currentText()
        self.isotherms = sorted(
            self.isotherms,
            key=lambda x: x.adsorbate == self.main_adsorbate,
            reverse=True,
        )

        with log_hook:
            try:
                self.results = iast_binary_vle(
                    self.isotherms,
                    total_pressure=self.total_pressure,
                    npoints=self.number_points,
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
        plot_iast_vle(
            self.results['x'],
            self.results['y'],
            self.isotherms[0].adsorbate,
            self.isotherms[1].adsorbate,
            self.total_pressure,
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
        results = {
            f"Fraction {self.main_adsorbate} in bulk phase": self.results['y'],
            f"Fraction {self.main_adsorbate} in adsorbed phase": self.results['x'],
        }
        serialize(results, how="V", parent=self.view)
