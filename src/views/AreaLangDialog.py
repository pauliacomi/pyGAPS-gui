from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView

from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class AreaLangDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("AreaLangDialog")

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

        ## Langmuir plot
        self.langGraph = GraphView(parent=self)
        self.langGraph.setObjectName("langGraph")

        ## Layout them
        self.rGraphsLayout.addWidget(self.langGraph, 0, 1, 1, 1)

        # Results box
        self.resultsLayout = QW.QGridLayout(self.resultBox)

        # description labels
        self.resultsLayout.addWidget(LabelAlignRight("Fit (R^2):"), 0, 1, 1, 1)
        self.resultsLayout.addWidget(LabelAlignRight("Langmuir area [m2/g]:"), 1, 0, 1, 1)
        self.resultsLayout.addWidget(LabelAlignRight("K constant:"), 1, 2, 1, 1)
        self.resultsLayout.addWidget(LabelAlignRight("Monolayer uptake [mmol/g]:"), 2, 0, 1, 1)
        self.resultsLayout.addWidget(LabelAlignRight("Monolayer pressure [p/p0]:"), 2, 2, 1, 1)
        self.resultsLayout.addWidget(LabelAlignRight("Slope:"), 3, 0, 1, 1)
        self.resultsLayout.addWidget(LabelAlignRight("Intercept:"), 3, 2, 1, 1)

        # result labels
        self.result_r = LabelResult(self)
        self.resultsLayout.addWidget(self.result_r, 0, 2, 1, 1)
        self.result_lang = LabelResult(self)
        self.resultsLayout.addWidget(self.result_lang, 1, 1, 1, 1)
        self.result_k = LabelResult(self)
        self.resultsLayout.addWidget(self.result_k, 1, 3, 1, 1)
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
            QW.QApplication.translate("AreaLangDialog", "Calculate Langmuir area", None, -1)
        )
        self.optionsBox.setTitle(QW.QApplication.translate("AreaLangDialog", "Options", None, -1))
        self.rGraphsBox.setTitle(
            QW.QApplication.translate("AreaLangDialog", "Output Graphs", None, -1)
        )
        self.resultBox.setTitle(QW.QApplication.translate("AreaLangDialog", "Results", None, -1))
        self.auto_button.setText(
            QW.QApplication.translate("AreaLangDialog", "Auto-determine", None, -1)
        )
