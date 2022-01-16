from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from qtpy import PYSIDE6

from src.widgets.IsoUnitWidget import IsoUnitWidget
if PYSIDE6:
    import PySide6.QtSvgWidgets as QS
else:
    from qtpy import QtSvg as QS

from src.views.IsoGraphView import IsoGraphView
from src.widgets.UtilityWidgets import (EditAlignRight, LabelAlignRight, LabelOutput, LabelResult)


class IsoModelManualDialog(QW.QDialog):

    paramWidgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("IsoModelManualDialog")

        layout = QW.QGridLayout(self)
        layout.setObjectName("layout")

        # Model selection and parameters
        self.options_layout = QW.QVBoxLayout()
        layout.addLayout(self.options_layout, 0, 0)

        modelLayout = QW.QGridLayout()
        self.options_layout.addLayout(modelLayout)

        # Model selection
        self.modelLabel = LabelAlignRight("Model:", parent=self)
        modelLayout.addWidget(self.modelLabel, 0, 0, 1, 1)
        self.modelDropdown = QW.QComboBox(self)
        modelLayout.addWidget(self.modelDropdown, 0, 1, 1, 2)

        # Adsorbate selection
        self.adsorbate_label = LabelAlignRight("Adsorbate:", parent=self)
        modelLayout.addWidget(self.adsorbate_label, 1, 0, 1, 1)
        self.adsorbate_input = QW.QComboBox(self)
        self.adsorbate_input.setInsertPolicy(QW.QComboBox.NoInsert)
        self.adsorbate_input.setEditable(True)
        modelLayout.addWidget(self.adsorbate_input, 1, 1, 1, 2)

        # Temperature selection
        self.tempLabel = LabelAlignRight("Temperature:", parent=self)
        modelLayout.addWidget(self.tempLabel, 2, 0, 1, 1)
        self.tempInput = QW.QDoubleSpinBox(self)
        self.tempInput.setDecimals(2)
        self.tempInput.setValue(77)
        modelLayout.addWidget(self.tempInput, 2, 1, 1, 1)
        self.temperatureUnit = QW.QComboBox(self)
        self.temperatureUnit.setObjectName("temperatureUnit")
        modelLayout.addWidget(self.temperatureUnit, 2, 2, 1, 1)

        # Branch selection
        self.branchLabel = LabelAlignRight("Branch:", parent=self)
        modelLayout.addWidget(self.branchLabel, 3, 0, 1, 1)
        self.branchDropdown = QW.QComboBox(self)
        modelLayout.addWidget(self.branchDropdown, 3, 1, 1, 2)

        self.unit_widget = IsoUnitWidget(self.temperatureUnit, parent=self)
        self.options_layout.addWidget(self.unit_widget)

        btnLayout = QW.QHBoxLayout()
        self.manualButton = QW.QPushButton(self)
        btnLayout.addWidget(self.manualButton)
        self.options_layout.addLayout(btnLayout)

        # Parameter box
        self.paramBox = QW.QGroupBox(self)
        self.options_layout.addWidget(self.paramBox)
        self.paramLayout = QW.QVBoxLayout(self.paramBox)
        self.modelFormulaValue = QS.QSvgWidget(self.paramBox)
        self.modelFormulaValue.setMinimumSize(10, 50)
        self.paramLayout.addWidget(self.modelFormulaValue)

        self.options_layout.addStretch()

        # Output log
        self.output_label = QW.QLabel("Output log:")
        layout.addWidget(self.output_label, 1, 0)
        self.output = LabelOutput(self)
        layout.addWidget(self.output, 2, 0)

        # Isotherm display
        self.isoGraph = IsoGraphView(self, x_range_select=True)
        self.x_select = self.isoGraph.x_range_select
        layout.addWidget(self.isoGraph, 0, 1, 3, 1)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox(self)
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Cancel)
        layout.addWidget(self.button_box, 3, 0, 1, 2)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(1000, 800)

    def connect_signals(self):
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def translate_UI(self):
        self.setWindowTitle(
            QW.QApplication.translate("IsoModelManualDialog", "Isotherm model fitting", None, -1)
        )
        self.paramBox.setTitle(
            QW.QApplication.translate("IsoModelManualDialog", "Parameters", None, -1)
        )
        self.manualButton.setText(
            QW.QApplication.translate("IsoModelManualDialog", "Use selected parameters", None, -1)
        )
