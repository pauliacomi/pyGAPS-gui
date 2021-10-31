from qtpy import QtWidgets as QW
from qtpy import QtGui as QG
from qtpy import QtCore as QC


class MetadataEditWidget(QW.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setupUi()
        self.retranslateUi()

    def setupUi(self):

        # metadata buttons
        layout = QW.QHBoxLayout(self)

        self.propLabelAdd = QW.QLabel(self)
        self.propLabelAdd.setObjectName("propLabelAdd")
        layout.addWidget(self.propLabelAdd)

        self.propLineEditAdd = QW.QLineEdit(self)
        self.propLineEditAdd.setObjectName("propLineEditAdd")
        layout.addWidget(self.propLineEditAdd)

        self.propButtonAdd = QW.QPushButton(self)
        self.propButtonAdd.setObjectName("propButtonAdd")
        layout.addWidget(self.propButtonAdd)

        propDivideLine = QW.QFrame(self)
        propDivideLine.setFrameShape(QW.QFrame.VLine)
        propDivideLine.setFrameShadow(QW.QFrame.Sunken)
        layout.addWidget(propDivideLine)

        self.propButtonEdit = QW.QPushButton(self)
        self.propButtonEdit.setObjectName("propButtonEdit")
        layout.addWidget(self.propButtonEdit)

        propDivideLine = QW.QFrame(self)
        propDivideLine.setFrameShape(QW.QFrame.VLine)
        propDivideLine.setFrameShadow(QW.QFrame.Sunken)
        layout.addWidget(propDivideLine)

        self.propButtonDelete = QW.QPushButton(self)
        self.propButtonDelete.setObjectName("propButtonDelete")
        layout.addWidget(self.propButtonDelete)

    def retranslateUi(self):
        self.propLabelAdd.setText(QW.QApplication.translate("MainWindowUI", "Metadata", None, -1))
        self.propButtonAdd.setText(QW.QApplication.translate("MainWindowUI", "add", None, -1))
        self.propButtonEdit.setText(QW.QApplication.translate("MainWindowUI", "edit", None, -1))
        self.propButtonDelete.setText(QW.QApplication.translate("MainWindowUI", "del", None, -1))
