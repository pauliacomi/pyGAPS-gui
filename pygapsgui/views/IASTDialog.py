from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.views.GraphView import GraphView
from pygapsgui.widgets.RangeGenerator import RangeGenWidget
from pygapsgui.widgets.UtilityWidgets import EditAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelOutput
from pygapsgui.widgets.UtilityWidgets import LabelResult


class IASTDialog(QW.QDialog):
    """IAST general multicomponent prediction: QT MVC Dialog."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        """Creates and sets-up static UI elements"""
        self.setObjectName("IASTDialog")

        _layout = QW.QGridLayout(self)

        # Options
        self.options_layout = QW.QGridLayout()
        _layout.addLayout(self.options_layout, 0, 0)

        ## Branch
        self.branch_label = LabelAlignRight("Branch used:")
        self.options_layout.addWidget(self.branch_label, 1, 0, 1, 1)
        self.branch_dropdown = QW.QComboBox()
        self.options_layout.addWidget(self.branch_dropdown, 1, 1, 1, 2)

        ## Data selection
        self.data_table = RangeGenWidget()
        self.data_table.setMinimumWidth(300)
        self.options_layout.addWidget(self.data_table, 2, 0, 1, 3)

        ## Button to calculate
        self.calc_button = QW.QPushButton()
        self.options_layout.addWidget(self.calc_button, 3, 0, 1, 3)

        ## Output log
        self.output_label = QW.QLabel("Calculation log:")
        self.output = LabelOutput()
        self.options_layout.addWidget(self.output_label, 4, 0)
        self.options_layout.addWidget(self.output, 5, 0, 1, 3)

        # Result display
        self.res_graph = GraphView()
        self.res_graph.setObjectName("graph")
        _layout.addWidget(self.res_graph, 0, 1, 1, 1)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Close)
        _layout.addWidget(self.button_box, 1, 0, 1, 2)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(1000, 800)

    def connect_signals(self):
        """Connect permanent signals."""
        pass

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("IASTDialog", "IAST: multicomponent uptake calculations", None, -1))
        self.calc_button.setText(QW.QApplication.translate("IASTDialog", "Calculate", None, -1))
        # yapf: enable
