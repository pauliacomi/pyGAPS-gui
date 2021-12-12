import warnings

from pygaps.characterisation.tplot import t_plot_raw
from pygaps.characterisation.models_thickness import (_THICKNESS_MODELS, get_thickness_model)
from pygaps.graphing.calc_graphs import tp_plot

from qtpy import QtWidgets as QW


class PlotTModel():
    def __init__(self, isotherm):

        self.isotherm = isotherm

        # Properties
        self.molar_mass = self.isotherm.adsorbate.molar_mass()
        self.liquid_density = self.isotherm.adsorbate.liquid_density(isotherm.temperature)

        # Loading and pressure
        self.loading = self.isotherm.loading(
            branch='ads', loading_unit='mol', loading_basis='molar'
        )
        self.pressure = self.isotherm.pressure(branch='ads', pressure_mode='relative')

        self.limits = None
        self.minimum = None
        self.maximum = None

        self.thickness_model = None

        self.t_curve = None
        self.results = None
        self.output = None

    def set_view(self, view):
        """Initial actions on view connect."""
        self.view = view

        # setup
        self.view.thicknessDropdown.addItems(list(_THICKNESS_MODELS.keys()))

        # connect signals
        self.view.thicknessDropdown.currentIndexChanged.connect(self.save_tmodel)
        self.view.auto_button.clicked.connect(self.calc_auto)
        self.view.pSlider.rangeChanged.connect(self.calc_with_limits)

        # run
        self.save_tmodel()
        self.calc_auto()

    def save_tmodel(self):
        tmodel_text = self.view.thicknessDropdown.currentText()
        self.thickness_model = get_thickness_model(tmodel_text)

    def calc_auto(self):
        """Automatic calculation."""
        self.limits = None
        self.calculate()
        self.output_results()
        self.plot()
        self.slider_reset()

    def calc_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        self.calculate()
        self.output_results()
        self.plot()

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
                    limits=self.limits,
                )

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output = f'<font color="red">Calculation failed! <br> {e}</font>'
                return

            if warning:
                self.output = '<br>'.join([
                    f'<font color="red">Warning: {a.message}</font>' for a in warning
                ])
            else:
                self.output = None

    def output_results(self):
        self.view.resultsTable.setRowCount(0)
        self.view.resultsTable.setRowCount(len(self.results))
        for index, result in enumerate(self.results):
            self.view.resultsTable.setItem(
                index, 0, QW.QTableWidgetItem(f"{result.get('adsorbed_volume'):g}")
            )
            self.view.resultsTable.setItem(index, 1, QW.QTableWidgetItem(f"{result.get('area'):g}"))
            self.view.resultsTable.setItem(
                index, 2, QW.QTableWidgetItem(f"{result.get('corr_coef'):g}")
            )
            self.view.resultsTable.setItem(
                index, 3, QW.QTableWidgetItem(f"{result.get('slope'):g}")
            )
            self.view.resultsTable.setItem(
                index, 4, QW.QTableWidgetItem(f"{result.get('intercept'):g}")
            )

    def plot(self):

        # Clear plots
        self.view.tGraph.clear()

        # Generate tplot
        tp_plot(
            self.t_curve,
            self.loading,
            self.results,
            ax=self.view.tGraph.ax,
        )

        # Draw figures
        self.view.tGraph.canvas.draw()

    def slider_reset(self):
        self.view.pSlider.setValues((self.t_curve[0], self.t_curve[-1]), emit=False)
