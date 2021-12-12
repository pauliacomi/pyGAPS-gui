import warnings

from pygaps.modelling import _MODELS
from pygaps.modelling import get_isotherm_model
from pygaps import ModelIsotherm

from qtpy import QtWidgets as QW
from qtpy import QtCore as QC
from src.utilities.tex2svg import tex2svg

from src.widgets.UtilityWidgets import error_dialog


class IsoModelByModel():
    def __init__(self, isotherm):

        self.isotherm = isotherm
        self.model_isotherm = None
        self.branch = "ads"

        self.auto = True

        self.output = None

    def set_view(self, view):
        """Initial actions on view connect."""
        self.view = view

        # view setup
        self.view.modelDropdown.addItems(_MODELS),
        self.view.branchDropdown.addItems(["ads", "des"])

        # plot isotherm
        self.view.isoGraph.set_isotherms([self.isotherm])
        self.view.isoGraph.draw_isotherms(branch=self.branch)

        # connect signals
        self.view.modelDropdown.currentIndexChanged.connect(self.change_model)
        self.view.branchDropdown.currentIndexChanged.connect(self.select_branch)
        self.view.autoButton.clicked.connect(self.model_auto)
        self.view.manualButton.clicked.connect(self.model_manual)

        # populate initial
        self.change_model()

    def change_model(self):
        self.current_model_str = self.view.modelDropdown.currentText()
        self.current_model = get_isotherm_model(self.current_model_str)

        if self.current_model.formula:
            self.view.modelFormulaValue.setVisible(True)
            self.view.modelFormulaValue.load(tex2svg(self.current_model.formula))
            aspectRatioMode = QC.Qt.AspectRatioMode(QC.Qt.KeepAspectRatio)
            self.view.modelFormulaValue.renderer().setAspectRatioMode(aspectRatioMode)
        else:
            self.view.modelFormulaValue.setVisible(False)

        self.view.setupModelParams(self.current_model.param_names)

    def select_branch(self):
        self.branch = self.view.branchDropdown.currentText()
        self.view.isoGraph.draw_isotherms(branch=self.branch)

    def model_auto(self):
        """Automatic calculation."""
        self.auto = True
        if self.model():
            self.set_model_params()
            self.plot()

    def model_manual(self):
        """Use model parameters."""
        self.auto = False
        self.get_model_params()
        if self.model():
            self.plot()

    def model(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            try:
                if self.auto:
                    self.model_isotherm = ModelIsotherm.from_pointisotherm(
                        self.isotherm,
                        model=self.current_model_str,
                        branch=self.branch,
                    )
                    self.current_model = self.model_isotherm.model
                else:
                    self.model_isotherm = ModelIsotherm(
                        model=self.current_model,
                        branch=self.branch,
                        **self.isotherm.to_dict(),
                    )

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                error_dialog(f'<font color="red">Model fitting failed! <br> {e}</font>')
                return False

            if warning:
                error_dialog(
                    '<br>'.join([
                        f'<font color="red">Fitting warning: {a.message}</font>' for a in warning
                    ])
                )
                self.output = None

            return True

    def set_model_params(self):
        for param in self.current_model.params:
            pval = self.current_model.params[param]
            self.view.paramWidgets[param].setValue(pval)

    def get_model_params(self):
        for param in self.current_model.params:
            pval = self.view.paramWidgets[param].getValue()
            pval = float(pval)
            self.current_model.params[param] = pval

        # The pressure range on which the model was built.
        pressure = self.isotherm.pressure(branch=self.branch)
        self.current_model.pressure_range = [min(pressure), max(pressure)]

        # The loading range on which the model was built.
        loading = self.isotherm.loading(branch=self.branch)
        self.current_model.loading_range = [min(loading), max(loading)]

    def plot(self):
        self.view.isoGraph.set_isotherms([self.isotherm, self.model_isotherm])
        self.view.isoGraph.draw_isotherms(branch=self.branch)
