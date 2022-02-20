from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.views.GraphView import GraphView
from pygapsgui.views.IsoGraphView import IsoGraphView
from pygapsgui.widgets.UtilityWidgets import LabelAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelOutput
from pygapsgui.widgets.UtilityWidgets import LabelResult


class PSDMicroDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        """Creates and sets-up static UI elements"""
        self.setObjectName("PSDMicroDialog")

        _layout = QW.QGridLayout(self)

        self.options_box = QW.QGroupBox()
        _layout.addWidget(self.options_box, 0, 0, 1, 1)
        self.res_graphs_box = QW.QGroupBox()
        _layout.addWidget(self.res_graphs_box, 1, 0, 1, 1)
        _layout.setRowStretch(0, 1)
        _layout.setRowStretch(1, 1)

        # Options box
        self.options_layout = QW.QHBoxLayout(self.options_box)

        ## Iso graph and slider
        self.iso_graph = IsoGraphView(x_range_select=True)
        self.iso_graph.setObjectName("iso_graph")
        self.x_select = self.iso_graph.x_range_select
        self.options_layout.addWidget(self.iso_graph)

        ## Options sub box
        self.options_sub_layout = QW.QGridLayout()
        self.options_layout.addLayout(self.options_sub_layout)

        ## Branch used
        self.branch_label = LabelAlignRight("Branch used:")
        self.branch_dropdown = QW.QComboBox()
        self.options_sub_layout.addWidget(self.branch_label, 0, 0, 1, 1)
        self.options_sub_layout.addWidget(self.branch_dropdown, 0, 1, 1, 1)

        ## PSD model
        self.model_label = LabelAlignRight("PSD model used:")
        self.model_dropdown = QW.QComboBox()
        self.options_sub_layout.addWidget(self.model_label, 1, 0, 1, 1)
        self.options_sub_layout.addWidget(self.model_dropdown, 1, 1, 1, 1)

        ## Pore geometry
        self.geometry_label = LabelAlignRight("Pore geometry:")
        self.geometry_dropdown = QW.QComboBox()
        self.options_sub_layout.addWidget(self.geometry_label, 2, 0, 1, 1)
        self.options_sub_layout.addWidget(self.geometry_dropdown, 2, 1, 1, 1)

        ## material model
        self.amodel_label = LabelAlignRight("Kelvin model:")
        self.amodel_dropdown = QW.QComboBox()
        self.options_sub_layout.addWidget(self.amodel_label, 3, 0, 1, 1)
        self.options_sub_layout.addWidget(self.amodel_dropdown, 3, 1, 1, 1)

        ## Autodetermine
        self.calc_auto_button = QW.QPushButton()
        self.options_sub_layout.addWidget(self.calc_auto_button, 4, 0, 1, 2)

        # Results graph box
        self.res_graphs_layout = QW.QVBoxLayout(self.res_graphs_box)

        ## PSD graph
        self.res_graph = GraphView()
        self.res_graphs_layout.addWidget(self.res_graph)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Close)
        _layout.addWidget(self.button_box, 2, 0, 1, 1)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(800, 900)

    def connect_signals(self):
        """Connect permanent signals."""
        pass

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("PSDMicroDialog", "Calculate microporous PSD", None, -1))
        self.options_box.setTitle(QW.QApplication.translate("PSDMicroDialog", "Options", None, -1))
        self.res_graphs_box.setTitle(QW.QApplication.translate("PSDMicroDialog", "Results", None, -1))
        self.calc_auto_button.setText(QW.QApplication.translate("PSDMicroDialog", "Calculate", None, -1))
        # yapf: enable
