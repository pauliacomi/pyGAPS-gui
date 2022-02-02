from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.models.IsoDataTableModel import IsoDataTableModel
from src.widgets.SciDoubleSpinbox import SciFloatDelegate
from src.widgets.UtilityWidgets import LabelAlignCenter


class IsoEditPointDialog(QW.QDialog):
    def __init__(self, isotherm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()

        self.isotherm = isotherm
        self.model = IsoDataTableModel(isotherm.data_raw.copy())
        self.table_view.setModel(self.model)
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("IsoEditPointDialog")

        # Create/set layout
        _layout = QW.QVBoxLayout(self)

        # Table View
        self.table_view = QW.QTableView()
        delegate = SciFloatDelegate()
        self.table_view.setItemDelegateForColumn(0, delegate)
        self.table_view.setItemDelegateForColumn(1, delegate)
        _layout.addWidget(self.table_view)

        # table view Headers
        self.horizontal_header = self.table_view.horizontalHeader()
        self.vertical_header = self.table_view.verticalHeader()
        self.horizontal_header.setSectionResizeMode(QW.QHeaderView.Stretch)
        self.vertical_header.setSectionResizeMode(QW.QHeaderView.ResizeToContents)

        # Edit functions
        edit_widget = QW.QWidget()
        _layout.addWidget(edit_widget)
        edit_layout = QW.QGridLayout(edit_widget)
        self.edit_label = LabelAlignCenter()
        self.edit_add_row = QW.QPushButton()
        self.edit_del_row = QW.QPushButton()
        self.edit_add_col = QW.QPushButton()
        self.edit_del_col = QW.QPushButton()
        edit_layout.addWidget(self.edit_label, 0, 0, 1, 2)
        edit_layout.addWidget(self.edit_add_row, 1, 0)
        edit_layout.addWidget(self.edit_del_row, 1, 1)
        edit_layout.addWidget(self.edit_add_col, 2, 0)
        edit_layout.addWidget(self.edit_del_col, 2, 1)

        # Button box
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Ok | QW.QDialogButtonBox.Cancel)
        _layout.addWidget(self.button_box)

    def connect_signals(self):
        # Button box connections
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.edit_add_row.pressed.connect(self.add_row)
        self.edit_del_row.pressed.connect(self.del_row)
        self.edit_add_col.pressed.connect(self.add_col)
        self.edit_del_col.pressed.connect(self.del_col)

    def add_row(self):
        self.model.insertRow(self.table_view.currentIndex().row())

    def del_row(self):
        row = self.table_view.currentIndex().row()
        self.model.removeRow(row)
        self.table_view.selectRow(row)

    def add_col(self):
        dialog = QW.QDialog()
        layout = QW.QVBoxLayout(dialog)
        layout.addWidget(QW.QLabel("Set Data Name:"))
        input = QW.QLineEdit()
        layout.addWidget(input)
        btn = QW.QPushButton("Ok")
        layout.addWidget(btn)
        btn.pressed.connect(dialog.accept)
        ret = dialog.exec()
        if ret != QW.QDialog.Accepted:
            return

        self.model.insertColumn(2)
        self.model.setHeaderData(2, QC.Qt.Horizontal, input.text())

    def del_col(self):
        col = self.table_view.currentIndex().column()
        self.model.removeColumn(col)
        self.table_view.selectColumn(col)

    def accept(self) -> None:
        self.isotherm.data_raw = self.model._data
        return super().accept()

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(self.table_view.model().columnCount() * 120, 600)

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("IsoEditPointDialog", "Isotherm Data", None, -1))
        self.edit_label.setText(QW.QApplication.translate("IsoEditPointDialog", "Double click to edit individual points.", None, -1))
        self.edit_add_row.setText(QW.QApplication.translate("IsoEditPointDialog", "Insert Row", None, -1))
        self.edit_del_row.setText(QW.QApplication.translate("IsoEditPointDialog", "Delete Row", None, -1))
        self.edit_add_col.setText(QW.QApplication.translate("IsoEditPointDialog", "New data type", None, -1))
        self.edit_del_col.setText(QW.QApplication.translate("IsoEditPointDialog", "Delete data type", None, -1))
        # yapf: enable
