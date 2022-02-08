import numpy as np
from qtpy import QtWidgets as QW

import pygaps
from pygaps.graphing.iast_graphs import plot_iast
from pygaps.graphing.labels import label_units_iso
from pygaps.iast.pgiast import iast_point_fraction
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.widgets.UtilityWidgets import error_dialog


class IASTModel():

    isotherms = None
    view = None

    # Settings
    setting_data = None
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
            self.output = '<font color="magenta">Careful, using PointIsotherms interpolates then numerically calculates spreading pressure. Calculations may be slow.</font>'
            self.view.output.setText(self.output)

        if not all(i.temperature == isotherms[0].temperature for i in isotherms):
            self.output = '<font color="magenta">Isotherms do not seem to have the same temperature. Is this correct?</font>'
            self.view.output.setText(self.output)

        # View actions
        # view setup
        props = ["Total P"] + [f"{i.adsorbate} fraction" for i in self.isotherms]
        self.view.data_table.set_data(props=props, data=self.setting_data)
        self.view.branch_dropdown.addItems(["ads", "des"])
        self.view.branch_dropdown.setCurrentText(self.branch)

        # connect signals
        self.view.branch_dropdown.currentIndexChanged.connect(self.select_branch)
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

        pressures_t = self.view.data_table.data["Total P"].to_numpy()
        pressures_p = self.view.data_table.data.iloc[:, 1:].to_numpy()
        fractions = np.apply_along_axis(lambda x: x / np.sum(x), 1, pressures_p)

        if pressures_t is None:
            error_dialog("First specify total pressure and partial pressures.")
            return

        with log_hook:
            try:
                # Generate the array of partial pressures
                results = np.zeros(pressures_p.shape)

                for ind, fraction in enumerate(fractions):
                    results[ind, :] = iast_point_fraction(
                        self.isotherms,
                        gas_mole_fraction=fraction,
                        total_pressure=pressures_t[ind],
                        branch=self.branch,
                    )
                self.results = results
                self.pressures = pressures_t
                self.fractions = fractions
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
        plot_iast(
            self.pressures,
            self.results,
            [i.adsorbate for i in self.isotherms],
            label_units_iso(self.isotherms[0], "pressure"),
            label_units_iso(self.isotherms[0], "loading"),
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
        if self.results is None:
            error_dialog("No results to export.")
            return
        from pygapsgui.utilities.result_export import serialize
        p_label = label_units_iso(self.isotherms[0], "pressure")
        l_label = label_units_iso(self.isotherms[0], "loading")
        results = {f"Total {p_label}": self.pressures}
        results.update({
            f"{iso.adsorbate} {l_label}": self.results.T[i]
            for i, iso in enumerate(self.isotherms)
        })

        serialize(results, how="V", parent=self.view)
