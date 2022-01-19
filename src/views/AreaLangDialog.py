from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView

from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class AreaLangDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("AreaLangDialog")

        _layout = QW.QGridLayout(self)

        self.options_box = QW.QGroupBox()
        _layout.addWidget(self.options_box, 0, 0, 1, 1)
        self.res_graphs_box = QW.QGroupBox()
        _layout.addWidget(self.res_graphs_box, 0, 1, 2, 1)
        self.res_text_box = QW.QGroupBox()
        _layout.addWidget(self.res_text_box, 1, 0, 1, 1)

        # Options box
        self.options_layout = QW.QGridLayout(self.options_box)

        ## Isotherm display
        self.iso_graph = IsoGraphView(x_range_select=True)
        self.x_select = self.iso_graph.x_range_select

        ## other options
        self.branch_label = LabelAlignRight("Branch used:")
        self.branch_dropdown = QW.QComboBox()
        self.calc_auto_button = QW.QPushButton()

        ## Layout them
        self.options_layout.addWidget(self.iso_graph, 0, 0, 1, 4)
        self.options_layout.addWidget(self.branch_label, 1, 0, 1, 1)
        self.options_layout.addWidget(self.branch_dropdown, 1, 1, 1, 1)
        self.options_layout.addWidget(self.calc_auto_button, 1, 3, 1, 1)

        # Results graph box
        self.res_graphs_layout = QW.QGridLayout(self.res_graphs_box)

        ## Langmuir plot
        self.lang_graph = GraphView()
        self.lang_graph.setObjectName("lang_graph")

        ## Layout them
        self.res_graphs_layout.addWidget(self.lang_graph, 0, 1, 1, 1)

        # Results box
        self.res_text_layout = QW.QGridLayout(self.res_text_box)

        # description labels
        self.res_text_layout.addWidget(LabelAlignRight("Fit (R^2):"), 0, 1, 1, 1)
        self.res_text_layout.addWidget(LabelAlignRight("Langmuir area [m2/g]:"), 1, 0, 1, 1)
        self.res_text_layout.addWidget(LabelAlignRight("K constant:"), 1, 2, 1, 1)
        self.res_text_layout.addWidget(LabelAlignRight("Monolayer uptake [mmol/g]:"), 2, 0, 1, 1)
        self.res_text_layout.addWidget(LabelAlignRight("Monolayer pressure [p/p0]:"), 2, 2, 1, 1)
        self.res_text_layout.addWidget(LabelAlignRight("Slope:"), 3, 0, 1, 1)
        self.res_text_layout.addWidget(LabelAlignRight("Intercept:"), 3, 2, 1, 1)

        # result labels
        self.result_r = LabelResult()
        self.result_lang = LabelResult()
        self.result_k = LabelResult()
        self.result_mono_n = LabelResult()
        self.result_mono_p = LabelResult()
        self.result_slope = LabelResult()
        self.result_intercept = LabelResult()

        self.res_text_layout.addWidget(self.result_r, 0, 2, 1, 1)
        self.res_text_layout.addWidget(self.result_lang, 1, 1, 1, 1)
        self.res_text_layout.addWidget(self.result_k, 1, 3, 1, 1)
        self.res_text_layout.addWidget(self.result_mono_n, 2, 1, 1, 1)
        self.res_text_layout.addWidget(self.result_mono_p, 2, 3, 1, 1)
        self.res_text_layout.addWidget(self.result_slope, 3, 1, 1, 1)
        self.res_text_layout.addWidget(self.result_intercept, 3, 3, 1, 1)

        self.output_label = QW.QLabel("Calculation log:")
        self.output = LabelOutput()
        self.res_text_layout.addWidget(self.output_label, 4, 0, 1, 2)
        self.res_text_layout.addWidget(self.output, 5, 0, 2, 4)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Close)
        _layout.addWidget(self.button_box, 2, 0, 1, 2)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(1000, 700)

    def connect_signals(self):
        pass

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("AreaLangDialog", "Calculate Langmuir area", None, -1))
        self.options_box.setTitle(QW.QApplication.translate("AreaLangDialog", "Options", None, -1))
        self.res_graphs_box.setTitle(QW.QApplication.translate("AreaLangDialog", "Output Graphs", None, -1))
        self.res_text_box.setTitle(QW.QApplication.translate("AreaLangDialog", "Results", None, -1))
        self.calc_auto_button.setText(QW.QApplication.translate("AreaLangDialog", "Auto-determine", None, -1))
        # yapf: enable
