import warnings

from pygaps import ModelIsotherm
from pygaps.modelling import _GUESS_MODELS, _MODELS
from pygaps.utilities.exceptions import CalculationError

from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.utilities.log_hook import LogHook
from src.widgets.UtilityWidgets import error_dialog


class IsoModelGuessModel():

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
        for model in _MODELS:
            item = QW.QListWidgetItem(model)
            if model in _GUESS_MODELS:
                item.setCheckState(QC.Qt.Checked)
            else:
                item.setCheckState(QC.Qt.Unchecked)
            self.view.modelList.addItem(item)
        self.view.branchDropdown.addItems(["ads", "des"])
        self.view.branchDropdown.setCurrentText(self.branch)

        # plot setup
        self.view.isoGraph.set_isotherms([self.isotherm])
        self.limits = self.view.isoGraph.x_range

        # connect signals
        self.view.branchDropdown.currentIndexChanged.connect(self.select_branch)
        self.view.x_select.slider.rangeChanged.connect(self.model_with_limits)
        self.view.autoButton.clicked.connect(self.model_auto)

        # populate initial
        self.prepare_values()
        self.view.isoGraph.draw_isotherms(branch=self.branch)

    def prepare_values(self):
        # Loading and pressure
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

    def model_auto(self):
        """Automatic calculation."""
        self.auto = True
        self.model()
        self.slider_reset()
        self.output_results()
        self.plot_results()

    def model_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        self.prepare_values()

    def model(self):
        self.model_attempts = []
        checked_models = [
            self.view.modelList.item(row).data(QC.Qt.DisplayRole)
            for row in range(self.view.modelList.count())
            if self.view.modelList.item(row).checkState() == QC.Qt.Checked
        ]
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            with LogHook() as hook:
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
                        except CalculationError as e:
                            hook.logger.info(
                                f'<font color="red">Modelling using {model} failed.</font>'
                            )
                # We catch any errors or warnings and display them to the user
                except Exception as e:
                    self.output += f'<font color="red">Model fitting failed! <br> {e}</font>'

            self.output += hook.getLogs().replace("\n", "<br>")
            if warning:
                self.output += '<br>'.join([
                    f'<font color="red">Fitting warning: {a.message}</font>' for a in warning
                ])

            if not self.model_attempts:
                self.output += '<font color="red">No model could be reliably fit on the isotherm.</font><br>'
                return

            errors = [x.model.rmse for x in self.model_attempts]
            self.model_isotherm = self.model_attempts[errors.index(min(errors))]

    def select_branch(self):
        self.branch = self.view.branchDropdown.currentText()
        self.view.isoGraph.branch = self.branch
        self.model_isotherm = None
        self.plot_results()

    def slider_reset(self):
        self.view.x_select.setValues(self.limits, emit=False)
        self.view.isoGraph.draw_limits(self.limits[0], self.limits[1])

    def output_results(self):
        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):
        self.view.isoGraph.model_isotherm = self.model_isotherm
        self.view.isoGraph.draw_isotherms(branch=self.branch)
