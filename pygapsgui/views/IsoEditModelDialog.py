from qtpy import PYSIDE6
from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from pygapsgui.utilities.tex2svg import tex2svg

if PYSIDE6:
    import PySide6.QtSvgWidgets as QS
else:
    from qtpy import QtSvg as QS

from pygapsgui.widgets.SciDoubleSpinbox import ScientificDoubleSpinBox
from pygapsgui.widgets.SciDoubleSpinbox import SciFloatSpinDelegate
from pygapsgui.widgets.UtilityWidgets import FloatStandardItem
from pygapsgui.widgets.UtilityWidgets import LabelAlignCenter
from pygapsgui.widgets.UtilityWidgets import LimitEdit


class IsoEditModelDialog(QW.QDialog):
    """Dialog allowing the editing of ModelIsotherm parameters."""
    def __init__(self, isotherm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isotherm = isotherm
        self.setup_UI()
        self.translate_UI()
        self.populate_UI()
        self.connect_signals()

    def setup_UI(self):
        """Creates and sets-up static UI elements"""
        self.setObjectName("IsoEditModelDialog")

        # Create/set layout
        _layout = QW.QVBoxLayout(self)

        self.model_label = LabelAlignCenter()
        _layout.addWidget(self.model_label)

        # Model formula display
        self.model_formula = QS.QSvgWidget()
        self.model_formula.setFixedHeight(30)
        _layout.addWidget(self.model_formula)

        # Other model details

        details_layout = QW.QFormLayout()
        self.rmse_label = LabelAlignCenter()
        self.rmse_edit = ScientificDoubleSpinBox()
        self.plimit_label = LabelAlignCenter()
        self.plimit_edit = LimitEdit()
        self.llimit_label = LabelAlignCenter()
        self.llimit_edit = LimitEdit()

        details_layout.addRow(self.rmse_label, self.rmse_edit)
        details_layout.addRow(self.plimit_label, self.plimit_edit)
        details_layout.addRow(self.llimit_label, self.llimit_edit)
        _layout.addLayout(details_layout)

        # Table model/view
        self.table_view = QW.QTableView()
        self.model = QG.QStandardItemModel(0, 2)
        self.table_view.setModel(self.model)
        sci_delegate = SciFloatSpinDelegate()
        self.table_view.setItemDelegateForColumn(1, sci_delegate)
        self.table_view.horizontalHeader().setSectionResizeMode(QW.QHeaderView.Stretch)
        self.model.setHorizontalHeaderLabels(("Parameter", "Value"))
        _layout.addWidget(self.table_view)

        # Edits
        self.edit_label = LabelAlignCenter()
        _layout.addWidget(self.edit_label)

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

    def populate_UI(self):
        """Set all the values from the model."""
        model = self.isotherm.model
        self.model_label.setText(f"Model type: '{model.name}'.")

        # Details
        self.rmse_edit.setValue(model.rmse)
        self.plimit_edit.set_values(model.pressure_range)
        self.llimit_edit.set_values(model.loading_range)

        # Model formula display
        if model.formula:
            self.model_formula.setVisible(True)
            self.model_formula.load(tex2svg(model.formula))
            aspectRatioMode = QC.Qt.AspectRatioMode(QC.Qt.KeepAspectRatio)
            self.model_formula.renderer().setAspectRatioMode(aspectRatioMode)
        else:
            self.model_formula.setVisible(False)

        # Set the parameter/value pair.
        self.model.setRowCount(len(model.params))
        for ind, (param, val) in enumerate(model.params.items()):
            param_name = QG.QStandardItem(param)
            param_name.setFlags(QC.Qt.ItemIsSelectable)
            param_value = FloatStandardItem()
            param_value.setData(val)
            param_name.setFlags(QC.Qt.ItemIsSelectable | QC.Qt.ItemIsEditable)
            self.model.setItem(ind, 0, param_name)
            self.model.setItem(ind, 1, param_value)

    def accept(self) -> None:
        """Commit the changes to the model if accepted."""
        model = self.isotherm.model
        for ind, param in enumerate(model.params):
            model.params[param] = self.model.item(ind, 1).data()
        model.rmse = self.rmse_edit.value()
        model.pressure_range = self.plimit_edit.values()
        model.loading_range = self.llimit_edit.values()
        return super().accept()

    def sizeHint(self) -> QC.QSize:
        """Suggest ideal dimensions."""
        return QC.QSize(300, 500)

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("IsoEditPointDialog", "Isotherm Model Parameters", None, -1))
        self.edit_label.setText(QW.QApplication.translate("IsoEditPointDialog", "Double click to edit parameters.", None, -1))
        self.rmse_label.setText(QW.QApplication.translate("IsoEditPointDialog", "RMSE", None, -1))
        self.plimit_label.setText(QW.QApplication.translate("IsoEditPointDialog", "Pressure range", None, -1))
        self.llimit_label.setText(QW.QApplication.translate("IsoEditPointDialog", "Loading range", None, -1))
        # yapf: enable
