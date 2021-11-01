from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.models.MatPropTableModel import MatPropTableModel
from src.widgets.MetadataEditWidget import MetadataEditWidget
from src.widgets.MetadataTableWidget import MetadataTableWidget
from src.widgets.UtilityWidgets import ErrorMessageBox


class MaterialView(QW.QDialog):
    def __init__(self, material, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.material = material
        self.setupUi()
        self.setupModel()
        self.connectSignals()
        self.retranslateUi()

    def setupUi(self):
        self.setObjectName("MaterialView")
        self.resize(400, 500)

        # Create/set layout
        layout = QW.QVBoxLayout(self)

        # Create widgets
        #
        # Named properties
        self.propertiesWidget = QW.QWidget(self)
        self.propertiesLayout = QW.QFormLayout(self.propertiesWidget)
        self.propertiesLayout.setObjectName("propertiesLayout")

        self.matNameLabel = QW.QLabel(self.propertiesWidget)
        self.matNameValue = QW.QLineEdit(self.propertiesWidget)
        self.matDensityLabel = QW.QLabel(self.propertiesWidget)
        self.matDensityValue = QW.QLineEdit(self.propertiesWidget)
        self.matMMLabel = QW.QLabel(self.propertiesWidget)
        self.matMMValue = QW.QLineEdit(self.propertiesWidget)
        self.propertiesLayout.addRow(self.matNameLabel, self.matNameValue)
        self.propertiesLayout.addRow(self.matDensityLabel, self.matDensityValue)
        self.propertiesLayout.addRow(self.matMMLabel, self.matMMValue)

        layout.addWidget(self.propertiesWidget)

        # metadata
        self.metaLabel = QW.QLabel(self)
        layout.addWidget(self.metaLabel)

        # metadata edit widget
        self.metaButtonWidget = MetadataEditWidget(self)
        layout.addWidget(self.metaButtonWidget)

        # Table view
        self.tableView = MetadataTableWidget(self)
        layout.addWidget(self.tableView)

        # Button box
        self.buttonBox = QW.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QC.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QW.QDialogButtonBox.Cancel | QW.QDialogButtonBox.Ok)
        layout.addWidget(self.buttonBox)

    def setupModel(self):
        self.matNameValue.setText(self.material.name)
        density = self.material.density
        density = str(density) if density else density
        self.matDensityValue.setText(density)
        mmass = self.material.molar_mass
        mmass = str(mmass) if mmass else mmass
        self.matMMValue.setText(mmass)

        self.tableModel = MatPropTableModel(self.material)
        self.tableView.setModel(self.tableModel)

    def connectSignals(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.tableView.selectionModel().selectionChanged.connect(self.extra_prop_select)
        self.metaButtonWidget.propButtonSave.clicked.connect(self.extra_prop_save)
        self.metaButtonWidget.propButtonDelete.clicked.connect(self.extra_prop_delete)

    def accept(self) -> None:

        if self.matNameValue.text() != self.material.name:
            self.material.name = self.matNameValue.text()

        if self.matDensityValue.text() != self.material.density:
            self.material.density = self.matDensityValue.text()

        if self.matMMValue.text() != self.material.molar_mass:
            self.material.molar_mass = self.matMMValue.text()

        return super().accept()

    def extra_prop_select(self):
        index = self.tableView.selectionModel().currentIndex()
        if index:
            data = self.tableModel.rowData(index)
            if data:
                self.metaButtonWidget.display(*data)
            else:
                self.metaButtonWidget.clear()

    def extra_prop_save(self):

        propName = self.metaButtonWidget.nameEdit.text()
        propValue = self.metaButtonWidget.valueEdit.text()
        propType = self.metaButtonWidget.typeEdit.currentText()
        if not propName:
            return

        if propType == "number":
            try:
                propValue = float(propValue)
            except ValueError:
                errorbox = ErrorMessageBox()
                errorbox.setText("Could not convert metadata value to number.")
                errorbox.exec_()
                return

        self.tableModel.setOrInsertRow(data=[propName, propValue, propType])
        self.tableView.resizeColumns()

    def extra_prop_delete(self):
        index = self.tableView.selectionModel().currentIndex()
        self.tableModel.removeRow(index.row())

    def retranslateUi(self):
        self.setWindowTitle(QW.QApplication.translate("MaterialView", "Material details", None, -1))
        self.matNameLabel.setText(QW.QApplication.translate("MaterialView", "Material Name", None, -1))
        self.matDensityLabel.setText(QW.QApplication.translate("MaterialView", "Material Density", None, -1))
        self.matMMLabel.setText(QW.QApplication.translate("MaterialView", "Material Molar Mass", None, -1))
        self.metaLabel.setText(QW.QApplication.translate("MaterialView", "Other Metadata", None, -1))
