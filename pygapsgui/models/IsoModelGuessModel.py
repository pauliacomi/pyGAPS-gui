from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygaps import ModelIsotherm
from pygaps.modelling import _GUESS_MODELS
from pygaps.modelling import _MODELS
from pygaps.utilities.exceptions import CalculationError
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.widgets.UtilityDialogs import error_dialog


class IsoModelGuessModel():
    """Automatic isotherm model fit: MV model."""

    isotherm = None
    model_isotherm = None
    model_attempts = None
    view = None

    # Calculated
    iso_params = None
    loading = None
    pressure = None

    # Settings
    branch = "ads"
    limits = None
    auto = True

    # Results
    output = ""
    success = True

    def __init__(self, isotherm, view):
        """First init"""
        # Save refs
        self.isotherm = isotherm
        self.view = view

        # Fail condition
        if isinstance(isotherm, ModelIsotherm):
            error_dialog("Isotherm selected is already a model")
            self.success = False
            return

        # view setup
        self.view.setWindowTitle(
            self.view.windowTitle() + f" '{isotherm.material} - {isotherm.adsorbate}'"
        )
        for model in _MODELS:
            item = QW.QListWidgetItem(model)
            if model in _GUESS_MODELS:
                item.setCheckState(QC.Qt.Checked)
            else:
                item.setCheckState(QC.Qt.Unchecked)
            self.view.model_list.addItem(item)
        self.view.branch_dropdown.addItems(["ads", "des"])
        self.view.branch_dropdown.setCurrentText(self.branch)

        # plot setup
        self.view.iso_graph.branch = self.branch
        self.view.iso_graph.lgd_keys = ["material"]
        self.view.iso_graph.set_isotherms([self.isotherm])
        self.limits = self.view.iso_graph.x_range

        # connect signals
        self.view.branch_dropdown.currentIndexChanged.connect(self.select_branch)
        self.view.x_select.slider.rangeChanged.connect(self.calculate_with_limits)
        self.view.calc_auto_button.clicked.connect(self.calculate_auto)

        # populate initial
        self.prepare_values()
        self.view.iso_graph.draw_isotherms()

    def prepare_values(self):
        """Preliminary calculation of values that rarely change."""
        self.iso_params = self.isotherm.to_dict()
        pressure = self.isotherm.pressure(
            branch=self.branch,
            limits=self.limits,
            indexed=True,
        )
        loading = self.isotherm.loading(
            branch=self.branch,
            indexed=True,
        )
        loading = loading[pressure.index]
        self.pressure = pressure.values
        self.loading = loading.values

    def calculate_auto(self):
        """Automatic calculation."""
        self.auto = True
        if self.calculate():
            self.output_log()
            self.output_results()
            self.plot_results()
        else:
            self.output_log()
            self.plot_clear()

    def calculate_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        self.prepare_values()

    def calculate(self):
        """Call pyGAPS to perform main calculation."""
        self.model_attempts = []
        checked_models = [
            self.view.model_list.item(row).data(QC.Qt.DisplayRole)
            for row in range(self.view.model_list.count())
            if self.view.model_list.item(row).checkState() == QC.Qt.Checked
        ]
        with log_hook:
            try:
                for model in checked_models:
                    try:
                        isotherm = ModelIsotherm(
                            pressure=self.pressure,
                            loading=self.loading,
                            branch=self.branch,
                            model=model,
                            verbose=True,
                            plot_fit=False,
                            **self.iso_params,
                        )
                        self.model_attempts.append(isotherm)
                    except CalculationError as err:
                        log_hook.logger.info(
                            f'<font color="red">Modelling using {model} failed.</font>'
                        )
                # We catch any errors or warnings and display them to the user
            except Exception as err:
                self.output += f'<font color="red">Model fitting failed! <br> {err}</font>'
                return False
            self.output += log_hook.get_logs()

            if not self.model_attempts:
                self.output += '<font color="red">No model could be reliably fit on the isotherm.</font><br>'
                return False

            errors = [x.model.rmse for x in self.model_attempts]
            self.model_isotherm = self.model_attempts[errors.index(min(errors))]
            self.output += f'<font color="green">Best model fit is {self.model_isotherm.model.name}.</font>'
            return True

    def plot_results(self):
        """Fill in any GUI plots with results."""
        self.view.iso_graph.model_isotherm = self.model_isotherm
        self.view.iso_graph.draw_isotherms()

    def plot_clear(self):
        """Reset plots to default values."""
        self.view.iso_graph.draw_isotherms()

    def output_results(self):
        """Fill in any GUI text output with results"""
        pass

    def output_log(self):
        """Output text or dialog error/warning/info."""
        self.view.output.setText(self.output)
        self.output = ""

    def slider_reset(self):
        """Resets the GUI selection sliders."""
        self.view.x_select.setValues(self.limits, emit=False)
        self.view.iso_graph.draw_xlimits(self.limits[0], self.limits[1])

    def select_branch(self):
        """Handle isotherm branch selection."""
        self.branch = self.view.branch_dropdown.currentText()
        self.view.iso_graph.branch = self.branch
        self.model_isotherm = None
        self.plot_results()
