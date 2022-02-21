from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.widgets.SciDoubleSpinbox import ScientificDoubleSpinBox
from pygapsgui.widgets.UtilityWidgets import LabelAlignCenter


class IsoEditModelDialog(QW.QDialog):
    def __init__(self, isotherm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isotherm = isotherm
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()
        self.populate_table()

    def setup_UI(self):
        """Creates and sets-up static UI elements"""
        self.setObjectName("IsoEditModelDialog")

        # Create/set layout
        _layout = QW.QVBoxLayout(self)

        self.model_label = LabelAlignCenter()
        _layout.addWidget(self.model_label)

        # Table Widget
        self.table_view = QW.QTableWidget(0, 2)
        self.table_view.setHorizontalHeaderLabels(("Parameter", "Value"))
        self.table_view.horizontalHeader().setSectionResizeMode(QW.QHeaderView.Stretch)
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

    def populate_table(self):
        model = self.isotherm.model
        self.model_label.setText(f"Model type: '{model.name}'.")
        self.table_view.setRowCount(len(model.params))
        for ind, (param, val) in enumerate(model.params.items()):
            param_name = QW.QTableWidgetItem(param)
            param_name.setFlags(QC.Qt.ItemIsSelectable)
            param_value = ScientificDoubleSpinBox()
            param_value.setValue(val)
            self.table_view.setItem(ind, 0, param_name)
            self.table_view.setCellWidget(ind, 1, param_value)

    def accept(self) -> None:
        model = self.isotherm.model
        for ind, param in enumerate(model.params):
            model.params[param] = self.table_view.cellWidget(ind, 1).value()
        return super().accept()

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(300, 300)

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("IsoEditPointDialog", "Isotherm Model Parameters", None, -1))
        self.edit_label.setText(QW.QApplication.translate("IsoEditPointDialog", "Double click to edit parameters.", None, -1))
        # yapf: enable
