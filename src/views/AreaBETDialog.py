from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView

from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class AreaBETDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("AreaBETDialog")

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

        ## Isotherm display
        self.isoGraph = IsoGraphView(x_range_select=True, parent=self)
        self.isoGraph.setObjectName("isoGraph")
        self.x_select = self.isoGraph.x_range_select

        ## other options
        self.branchLabel = LabelAlignRight("Branch used:")
        self.branchDropdown = QW.QComboBox(self)
        self.auto_button = QW.QPushButton(self)

        ## Layout them
        self.options_layout.addWidget(self.isoGraph, 0, 0, 1, 4)
        self.options_layout.addWidget(self.branchLabel, 1, 0, 1, 1)
        self.options_layout.addWidget(self.branchDropdown, 1, 1, 1, 1)
        self.options_layout.addWidget(self.auto_button, 1, 3, 1, 1)

        # Results graph box
        self.rGraphsLayout = QW.QGridLayout(self.rGraphsBox)

        ## BET plot
        self.betGraph = GraphView(parent=self)
        self.betGraph.setObjectName("betGraph")

        ## Rouquerol plot
        self.rouqGraph = GraphView(parent=self)
        self.rouqGraph.setObjectName("rouqGraph")

        ## Layout them
        self.rGraphsLayout.addWidget(self.betGraph, 0, 0, 1, 1)
        self.rGraphsLayout.addWidget(self.rouqGraph, 1, 0, 1, 1)

        # Results box
        self.resultsLayout = QW.QGridLayout(self.resultBox)

        # description labels
        self.label_fit = LabelAlignRight("Fit (R^2):")
        self.label_area = LabelAlignRight("BET area [m2/g]:")
        self.label_c = LabelAlignRight("C constant:")
        self.label_n_mono = LabelAlignRight("Monolayer uptake [mmol/g]:")
        self.label_p_mono = LabelAlignRight("Monolayer pressure [p/p0]:")
        self.label_slope = LabelAlignRight("Slope:")
        self.label_intercept = LabelAlignRight("Intercept:")
        self.resultsLayout.addWidget(self.label_fit, 0, 1, 1, 1)
        self.resultsLayout.addWidget(self.label_area, 1, 0, 1, 1)
        self.resultsLayout.addWidget(self.label_c, 1, 2, 1, 1)
        self.resultsLayout.addWidget(self.label_n_mono, 2, 0, 1, 1)
        self.resultsLayout.addWidget(self.label_p_mono, 2, 2, 1, 1)
        self.resultsLayout.addWidget(self.label_slope, 3, 0, 1, 1)
        self.resultsLayout.addWidget(self.label_intercept, 3, 2, 1, 1)

        # result labels
        self.result_r = LabelResult(self)
        self.resultsLayout.addWidget(self.result_r, 0, 2, 1, 1)
        self.result_bet = LabelResult(self)
        self.resultsLayout.addWidget(self.result_bet, 1, 1, 1, 1)
        self.result_c = LabelResult(self)
        self.resultsLayout.addWidget(self.result_c, 1, 3, 1, 1)
        self.result_mono_n = LabelResult(self)
        self.resultsLayout.addWidget(self.result_mono_n, 2, 1, 1, 1)
        self.result_mono_p = LabelResult(self)
        self.resultsLayout.addWidget(self.result_mono_p, 2, 3, 1, 1)
        self.result_slope = LabelResult(self)
        self.resultsLayout.addWidget(self.result_slope, 3, 1, 1, 1)
        self.result_intercept = LabelResult(self)
        self.resultsLayout.addWidget(self.result_intercept, 3, 3, 1, 1)

        self.resultsLayout.addWidget(QW.QLabel("Calculation log:"), 4, 0, 1, 2)
        self.output = LabelOutput(self)
        self.resultsLayout.addWidget(self.output, 5, 0, 2, 4)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox(self)
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Close)
        layout.addWidget(self.button_box, 2, 0, 1, 2)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(1000, 700)

    def connect_signals(self):
        pass

    def translate_UI(self):
        self.setWindowTitle(
            QW.QApplication.translate("AreaBETDialog", "Calculate BET area", None, -1)
        )
        self.optionsBox.setTitle(QW.QApplication.translate("AreaBETDialog", "Options", None, -1))
        self.rGraphsBox.setTitle(
            QW.QApplication.translate("AreaBETDialog", "Output Graphs", None, -1)
        )
        self.resultBox.setTitle(QW.QApplication.translate("AreaBETDialog", "Results", None, -1))
        self.auto_button.setText(
            QW.QApplication.translate("AreaBETDialog", "Auto-determine", None, -1)
        )
