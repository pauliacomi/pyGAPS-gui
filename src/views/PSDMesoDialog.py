from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView

from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class PSDMesoDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("PSDMesoDialog")

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
        self.tmodel_label = LabelAlignRight("PSD model used:")
        self.tmodel_dropdown = QW.QComboBox()
        self.options_sub_layout.addWidget(self.tmodel_label, 1, 0, 1, 1)
        self.options_sub_layout.addWidget(self.tmodel_dropdown, 1, 1, 1, 1)

        ## Thickness function
        self.thickness_label = LabelAlignRight("Thickness function:")
        self.thickness_dropdown = QW.QComboBox()
        self.options_sub_layout.addWidget(self.thickness_label, 2, 0, 1, 1)
        self.options_sub_layout.addWidget(self.thickness_dropdown, 2, 1, 1, 1)

        ## Pore geometry
        self.geometry_label = LabelAlignRight("Pore geometry:")
        self.geometry_dropdown = QW.QComboBox()
        self.options_sub_layout.addWidget(self.geometry_label, 3, 0, 1, 1)
        self.options_sub_layout.addWidget(self.geometry_dropdown, 3, 1, 1, 1)

        ## Kelvin model
        self.kmodel_label = LabelAlignRight("Kelvin model:")
        self.kmodel_dropdown = QW.QComboBox()
        self.options_sub_layout.addWidget(self.kmodel_label, 4, 0, 1, 1)
        self.options_sub_layout.addWidget(self.kmodel_dropdown, 4, 1, 1, 1)

        # Autodetermine
        self.calc_auto_button = QW.QPushButton()
        self.options_sub_layout.addWidget(self.calc_auto_button, 5, 0, 1, 2)

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
        pass

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("PSDMesoDialog", "Calculate mesoporous PSD", None, -1))
        self.options_box.setTitle(QW.QApplication.translate("PSDMesoDialog", "Options", None, -1))
        self.res_graphs_box.setTitle(QW.QApplication.translate("PSDMesoDialog", "Results", None, -1))
        self.calc_auto_button.setText(QW.QApplication.translate("PSDMesoDialog", "Calculate", None, -1))
        # yapf: enable
