from src.utilities.log_hook import log_hook

import pygaps
from pygaps.iast import iast_binary_vle
from pygaps.utilities.exceptions import CalculationError
from pygaps.graphing.iast_graphs import plot_iast_vle

from src.widgets.UtilityWidgets import error_dialog


class IASTVLEModel():

    isotherms = None
    view = None

    # Settings
    main_adsorbate = None
    total_pressure = None
    number_points = None

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
        self.total_pressure = float(self.view.pressure_input.text())
        self.number_points = int(self.view.point_input.text())
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
                    warningoff=False,
                )
            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Model failed! <br> {e}</font>'
                return False
            self.output += log_hook.getLogs()
            return True

    def output_results(self):
        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):
        if self.results is None:
            return
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
