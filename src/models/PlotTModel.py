import warnings

from pygaps.characterisation.t_plots import t_plot_raw
from pygaps.characterisation.models_thickness import (_THICKNESS_MODELS, get_thickness_model)
from pygaps.graphing.calc_graphs import tp_plot
from pygaps.utilities.exceptions import CalculationError

from src.widgets.UtilityWidgets import error_dialog

from qtpy import QtWidgets as QW


class PlotTModel():

    isotherm = None
    view = None

    # Settings
    branch = "ads"
    limits = None
    thickness_model = None
    molar_mass = None
    liquid_density = None

    # Results
    t_curve = None
    results = None

    output = ""
    success = True

    def __init__(self, isotherm, view):
        # Save refs
        self.isotherm = isotherm
        self.view = view

        # Fail condition
        try:
            self.isotherm.pressure(pressure_mode="relative")
        except CalculationError:
            error_dialog(
                "T-plots cannot be defined for supercritical "
                "adsorbates or those with an unknown saturation pressure. If "
                "your adsorbate does not have a thermodynamic backend add a "
                "'saturation_pressure' metadata to it."
            )
            self.success = False
            return

        # View actions

        # setup
        self.view.branch_dropdown.addItems(["ads", "des"])
        self.view.branch_dropdown.setCurrentText(self.branch)
        models = list(_THICKNESS_MODELS.keys())
        self.view.thickness_dropdown.addItems(models)

        # connect signals
        self.view.branch_dropdown.currentIndexChanged.connect(self.select_branch)
        # TODO: add the ability for custom callable models
        self.view.thickness_dropdown.currentIndexChanged.connect(self.select_tmodel)
        self.view.calc_auto_button.clicked.connect(self.calc_auto)
        self.view.x_select.slider.rangeChanged.connect(self.calc_with_limits)
        self.view.button_box.accepted.connect(self.export_results)
        self.view.button_box.rejected.connect(self.view.reject)

        # Calculation
        # static parameters
        self.molar_mass = self.isotherm.adsorbate.molar_mass()
        self.liquid_density = self.isotherm.adsorbate.liquid_density(isotherm.temperature)
        self.thickness_model = get_thickness_model(models[0])
        # dynamic parameters
        self.prepare_values()
        # run calculation
        self.calc_auto()

    def prepare_values(self):
        # Loading and pressure
        self.loading = self.isotherm.loading(
            branch=self.branch,
            loading_basis='molar',
            loading_unit='mol',
        )
        self.pressure = self.isotherm.pressure(
            branch=self.branch,
            pressure_mode="relative",
        )
        if self.branch == 'des':
            self.loading = self.loading[::-1]
            self.pressure = self.pressure[::-1]

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        self.calculate()
        self.slider_reset()
        self.output_results()
        self.plot_results()

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        self.calculate()
        self.output_results()
        self.plot_results()

    def calculate(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            try:
                self.results, self.t_curve = t_plot_raw(
                    self.loading,
                    self.pressure,
                    self.thickness_model,
                    self.liquid_density,
                    self.molar_mass,
                    t_limits=self.limits,
                )

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Calculation failed! <br> {e}</font>'

            if warning:
                self.output += '<br>'.join([
                    f'<font color="magenta">Warning: {a.message}</font>' for a in warning
                ])

    def output_results(self):
        self.view.res_table.setRowCount(0)
        self.view.res_table.setRowCount(len(self.results))
        for index, result in enumerate(self.results):
            self.view.res_table.setItem(
                index, 0, QW.QTableWidgetItem(f"{result.get('adsorbed_volume'):g}")
            )
            self.view.res_table.setItem(index, 1, QW.QTableWidgetItem(f"{result.get('area'):g}"))
            self.view.res_table.setItem(
                index, 2, QW.QTableWidgetItem(f"{result.get('corr_coef'):g}")
            )
            self.view.res_table.setItem(index, 3, QW.QTableWidgetItem(f"{result.get('slope'):g}"))
            self.view.res_table.setItem(
                index, 4, QW.QTableWidgetItem(f"{result.get('intercept'):g}")
            )

        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):

        # Generate tplot
        self.view.res_graph.clear()
        tp_plot(
            self.t_curve,
            self.loading,
            self.results,
            ax=self.view.res_graph.ax,
        )
        self.view.res_graph.canvas.draw()

    def slider_reset(self):
        self.view.x_select.setRange((0, self.t_curve[-1]))
        self.view.x_select.setValues((self.t_curve[0], self.t_curve[-1]), emit=False)
        self.view.res_graph.draw_limits(self.t_curve[0], self.t_curve[-1])

    def select_tmodel(self):
        tmodel_text = self.view.thickness_dropdown.currentText()
        self.thickness_model = get_thickness_model(tmodel_text)
        self.calc_auto()

    def select_branch(self):
        self.branch = self.view.branch_dropdown.currentText()
        self.prepare_values()
        self.calc_auto()

    def export_results(self):
        if not self.results:
            error_dialog("No results to export.")
            return
        from src.utilities.result_export import serialize
        results = {
            e: {
                "Pore volume [cm3/g]": result.get("adsorbed_volume"),
                "Area [m2/g]": result.get("area"),
                "R^2": result.get("corr_coef"),
                "Slope": result.get("slope"),
                "Intercept": result.get("intercept"),
            }
            for e, result in enumerate(self.results)
        }
        if serialize(results, parent=self.view):
            self.view.accept()
