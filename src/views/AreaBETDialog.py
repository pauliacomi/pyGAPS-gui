from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView

from src.widgets.RangeSlider import QHSpinBoxRangeSlider
from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class AreaBETDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()
        self.retranslateUi()
        self.connectSignals()

    def setupUi(self):
        self.setObjectName("AreaBETDialog")
        self.resize(1000, 800)

        layout = QW.QGridLayout(self)
        layout.setObjectName("layout")

        # Isotherm display
        self.isoGraph = IsoGraphView(selector=True, parent=self)
        self.isoGraph.setObjectName("isoGraph")
        self.pSlider = self.isoGraph.selector.slider
        layout.addWidget(self.isoGraph, 0, 0, 1, 1)

        # BET plot
        self.betGraph = GraphView(parent=self)
        self.betGraph.setObjectName("betGraph")
        layout.addWidget(self.betGraph, 0, 1, 1, 1)

        # Rouquerol plot
        self.rouqGraph = GraphView(parent=self)
        self.rouqGraph.setObjectName("rouqGraph")
        layout.addWidget(self.rouqGraph, 1, 1, 1, 1)

        # Options/results box
        self.optionsBox = QW.QGroupBox(self)
        layout.addWidget(self.optionsBox, 1, 0, 1, 1)

        self.optionsLayout = QW.QGridLayout(self.optionsBox)

        self.branchLabel = LabelAlignRight("Branch used:")
        self.optionsLayout.addWidget(self.branchLabel, 0, 0, 1, 1)
        self.branchDropdown = QW.QComboBox(self)
        self.branchDropdown.addItems(["ads", "des"]),
        self.optionsLayout.addWidget(self.branchDropdown, 0, 1, 1, 1)

        self.optionsLayout.addWidget(QW.QLabel("Fit (R):"), 1, 0, 1, 1)
        self.result_r = LabelResult(self)
        self.optionsLayout.addWidget(self.result_r, 1, 1, 1, 1)
        self.auto_button = QW.QPushButton(self)
        self.optionsLayout.addWidget(self.auto_button, 1, 3, 1, 1)

        # description labels
        self.optionsLayout.addWidget(QW.QLabel("Calculated results:"), 2, 0, 1, 2)
        self.optionsLayout.addWidget(LabelAlignRight("BET area:"), 3, 0, 1, 1)
        self.optionsLayout.addWidget(LabelAlignRight("C constant:"), 3, 2, 1, 1)
        self.optionsLayout.addWidget(LabelAlignRight("Monolayer uptake:"), 4, 0, 1, 1)
        self.optionsLayout.addWidget(LabelAlignRight("Monolayer pressure:"), 4, 2, 1, 1)
        self.optionsLayout.addWidget(LabelAlignRight("Slope:"), 5, 0, 1, 1)
        self.optionsLayout.addWidget(LabelAlignRight("Intercept:"), 5, 2, 1, 1)

        # result labels
        self.result_bet = LabelResult(self)
        self.optionsLayout.addWidget(self.result_bet, 2, 1, 1, 1)
        self.result_c = LabelResult(self)
        self.optionsLayout.addWidget(self.result_c, 2, 3, 1, 1)
        self.result_mono_n = LabelResult(self)
        self.optionsLayout.addWidget(self.result_mono_n, 3, 1, 1, 1)
        self.result_mono_p = LabelResult(self)
        self.optionsLayout.addWidget(self.result_mono_p, 3, 3, 1, 1)
        self.result_slope = LabelResult(self)
        self.optionsLayout.addWidget(self.result_slope, 4, 1, 1, 1)
        self.result_intercept = LabelResult(self)
        self.optionsLayout.addWidget(self.result_intercept, 4, 3, 1, 1)

        self.optionsLayout.addWidget(QW.QLabel("Calculation log:"), 6, 0, 1, 2)
        self.output = LabelOutput(self)
        self.optionsLayout.addWidget(self.output, 7, 0, 2, 4)

        # Bottom buttons
        self.buttonBox = QW.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QC.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QW.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        layout.addWidget(self.buttonBox, 8, 0, 1, 2)

    def connectSignals(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        self.setWindowTitle(
            QW.QApplication.translate("AreaBETDialog", "Calculate BET area", None, -1)
        )
        self.optionsBox.setTitle(QW.QApplication.translate("AreaBETDialog", "Options", None, -1))
        self.auto_button.setText(
            QW.QApplication.translate("AreaBETDialog", "Auto-determine", None, -1)
        )
