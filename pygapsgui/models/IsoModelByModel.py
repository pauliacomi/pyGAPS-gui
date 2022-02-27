import numpy
from qtpy import QtCore as QC

from pygaps import ModelIsotherm
from pygaps.modelling import _MODELS
from pygaps.modelling import get_isotherm_model
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.utilities.tex2svg import tex2svg
from pygapsgui.widgets.SpinBoxSlider import QHSpinBoxSlider
from pygapsgui.widgets.UtilityDialogs import error_dialog


class IsoModelByModel():
    """Fit an isotherm by a specific isotherm model: QT MVC Model."""

    isotherm = None
    model_isotherm = None
    view = None

    # Settings
    branch = "ads"
    limits = None
    auto = True
    current_model = None
    current_model_name = None

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
        self.view.model_dropdown.addItems(_MODELS),
        self.view.branch_dropdown.addItems(["ads", "des"])
        self.view.branch_dropdown.setCurrentText(self.branch)

        # plot setup
        self.view.iso_graph.branch = self.branch
        self.view.iso_graph.lgd_keys = ["material"]
        self.view.iso_graph.set_isotherms([self.isotherm])
        self.limits = self.view.iso_graph.x_range

        # connect signals
        self.view.model_dropdown.currentIndexChanged.connect(self.select_model)
        self.view.branch_dropdown.currentIndexChanged.connect(self.select_branch)
        self.view.x_select.slider.rangeChanged.connect(self.calculate_with_limits)
        self.view.calc_auto_button.clicked.connect(self.calculate_auto)
        self.view.calc_manual_button.clicked.connect(self.calculate_manual)

        # populate initial
        self.select_model()

    def calculate_auto(self):
        """Automatic calculation."""
        self.auto = True
        if self.calculate():
            self.set_model_params()
            self.output_log()
            self.output_results()
            self.plot_results()
        else:
            self.output_log()
            self.plot_clear()

    def calculate_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        self.calculate_auto()

    def calculate_manual(self):
        """Use model parameters."""
        self.auto = False
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
        self.model_isotherm = None
        with log_hook:
            try:
                if self.auto:
                    iso_params = self.isotherm.to_dict()
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

                    self.model_isotherm = ModelIsotherm(
                        pressure=pressure.values,
                        loading=loading.values,
                        branch=self.branch,
                        model=self.current_model_name,
                        **iso_params
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
                self.output += f'<font color="red">Model fitting failed! <br> {e}</font>'
                return False
            self.output += log_hook.get_logs()
            return True

    def output_results(self):
        """Fill in any GUI text output with results"""
        pass

    def output_log(self):
        """Output text or dialog error/warning/info."""
        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):
        """Fill in any GUI plots with results."""
        self.view.iso_graph.model_isotherm = self.model_isotherm
        self.view.iso_graph.draw_isotherms()

    def plot_clear(self):
        """Reset plots to default values."""
        self.view.iso_graph.model_isotherm = self.model_isotherm
        self.view.iso_graph.draw_isotherms()

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
            widget = QHSpinBoxSlider()
            widget.setText(param)
            minv, maxv = self.current_model.param_bounds[param]
            if not minv or minv == -numpy.inf:
                minv = 0
            if not maxv or maxv == numpy.inf:
                maxv = 100
            widget.setRange(minv=minv, maxv=maxv)
            self.view.param_layout.addWidget(widget)
            self.view.paramWidgets[param] = widget

        # Update plot
        self.plot_clear()

    def set_model_params(self):
        for param in self.current_model.param_names:
            pval = self.current_model.params[param]
            minv, maxv = self.current_model.param_bounds[param]
            if not minv or minv == -numpy.inf:
                minv = 0
            if not maxv or maxv == numpy.inf:
                maxv = pval * 2
            self.view.paramWidgets[param].setRange(minv=minv, maxv=maxv)
            self.view.paramWidgets[param].setValue(pval)

    def get_model_params(self):
        for param in self.current_model.params:
            pval = self.view.paramWidgets[param].getValue()
            self.current_model.params[param] = float(pval)

        # The pressure range on which the model was built.
        self.current_model.pressure_range = self.limits

        # The loading range on which the model was built.
        loading = self.isotherm.loading(branch=self.branch)
        self.current_model.loading_range = [min(loading), max(loading)]

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
