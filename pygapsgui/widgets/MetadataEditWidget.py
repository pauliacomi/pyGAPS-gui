from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.models.MetadataTableModel import MetadataTableModel
from pygapsgui.views.MetadataTableView import MetadataTableView
from pygapsgui.widgets.SciDoubleSpinbox import SciFloatDelegate
from pygapsgui.widgets.UtilityDialogs import error_dialog


class MetadataEditWidget(QW.QWidget):
    """
    A widget to set/change/delete metadata from pyGAPS classes.

    Implements both a MetadataTableView/MetadataTableModel pair.
    """

    changed = QC.Signal()
    metadata_table_model: MetadataTableModel = None
    metadata_table_view: MetadataTableView = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.meta_types = ["text", "number", "list"]
        self.setup_UI()
        self.connect_signals()
        self.translate_UI()

    def setup_UI(self):
        """Create and set-up static UI elements."""

        _layout = QW.QGridLayout(self)

        # metadata
        self.name_label = QW.QLabel()
        self.name_label.setObjectName("name_label")
        self.name_input = QW.QLineEdit(self)
        self.name_input.setObjectName("name_input")
        self.value_label = QW.QLabel()
        self.value_label.setObjectName("value_label")
        self.value_input = QW.QLineEdit(self)
        self.value_input.setObjectName("value_input")
        self.type_input = QW.QComboBox()
        self.type_input.setObjectName("type_input")
        self.type_input.addItems(self.meta_types)

        _layout.addWidget(self.name_label, 0, 0, 1, 1)
        _layout.addWidget(self.value_label, 1, 0, 1, 1)
        _layout.addWidget(self.name_input, 0, 1, 1, 2)
        _layout.addWidget(self.type_input, 0, 3, 1, 1)
        _layout.addWidget(self.value_input, 1, 1, 1, 3)

        # buttons
        self.save_button = QW.QPushButton()
        self.save_button.setObjectName("save_button")
        self.delete_button = QW.QPushButton()
        self.delete_button.setObjectName("delete_button")

        _layout.addWidget(self.save_button, 2, 0, 1, 2)
        _layout.addWidget(self.delete_button, 2, 2, 1, 2)

        # table
        self.metadata_table_view = MetadataTableView()
        delegate = SciFloatDelegate()
        self.metadata_table_view.setItemDelegate(delegate)
        _layout.addWidget(self.metadata_table_view, 3, 0, 1, 4)

    def connect_signals(self):
        """Connect permanent signals."""
        self.save_button.clicked.connect(self.metadata_save)
        self.delete_button.clicked.connect(self.metadata_delete)

    def set_model(self, coreclass):
        """Connect a suitable model."""
        self.metadata_table_model = MetadataTableModel(coreclass)
        self.metadata_table_view.setModel(self.metadata_table_model)
        self.metadata_table_view.selectionModel().selectionChanged.connect(self.metadata_select)

    def display(self, name, value, mtype):
        """Display one metadata."""
        self.name_input.setText(str(name))
        self.value_input.setText(str(value))
        self.type_input.setCurrentIndex(self.meta_types.index(str(mtype)))

    def clear(self):
        """Clear all data and reset."""
        self.name_input.clear()
        self.value_input.clear()
        self.type_input.setCurrentIndex(0)

    def metadata_select(self):
        """Update display when a metadata point is selected."""
        index = self.metadata_table_view.currentIndex()
        if not index or not index.isValid():
            return
        data = self.metadata_table_model.rowData(index)
        if data:
            self.display(*data)
        else:
            self.clear()

    def metadata_save(self):
        """Save a metadata point."""
        meta_name = self.name_input.text()
        meta_value = self.value_input.text()
        meta_type = self.type_input.currentText()
        if not meta_name:
            error_dialog("Fill property name!")
            return
        if not meta_value:
            error_dialog("Fill property value!")
            return

        if meta_type == "number":
            try:
                meta_value = float(meta_value)
            except ValueError:
                error_dialog("Could not convert metadata value to number.")
                return

        self.metadata_table_model.setOrInsertRow(data=[meta_name, meta_value, meta_type])
        self.metadata_table_view.resizeColumns()
        self.changed.emit()

    def metadata_save_bulk(self, results: dict):
        """Save multiple metadatas from a dictionary."""
        if not results:
            return

        for meta_name, meta_value in results.items():
            if isinstance(meta_value, (int, float)):
                self.metadata_table_model.setOrInsertRow(data=[meta_name, meta_value, "number"])
            elif isinstance(meta_value, (list, tuple)):
                self.metadata_table_model.setOrInsertRow(data=[meta_name, meta_value, "list"])
            else:
                self.metadata_table_model.setOrInsertRow(data=[meta_name, meta_value, "text"])

        self.metadata_table_view.resizeColumns()
        self.changed.emit()

    def metadata_delete(self):
        """Delete a metadata point."""
        index = self.metadata_table_view.currentIndex()
        if not index.isValid():
            return
        self.metadata_table_model.removeRow(index.row())
        self.changed.emit()

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.name_label.setText(QW.QApplication.translate("MetaEditWidget", "Name", None, -1))
        self.value_label.setText(QW.QApplication.translate("MetaEditWidget", "Value", None, -1))
        self.save_button.setText(QW.QApplication.translate("MetaEditWidget", "save", None, -1))
        self.delete_button.setText(QW.QApplication.translate("MetaEditWidget", "delete", None, -1))
        # yapf: enable
