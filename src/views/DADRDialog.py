from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView

from src.widgets.RangeSlider import QHSpinBoxRangeSlider
from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class DADRDialog(QW.QDialog):
    def __init__(self, ptype="DR", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ptype = ptype

        self.setupUi()
        self.retranslateUi()
        self.connectSignals()

    def setupUi(self):
        self.setObjectName("DADRDialog")
        self.resize(500, 700)

        layout = QW.QVBoxLayout(self)
        layout.setObjectName("layout")

        # DA/DR plot
        self.graph = GraphView(self)
        self.graph.setObjectName("DADRGraph")
        layout.addWidget(self.graph)

        # Options/results box
        self.optionsBox = QW.QGroupBox(self)
        layout.addWidget(self.optionsBox)

        self.optionsLayout = QW.QGridLayout(self.optionsBox)

        row = 0
        if self.ptype == "DA":
            self.optionsLayout.addWidget(LabelAlignRight("D-A Exponent:"), row, 1, 1, 1)
            self.DRExponent = QW.QDoubleSpinBox(self)
            self.DRExponent.setSingleStep(0.1)
            self.optionsLayout.addWidget(self.DRExponent, row, 2, 1, 1)
            row = row + 1

        self.auto_button = QW.QPushButton(self)
        self.optionsLayout.addWidget(self.auto_button, row, 0, 1, 4)
        row = row + 1

        self.pSlider = QHSpinBoxRangeSlider(parent=self, dec_pnts=3, slider_range=[0, 1, 0.01], values=[0, 1])
        self.pSlider.setMaximumHeight(50)
        self.pSlider.setEmitWhileMoving(False)
        self.optionsLayout.addWidget(self.pSlider, row, 0, 1, 4)
        row = row + 1

        self.optionsLayout.addWidget(LabelAlignRight("Micropore Volume"), row, 0, 1, 2)
        self.result_microporevol = LabelResult(self)
        self.optionsLayout.addWidget(self.result_microporevol, row, 2, 1, 2)
        row = row + 1

        self.optionsLayout.addWidget(LabelAlignRight("Effective Potential"), row, 0, 1, 2)
        self.result_adspotential = LabelResult(self)
        self.optionsLayout.addWidget(self.result_adspotential, row, 2, 1, 2)
        row = row + 1

        self.optionsLayout.addWidget(QW.QLabel("Calculation log:"), row, 0, 1, 2)
        row = row + 1
        self.output = LabelOutput(self)
        self.optionsLayout.addWidget(self.output, row, 0, 1, 4)

        # Bottom buttons
        self.buttonBox = QW.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QC.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QW.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        layout.addWidget(self.buttonBox)

    def connectSignals(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        key = "Dubinin-Radushkevich plot"
        if self.ptype == "DA":
            key = "Dubinin-Astakov plot"
        self.setWindowTitle(QW.QApplication.translate("DADRDialog", key, None, -1))
        self.optionsBox.setTitle(QW.QApplication.translate("DADRDialog", "Options", None, -1))
        self.auto_button.setText(QW.QApplication.translate("DADRDialog", "Auto-determine", None, -1))
