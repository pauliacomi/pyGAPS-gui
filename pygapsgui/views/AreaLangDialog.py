from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.views.GraphView import GraphView
from pygapsgui.views.IsoGraphView import IsoGraphView
from pygapsgui.widgets.UtilityWidgets import LabelAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelOutput
from pygapsgui.widgets.UtilityWidgets import LabelResult


class AreaLangDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        """Creates and sets-up static UI elements"""
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
        self.label_fit = LabelAlignRight("Fit (R^2):")
        self.label_area = LabelAlignRight("Langmuir area [m2/g]:")
        self.label_k = LabelAlignRight("K constant:")
        self.label_n_mono = LabelAlignRight("Monolayer uptake [mmol/g]:")
        self.label_p_mono = LabelAlignRight("Monolayer pressure [p/p0]:")
        self.label_slope = LabelAlignRight("Slope:")
        self.label_intercept = LabelAlignRight("Intercept:")
        self.res_text_layout.addWidget(self.label_fit, 0, 1, 1, 1)
        self.res_text_layout.addWidget(self.label_area, 1, 0, 1, 1)
        self.res_text_layout.addWidget(self.label_k, 1, 2, 1, 1)
        self.res_text_layout.addWidget(self.label_n_mono, 2, 0, 1, 1)
        self.res_text_layout.addWidget(self.label_p_mono, 2, 2, 1, 1)
        self.res_text_layout.addWidget(self.label_slope, 3, 0, 1, 1)
        self.res_text_layout.addWidget(self.label_intercept, 3, 2, 1, 1)

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
        """Connect permanent signals."""
        pass

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("AreaLangDialog", "Calculate Langmuir area", None, -1))
        self.options_box.setTitle(QW.QApplication.translate("AreaLangDialog", "Options", None, -1))
        self.res_graphs_box.setTitle(QW.QApplication.translate("AreaLangDialog", "Output Graphs", None, -1))
        self.res_text_box.setTitle(QW.QApplication.translate("AreaLangDialog", "Results", None, -1))
        self.calc_auto_button.setText(QW.QApplication.translate("AreaLangDialog", "Auto-determine", None, -1))
        # yapf: enable
