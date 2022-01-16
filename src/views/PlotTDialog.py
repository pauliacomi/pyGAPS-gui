from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView

from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class PlotTDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("PlotTDialog")

        layout = QW.QVBoxLayout(self)
        layout.setObjectName("layout")

        self.optionsBox = QW.QGroupBox(self)
        layout.addWidget(self.optionsBox)
        self.resultBox = QW.QGroupBox(self)
        layout.addWidget(self.resultBox)

        # Options box
        self.options_layout = QW.QGridLayout(self.optionsBox)

        ## Plot display
        self.tGraph = GraphView(self, x_range_select=True)
        self.tGraph.setObjectName("tGraph")
        self.x_select = self.tGraph.x_range_select
        self.options_layout.addWidget(self.tGraph, 0, 0, 1, 4)

        self.options_layout.addWidget(LabelAlignRight("Thickness function:"), 1, 0, 1, 1)
        self.thicknessDropdown = QW.QComboBox(self)
        self.options_layout.addWidget(self.thicknessDropdown, 1, 1, 1, 2)

        self.options_layout.addWidget(LabelAlignRight("Isotherm branch:"), 2, 0, 1, 1)
        self.branchDropdown = QW.QComboBox(self)
        self.options_layout.addWidget(self.branchDropdown, 2, 1, 1, 2)

        self.auto_button = QW.QPushButton(self)
        self.options_layout.addWidget(self.auto_button, 2, 3, 1, 1)

        # Results box
        self.resultsLayout = QW.QGridLayout(self.resultBox)

        self.resultsTable = QW.QTableWidget(0, 5, self)
        self.resultsTable.setHorizontalHeaderLabels(
            ("V [cm3/g]", "A [m2/g]", "R^2", "Slope", "Intercept")
        )
        self.resultsTable.horizontalHeader().setSectionResizeMode(QW.QHeaderView.Stretch)
        self.resultsLayout.addWidget(self.resultsTable, 0, 0, 1, 4)

        self.resultsLayout.addWidget(QW.QLabel("Calculation log:"), 1, 0, 1, 2)
        self.output = LabelOutput(self)
        self.resultsLayout.addWidget(self.output, 2, 0, 1, 4)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox(self)
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Close)
        layout.addWidget(self.button_box)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(500, 800)

    def connect_signals(self):
        pass

    def translate_UI(self):
        self.setWindowTitle(
            QW.QApplication.translate("PlotTDialog", "Use the t-plot method", None, -1)
        )
        self.optionsBox.setTitle(QW.QApplication.translate("PlotTDialog", "Options", None, -1))
        self.resultBox.setTitle(QW.QApplication.translate("PlotTDialog", "Results", None, -1))
        self.auto_button.setText(
            QW.QApplication.translate("PlotTDialog", "Auto-determine", None, -1)
        )
