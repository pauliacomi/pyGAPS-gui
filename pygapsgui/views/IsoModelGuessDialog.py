from qtpy import PYSIDE6
from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

if PYSIDE6:
    import PySide6.QtSvgWidgets as QS
else:
    from qtpy import QtSvg as QS

from pygapsgui.views.IsoGraphView import IsoModelGraphView
from pygapsgui.widgets.SpinBoxSlider import QHSpinBoxSlider
from pygapsgui.widgets.UtilityWidgets import EditAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelOutput
from pygapsgui.widgets.UtilityWidgets import LabelResult


class IsoModelGuessDialog(QW.QDialog):
    """Automatic isotherm fit by several models: QT MVC Dialog."""

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

        # list
        self.options_layout.addWidget(QW.QLabel("Available models:"))
        self.model_list = QW.QListWidget()
        self.options_layout.addWidget(self.model_list)

        model_layout = QW.QFormLayout()
        self.options_layout.addLayout(model_layout)

        # Branch selection
        self.branch_label = LabelAlignRight("Branch:")
        self.branch_dropdown = QW.QComboBox()
        model_layout.addRow(self.branch_label, self.branch_dropdown)

        self.calc_auto_button = QW.QPushButton()
        self.calc_auto_button.setDefault(True)
        self.calc_auto_button.setAutoDefault(True)
        self.options_layout.addWidget(self.calc_auto_button)

        # Output log
        self.output_label = QW.QLabel("Output log:")
        self.output = LabelOutput()
        _layout.addWidget(self.output_label, 1, 0)
        _layout.addWidget(self.output, 2, 0)

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
        self.setWindowTitle(QW.QApplication.translate("IsoModelGuessDialog", "Isotherm model fitting", None, -1))
        self.calc_auto_button.setText(QW.QApplication.translate("IsoModelGuessDialog", "Fit selected models", None, -1))
        # yapf: enable
