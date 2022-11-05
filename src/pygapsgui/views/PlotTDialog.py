from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.views.GraphView import GraphView
from pygapsgui.widgets.UtilityWidgets import LabelAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelOutput
from pygapsgui.widgets.UtilityWidgets import LabelResult


class PlotTDialog(QW.QDialog):
    """T-plot calculations: QT MVC Dialog."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        """Create and set-up static UI elements."""
        self.setObjectName("PlotTDialog")

        _layout = QW.QVBoxLayout(self)

        self.options_box = QW.QGroupBox()
        _layout.addWidget(self.options_box)
        self.res_text_box = QW.QGroupBox()
        _layout.addWidget(self.res_text_box)

        # Options box
        self.options_layout = QW.QGridLayout(self.options_box)

        ## Plot display
        self.res_graph = GraphView(x_range_select=True)
        self.res_graph.setObjectName("res_graph")
        self.x_select = self.res_graph.x_range_select
        self.options_layout.addWidget(self.res_graph, 0, 0, 1, 4)

        self.options_layout.addWidget(LabelAlignRight("Thickness function:"), 1, 0, 1, 1)
        self.thickness_dropdown = QW.QComboBox()
        self.options_layout.addWidget(self.thickness_dropdown, 1, 1, 1, 2)

        self.options_layout.addWidget(LabelAlignRight("Isotherm branch:"), 2, 0, 1, 1)
        self.branch_dropdown = QW.QComboBox()
        self.options_layout.addWidget(self.branch_dropdown, 2, 1, 1, 2)

        self.calc_auto_button = QW.QPushButton()
        self.calc_auto_button.setDefault(True)
        self.calc_auto_button.setAutoDefault(True)
        self.options_layout.addWidget(self.calc_auto_button, 2, 3, 1, 1)

        # Results box
        self.res_text_layout = QW.QGridLayout(self.res_text_box)

        self.res_table = QW.QTableWidget(0, 5, self)
        self.res_table.horizontalHeader().setSectionResizeMode(QW.QHeaderView.Stretch)
        self.res_table.verticalHeader().setSectionResizeMode(QW.QHeaderView.ResizeToContents)
        self.res_table.setMinimumHeight(100)
        self.res_text_layout.addWidget(self.res_table, 0, 0, 1, 4)

        self.res_text_layout.addWidget(QW.QLabel("Calculation log:"), 1, 0, 1, 2)
        self.output = LabelOutput()
        self.res_text_layout.addWidget(self.output, 2, 0, 1, 4)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.addButton("Save as metadata", QW.QDialogButtonBox.AcceptRole)
        self.export_btn = self.button_box.addButton(
            "Export results", QW.QDialogButtonBox.ActionRole
        )
        self.button_box.addButton("Help", QW.QDialogButtonBox.HelpRole)
        self.button_box.addButton("Cancel", QW.QDialogButtonBox.RejectRole)
        _layout.addWidget(self.button_box)

    def sizeHint(self) -> QC.QSize:
        """Suggest ideal dimensions."""
        return QC.QSize(500, 800)

    def connect_signals(self):
        """Connect permanent signals."""
        pass

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("PlotTDialog", "Use the t-plot method", None, -1))
        self.options_box.setTitle(QW.QApplication.translate("PlotTDialog", "Options", None, -1))
        self.res_text_box.setTitle(QW.QApplication.translate("PlotTDialog", "Results", None, -1))
        self.calc_auto_button.setText(QW.QApplication.translate("PlotTDialog", "Auto-determine", None, -1))
        # yapf: enable
