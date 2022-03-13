from qtpy import PYSIDE6
from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

if PYSIDE6:
    import PySide6.QtSvgWidgets as QS
else:
    from qtpy import QtSvg as QS

from pygapsgui.views.IsoGraphView import IsoModelGraphView
from pygapsgui.widgets.UtilityWidgets import EditAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelOutput
from pygapsgui.widgets.UtilityWidgets import LabelResult


class IsoModelByDialog(QW.QDialog):
    """Fit an isotherm by a specific isotherm model: QT MVC Dialog."""

    paramWidgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        """Creates and sets-up static UI elements"""
        self.setObjectName("IsoModelByDialog")

        _layout = QW.QGridLayout(self)

        # Model selection and parameters
        self.options_layout = QW.QVBoxLayout()
        _layout.addLayout(self.options_layout, 0, 0)

        model_layout = QW.QFormLayout()
        self.options_layout.addLayout(model_layout)

        # Model selection
        self.model_label = LabelAlignRight("Model:")
        self.model_dropdown = QW.QComboBox()
        model_layout.addRow(self.model_label, self.model_dropdown)

        # Branch selection
        self.branch_label = LabelAlignRight("Branch:")
        self.branch_dropdown = QW.QComboBox()
        model_layout.addRow(self.branch_label, self.branch_dropdown)

        opt_button_layout = QW.QHBoxLayout()
        self.options_layout.addLayout(opt_button_layout)
        self.calc_auto_button = QW.QPushButton()
        self.calc_autolim_button = QW.QPushButton()
        self.calc_manual_button = QW.QPushButton()
        opt_button_layout.addWidget(self.calc_auto_button)
        opt_button_layout.addWidget(self.calc_autolim_button)
        opt_button_layout.addWidget(self.calc_manual_button)

        # Parameter box
        self.param_box = QW.QGroupBox()
        self.param_box_layout = QW.QVBoxLayout(self.param_box)
        self.options_layout.addWidget(self.param_box)

        param_box_widget = QW.QWidget()
        self.param_layout = QW.QVBoxLayout(param_box_widget)
        self.scroll_area = QW.QScrollArea()
        self.scroll_area.setFrameStyle(QW.QFrame.NoFrame)
        self.scroll_area.setWidget(param_box_widget)
        self.scroll_area.setWidgetResizable(True)
        self.param_box_layout.addWidget(self.scroll_area)

        self.model_formula = QS.QSvgWidget(self.param_box)
        self.model_formula.setFixedHeight(30)
        self.param_layout.addWidget(self.model_formula)
        self.param_layout.addStretch()

        # Output log
        self.output_label = QW.QLabel("Output log:")
        self.options_layout.addWidget(self.output_label)
        self.output = LabelOutput()
        self.output.setMaximumHeight(130)
        self.options_layout.addWidget(self.output)

        # Isotherm display
        self.iso_graph = IsoModelGraphView(x_range_select=True)
        self.x_select = self.iso_graph.x_range_select
        _layout.addWidget(self.iso_graph, 0, 1, 3, 1)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Cancel)
        _layout.addWidget(self.button_box, 3, 0, 1, 2)

    def sizeHint(self) -> QC.QSize:
        """Suggest ideal dimensions."""
        return QC.QSize(1000, 800)

    def connect_signals(self):
        """Connect permanent signals."""
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("IsoModelByDialog", "Isotherm model fitting", None, -1))
        self.param_box.setTitle(QW.QApplication.translate("IsoModelByDialog", "Parameters", None, -1))
        self.calc_auto_button.setText(QW.QApplication.translate("IsoModelByDialog", "Autofit", None, -1))
        self.calc_autolim_button.setText(QW.QApplication.translate("IsoModelByDialog", "Autofit with bounds", None, -1))
        self.calc_manual_button.setText(QW.QApplication.translate("IsoModelByDialog", "Use selected parameters", None, -1))
        # yapf: enable
