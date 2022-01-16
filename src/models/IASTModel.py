import warnings

import pygaps
from pygaps.iast.pgiast import iast_point_fraction
from pygaps.graphing.iast_graphs import plot_iast

import numpy as np

from src.widgets.UtilityWidgets import error_dialog

from qtpy import QtWidgets as QW


class IASTModel():

    isotherms = None
    view = None

    # Settings
    setting_data = None

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
        props = ["Total P"] + [f"{i.adsorbate} R" for i in self.isotherms]
        self.view.data_table.set_data(props=props, data=self.setting_data)

        # connect signals
        self.view.calc_button.clicked.connect(self.calc_auto)

        # TODO export
        # self.view.button_box.accepted.connect(self.export_results)

        # Calculation

    def calc_auto(self):
        """Automatic calculation."""
        self.calculate()
        self.output_results()
        self.plot_results()

    def calculate(self):

        pressures_t = self.view.data_table.data["Total P"].to_numpy()
        pressures_p = self.view.data_table.data.iloc[:, 1:].to_numpy()
        fractions = np.apply_along_axis(lambda x: x / np.sum(x), 1, pressures_p)

        if pressures_t is None:
            error_dialog("First specify total pressure and partial pressures.")
            return

        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            try:
                # Generate the array of partial pressures
                results = np.zeros(pressures_p.shape)

                for ind, fraction in enumerate(fractions):
                    results[ind, :] = iast_point_fraction(
                        self.isotherms,
                        gas_mole_fraction=fraction,
                        total_pressure=pressures_t[ind],
                    )
                self.results = results
                self.pressures = pressures_t
                self.fractions = fractions

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Model failed! <br> {e}</font>'
            if warning:
                self.output += '<br>'.join([
                    f'<font color="red">Warning: {a.message}</font>' for a in warning
                ])

    def output_results(self):
        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):
        if self.results is None:
            return
        self.view.res_graph.clear()
        plot_iast(
            self.pressures,
            self.results,
            [i.adsorbate for i in self.isotherms],
            "bar",
            "mmol/g",
            ax=self.view.res_graph.ax,
        )
        self.view.res_graph.canvas.draw()
