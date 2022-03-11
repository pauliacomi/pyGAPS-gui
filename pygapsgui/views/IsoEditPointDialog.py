from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.models.IsoDataTableModel import IsoDataTableModel
from pygapsgui.utilities.table_to_clipboard import clipboard_to_table
from pygapsgui.utilities.table_to_clipboard import table_to_clipboard
from pygapsgui.widgets.SciDoubleSpinbox import SciFloatDelegate
from pygapsgui.widgets.SciDoubleSpinbox import SciFloatSpinDelegate
from pygapsgui.widgets.UtilityWidgets import LabelAlignCenter


class IsoEditPointDialog(QW.QDialog):
    """A dialog that allows editing of PointIsotherm points."""
    def __init__(self, isotherm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()

        self.isotherm = isotherm
        self.model = IsoDataTableModel(isotherm.data_raw.copy())
        self.table_view.setModel(self.model)
        self.connect_signals()

    def setup_UI(self):
        """Creates and sets-up static UI elements"""
        self.setObjectName("IsoEditPointDialog")

        # Create/set layout
        _layout = QW.QVBoxLayout(self)

        # Table View
        self.table_view = QW.QTableView()
        sci_delegate = SciFloatSpinDelegate()
        str_delegate = SciFloatDelegate()
        self.table_view.setItemDelegate(str_delegate)
        self.table_view.setItemDelegateForColumn(0, sci_delegate)
        self.table_view.setItemDelegateForColumn(1, sci_delegate)
        self.table_view.setSelectionMode(QW.QAbstractItemView.ContiguousSelection)
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
        """Connect permanent signals."""
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.edit_add_row.pressed.connect(self.add_row)
        self.edit_del_row.pressed.connect(self.del_row)
        self.edit_add_col.pressed.connect(self.add_col)
        self.edit_del_col.pressed.connect(self.del_col)

    def add_row(self):
        """Insert a row at current location."""
        self.model.insertRow(self.table_view.currentIndex().row())

    def del_row(self):
        """Delete current highlighted row."""
        row = self.table_view.currentIndex().row()
        self.model.removeRow(row)
        self.table_view.selectRow(row)

    def add_col(self):
        """Add a data column to the end of the table."""
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

        ncols = self.model.columnCount()
        self.model.insertColumn(ncols)
        self.model.setHeaderData(ncols, QC.Qt.Horizontal, input.text())

    def del_col(self):
        """Delete current highlighted column."""
        col = self.table_view.currentIndex().column()
        self.model.removeColumn(col)
        self.table_view.selectColumn(col)

    def keyPressEvent(self, event):
        """Handle copy/paste."""
        if self.table_view.hasFocus():
            if event.key() == QC.Qt.Key_C and (event.modifiers() & QC.Qt.ControlModifier):
                table_to_clipboard(self.table_view)
                event.accept()
            if event.key() == QC.Qt.Key_V and (event.modifiers() & QC.Qt.ControlModifier):
                clipboard_to_table(self.table_view)
                event.accept()
            else:
                super().keyPressEvent(event)

    def accept(self) -> None:
        """If accepted we commit the data."""
        self.isotherm.data_raw = self.model._data
        return super().accept()

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(self.table_view.model().columnCount() * 120, 600)

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("IsoEditPointDialog", "Isotherm Data", None, -1))
        self.edit_label.setText(QW.QApplication.translate("IsoEditPointDialog", "Double click to edit individual points.", None, -1))
        self.edit_add_row.setText(QW.QApplication.translate("IsoEditPointDialog", "Insert Row", None, -1))
        self.edit_del_row.setText(QW.QApplication.translate("IsoEditPointDialog", "Delete Row", None, -1))
        self.edit_add_col.setText(QW.QApplication.translate("IsoEditPointDialog", "New data type", None, -1))
        self.edit_del_col.setText(QW.QApplication.translate("IsoEditPointDialog", "Delete data type", None, -1))
        # yapf: enable
