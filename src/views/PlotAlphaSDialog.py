from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView

from src.widgets.RangeSlider import QHSpinBoxRangeSlider
from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class PlotAlphaSDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()
        self.retranslateUi()
        self.connectSignals()

    def setupUi(self):
        self.setObjectName("PlotAlphaSDialog")
        self.resize(500, 700)

        layout = QW.QVBoxLayout(self)
        layout.setObjectName("layout")

        # T plot
        self.tGraph = GraphView(self)
        self.tGraph.setObjectName("tGraph")
        layout.addWidget(self.tGraph)

        # Options/results box
        self.optionsBox = QW.QGroupBox(self)
        layout.addWidget(self.optionsBox)

        self.optionsLayout = QW.QGridLayout(self.optionsBox)

        self.optionsLayout.addWidget(LabelAlignRight("Thickness function:"), 0, 0, 1, 1)
        self.thicknessDropdown = QW.QComboBox(self)
        self.optionsLayout.addWidget(self.thicknessDropdown, 0, 1, 1, 2)

        self.auto_button = QW.QPushButton(self)
        self.optionsLayout.addWidget(self.auto_button, 0, 3, 1, 1)

        self.pSlider = QHSpinBoxRangeSlider(parent=self, dec_pnts=3, slider_range=[0, 1, 0.01], values=[0, 1])
        self.pSlider.setMaximumHeight(50)
        self.pSlider.setEmitWhileMoving(False)
        self.optionsLayout.addWidget(self.pSlider, 1, 0, 1, 4)

        self.resultsTable = QW.QTableWidget(0, 5, self)
        self.resultsTable.setHorizontalHeaderLabels(("V", "A", "R^2", "Slope", "Intercept"))
        self.resultsTable.horizontalHeader().setSectionResizeMode(QW.QHeaderView.Stretch)
        self.optionsLayout.addWidget(self.resultsTable, 2, 0, 1, 4)

        self.optionsLayout.addWidget(QW.QLabel("Calculation log:"), 3, 0, 1, 2)
        self.output = LabelOutput(self)
        self.optionsLayout.addWidget(self.output, 4, 0, 1, 4)

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
        self.setWindowTitle(QW.QApplication.translate("PlotAlphaSDialog", "Use the alpha-s method", None, -1))
        self.optionsBox.setTitle(QW.QApplication.translate("PlotAlphaSDialog", "Options", None, -1))
        self.auto_button.setText(QW.QApplication.translate("PlotAlphaSDialog", "Auto-determine", None, -1))
