from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygaps.core.pointisotherm import PointIsotherm


class IsoUnitWidget(QW.QWidget):

    pressure_changed = QC.Signal(str, str)
    loading_changed = QC.Signal(str, str)
    material_changed = QC.Signal(str, str)
    temperature_changed = QC.Signal(str)

    units_active: bool = False

    def __init__(self, temp_combo_ref, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.temperature_unit = temp_combo_ref
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        """Creates and sets-up static UI elements"""

        _layout = QW.QHBoxLayout(self)
        self.pressure_box = QW.QGroupBox()
        self.loading_box = QW.QGroupBox()
        self.material_box = QW.QGroupBox()

        _layout.addWidget(self.pressure_box)
        _layout.addWidget(self.loading_box)
        _layout.addWidget(self.material_box)

        self.pressure_box_layout = QW.QVBoxLayout(self.pressure_box)
        self.loading_box_layout = QW.QVBoxLayout(self.loading_box)
        self.material_box_layout = QW.QVBoxLayout(self.material_box)

        self.pressure_mode = QW.QComboBox()
        self.pressure_mode.setObjectName("pressure_mode")
        self.pressure_box_layout.addWidget(self.pressure_mode)

        self.pressure_unit = QW.QComboBox()
        self.pressure_unit.setObjectName("pressure_unit")
        self.pressure_box_layout.addWidget(self.pressure_unit)

        self.loading_basis = QW.QComboBox()
        self.loading_basis.setObjectName("loading_basis")
        self.loading_box_layout.addWidget(self.loading_basis)

        self.loading_unit = QW.QComboBox()
        self.loading_unit.setObjectName("loading_unit")
        self.loading_box_layout.addWidget(self.loading_unit)

        self.material_basis = QW.QComboBox()
        self.material_basis.setObjectName("material_basis")
        self.material_box_layout.addWidget(self.material_basis)

        self.material_unit = QW.QComboBox()
        self.material_unit.setObjectName("material_unit")
        self.material_box_layout.addWidget(self.material_unit)

    def connect_signals(self):
        """Connect permanent signals."""

        self.pressure_mode.currentIndexChanged.connect(self.handle_pressure_change)
        self.pressure_unit.currentIndexChanged.connect(self.emit_pressure)
        self.loading_basis.currentIndexChanged.connect(self.handle_loading_change)
        self.loading_unit.currentIndexChanged.connect(self.emit_loading)
        self.material_basis.currentIndexChanged.connect(self.handle_material_change)
        self.material_unit.currentIndexChanged.connect(self.emit_material)
        self.temperature_unit.currentIndexChanged.connect(self.emit_temperature)

    def block_signals(self, state):
        self.pressure_mode.blockSignals(state)
        self.pressure_unit.blockSignals(state)
        self.loading_basis.blockSignals(state)
        self.loading_unit.blockSignals(state)
        self.material_basis.blockSignals(state)
        self.material_unit.blockSignals(state)
        self.material_unit.blockSignals(state)
        self.temperature_unit.blockSignals(state)

    def clear(self):
        self.units_active = None
        self.pressure_mode.setEnabled(False)
        self.pressure_unit.setEnabled(False)
        self.loading_basis.setEnabled(False)
        self.loading_unit.setEnabled(False)
        self.material_basis.setEnabled(False)
        self.material_unit.setEnabled(False)
        self.temperature_unit.setEnabled(False)

    def init_boxes(self, p_dict, l_dict, m_dict, t_dict):

        self.block_signals(True)

        self.pressure_dict = p_dict
        self.pressure_mode.addItems(list(p_dict.keys()))
        self.pressure_mode.setEnabled(False)
        self.pressure_unit.setEnabled(False)

        self.loading_dict = l_dict
        self.loading_basis.addItems(list(l_dict.keys()))
        self.loading_basis.setEnabled(False)
        self.loading_unit.setEnabled(False)

        self.material_dict = m_dict
        self.material_basis.addItems(list(m_dict.keys()))
        self.material_basis.setEnabled(False)
        self.material_unit.setEnabled(False)

        self.temperature_dict = t_dict
        self.temperature_unit.addItems(list(t_dict.keys()))
        self.temperature_unit.setEnabled(False)

        self.block_signals(False)

    def init_units(self, isotherm):

        self.block_signals(True)
        self.units_active = isinstance(isotherm, PointIsotherm)
        self.init_pressure(isotherm.pressure_mode, isotherm.pressure_unit)
        self.init_loading(isotherm.loading_basis, isotherm.loading_unit)
        self.init_material(isotherm.material_basis, isotherm.material_unit)
        self.init_temperature(isotherm.temperature_unit)
        self.block_signals(False)

    def init_pressure(self, pressure_mode, pressure_unit):

        self.pressure_mode.setEnabled(self.units_active)
        self.pressure_mode.setCurrentText(pressure_mode)

        self.init_pressure_unit(pressure_mode, pressure_unit)

    def init_pressure_unit(self, pressure_mode, pressure_unit=None):
        self.pressure_unit.clear()
        self.pressure_unit.setEnabled(False)
        pressure_units = self.pressure_dict.get(pressure_mode, None)
        if not pressure_units:
            return
        self.pressure_unit.setEnabled(self.units_active)
        pressure_units = list(pressure_units.keys())
        if not pressure_unit:
            pressure_unit = pressure_units[0]
        self.pressure_unit.addItems(pressure_units)
        self.pressure_unit.setCurrentText(pressure_unit)

    def init_loading(self, loading_basis, loading_unit):

        self.loading_basis.setEnabled(self.units_active)
        self.loading_basis.setCurrentText(loading_basis)

        self.init_loading_unit(loading_basis, loading_unit)

    def init_loading_unit(self, loading_basis, loading_unit=None):
        self.loading_unit.clear()
        self.loading_unit.setEnabled(False)
        loading_units = self.loading_dict.get(loading_basis, None)
        if not loading_units:
            return
        self.loading_unit.setEnabled(self.units_active)
        loading_units = list(loading_units.keys())
        self.loading_unit.addItems(loading_units)
        if not loading_unit:
            loading_unit = loading_units[0]
        self.loading_unit.setCurrentText(loading_unit)

    def init_material(self, material_basis, material_unit):

        self.material_basis.setEnabled(self.units_active)
        self.material_basis.setCurrentText(material_basis)

        self.material_unit.blockSignals(True)
        self.init_material_unit(material_basis, material_unit)
        self.material_unit.blockSignals(False)

    def init_material_unit(self, material_basis, material_unit=None):
        self.material_unit.clear()
        self.material_unit.setEnabled(False)
        material_units = self.material_dict.get(material_basis, None)
        if not material_units:
            return
        self.material_unit.setEnabled(self.units_active)
        material_units = list(material_units.keys())
        self.material_unit.addItems(material_units)
        if not material_unit:
            material_unit = material_units[0]
        self.material_unit.setCurrentText(material_unit)

    def init_temperature(self, temperature_unit):
        self.temperature_unit.setEnabled(True)
        self.temperature_unit.setCurrentText(temperature_unit)

    def handle_pressure_change(self):
        pressure_mode = self.pressure_mode.currentText()
        self.loading_unit.blockSignals(True)
        self.init_pressure_unit(pressure_mode, None)
        self.loading_unit.blockSignals(False)
        self.emit_pressure()

    def emit_pressure(self):
        mode_to = self.pressure_mode.currentText()
        unit_to = self.pressure_unit.currentText()
        self.pressure_changed.emit(mode_to, unit_to)

    def handle_loading_change(self):
        loading_basis = self.loading_basis.currentText()
        self.loading_unit.blockSignals(True)
        self.init_loading_unit(loading_basis, None)
        self.loading_unit.blockSignals(False)
        self.emit_loading()

    def emit_loading(self):
        basis_to = self.loading_basis.currentText()
        unit_to = self.loading_unit.currentText()
        self.loading_changed.emit(basis_to, unit_to)

    def handle_material_change(self):
        material_basis = self.material_basis.currentText()
        self.material_unit.blockSignals(True)
        self.init_material_unit(material_basis, None)
        self.material_unit.blockSignals(False)
        self.emit_material()

    def emit_material(self):
        basis_to = self.material_basis.currentText()
        unit_to = self.material_unit.currentText()
        self.material_changed.emit(basis_to, unit_to)

    def emit_temperature(self):
        unit_to = self.temperature_unit.currentText()
        self.temperature_changed.emit(unit_to)

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.pressure_box.setTitle(QW.QApplication.translate("IsoUnitWidget", "pressure units", None, -1))
        self.loading_box.setTitle(QW.QApplication.translate("IsoUnitWidget", "loading units", None, -1))
        self.material_box.setTitle(QW.QApplication.translate("IsoUnitWidget", "material units", None, -1))
        # yapf: enable
