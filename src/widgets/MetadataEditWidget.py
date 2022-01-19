from qtpy import QtWidgets as QW
from qtpy import QtGui as QG
from qtpy import QtCore as QC


class MetadataEditWidget(QW.QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.meta_types = ["text", "number"]
        self.setup_UI()
        self.translate_UI()

    def setup_UI(self):

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

    def display(self, name, value, mtype):

        self.name_input.setText(str(name))
        self.value_input.setText(str(value))
        self.type_input.setCurrentIndex(self.meta_types.index(str(mtype)))

    def clear(self):

        self.name_input.clear()
        self.value_input.clear()
        self.type_input.setCurrentIndex(0)

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.name_label.setText(QW.QApplication.translate("MetaEditWidget", "Name", None, -1))
        self.value_label.setText(QW.QApplication.translate("MetaEditWidget", "Value", None, -1))
        self.save_button.setText(QW.QApplication.translate("MetaEditWidget", "save", None, -1))
        self.delete_button.setText(QW.QApplication.translate("MetaEditWidget", "delete", None, -1))
        # yapf: enable
