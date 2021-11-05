from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView

from src.widgets.RangeSlider import QHSpinBoxRangeSlider
from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class IsostericDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()
        self.retranslateUi()
        self.connectSignals()

    def setupUi(self):
        self.setObjectName("IsostericDialog")
        self.resize(900, 600)

        layout = QW.QGridLayout(self)
        layout.setObjectName("layout")

        # Iso graph and slider
        isoLayout = QW.QVBoxLayout()
        layout.addLayout(isoLayout, 0, 0, 2, 1)

        self.isoGraph = IsoGraphView(self)
        self.isoGraph.setObjectName("graph")
        isoLayout.addWidget(self.isoGraph)

        self.pSlider = QHSpinBoxRangeSlider(parent=self, dec_pnts=3, slider_range=[0, 1, 0.01], values=[0, 1])
        self.pSlider.setMaximumHeight(50)
        self.pSlider.setEmitWhileMoving(False)
        isoLayout.addWidget(self.pSlider)

        # Options/results box
        self.optionsBox = QW.QGroupBox(self)
        layout.addWidget(self.optionsBox, 0, 1, 1, 1)

        self.optionsLayout = QW.QGridLayout(self.optionsBox)

        # Branch used
        self.branchLabel = LabelAlignRight("Branch used:")
        self.optionsLayout.addWidget(self.branchLabel, 0, 0, 1, 1)
        self.branchDropdown = QW.QComboBox(self)
        self.optionsLayout.addWidget(self.branchDropdown, 0, 1, 1, 1)

        # Autodetermine
        self.autoButton = QW.QPushButton(self)
        self.optionsLayout.addWidget(self.autoButton, 3, 0, 1, 2)

        # Enthalpy graph
        self.resGraph = GraphView(self)
        self.resGraph.setObjectName("resGraph")
        layout.addWidget(self.resGraph, 1, 1, 1, 1)

        # Bottom buttons
        self.buttonBox = QW.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QC.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QW.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        layout.addWidget(self.buttonBox, 2, 0, 1, 1)

    def connectSignals(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        self.setWindowTitle(QW.QApplication.translate("IsostericDialog", "Isosteric Enthalpy", None, -1))
        self.optionsBox.setTitle(QW.QApplication.translate("IsostericDialog", "Options", None, -1))
        self.autoButton.setText(QW.QApplication.translate("IsostericDialog", "Calculate", None, -1))
