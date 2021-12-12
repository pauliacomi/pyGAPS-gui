from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView

from src.widgets.RangeSlider import QHSpinBoxRangeSlider
from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class AreaLangDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()
        self.retranslateUi()
        self.connectSignals()

    def setupUi(self):
        self.setObjectName("AreaLangDialog")
        self.resize(1000, 800)

        layout = QW.QGridLayout(self)
        layout.setObjectName("layout")

        # Isotherm display
        self.isoGraph = IsoGraphView(selector=True, parent=self)
        self.isoGraph.setObjectName("isoGraph")
        layout.addWidget(self.isoGraph, 0, 0, 1, 1)

        # Langmuir plot
        self.langGraph = GraphView(parent=self)
        self.langGraph.setObjectName("langGraph")
        layout.addWidget(self.langGraph, 0, 1, 1, 1)

        # Options/results box
        self.optionsBox = QW.QGroupBox(self)
        layout.addWidget(self.optionsBox, 1, 0, 1, 1)

        self.optionsLayout = QW.QGridLayout(self.optionsBox)
        self.pSlider = QHSpinBoxRangeSlider(
            parent=self, dec_pnts=3, slider_range=[0, 1, 0.01], values=[0, 1]
        )
        self.pSlider.setMaximumHeight(50)
        self.pSlider.setEmitWhileMoving(False)
        self.optionsLayout.addWidget(self.pSlider, 0, 0, 1, 4)

        self.optionsLayout.addWidget(QW.QLabel("Fit (R):"), 1, 0, 1, 1)
        self.result_r = LabelResult(self)
        self.optionsLayout.addWidget(self.result_r, 1, 1, 1, 1)
        self.auto_button = QW.QPushButton(self)
        self.optionsLayout.addWidget(self.auto_button, 1, 3, 1, 1)

        # description labels
        self.optionsLayout.addWidget(QW.QLabel("Calculated results:"), 2, 0, 1, 2)
        self.optionsLayout.addWidget(LabelAlignRight("Langmuir area:"), 3, 0, 1, 1)
        self.optionsLayout.addWidget(LabelAlignRight("K constant:"), 3, 2, 1, 1)
        self.optionsLayout.addWidget(LabelAlignRight("Monolayer uptake:"), 4, 0, 1, 1)
        self.optionsLayout.addWidget(LabelAlignRight("Monolayer pressure:"), 4, 2, 1, 1)
        self.optionsLayout.addWidget(LabelAlignRight("Slope:"), 5, 0, 1, 1)
        self.optionsLayout.addWidget(LabelAlignRight("Intercept:"), 5, 2, 1, 1)

        # result labels
        self.result_lang = LabelResult(self)
        self.optionsLayout.addWidget(self.result_lang, 3, 1, 1, 1)
        self.result_k = LabelResult(self)
        self.optionsLayout.addWidget(self.result_k, 3, 3, 1, 1)
        self.result_mono_n = LabelResult(self)
        self.optionsLayout.addWidget(self.result_mono_n, 4, 1, 1, 1)
        self.result_mono_p = LabelResult(self)
        self.optionsLayout.addWidget(self.result_mono_p, 4, 3, 1, 1)
        self.result_slope = LabelResult(self)
        self.optionsLayout.addWidget(self.result_slope, 5, 1, 1, 1)
        self.result_intercept = LabelResult(self)
        self.optionsLayout.addWidget(self.result_intercept, 5, 3, 1, 1)

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
            QW.QApplication.translate("AreaLangDialog", "Calculate Langmuir area", None, -1)
        )
        self.optionsBox.setTitle(QW.QApplication.translate("AreaLangDialog", "Options", None, -1))
        self.auto_button.setText(
            QW.QApplication.translate("AreaLangDialog", "Auto-determine", None, -1)
        )
