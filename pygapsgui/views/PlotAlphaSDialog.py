from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.views.GraphView import GraphView
from pygapsgui.widgets.UtilityWidgets import LabelAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelOutput
from pygapsgui.widgets.UtilityWidgets import LabelResult


class PlotAlphaSDialog(QW.QDialog):
    """Alpha-s plot calculations: QT MVC Dialog."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        """Creates and sets-up static UI elements"""
        self.setObjectName("PlotAlphaSDialog")

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

        self.options_layout.addWidget(LabelAlignRight("Isotherm branch:"), 1, 0, 1, 1)
        self.branch_dropdown = QW.QComboBox()
        self.options_layout.addWidget(self.branch_dropdown, 1, 1, 1, 2)

        self.options_layout.addWidget(LabelAlignRight("Reference isotherm branch:"), 2, 0, 1, 1)
        self.refbranch_dropdown = QW.QComboBox()
        self.options_layout.addWidget(self.refbranch_dropdown, 2, 1, 1, 2)

        self.refarea_label = LabelAlignRight("Reference material area:")
        self.refarea_dropdown = QW.QComboBox()
        self.refarea_dropdown.addItems(["BET", "Langmuir", "specify"]),
        self.refarea_input = QW.QLineEdit(self)
        self.refarea_input.setEnabled(False)
        self.options_layout.addWidget(self.refarea_label, 3, 0, 1, 1)
        self.options_layout.addWidget(self.refarea_dropdown, 3, 1, 1, 2)
        self.options_layout.addWidget(self.refarea_input, 3, 3, 1, 1)

        self.options_layout.addWidget(LabelAlignRight("Reducing pressure:"), 4, 0, 1, 1)
        self.pressure_input = QW.QLineEdit(self)
        self.pressure_input.setText(str(0.4))
        self.options_layout.addWidget(self.pressure_input, 4, 1, 1, 2)

        self.calc_auto_button = QW.QPushButton()
        self.options_layout.addWidget(self.calc_auto_button, 4, 3, 1, 1)

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
        return QC.QSize(500, 800)

    def connect_signals(self):
        """Connect permanent signals."""
        pass

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("PlotAlphaSDialog", "Use the alpha-s method", None, -1))
        self.options_box.setTitle(QW.QApplication.translate("PlotAlphaSDialog", "Options", None, -1))
        self.res_text_box.setTitle(QW.QApplication.translate("PlotAlphaSDialog", "Results", None, -1))
        self.calc_auto_button.setText(QW.QApplication.translate("PlotAlphaSDialog", "Auto-calculate", None, -1))
        # yapf: enable
