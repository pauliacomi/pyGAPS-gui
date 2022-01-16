from qtpy import QtWidgets as QW
from qtpy import QtGui as QG
from qtpy import QtCore as QC


class MetadataEditWidget(QW.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.meta_types = ["text", "number"]
        self.setup_UI()
        self.translate_UI()

    def setup_UI(self):

        # metadata buttons
        layout = QW.QGridLayout(self)

        self.nameLabel = QW.QLabel(self)
        self.nameLabel.setObjectName("nameLabel")
        layout.addWidget(self.nameLabel, 0, 0, 1, 1)

        self.valueLabel = QW.QLabel(self)
        self.valueLabel.setObjectName("valueLabel")
        layout.addWidget(self.valueLabel, 1, 0, 1, 1)

        self.nameEdit = QW.QLineEdit(self)
        self.nameEdit.setObjectName("nameEdit")
        layout.addWidget(self.nameEdit, 0, 1, 1, 2)

        self.typeEdit = QW.QComboBox(self)
        self.typeEdit.setObjectName("typeEdit")
        self.typeEdit.addItems(self.meta_types)
        layout.addWidget(self.typeEdit, 0, 3, 1, 1)

        self.valueEdit = QW.QLineEdit(self)
        self.valueEdit.setObjectName("valueEdit")
        layout.addWidget(self.valueEdit, 1, 1, 1, 3)

        self.propButtonSave = QW.QPushButton(self)
        self.propButtonSave.setObjectName("propButtonSave")
        layout.addWidget(self.propButtonSave, 2, 0, 1, 2)

        self.propButtonDelete = QW.QPushButton(self)
        self.propButtonDelete.setObjectName("propButtonDelete")
        layout.addWidget(self.propButtonDelete, 2, 2, 1, 2)

    def translate_UI(self):
        self.nameLabel.setText(QW.QApplication.translate("MetaEditWidget", "Name", None, -1))
        self.valueLabel.setText(QW.QApplication.translate("MetaEditWidget", "Value", None, -1))
        self.propButtonSave.setText(QW.QApplication.translate("MetaEditWidget", "save", None, -1))
        self.propButtonDelete.setText(
            QW.QApplication.translate("MetaEditWidget", "delete", None, -1)
        )

    def display(self, name, value, mtype):

        self.nameEdit.setText(str(name))
        self.valueEdit.setText(str(value))
        self.typeEdit.setCurrentIndex(self.meta_types.index(str(mtype)))

    def clear(self):

        self.nameEdit.clear()
        self.valueEdit.clear()
        self.typeEdit.setCurrentIndex(0)
