from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from src.views.GraphView import GraphView
from src.widgets.SpinBoxSlider import QHSpinBoxSlider

from src.widgets.UtilityWidgets import (EditAlignRight, LabelAlignRight, LabelOutput, LabelResult)


class IASTSVPDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("IASTSVPDialog")

        _layout = QW.QGridLayout(self)

        # Options
        self.options_layout = QW.QGridLayout()
        _layout.addLayout(self.options_layout, 0, 0)

        ## Adsorbate selection
        self.adsorbate_label = LabelAlignRight("Adsorbate of interest:")
        self.options_layout.addWidget(self.adsorbate_label, 0, 0, 1, 1)
        self.adsorbate_input = QW.QComboBox()
        self.options_layout.addWidget(self.adsorbate_input, 0, 1, 1, 2)

        ## Molar fraction selection
        self.fraction_slider = QHSpinBoxSlider()
        self.fraction_slider.label.setText("Molar fraction:")
        self.fraction_slider.label.setMaximumSize(50, 10)
        self.fraction_slider.setRange(0, 1)
        self.fraction_slider.setValue(0.5, emit=False)
        self.options_layout.addWidget(self.fraction_slider, 1, 0, 1, 3)

        ## Point selection
        self.points_button = QW.QPushButton()
        self.options_layout.addWidget(self.points_button, 2, 0, 1, 3)

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
        self.setWindowTitle(QW.QApplication.translate("IASTSVPDialog", "IAST: selectivity-pressure calculation", None, -1))
        self.points_button.setText(QW.QApplication.translate("IASTSVPDialog", "Specify pressure", None, -1))
        self.calc_button.setText(QW.QApplication.translate("IASTSVPDialog", "Calculate", None, -1))
        # yapf: enable
