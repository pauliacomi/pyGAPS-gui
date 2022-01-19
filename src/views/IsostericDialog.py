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

        _layout = QW.QGridLayout(self)

        # Iso graph and slider
        self.iso_graph = IsoGraphView(x_range_select=True)
        self.iso_graph.setObjectName("iso_graph")
        self.x_select = self.iso_graph.x_range_select
        _layout.addWidget(self.iso_graph, 0, 0, 2, 1)

        # Options/results box
        self.options_box = QW.QGroupBox()
        _layout.addWidget(self.options_box, 0, 1, 1, 1)
        self.options_layout = QW.QGridLayout(self.options_box)

        # Branch used
        self.branch_label = LabelAlignRight("Branch used:")
        self.branch_dropdown = QW.QComboBox()
        self.options_layout.addWidget(self.branch_label, 0, 0, 1, 1)
        self.options_layout.addWidget(self.branch_dropdown, 0, 1, 1, 1)

        # Autodetermine
        self.calc_auto_button = QW.QPushButton()
        self.options_layout.addWidget(self.calc_auto_button, 3, 0, 1, 2)

        # Enthalpy graph
        self.res_graph = GraphView()
        _layout.addWidget(self.res_graph, 1, 1, 1, 1)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Close)
        _layout.addWidget(self.button_box, 2, 0, 1, 1)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(800, 900)

    def connect_signals(self):
        pass

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("IsostericDialog", "Isosteric Enthalpy", None, -1))
        self.options_box.setTitle(QW.QApplication.translate("IsostericDialog", "Options", None, -1))
        self.calc_auto_button.setText(QW.QApplication.translate("IsostericDialog", "Calculate", None, -1))
        # yapf: enable
