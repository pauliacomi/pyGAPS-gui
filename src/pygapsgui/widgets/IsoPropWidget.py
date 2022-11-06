from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.widgets.UtilityWidgets import LabelAlignRight


class IsoPropWidget(QW.QWidget):
    """Selects isotherm essential properties (material, adsorbate, temperature)."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Material selection
        self.m_label = LabelAlignRight()
        self.m_label.setObjectName("material_label")
        self.m_input = QW.QComboBox()
        self.m_input.setInsertPolicy(QW.QComboBox.NoInsert)
        self.m_input.setObjectName("material_input")
        self.m_input.setEditable(True)
        self.m_button = QW.QPushButton()
        self.m_button.setObjectName("material_details")

        # Adsorbate selection
        self.a_label = LabelAlignRight()
        self.a_label.setObjectName("adsorbate_label")
        self.a_input = QW.QComboBox()
        self.a_input.setInsertPolicy(QW.QComboBox.NoInsert)
        self.a_input.setObjectName("adsorbate_input")
        self.a_input.setEditable(True)
        self.a_button = QW.QPushButton()
        self.a_button.setObjectName("adsorbate_details")

        # Temperature selection
        self.t_label = LabelAlignRight()
        self.t_label.setObjectName("temperature_label")
        self.t_input = QW.QDoubleSpinBox()
        self.t_input.setMinimum(-999)
        self.t_input.setMaximum(9999)
        self.t_input.setObjectName("temperature_input")
        self.t_unit = QW.QComboBox()
        self.t_unit.setObjectName("temperature_unit")

        _layout = QW.QGridLayout(self)
        _layout.addWidget(self.m_label, 0, 0, 1, 1)
        _layout.addWidget(self.m_input, 0, 1, 1, 1)
        _layout.addWidget(self.m_button, 0, 2, 1, 1)

        _layout.addWidget(self.a_label, 1, 0, 1, 1)
        _layout.addWidget(self.a_input, 1, 1, 1, 1)
        _layout.addWidget(self.a_button, 1, 2, 1, 1)

        _layout.addWidget(self.t_label, 2, 0, 1, 1)
        _layout.addWidget(self.t_input, 2, 1, 1, 1)
        _layout.addWidget(self.t_unit, 2, 2, 1, 1)

        self.translate_UI()

    def translate_UI(self):
        """Set UI text."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.m_label.setText(QW.QApplication.translate("MainWindow", "Material", None, -1))
        self.m_button.setText(QW.QApplication.translate("MainWindow", "Details", None, -1))
        self.a_label.setText(QW.QApplication.translate("MainWindow", "Adsorbate", None, -1))
        self.a_button.setText(QW.QApplication.translate("MainWindow", "Details", None, -1))
        self.t_label.setText(QW.QApplication.translate("MainWindow", "Temperature", None, -1))
        # yapf: enable
