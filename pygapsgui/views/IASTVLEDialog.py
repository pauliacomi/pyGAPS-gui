from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.views.GraphView import GraphView
from pygapsgui.widgets.UtilityWidgets import EditAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelOutput
from pygapsgui.widgets.UtilityWidgets import LabelResult


class IASTVLEDialog(QW.QDialog):
    """IAST vapour-liquid equilibrium prediction: QT MVC Dialog."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        """Creates and sets-up static UI elements"""
        self.setObjectName("IASTVLEDialog")

        _layout = QW.QGridLayout(self)

        # Options
        self.options_layout = QW.QGridLayout()
        _layout.addLayout(self.options_layout, 0, 0)

        ## Adsorbate selection
        self.adsorbate_label = LabelAlignRight("Adsorbate of interest:")
        self.options_layout.addWidget(self.adsorbate_label, 0, 0, 1, 1)
        self.adsorbate_input = QW.QComboBox()
        self.options_layout.addWidget(self.adsorbate_input, 0, 1, 1, 2)

        self.branch_label = LabelAlignRight("Branch used:")
        self.options_layout.addWidget(self.branch_label, 1, 0, 1, 1)
        self.branch_dropdown = QW.QComboBox()
        self.options_layout.addWidget(self.branch_dropdown, 1, 1, 1, 2)

        ## Pressure selection
        self.pressure_label = LabelAlignRight("Total pressure:")
        self.options_layout.addWidget(self.pressure_label, 2, 0, 1, 1)
        self.pressure_input = QW.QDoubleSpinBox()
        self.pressure_input.setDecimals(2)
        self.pressure_input.setValue(1)
        self.options_layout.addWidget(self.pressure_input, 2, 1, 1, 2)

        ## Point selection
        self.point_label = LabelAlignRight("Number of points:")
        self.options_layout.addWidget(self.point_label, 3, 0, 1, 1)
        self.point_input = QW.QSpinBox()
        self.point_input.setValue(30)
        self.options_layout.addWidget(self.point_input, 3, 1, 1, 2)

        ## Button to calculate
        self.calc_button = QW.QPushButton()
        self.calc_button.setDefault(True)
        self.calc_button.setAutoDefault(True)
        self.options_layout.addWidget(self.calc_button, 4, 0, 1, 3)

        ## Output log
        self.output_label = QW.QLabel("Calculation log:")
        self.output = LabelOutput()
        self.options_layout.addWidget(self.output_label, 5, 0)
        self.options_layout.addWidget(self.output, 6, 0, 1, 3)

        # Result display
        self.res_graph = GraphView()
        _layout.addWidget(self.res_graph, 0, 1, 1, 1)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Close)
        _layout.addWidget(self.button_box, 1, 0, 1, 2)

    def sizeHint(self) -> QC.QSize:
        """Suggest ideal dimensions."""
        return QC.QSize(800, 800)

    def connect_signals(self):
        """Connect permanent signals."""
        pass

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("IASTVLEDialog", "IAST: bulk-adsorbed equilibrium", None, -1))
        self.calc_button.setText(QW.QApplication.translate("IsoModelByDialog", "Calculate", None, -1))
        # yapf: enable
