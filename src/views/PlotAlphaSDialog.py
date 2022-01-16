from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView

from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class PlotAlphaSDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("PlotAlphaSDialog")

        layout = QW.QVBoxLayout(self)
        layout.setObjectName("layout")

        self.optionsBox = QW.QGroupBox(self)
        layout.addWidget(self.optionsBox)
        self.resultBox = QW.QGroupBox(self)
        layout.addWidget(self.resultBox)

        # Options box
        self.options_layout = QW.QGridLayout(self.optionsBox)

        ## Plot display
        self.tGraph = GraphView(x_range_select=True, parent=self)
        self.tGraph.setObjectName("tGraph")
        self.x_select = self.tGraph.x_range_select
        self.options_layout.addWidget(self.tGraph, 0, 0, 1, 4)

        self.options_layout.addWidget(LabelAlignRight("Isotherm branch:"), 1, 0, 1, 1)
        self.branchDropdown = QW.QComboBox(self)
        self.options_layout.addWidget(self.branchDropdown, 1, 1, 1, 2)

        self.options_layout.addWidget(LabelAlignRight("Reference isotherm branch:"), 2, 0, 1, 1)
        self.refbranchDropdown = QW.QComboBox(self)
        self.options_layout.addWidget(self.refbranchDropdown, 2, 1, 1, 2)

        self.options_layout.addWidget(LabelAlignRight("Reference material area:"), 3, 0, 1, 1)
        self.areaDropdown = QW.QComboBox(self)
        self.areaDropdown.addItems(["BET", "Langmuir", "specify"]),
        self.options_layout.addWidget(self.areaDropdown, 3, 1, 1, 2)
        self.areaInput = QW.QLineEdit(self)
        self.areaInput.setEnabled(False)
        self.options_layout.addWidget(self.areaInput, 3, 3, 1, 1)

        self.options_layout.addWidget(LabelAlignRight("Reducing pressure:"), 4, 0, 1, 1)
        self.pressure_input = QW.QLineEdit(self)
        self.pressure_input.setText(str(0.4))
        self.options_layout.addWidget(self.pressure_input, 4, 1, 1, 2)

        self.auto_button = QW.QPushButton(self)
        self.options_layout.addWidget(self.auto_button, 4, 3, 1, 1)

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
            QW.QApplication.translate("PlotAlphaSDialog", "Use the alpha-s method", None, -1)
        )
        self.optionsBox.setTitle(QW.QApplication.translate("PlotAlphaSDialog", "Options", None, -1))
        self.resultBox.setTitle(QW.QApplication.translate("PlotAlphaSDialog", "Results", None, -1))
        self.auto_button.setText(
            QW.QApplication.translate("PlotAlphaSDialog", "Auto-calculate", None, -1)
        )
