from qtpy import QtWidgets as QW
from qtpy import QtCore as QC


class IsoUnitWidget(QW.QWidget):

    unitsChanged = QC.Signal()

    def __init__(self, temp_qcombo_ref, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.isotherm = None
        self.temperatureUnit = temp_qcombo_ref
        self.setupUI()
        self.retranslateUi()
        self.connectSignals()

    def setupUI(self):

        self.unitPropLayout = QW.QHBoxLayout(self)
        self.pressureGrid = QW.QGroupBox(self)
        self.loadingGrid = QW.QGroupBox(self)
        self.materialGrid = QW.QGroupBox(self)

        self.unitPropLayout.addWidget(self.pressureGrid)
        self.unitPropLayout.addWidget(self.loadingGrid)
        self.unitPropLayout.addWidget(self.materialGrid)

        self.pressurePropLayout = QW.QVBoxLayout(self.pressureGrid)
        self.loadingPropLayout = QW.QVBoxLayout(self.loadingGrid)
        self.materialPropLayout = QW.QVBoxLayout(self.materialGrid)

        self.pressureMode = QW.QComboBox()
        self.pressureMode.setObjectName("pressureMode")
        self.pressurePropLayout.addWidget(self.pressureMode)

        self.pressureUnit = QW.QComboBox()
        self.pressureUnit.setObjectName("pressureUnit")
        self.pressurePropLayout.addWidget(self.pressureUnit)

        self.loadingBasis = QW.QComboBox()
        self.loadingBasis.setObjectName("loadingBasis")
        self.loadingPropLayout.addWidget(self.loadingBasis)

        self.loadingUnit = QW.QComboBox()
        self.loadingUnit.setObjectName("loadingUnit")
        self.loadingPropLayout.addWidget(self.loadingUnit)

        self.materialBasis = QW.QComboBox()
        self.materialBasis.setObjectName("materialBasis")
        self.materialPropLayout.addWidget(self.materialBasis)

        self.materialUnit = QW.QComboBox()
        self.materialUnit.setObjectName("materialUnit")
        self.materialPropLayout.addWidget(self.materialUnit)

    def connectSignals(self):

        self.pressureMode.currentIndexChanged.connect(self.convert_pressure)
        self.pressureUnit.currentIndexChanged.connect(self.convert_pressure)
        self.loadingBasis.currentIndexChanged.connect(self.convert_loading)
        self.loadingUnit.currentIndexChanged.connect(self.convert_loading)
        self.materialBasis.currentIndexChanged.connect(self.convert_material)
        self.materialUnit.currentIndexChanged.connect(self.convert_material)
        self.temperatureUnit.currentIndexChanged.connect(self.convert_temperature)

    def blockComboSignals(self, state):
        self.pressureMode.blockSignals(state)
        self.pressureUnit.blockSignals(state)
        self.loadingBasis.blockSignals(state)
        self.loadingUnit.blockSignals(state)
        self.materialBasis.blockSignals(state)
        self.materialUnit.blockSignals(state)
        self.materialUnit.blockSignals(state)
        self.temperatureUnit.blockSignals(state)

    def init_boxes(self, p_dict, l_dict, m_dict, t_dict):

        self.blockComboSignals(True)

        self.pressure_dict = p_dict
        self.pressureMode.addItems(list(p_dict.keys()))
        self.pressureMode.setEnabled(False)
        self.pressureUnit.setEnabled(False)

        self.loading_dict = l_dict
        self.loadingBasis.addItems(list(l_dict.keys()))
        self.loadingBasis.setEnabled(False)
        self.loadingUnit.setEnabled(False)

        self.material_dict = m_dict
        self.materialBasis.addItems(list(m_dict.keys()))
        self.materialBasis.setEnabled(False)
        self.materialUnit.setEnabled(False)

        self.t_dict = t_dict
        self.temperatureUnit.addItems(list(t_dict.keys()))
        self.temperatureUnit.setEnabled(False)

        self.blockComboSignals(False)

    def init_units(self, isotherm):

        self.isotherm = isotherm
        self.blockComboSignals(True)
        self.init_pressure(isotherm.pressure_mode, isotherm.pressure_unit)
        self.init_loading(isotherm.loading_basis, isotherm.loading_unit)
        self.init_material(isotherm.material_basis, isotherm.material_unit)
        self.init_temperature(isotherm.temperature_unit)
        self.blockComboSignals(False)

    def init_pressure(self, pressure_mode, pressure_unit):

        self.pressureMode.setEnabled(True)
        pressure_modes = list(self.pressure_dict.keys())
        self.pm_index = pressure_modes.index(pressure_mode)
        self.pressureMode.setCurrentIndex(self.pm_index)

        self.pressureUnit.clear()
        pressure_units = self.pressure_dict.get(pressure_mode, None)
        if pressure_units:
            self.pressureUnit.setEnabled(True)
            pressure_units = list(pressure_units.keys())
            self.pu_index = pressure_units.index(pressure_unit)
            self.pressureUnit.addItems(pressure_units)
            self.pressureUnit.setCurrentIndex(self.pu_index)

    def init_loading(self, loading_basis, loading_unit):

        self.loadingBasis.setEnabled(True)
        loading_bases = list(self.loading_dict.keys())
        self.lm_index = loading_bases.index(loading_basis)
        self.loadingBasis.setCurrentIndex(self.lm_index)

        self.loadingUnit.clear()
        loading_units = self.loading_dict.get(loading_basis, None)
        if loading_units:
            self.loadingUnit.setEnabled(True)
            loading_units = list(loading_units.keys())
            self.lu_index = loading_units.index(loading_unit)
            self.loadingUnit.addItems(loading_units)
            self.loadingUnit.setCurrentIndex(self.lu_index)

    def init_material(self, material_basis, material_unit):

        self.materialBasis.setEnabled(True)
        material_bases = list(self.material_dict.keys())
        self.mm_index = material_bases.index(material_basis)
        self.materialBasis.setCurrentIndex(self.mm_index)

        self.materialUnit.clear()
        material_units = self.material_dict.get(material_basis, None)
        if material_units:
            self.materialUnit.setEnabled(True)
            material_units = list(material_units.keys())
            self.mu_index = material_units.index(material_unit)
            self.materialUnit.addItems(material_units)
            self.materialUnit.setCurrentIndex(self.mu_index)

    def init_temperature(self, temperature_unit):

        self.temperatureUnit.setEnabled(True)
        temperature_units = list(self.t_dict.keys())
        self.tm_index = temperature_units.index(temperature_unit)
        self.loadingBasis.setCurrentIndex(self.lm_index)

    def clear(self):
        self.isotherm = None
        self.pressureMode.setEnabled(False)
        self.pressureUnit.setEnabled(False)
        self.loadingBasis.setEnabled(False)
        self.loadingUnit.setEnabled(False)
        self.materialBasis.setEnabled(False)
        self.materialUnit.setEnabled(False)
        self.temperatureUnit.setEnabled(False)

    def convert_pressure(self):
        if not self.isotherm:
            return

        mode_to = self.pressureMode.currentText()
        unit_to = self.pressureUnit.currentText()

        if (self.isotherm.pressure_mode != mode_to or self.isotherm.pressure_unit != unit_to):

            if self.isotherm.pressure_mode != mode_to:
                units = self.pressure_dict[mode_to]
                if units:
                    unit_to = list(units.keys())[0]

            self.isotherm.convert_pressure(mode_to=mode_to, unit_to=unit_to)

            self.unitsChanged.emit()

    def convert_loading(self):
        if not self.isotherm:
            return

        basis_to = self.loadingBasis.currentText()
        unit_to = self.loadingUnit.currentText()

        if (self.isotherm.loading_basis != basis_to or self.isotherm.loading_unit != unit_to):

            if self.isotherm.loading_basis != basis_to:
                units = self.loading_dict[basis_to]
                if units:
                    unit_to = list(units.keys())[0]

            self.isotherm.convert_loading(basis_to=basis_to, unit_to=unit_to)

            self.unitsChanged.emit()

    def convert_material(self):
        if not self.isotherm:
            return

        basis_to = self.materialBasis.currentText()
        unit_to = self.materialUnit.currentText()

        if (self.isotherm.material_basis != basis_to or self.isotherm.material_unit != unit_to):

            if self.isotherm.material_basis != basis_to:
                units = self.material_dict[basis_to]
                if units:
                    unit_to = list(units.keys())[0]

            try:
                self.isotherm.convert_material(basis_to=basis_to, unit_to=unit_to)
            except Exception as ex:
                from src.widgets.UtilityWidgets import ErrorMessageBox

                errorbox = ErrorMessageBox()
                if basis_to == "volume":
                    errorbox.setText("Could not convert material to a volume basis. Does it have a density set?")
                elif basis_to == "molar":
                    errorbox.setText("Could not convert material to a molar basis. Does it have a molar_mass set?")
                else:
                    raise Exception from ex
                errorbox.exec_()

            self.unitsChanged.emit()

    def convert_temperature(self):
        if not self.isotherm:
            return

        unit_to = self.temperatureUnit.currentText()
        self.isotherm.convert_temperature(unit_to=unit_to)

        self.unitsChanged.emit()

    def retranslateUi(self):
        self.pressureGrid.setTitle(QW.QApplication.translate("IsoUnitWidget", "pressure", None, -1))
        self.loadingGrid.setTitle(QW.QApplication.translate("IsoUnitWidget", "loading", None, -1))
        self.materialGrid.setTitle(QW.QApplication.translate("IsoUnitWidget", "material", None, -1))
