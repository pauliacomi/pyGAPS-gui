from qtpy import PYSIDE6
from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.widgets.IsoUnitWidget import IsoUnitWidget
from pygapsgui.widgets.SciDoubleSpinbox import ScientificDoubleSpinBox

if PYSIDE6:
    import PySide6.QtSvgWidgets as QS
else:
    from qtpy import QtSvg as QS

from pygapsgui.views.IsoGraphView import IsoGraphView
from pygapsgui.widgets.UtilityWidgets import EditAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelAlignRight
from pygapsgui.widgets.UtilityWidgets import LabelOutput
from pygapsgui.widgets.UtilityWidgets import LabelResult


class IsoModelManualDialog(QW.QDialog):
    """Manually create an isotherm model: QT MVC Dialog."""

    paramWidgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        """Creates and sets-up static UI elements"""
        self.setObjectName("IsoModelManualDialog")

        _layout = QW.QGridLayout(self)

        # Model selection and parameters
        self.options_layout = QW.QVBoxLayout()
        _layout.addLayout(self.options_layout, 0, 0)

        model_layout = QW.QGridLayout()
        self.options_layout.addLayout(model_layout)

        # Model selection
        self.model_label = LabelAlignRight("Model:")
        model_layout.addWidget(self.model_label, 0, 0, 1, 1)
        self.model_dropdown = QW.QComboBox()
        model_layout.addWidget(self.model_dropdown, 0, 1, 1, 2)

        # Adsorbate selection
        self.adsorbate_label = LabelAlignRight("Adsorbate:")
        self.adsorbate_input = QW.QComboBox()
        self.adsorbate_input.setInsertPolicy(QW.QComboBox.NoInsert)
        self.adsorbate_input.setEditable(True)
        model_layout.addWidget(self.adsorbate_label, 1, 0, 1, 1)
        model_layout.addWidget(self.adsorbate_input, 1, 1, 1, 2)

        # Temperature selection
        self.temperature_label = LabelAlignRight("Temperature:")
        self.temperature_input = QW.QDoubleSpinBox()
        self.temperature_input.setDecimals(2)
        self.temperature_input.setValue(77)
        self.temperature_input.setMaximum(1000)
        self.temperature_unit = QW.QComboBox()
        self.temperature_unit.setObjectName("temperature_unit")
        model_layout.addWidget(self.temperature_label, 2, 0, 1, 1)
        model_layout.addWidget(self.temperature_input, 2, 1, 1, 1)
        model_layout.addWidget(self.temperature_unit, 2, 2, 1, 1)

        # Branch selection
        self.branch_label = LabelAlignRight("Branch:")
        self.branch_dropdown = QW.QComboBox()
        model_layout.addWidget(self.branch_label, 3, 0, 1, 1)
        model_layout.addWidget(self.branch_dropdown, 3, 1, 1, 2)

        self.unit_widget = IsoUnitWidget(self.temperature_unit)
        self.options_layout.addWidget(self.unit_widget)

        # Limits display
        self.limits_box = QW.QGroupBox()
        limits_layout = QW.QGridLayout(self.limits_box)

        self.p_min = ScientificDoubleSpinBox()
        self.p_max = ScientificDoubleSpinBox()
        self.l_min = ScientificDoubleSpinBox()
        self.l_max = ScientificDoubleSpinBox()
        self.p_min.setMinimum(0)
        self.p_max.setMinimum(0)
        self.l_min.setMinimum(0)
        self.l_max.setMinimum(0)
        self.p_max.setValue(1)
        self.l_max.setValue(1)
        limits_layout.addWidget(QW.QLabel("Pressure min"), 0, 0)
        limits_layout.addWidget(QW.QLabel("Pressure max"), 1, 0)
        limits_layout.addWidget(QW.QLabel("Loading max"), 0, 2)
        limits_layout.addWidget(QW.QLabel("Loading max"), 1, 2)
        limits_layout.addWidget(self.p_min, 0, 1)
        limits_layout.addWidget(self.p_max, 1, 1)
        limits_layout.addWidget(self.l_min, 0, 3)
        limits_layout.addWidget(self.l_max, 1, 3)

        self.options_layout.addWidget(self.limits_box)

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

        opt_button_layout = QW.QHBoxLayout()
        self.calc_manual_button = QW.QPushButton()
        opt_button_layout.addWidget(self.calc_manual_button)
        self.options_layout.addLayout(opt_button_layout)

        # Output
        self.output_layout = QW.QVBoxLayout()
        _layout.addLayout(self.output_layout, 0, 1)

        # Isotherm display
        self.iso_graph = IsoGraphView()
        self.output_layout.addWidget(self.iso_graph)

        # Output log
        self.output_label = QW.QLabel("Output log:")
        self.output = LabelOutput()
        self.output.setMaximumHeight(120)
        self.output_layout.addWidget(self.output_label)
        self.output_layout.addWidget(self.output)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Cancel)
        _layout.addWidget(self.button_box, 4, 0, 1, 2)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(1000, 800)

    def connect_signals(self):
        """Connect permanent signals."""
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("IsoModelManualDialog", "Isotherm model fitting", None, -1))
        self.param_box.setTitle(QW.QApplication.translate("IsoModelManualDialog", "Parameters", None, -1))
        self.limits_box.setTitle(QW.QApplication.translate("IsoModelManualDialog", "Limits", None, -1))
        self.calc_manual_button.setText(QW.QApplication.translate("IsoModelManualDialog", "Create model from parameters", None, -1))
        # yapf: enable
