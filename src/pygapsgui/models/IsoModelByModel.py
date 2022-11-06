from pygaps import ModelIsotherm
from pygapsgui.utilities.log_hook import log_hook
from pygapsgui.widgets.UtilityDialogs import error_dialog


class IsoModelByModel():
    """Fit an isotherm by a specific isotherm model: QT MVC Model."""

    isotherm = None
    isotherm_params: dict = None
    model_isotherm = None
    view = None

    # Settings
    branch: str = "ads"
    limits: "tuple[float, float]" = None
    auto: bool = True
    bounds: bool = False

    # Results
    output = ""
    success = True

    def __init__(self, isotherm, view):
        """First init"""
        # Save refs
        self.isotherm = isotherm
        self.isotherm_params = isotherm.to_dict()
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
        self.view.branch_dropdown.setCurrentText(self.branch)
        self.view.model_edit.set_fitting_model("Henry", self.branch)

        # plot setup
        self.view.iso_graph.branch = self.branch
        self.view.iso_graph.lgd_keys = ["material"]
        self.view.iso_graph.set_isotherms([self.isotherm])
        self.limits = self.view.iso_graph.x_range
        self.view.iso_graph.draw_isotherms()

        # connect signals
        self.view.model_edit.changed.connect(self.calculate_manual)
        self.view.x_select.slider.rangeChanged.connect(self.calculate_with_limits)
        self.view.calc_auto_button.clicked.connect(self.calculate_auto)
        self.view.calc_autolim_button.clicked.connect(self.calculate_with_bounds)

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
        self.calculate_auto()

    def calculate_with_bounds(self):
        """Use the selected parameter bounds for fitting."""
        self.bounds = True
        self.calculate_auto()
        self.bounds = False

    def calculate_manual(self):
        """Use model parameters."""
        self.auto = False
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

                    if self.bounds:
                        param_bounds = self.view.model_edit.get_model_bounds()
                    else:
                        param_bounds = None

                    self.model_isotherm = ModelIsotherm(
                        pressure=pressure.values,
                        loading=loading.values,
                        branch=self.branch,
                        model=self.view.model_edit.current_model.name,
                        param_bounds=param_bounds,
                        **self.isotherm_params
                    )
                    self.view.model_edit.set_fitting_model(self.model_isotherm.model)
                else:
                    self.model_isotherm = ModelIsotherm(
                        model=self.view.model_edit.current_model,
                        branch=self.branch,
                        **self.isotherm_params,
                    )
            # We catch any errors or warnings and display them to the user
            except Exception as err:
                self.output += f'<font color="red">Model fitting failed! <br> {err}</font>'
                return False
            self.output += log_hook.get_logs()
            self.output += self.view.model_edit.current_model.__str__().replace("\n", "<br>")
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

    def slider_reset(self):
        """Reset the GUI selection sliders."""
        self.view.p_selector.setValues(self.limits, emit=False)
        self.view.iso_graph.draw_xlimits(self.limits[0], self.limits[1])
