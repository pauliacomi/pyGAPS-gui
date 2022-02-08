from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.views.GraphView import GraphView
from pygapsgui.views.IsoGraphView import IsoGraphView
from pygapsgui.widgets.UtilityWidgets import LabelAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelOutput
from pygapsgui.widgets.UtilityWidgets import LabelResult


class DADRDialog(QW.QDialog):
    def __init__(self, ptype="DR", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ptype = ptype

        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        """Creates and sets-up static UI elements"""
        self.setObjectName("DADRDialog")

        _layout = QW.QGridLayout(self)

        self.options_box = QW.QGroupBox()
        _layout.addWidget(self.options_box, 0, 0, 1, 1)
        self.res_graphs_box = QW.QGroupBox()
        _layout.addWidget(self.res_graphs_box, 0, 1, 2, 1)
        self.res_text_box = QW.QGroupBox()
        _layout.addWidget(self.res_text_box, 1, 0, 1, 1)

        # Options box
        self.options_layout = QW.QGridLayout(self.options_box)
        row = 0

        ## Isotherm display
        self.iso_graph = IsoGraphView(x_range_select=True)
        self.iso_graph.setObjectName("iso_graph")
        self.x_select = self.iso_graph.x_range_select
        self.options_layout.addWidget(self.iso_graph, row, 0, 1, 4)
        row = row + 1

        ## other options
        self.branch_label = LabelAlignRight("Branch used:")
        self.branch_dropdown = QW.QComboBox()
        self.options_layout.addWidget(self.branch_label, row, 0, 1, 1)
        self.options_layout.addWidget(self.branch_dropdown, row, 1, 1, 1)

        if self.ptype == "DA":
            self.dr_exp_input = QW.QDoubleSpinBox()
            self.dr_exp_input.setSingleStep(0.1)
            self.options_layout.addWidget(LabelAlignRight("D-A Exponent:"), row, 2, 1, 1)
            self.options_layout.addWidget(self.dr_exp_input, row, 3, 1, 1)

        row = row + 1

        self.calc_auto_button = QW.QPushButton()
        self.options_layout.addWidget(self.calc_auto_button, row, 0, 1, 4)

        # Results graph box
        self.res_graphs_layout = QW.QGridLayout(self.res_graphs_box)

        ## DA/DR plot
        self.rgraph = GraphView()
        self.rgraph.setObjectName("DADRGraph")
        self.res_graphs_layout.addWidget(self.rgraph, 0, 1, 1, 1)

        # Results box
        self.res_text_layout = QW.QGridLayout(self.res_text_box)

        # description labels
        self.label_vol = LabelAlignRight("Micropore Volume [cm3/g]")
        self.res_text_layout.addWidget(LabelAlignRight("Fit (R^2):"), 0, 2, 1, 1)
        self.res_text_layout.addWidget(self.label_vol, 1, 0, 1, 1)
        self.res_text_layout.addWidget(LabelAlignRight("Effective Potential [kJ/mol]"), 1, 2, 1, 1)
        self.res_text_layout.addWidget(LabelAlignRight("Slope:"), 2, 0, 1, 1)
        self.res_text_layout.addWidget(LabelAlignRight("Intercept:"), 2, 2, 1, 1)

        # result labels
        self.result_r = LabelResult()
        self.result_microporevol = LabelResult()
        self.result_adspotential = LabelResult()
        self.result_slope = LabelResult()
        self.result_intercept = LabelResult()
        self.res_text_layout.addWidget(self.result_r, 0, 3, 1, 1)
        self.res_text_layout.addWidget(self.result_microporevol, 1, 1, 1, 1)
        self.res_text_layout.addWidget(self.result_adspotential, 1, 3, 1, 1)
        self.res_text_layout.addWidget(self.result_slope, 2, 1, 1, 1)
        self.res_text_layout.addWidget(self.result_intercept, 2, 3, 1, 1)

        self.output_label = QW.QLabel("Calculation log:")
        self.output = LabelOutput()
        self.res_text_layout.addWidget(self.output_label, 3, 0, 1, 2)
        self.res_text_layout.addWidget(self.output, 4, 0, 2, 4)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Close)
        _layout.addWidget(self.button_box, 2, 0, 1, 2)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(1000, 800)

    def connect_signals(self):
        """Connect permanent signals."""
        pass

    def translate_UI(self):
        key = "Dubinin-Radushkevich plot"
        if self.ptype == "DA":
            key = "Dubinin-Astakov plot"
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("DADRDialog", key, None, -1))
        self.options_box.setTitle(QW.QApplication.translate("DADRDialog", "Options", None, -1))
        self.res_text_box.setTitle(QW.QApplication.translate("DADRDialog", "Results", None, -1))
        self.calc_auto_button.setText(QW.QApplication.translate("DADRDialog", "Auto-determine", None, -1))
        # yapf: enabke
