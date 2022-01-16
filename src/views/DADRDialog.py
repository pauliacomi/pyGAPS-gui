from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView

from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class DADRDialog(QW.QDialog):
    def __init__(self, ptype="DR", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ptype = ptype

        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("DADRDialog")

        layout = QW.QGridLayout(self)
        layout.setObjectName("layout")

        self.optionsBox = QW.QGroupBox(self)
        layout.addWidget(self.optionsBox, 0, 0, 1, 1)
        self.rGraphsBox = QW.QGroupBox(self)
        layout.addWidget(self.rGraphsBox, 0, 1, 2, 1)
        self.resultBox = QW.QGroupBox(self)
        layout.addWidget(self.resultBox, 1, 0, 1, 1)

        # Options box
        self.options_layout = QW.QGridLayout(self.optionsBox)
        row = 0

        ## Isotherm display
        self.isoGraph = IsoGraphView(x_range_select=True, parent=self)
        self.isoGraph.setObjectName("isoGraph")
        self.x_select = self.isoGraph.x_range_select
        self.options_layout.addWidget(self.isoGraph, row, 0, 1, 4)
        row = row + 1

        ## other options
        self.branchLabel = LabelAlignRight("Branch used:")
        self.options_layout.addWidget(self.branchLabel, row, 0, 1, 1)
        self.branchDropdown = QW.QComboBox(self)
        self.options_layout.addWidget(self.branchDropdown, row, 1, 1, 1)

        if self.ptype == "DA":
            self.options_layout.addWidget(LabelAlignRight("D-A Exponent:"), row, 2, 1, 1)
            self.DRExponent = QW.QDoubleSpinBox(self)
            self.DRExponent.setSingleStep(0.1)
            self.options_layout.addWidget(self.DRExponent, row, 3, 1, 1)

        row = row + 1

        self.auto_button = QW.QPushButton(self)
        self.options_layout.addWidget(self.auto_button, row, 0, 1, 4)

        # Results graph box
        self.rGraphsLayout = QW.QGridLayout(self.rGraphsBox)

        ## DA/DR plot
        self.rgraph = GraphView(self)
        self.rgraph.setObjectName("DADRGraph")
        self.rGraphsLayout.addWidget(self.rgraph, 0, 1, 1, 1)

        # Results box
        self.resultsLayout = QW.QGridLayout(self.resultBox)

        # description labels
        self.resultsLayout.addWidget(LabelAlignRight("Fit (R^2):"), 0, 2, 1, 1)
        self.resultsLayout.addWidget(LabelAlignRight("Micropore Volume [cm3/g]"), 1, 0, 1, 1)
        self.resultsLayout.addWidget(LabelAlignRight("Effective Potential [kJ/mol]"), 1, 2, 1, 1)
        self.resultsLayout.addWidget(LabelAlignRight("Slope:"), 2, 0, 1, 1)
        self.resultsLayout.addWidget(LabelAlignRight("Intercept:"), 2, 2, 1, 1)

        # result labels
        self.result_r = LabelResult(self)
        self.resultsLayout.addWidget(self.result_r, 0, 3, 1, 1)
        self.result_microporevol = LabelResult(self)
        self.resultsLayout.addWidget(self.result_microporevol, 1, 1, 1, 1)
        self.result_adspotential = LabelResult(self)
        self.resultsLayout.addWidget(self.result_adspotential, 1, 3, 1, 1)
        self.result_slope = LabelResult(self)
        self.resultsLayout.addWidget(self.result_slope, 2, 1, 1, 1)
        self.result_intercept = LabelResult(self)
        self.resultsLayout.addWidget(self.result_intercept, 2, 3, 1, 1)

        self.resultsLayout.addWidget(QW.QLabel("Calculation log:"), 3, 0, 1, 2)
        self.output = LabelOutput(self)
        self.resultsLayout.addWidget(self.output, 4, 0, 2, 4)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox(self)
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Close)
        layout.addWidget(self.button_box, 2, 0, 1, 2)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(1000, 800)

    def connect_signals(self):
        pass

    def translate_UI(self):
        key = "Dubinin-Radushkevich plot"
        if self.ptype == "DA":
            key = "Dubinin-Astakov plot"
        self.setWindowTitle(QW.QApplication.translate("DADRDialog", key, None, -1))
        self.optionsBox.setTitle(QW.QApplication.translate("DADRDialog", "Options", None, -1))
        self.resultBox.setTitle(QW.QApplication.translate("DADRDialog", "Results", None, -1))
        self.auto_button.setText(
            QW.QApplication.translate("DADRDialog", "Auto-determine", None, -1)
        )
