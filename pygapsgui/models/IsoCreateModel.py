import pygaps
from pygaps import ModelIsotherm
from pygaps import PointIsotherm
from pygaps.core.baseisotherm import BaseIsotherm
from pygaps.units.converter_mode import _LOADING_MODE
from pygaps.units.converter_mode import _MATERIAL_MODE
from pygaps.units.converter_mode import _PRESSURE_MODE
from pygaps.units.converter_unit import _TEMPERATURE_UNITS
from pygapsgui.utilities.log_hook import log_hook


class IsoCreateModel():
    """Manually create an isotherm: QT MVC Model."""

    base_isotherm = None
    full_isotherm = None

    view = None

    # Settings
    iso_type = 0
    branch = "ads"
    limits = None
    current_model = None
    current_model_name = None

    # Results
    output = ""
    success = True

    def __init__(self, view):
        """First init."""

        # Instantiate parameters
        self.base_isotherm = BaseIsotherm(m="material", a="nitrogen", t=77.3)

        # Save refs
        self.view = view

        # populate view
        self.view.material_input.addItems([mat.name for mat in pygaps.MATERIAL_LIST])
        self.view.material_input.setCurrentText(self.base_isotherm.material.name)
        self.view.adsorbate_input.addItems([ads.name for ads in pygaps.ADSORBATE_LIST])
        self.view.adsorbate_input.setCurrentText(self.base_isotherm.adsorbate.name)
        self.view.temperature_input.setValue(self.base_isotherm.temperature)
        self.view.unit_widget.init_boxes(
            _PRESSURE_MODE,
            _LOADING_MODE,
            _MATERIAL_MODE,
            _TEMPERATURE_UNITS,
        )
        self.view.unit_widget.init_units(self.base_isotherm, active=True)
        self.view.metadata_extra_edit_widget.set_model(self.base_isotherm)

        # data
        self.view.model_edit.set_fitting_model("Langmuir", "ads")
        self.view.point_edit.set_datatable_model()

        # plot setup
        self.view.iso_graph.branch = self.branch
        self.view.iso_graph.lgd_keys = ["material", "adsorbate", "temperature"]

        # connect signals
        self.view.material_input.currentTextChanged.connect(self.handle_iso_baseprops)
        self.view.adsorbate_input.editTextChanged.connect(self.handle_iso_baseprops)
        self.view.temperature_input.valueChanged.connect(self.handle_iso_baseprops)
        self.view.unit_widget.pressure_changed.connect(self.handle_pressure)
        self.view.unit_widget.loading_changed.connect(self.handle_loading)
        self.view.unit_widget.material_changed.connect(self.handle_material)
        self.view.unit_widget.temperature_changed.connect(self.handle_temperature)
        self.view.metadata_extra_edit_widget.changed.connect(self.update)
        self.view.isotype_tab.currentChanged.connect(self.handle_isotype)
        self.view.point_edit.changed.connect(self.update)
        self.view.model_edit.changed.connect(self.update)

        # initial draw
        self.update()

    def handle_iso_baseprops(self):
        """Modify one of the current isotherm base properties (material/adsorbate/temperature)."""
        isotherm = self.base_isotherm
        modified = False

        if isotherm.material != self.view.material_input.lineEdit().text():
            isotherm.material = self.view.material_input.lineEdit().text()
            modified = True

        if isotherm.adsorbate != self.view.adsorbate_input.lineEdit().text():
            isotherm.adsorbate = self.view.adsorbate_input.lineEdit().text()
            modified = True

        if isotherm.temperature != self.view.temperature_input.value():
            isotherm.temperature = self.view.temperature_input.value()
            modified = True

        if modified:
            self.update()

    def handle_pressure(self, mode_to, unit_to):
        """Change isotherm pressure."""
        self.base_isotherm.pressure_mode = mode_to
        self.base_isotherm.pressure_unit = unit_to
        self.update()

    def handle_loading(self, basis_to, unit_to):
        """Change isotherm loading."""
        self.base_isotherm.loading_basis = basis_to
        self.base_isotherm.loading_unit = unit_to
        self.update()

    def handle_material(self, basis_to, unit_to):
        """Change isotherm material."""
        self.base_isotherm.material_basis = basis_to
        self.base_isotherm.material_unit = unit_to
        self.update()

    def handle_temperature(self, unit_to):
        """Change isotherm temperature."""
        self.base_isotherm.temperature_unit = unit_to
        self.update()

    def handle_isotype(self, index):
        """Change isotherm type."""
        self.iso_type = index
        self.update()

    def update(self):
        """Use model parameters."""
        if self.create_iso():
            self.output_log()
            self.plot_results()
        else:
            self.output_log()
            self.plot_clear()

    def create_iso(self):
        """Call pyGAPS to perform main calculation."""
        with log_hook:
            try:
                if self.iso_type == 0:
                    self.full_isotherm = PointIsotherm.from_isotherm(
                        isotherm=self.base_isotherm,
                        isotherm_data=self.view.point_edit.datatable_model._data,
                        pressure_key="pressure",
                        loading_key="loading",
                    )
                elif self.iso_type == 1:
                    self.full_isotherm = ModelIsotherm.from_isotherm(
                        isotherm=self.base_isotherm,
                        branch=self.view.model_edit.current_branch,
                        model=self.view.model_edit.current_model,
                    )

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Model failed! <br> {e}</font>'
                return False
            self.output += log_hook.get_logs()
            return True

    def output_log(self):
        """Output text or dialog error/warning/info."""
        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):
        """Fill in any GUI plots with results."""
        self.view.iso_graph.set_isotherms([self.full_isotherm], autorange=False)
        if self.iso_type == 0:
            self.view.iso_graph.branch = "all"
        elif self.iso_type == 1:
            self.view.iso_graph.branch = self.full_isotherm.branch
        self.view.iso_graph.draw_isotherms()

    def plot_clear(self):
        """Reset plots to default values."""
        self.view.iso_graph.full_isotherm = self.full_isotherm
        self.view.iso_graph.draw_isotherms()
