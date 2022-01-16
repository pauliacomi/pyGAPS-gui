from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView

from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class IsostericDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("IsostericDialog")

        layout = QW.QGridLayout(self)
        layout.setObjectName("layout")

        # Iso graph and slider
        isoLayout = QW.QVBoxLayout()
        layout.addLayout(isoLayout, 0, 0, 2, 1)

        self.isoGraph = IsoGraphView(x_range_select=True, parent=self)
        self.isoGraph.setObjectName("isoGraph")
        self.x_select = self.isoGraph.x_range_select
        isoLayout.addWidget(self.isoGraph)

        # Options/results box
        self.optionsBox = QW.QGroupBox(self)
        layout.addWidget(self.optionsBox, 0, 1, 1, 1)

        self.options_layout = QW.QGridLayout(self.optionsBox)

        # Branch used
        self.branchLabel = LabelAlignRight("Branch used:")
        self.options_layout.addWidget(self.branchLabel, 0, 0, 1, 1)
        self.branchDropdown = QW.QComboBox(self)
        self.options_layout.addWidget(self.branchDropdown, 0, 1, 1, 1)

        # Autodetermine
        self.autoButton = QW.QPushButton(self)
        self.options_layout.addWidget(self.autoButton, 3, 0, 1, 2)

        # Enthalpy graph
        self.res_graph = GraphView(self)
        layout.addWidget(self.res_graph, 1, 1, 1, 1)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox(self)
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Close)
        layout.addWidget(self.button_box, 2, 0, 1, 1)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(800, 900)

    def connect_signals(self):
        pass

    def translate_UI(self):
        self.setWindowTitle(
            QW.QApplication.translate("IsostericDialog", "Isosteric Enthalpy", None, -1)
        )
        self.optionsBox.setTitle(QW.QApplication.translate("IsostericDialog", "Options", None, -1))
        self.autoButton.setText(QW.QApplication.translate("IsostericDialog", "Calculate", None, -1))
