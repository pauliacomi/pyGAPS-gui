from itertools import zip_longest

import numpy
from qtpy import PYSIDE6
from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from pygaps.modelling import _MODELS
from pygaps.modelling import get_isotherm_model
from pygaps.modelling import model_from_dict
from pygapsgui.utilities.tex2svg import tex2svg
from pygapsgui.widgets.SpinBoxLimitSlider import QHSpinBoxLimitSlider

if PYSIDE6:
    import PySide6.QtSvgWidgets as QS
else:
    from qtpy import QtSvg as QS

from pygapsgui.widgets.UtilityWidgets import LabelAlignCenter
from pygapsgui.widgets.UtilityWidgets import LabelAlignRight
from pygapsgui.widgets.UtilityWidgets import LimitEdit


class IsoEditModelWidget(QW.QWidget):
    """A widget that allows editing of ModelIsotherm parameters."""

    current_branch = None
    current_model = None
    model_param_widgets = None

    changed = QC.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_param_widgets = []

        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def set_fitting_model(self, model=None, branch="ads"):
        """Set or create model."""
        if isinstance(model, str):
            model = get_isotherm_model(model)
            model.pressure_range = (0, 1)
            model.loading_range = (0, 1)
        self.current_model = model
        self.current_branch = branch

        # Populate model details
        self.block_signals(True)
        self.model_dropdown.setCurrentText(model.name)
        self.branch_dropdown.setCurrentText(branch)
        self.p_limit_edit.set_values(self.current_model.pressure_range)
        self.l_limit_edit.set_values(self.current_model.loading_range)
        self.block_signals(False)

        self.populate_UI(emit=False)

    def setup_UI(self):
        """Create and set-up static UI elements."""

        # Create/set layout
        _layout = QW.QVBoxLayout(self)

        # Main model options
        model_options_layout = QW.QGridLayout()
        _layout.addLayout(model_options_layout)

        # Model type
        self.model_label = LabelAlignRight("Model:")
        self.model_dropdown = QW.QComboBox()
        self.model_dropdown.addItems(_MODELS)
        model_options_layout.addWidget(self.model_label, 0, 0)
        model_options_layout.addWidget(self.model_dropdown, 0, 1)

        # Branch selection
        self.branch_label = LabelAlignRight("Branch:")
        self.branch_dropdown = QW.QComboBox()
        self.branch_dropdown.addItems(["ads", "des"])
        model_options_layout.addWidget(self.branch_label, 1, 0)
        model_options_layout.addWidget(self.branch_dropdown, 1, 1)

        # Limits display
        self.limits_box = QW.QGroupBox()
        limits_layout = QW.QFormLayout(self.limits_box)

        self.p_limit_label = LabelAlignCenter()
        self.p_limit_edit = LimitEdit()
        self.p_limit_edit.set_limits_lower(0, None)
        self.p_limit_edit.set_limits_upper(0, None)
        self.p_limit_edit.set_values((0, 1))

        self.l_limit_label = LabelAlignCenter()
        self.l_limit_edit = LimitEdit()
        self.l_limit_edit.set_limits_lower(0, None)
        self.l_limit_edit.set_limits_upper(0, None)
        self.l_limit_edit.set_values((0, 1))

        limits_layout.addRow(self.p_limit_label, self.p_limit_edit)
        limits_layout.addRow(self.l_limit_label, self.l_limit_edit)

        _layout.addWidget(self.limits_box)

        # Parameter box
        self.param_box = QW.QGroupBox()
        self.param_box_layout = QW.QVBoxLayout(self.param_box)
        _layout.addWidget(self.param_box)

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

    def populate_UI(self, model_name=None, emit=True):
        """Set an existing or new model."""
        # Model formula display

        if model_name is not None:
            self.current_model = get_isotherm_model(model_name)
            self.current_model.pressure_range = self.p_limit_edit.values()
            self.current_model.loading_range = self.l_limit_edit.values()

        if self.current_model.formula:
            self.model_formula.setVisible(True)
            self.model_formula.load(tex2svg(self.current_model.formula))
            aspectRatioMode = QC.Qt.AspectRatioMode(QC.Qt.KeepAspectRatio)
            self.model_formula.renderer().setAspectRatioMode(aspectRatioMode)
        else:
            self.model_formula.setVisible(False)

        # Model parameters
        for param, widget in zip_longest(self.current_model.param_names, self.model_param_widgets):
            # if not needed, set the widget as invisible
            if not param:
                widget.setVisible(False)
                continue

            # if not existing, create the required widget
            if not widget:
                widget = QHSpinBoxLimitSlider()
                widget.changed_named.connect(self.update_model_param)
                self.model_param_widgets.append(widget)
                self.param_layout.insertWidget(self.param_layout.count() - 1, widget)

            # set all correct parameters
            widget.name = param
            widget.setText(param)
            widget.setVisible(True)
            val = self.current_model.params[param]
            minv, maxv = self.current_model.param_bounds[param]
            if minv is None or minv == -numpy.inf:
                minv = -100
            if maxv is None or maxv == numpy.inf:
                maxv = 100
            if maxv < val:
                maxv = val * 1.2
            if minv > val:
                maxv = val
            widget.setRange(minv=minv, maxv=maxv)
            if not numpy.isnan(val):
                widget.setValue(val, emit=False)
            else:
                widget.setValue(minv, emit=False)

            if emit:
                self.changed.emit()

    def connect_signals(self):
        """Connect permanent signals."""
        self.model_dropdown.currentTextChanged.connect(self.populate_UI)
        self.branch_dropdown.currentTextChanged.connect(self.update_model_branch)
        self.p_limit_edit.lower_changed.connect(self.update_model_limits)
        self.p_limit_edit.upper_changed.connect(self.update_model_limits)
        self.l_limit_edit.lower_changed.connect(self.update_model_limits)
        self.l_limit_edit.upper_changed.connect(self.update_model_limits)

    def update_model_branch(self, branch):
        """Update model branch after change of dropdown."""
        self.current_branch = branch
        self.changed.emit()

    def update_model_param(self, name, value):
        """Update model parameter after change of slider values."""
        self.current_model.params[name] = value
        self.changed.emit()

    def update_model_limits(self):
        """Update model limits after change of values."""
        self.current_model.pressure_range = self.p_limit_edit.values()
        self.current_model.loading_range = self.l_limit_edit.values()
        self.changed.emit()

    def block_signals(self, block):
        """Block some widget signals to remove recursion."""
        self.model_dropdown.blockSignals(block)
        self.p_limit_edit.blockSignals(block)
        self.l_limit_edit.blockSignals(block)
        self.branch_dropdown.blockSignals(block)

    def get_model_bounds(self) -> dict:
        """Read user-defined parameter bounds."""
        return {
            widget.name: [widget.minv, widget.maxv]
            for widget in self.model_param_widgets
            if widget.isVisible()
        }

    def sizeHint(self) -> QC.QSize:
        """Suggest ideal dimensions."""
        return QC.QSize(400, 500)

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        # self.rmse_label.setText(QW.QApplication.translate("IsoEditPointWidget", "RMSE", None, -1))
        self.param_box.setTitle(QW.QApplication.translate("IsoCreateDialog", "Parameters", None, -1))
        self.limits_box.setTitle(QW.QApplication.translate("IsoCreateDialog", "Limits", None, -1))
        self.p_limit_label.setText(QW.QApplication.translate("IsoEditPointWidget", "Pressure range", None, -1))
        self.l_limit_label.setText(QW.QApplication.translate("IsoEditPointWidget", "Loading range", None, -1))
        # yapf: enable


class IsoEditModelDialog(QW.QDialog):
    """A dialog to edit ModelIsotherm parameters."""
    def __init__(self, isotherm, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.isotherm = isotherm

        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

        model_copy = model_from_dict(self.isotherm.model.to_dict())
        self.view.set_fitting_model(model_copy, self.isotherm.branch)

    def setup_UI(self):
        """Create and set-up static UI elements."""
        self.setObjectName("IsoEditModelDialog")

        # Create/set layout
        _layout = QW.QVBoxLayout(self)

        # View
        self.view = IsoEditModelWidget()
        _layout.addWidget(self.view)

        # Button box
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Ok | QW.QDialogButtonBox.Cancel)
        _layout.addWidget(self.button_box)

    def connect_signals(self):
        """Connect permanent signals."""
        # Button box connections
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def accept(self) -> None:
        """Commit the changes to the model if accepted."""
        self.isotherm.branch = self.view.current_branch
        self.isotherm.model = self.view.current_model
        return super().accept()

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("IsoEditPointDialog", "Isotherm Model Parameters", None, -1))
        # yapf: enable
