from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtSvg as QS

from src.views.IsoModelGraphView import IsoModelGraphView
from src.widgets.SpinBoxSlider import QHSpinBoxSlider
from src.widgets.UtilityWidgets import (EditAlignRight, LabelAlignRight, LabelOutput, LabelResult)


class IsoModelByDialog(QW.QDialog):

    paramWidgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()
        self.retranslateUi()
        self.connectSignals()

    def setupUi(self):
        self.setObjectName("IsoModelByDialog")
        self.resize(1000, 800)

        layout = QW.QGridLayout(self)
        layout.setObjectName("layout")

        # Model selection and parameters
        self.optionsLayout = QW.QVBoxLayout()
        layout.addLayout(self.optionsLayout, 0, 0)

        modelLayout = QW.QFormLayout()
        self.optionsLayout.addLayout(modelLayout)

        # Model selection
        self.modelLabel = LabelAlignRight("Model:", parent=self)
        self.modelDropdown = QW.QComboBox(self)
        modelLayout.addRow(self.modelLabel, self.modelDropdown)

        # Branch selection
        self.branchLabel = LabelAlignRight("Branch:", parent=self)
        self.branchDropdown = QW.QComboBox(self)
        modelLayout.addRow(self.branchLabel, self.branchDropdown)

        btnLayout = QW.QHBoxLayout()
        self.autoButton = QW.QPushButton(self)
        btnLayout.addWidget(self.autoButton)
        self.manualButton = QW.QPushButton(self)
        btnLayout.addWidget(self.manualButton)
        self.optionsLayout.addLayout(btnLayout)

        # Parameter box
        self.paramBox = QW.QGroupBox(self)
        self.optionsLayout.addWidget(self.paramBox)
        self.paramLayout = QW.QVBoxLayout(self.paramBox)
        self.modelFormulaValue = QS.QSvgWidget(self.paramBox)
        self.modelFormulaValue.setMinimumSize(10, 50)
        self.paramLayout.addWidget(self.modelFormulaValue)
        self.setupModelParams()

        self.optionsLayout.addStretch()

        # Output log
        self.outputLabel = QW.QLabel("Output log:")
        layout.addWidget(self.outputLabel, 1, 0)
        self.output = LabelOutput(self)
        layout.addWidget(self.output, 2, 0)

        # Isotherm display
        self.isoGraph = IsoModelGraphView(self)
        self.isoGraph.setObjectName("isoGraph")
        layout.addWidget(self.isoGraph, 0, 1, 3, 1)

        # Bottom buttons
        self.buttonBox = QW.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QC.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        layout.addWidget(self.buttonBox, 3, 0, 1, 2)

    def connectSignals(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def setupModelParams(self, params=None):

        if not params:
            return

        for param in self.paramWidgets:
            self.paramWidgets[param].deleteLater()

        self.paramWidgets = {}

        for param in params:

            widget = QHSpinBoxSlider(parent=self.paramBox)
            widget.setText(param)
            self.paramLayout.addWidget(widget)
            self.paramWidgets[param] = widget

    def retranslateUi(self):
        self.setWindowTitle(QW.QApplication.translate("IsoModelByDialog", "Isotherm model fitting", None, -1))
        self.paramBox.setTitle(QW.QApplication.translate("IsoModelByDialog", "Parameters", None, -1))
        self.autoButton.setText(QW.QApplication.translate("IsoModelByDialog", "Autofit", None, -1))
        self.manualButton.setText(QW.QApplication.translate("IsoModelByDialog", "Use parameters", None, -1))
