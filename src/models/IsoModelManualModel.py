import warnings

import pygaps
from pygaps.utilities.converter_mode import _PRESSURE_MODE, _LOADING_MODE, _MATERIAL_MODE
from pygaps.utilities.converter_unit import _TEMPERATURE_UNITS
from pygaps.modelling import _MODELS
from pygaps.modelling import get_isotherm_model
from pygaps import ModelIsotherm

from qtpy import QtCore as QC
from src.utilities.tex2svg import tex2svg
from src.widgets.SpinBoxSlider import QHSpinBoxSlider

from src.widgets.UtilityWidgets import error_dialog


class IsoModelManualModel():

    model_isotherm = None
    view = None

    # Settings
    branch = "ads"
    limits = None
    current_model = None
    current_model_name = None

    # Results
    output = ""
    success = True

    def __init__(self, view):
        """First init"""
        # Save refs
        self.view = view

        # view setup
        self.view.modelDropdown.addItems(_MODELS),
        self.view.branchDropdown.addItems(["ads", "des"])
        self.view.branchDropdown.setCurrentText(self.branch)
        self.view.adsorbate_input.insertItems(
            0,
            [ads.name for ads in pygaps.ADSORBATE_LIST],
        )
        # populate units view
        self.view.unit_widget.init_boxes(
            _PRESSURE_MODE,
            _LOADING_MODE,
            _MATERIAL_MODE,
            _TEMPERATURE_UNITS,
        )
        self.view.unit_widget.units_active = True
        self.view.unit_widget.init_pressure("absolute", "bar")
        self.view.unit_widget.init_loading("molar", "mmol")
        self.view.unit_widget.init_material("mass", "g")

        # plot setup
        self.limits = [0, 1]

        # connect signals
        self.view.modelDropdown.currentIndexChanged.connect(self.select_model)
        self.view.branchDropdown.currentIndexChanged.connect(self.select_branch)
        self.view.x_select.slider.rangeChanged.connect(self.model_with_limits)
        self.view.manualButton.clicked.connect(self.model_manual)

        # populate initial
        self.select_model()

    def model_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        self.model_manual()

    def model_manual(self):
        """Use model parameters."""
        self.get_model_params()
        self.model()
        self.output_results()
        self.plot_results()

    def model(self):
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            try:
                self.model_isotherm = ModelIsotherm(
                    model=self.current_model,
                    branch=self.branch,
                    material="Model",
                    adsorbate=self.view.adsorbate_input.lineEdit().text(),
                    temperature=float(self.view.tempInput.text()),
                    temperature_unit=self.view.temperatureUnit.currentText(),
                    pressure_mode=self.view.unit_widget.pressureMode.currentText(),
                    pressure_unit=self.view.unit_widget.pressureUnit.currentText(),
                    loading_basis=self.view.unit_widget.loadingBasis.currentText(),
                    loading_unit=self.view.unit_widget.loadingUnit.currentText(),
                    material_basis=self.view.unit_widget.materialBasis.currentText(),
                    material_unit=self.view.unit_widget.materialUnit.currentText(),
                )

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Model failed! <br> {e}</font>'
            if warning:
                self.output += '<br>'.join([
                    f'<font color="red">Warning: {a.message}</font>' for a in warning
                ])

    def select_model(self):
        self.model_isotherm = None
        self.current_model_name = self.view.modelDropdown.currentText()
        self.current_model = get_isotherm_model(self.current_model_name)

        # Model formula display
        if self.current_model.formula:
            self.view.modelFormulaValue.setVisible(True)
            self.view.modelFormulaValue.load(tex2svg(self.current_model.formula))
            aspectRatioMode = QC.Qt.AspectRatioMode(QC.Qt.KeepAspectRatio)
            self.view.modelFormulaValue.renderer().setAspectRatioMode(aspectRatioMode)
        else:
            self.view.modelFormulaValue.setVisible(False)

        # Model parameters
        for param in self.view.paramWidgets:
            self.view.paramWidgets[param].deleteLater()
        self.view.paramWidgets = {}

        for param in self.current_model.param_names:
            widget = QHSpinBoxSlider(parent=self.view.paramBox)
            widget.setText(param)
            self.view.paramLayout.addWidget(widget)
            self.view.paramWidgets[param] = widget

        # Update plot
        self.plot_results()

    def get_model_params(self):
        for param in self.current_model.params:
            pval = self.view.paramWidgets[param].getValue()
            self.current_model.params[param] = float(pval)

        # The pressure range on which the model was built.
        # TODO user-selectable limits for model
        self.current_model.pressure_range = self.limits

        # The loading range on which the model was built.
        # loading = self.isotherm.loading(branch=self.branch)
        # self.current_model.loading_range = [min(loading), max(loading)]

    def select_branch(self):
        self.branch = self.view.branchDropdown.currentText()
        self.view.isoGraph.branch = self.branch
        self.model_isotherm = None
        self.plot_results()

    def slider_reset(self):
        self.view.p_selector.setValues(self.limits, emit=False)
        self.view.isoGraph.draw_limits(self.limits[0], self.limits[1])

    def output_results(self):
        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):
        if self.model_isotherm:
            self.view.isoGraph.set_isotherms([self.model_isotherm])
            self.view.isoGraph.draw_isotherms(branch=self.branch)
