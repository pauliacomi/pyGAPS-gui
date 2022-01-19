import warnings

import pygaps
from pygaps.iast import iast_binary_svp
from pygaps.graphing.iast_graphs import plot_iast_svp

from src.widgets.UtilityWidgets import error_dialog

from qtpy import QtWidgets as QW


class IASTSVPModel():

    isotherms = None
    view = None

    # Settings
    main_adsorbate = None
    mole_fractions = None
    pressure_points = None

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

        # connect signals
        self.view.points_button.clicked.connect(self.create_points)
        self.view.calc_button.clicked.connect(self.calc_auto)
        # TODO export
        # self.view.button_box.accepted.connect(self.export_results)

        # Calculation

    def create_points(self):
        from src.widgets.RangeGenerator import RangeGenDialog
        dialog = RangeGenDialog(props=["Pressure"], data=self.pressure_points, parent=self.view)
        ret = dialog.exec()

        if ret == QW.QDialog.Accepted:
            points = dialog.widget.data["Pressure"].to_numpy()
            if points is not None and len(points) > 0:
                self.pressure_points = points
                self.view.points_button.setText("Modify pressure")
            else:
                self.pressure_points = None
                self.view.points_button.setText("Specify pressure")

    def calc_auto(self):
        """Automatic calculation."""
        self.calculate()
        self.output_results()
        self.plot_results()

    def calculate(self):
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

        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            try:
                self.results = iast_binary_svp(
                    self.isotherms,
                    mole_fractions=self.mole_fractions,
                    pressures=self.pressure_points,
                    warningoff=False,
                )
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
