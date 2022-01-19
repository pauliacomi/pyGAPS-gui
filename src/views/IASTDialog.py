from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from src.views.GraphView import GraphView
from src.widgets.RangeGenerator import RangeGenWidget

from src.widgets.UtilityWidgets import (EditAlignRight, LabelAlignRight, LabelOutput, LabelResult)


class IASTDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("IASTDialog")

        _layout = QW.QGridLayout(self)

        # Options
        self.options_layout = QW.QGridLayout()
        _layout.addLayout(self.options_layout, 0, 0)

        ## Data selection
        self.data_label = LabelAlignRight("Adsorbate of interest:")
        self.data_table = RangeGenWidget()
        self.options_layout.addWidget(self.data_label, 0, 0)
        self.options_layout.addWidget(self.data_table, 1, 0, 1, 3)

        ## Button to calculate
        self.calc_button = QW.QPushButton()
        self.options_layout.addWidget(self.calc_button, 2, 0, 1, 3)

        ## Output log
        self.output_label = QW.QLabel("Calculation log:")
        self.output = LabelOutput()
        self.options_layout.addWidget(self.output_label, 3, 0)
        self.options_layout.addWidget(self.output, 4, 0, 1, 3)

        # Result display
        self.res_graph = GraphView()
        self.res_graph.setObjectName("graph")
        _layout.addWidget(self.res_graph, 0, 1, 1, 1)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Cancel)
        _layout.addWidget(self.button_box, 1, 0, 1, 2)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(1000, 800)

    def connect_signals(self):
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("IASTDialog", "IAST: multicomponent uptake calculations", None, -1))
        self.calc_button.setText(QW.QApplication.translate("IASTDialog", "Calculate", None, -1))
        # yapf: enable
