import numpy
from qtpy import QtCore as QC

import pygaps
from pygaps import ModelIsotherm
from pygaps.modelling import _MODELS
from pygaps.modelling import get_isotherm_model
from pygaps.units.converter_mode import _LOADING_MODE
from pygaps.units.converter_mode import _MATERIAL_MODE
from pygaps.units.converter_mode import _PRESSURE_MODE
from pygaps.units.converter_unit import _TEMPERATURE_UNITS
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.utilities.tex2svg import tex2svg
from pygapsgui.widgets.SpinBoxLimitSlider import QHSpinBoxLimitSlider
from pygapsgui.widgets.UtilityDialogs import error_dialog


class IsoModelManualModel():
    """Manually create an isotherm model: QT MVC Model."""

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
        self.view.model_dropdown.addItems(_MODELS),
        self.view.branch_dropdown.addItems(["ads", "des"])
        self.view.branch_dropdown.setCurrentText(self.branch)
        self.view.adsorbate_input.addItems([ads.name for ads in pygaps.ADSORBATE_LIST], )
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
        self.view.iso_graph.branch = self.branch
        self.view.iso_graph.lgd_keys = ["material", "adsorbate", "temperature"]
        self.limits = [0, 1]

        # connect signals
        self.view.model_dropdown.currentIndexChanged.connect(self.select_model)
        self.view.branch_dropdown.currentIndexChanged.connect(self.select_branch)
        self.view.calc_manual_button.clicked.connect(self.calculate_manual)

        # populate initial
        self.select_model()

    def calculate_manual(self):
        """Use model parameters."""
        self.get_model_params()
        if self.calculate():
            self.output_log()
            self.output_results()
            self.plot_results()
        else:
            self.output_log()
            self.plot_clear()

    def calculate(self):
        """Call pyGAPS to perform main calculation."""
        with log_hook:
            try:
                self.model_isotherm = ModelIsotherm(
                    model=self.current_model,
                    branch=self.branch,
                    material="Model",
                    adsorbate=self.view.adsorbate_input.lineEdit().text(),
                    temperature=self.view.temperature_input.value(),
                    temperature_unit=self.view.temperature_unit.currentText(),
                    pressure_mode=self.view.unit_widget.pressure_mode.currentText(),
                    pressure_unit=self.view.unit_widget.pressure_unit.currentText(),
                    loading_basis=self.view.unit_widget.loading_basis.currentText(),
                    loading_unit=self.view.unit_widget.loading_unit.currentText(),
                    material_basis=self.view.unit_widget.material_basis.currentText(),
                    material_unit=self.view.unit_widget.material_unit.currentText(),
                )

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Model failed! <br> {e}</font>'
                return False
            self.output += log_hook.get_logs()
            return True

    def select_model(self):
        """What to do when the user selects a model."""
        self.model_isotherm = None
        self.current_model_name = self.view.model_dropdown.currentText()
        self.current_model = get_isotherm_model(self.current_model_name)

        # Model formula display
        if self.current_model.formula:
            self.view.model_formula.setVisible(True)
            self.view.model_formula.load(tex2svg(self.current_model.formula))
            aspectRatioMode = QC.Qt.AspectRatioMode(QC.Qt.KeepAspectRatio)
            self.view.model_formula.renderer().setAspectRatioMode(aspectRatioMode)
        else:
            self.view.model_formula.setVisible(False)

        # Model parameters
        for param in self.view.paramWidgets:
            self.view.paramWidgets[param].deleteLater()
        self.view.paramWidgets = {}

        for param in self.current_model.param_names:
            # TODO: creation/deletion of widgets is expensive... can they be reused?
            widget = QHSpinBoxLimitSlider()
            widget.setText(param)
            minv, maxv = self.current_model.param_bounds[param]
            if not minv or minv == -numpy.inf:
                minv = 0
            if not maxv or maxv == numpy.inf:
                maxv = 100
            widget.setRange(minv=minv, maxv=maxv)
            self.view.param_layout.insertWidget(self.view.param_layout.count() - 1, widget)
            self.view.paramWidgets[param] = widget

        # Update plot
        self.plot_clear()

    def output_results(self):
        """Fill in any GUI text output with results"""
        pass

    def output_log(self):
        """Output text or dialog error/warning/info."""
        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):
        """Fill in any GUI plots with results."""
        self.view.iso_graph.set_isotherms([self.model_isotherm])
        self.view.iso_graph.draw_isotherms()

    def plot_clear(self):
        """Reset plots to default values."""
        self.view.iso_graph.model_isotherm = self.model_isotherm
        self.view.iso_graph.draw_isotherms()

    def get_model_params(self):
        """Takes the parameters from the sliders and stores a model in memory."""
        for param in self.current_model.params:
            pval = self.view.paramWidgets[param].getValue()
            self.current_model.params[param] = float(pval)

        # TODO automatically convert limits on units change

        # The pressure range on which the model was built.
        self.current_model.pressure_range = (
            self.view.p_min.value(),
            self.view.p_max.value(),
        )

        # The loading range on which the model was built.
        self.current_model.loading_range = (
            self.view.l_min.value(),
            self.view.l_max.value(),
        )

    def select_branch(self):
        """Handle isotherm branch selection."""
        self.branch = self.view.branch_dropdown.currentText()
        self.view.iso_graph.branch = self.branch
        self.model_isotherm = None
        self.plot_clear()

    def slider_reset(self):
        """Resets the GUI selection sliders."""
        self.view.p_selector.setValues(self.limits, emit=False)
        self.view.iso_graph.draw_xlimits(self.limits[0], self.limits[1])
