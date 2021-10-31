from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.models.MatPropTableModel import MatPropTableModel
from src.widgets.MetadataEditWidget import MetadataEditWidget


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

        # metadata edit widget
        self.metaButtonWidget = MetadataEditWidget(self)
        layout.addWidget(self.metaButtonWidget)

        # Table view
        self.tableView = QW.QTableView(self)
        self.tableView.setSelectionBehavior(QW.QTableView.SelectRows)
        self.tableView.verticalHeader().setVisible(False)

        horizontalHTable = self.tableView.horizontalHeader()
        horizontalHTable.setSectionResizeMode(QW.QHeaderView.ResizeToContents)
        horizontalHTable.setStretchLastSection(True)
        verticalHTable = self.tableView.verticalHeader()
        verticalHTable.setSectionResizeMode(QW.QHeaderView.ResizeToContents)

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

        self.metaButtonWidget.propButtonAdd.clicked.connect(self.extra_prop_add)
        self.metaButtonWidget.propButtonEdit.clicked.connect(self.extra_prop_edit)
        self.metaButtonWidget.propButtonDelete.clicked.connect(self.extra_prop_delete)

    def extra_prop_add(self):
        propName = self.metaButtonWidget.propLineEditAdd.text()
        self.metaButtonWidget.propLineEditAdd.clear()
        if not propName:
            return
        self.tableModel.insertRows(self.tableModel.rowCount(), val=propName)
        self.tableView.scrollToBottom()
        self.tableView.selectRow(self.tableModel.rowCount() - 1)

    def accept(self) -> None:

        if self.matNameValue.text() != self.material.name:
            self.material.name = self.matNameValue.text()

        if self.matDensityValue.text() != self.material.density:
            self.material.density = self.matDensityValue.text()

        if self.matMMValue.text() != self.material.molar_mass:
            self.material.molar_mass = self.matMMValue.text()

        # TODO make sure to update isotherm display in parent
        return super().accept()

    def extra_prop_edit(self):
        index = self.tableView.selectionModel().currentIndex()
        if index:
            self.tableView.edit(index)

    def extra_prop_delete(self):
        index = self.tableView.selectionModel().currentIndex()
        self.tableModel.removeRow(index.row())

    def retranslateUi(self):
        self.setWindowTitle(QW.QApplication.translate("MaterialView", "Material details", None, -1))
        self.matNameLabel.setText(QW.QApplication.translate("MaterialView", "Material Name", None, -1))
        self.matDensityLabel.setText(QW.QApplication.translate("MaterialView", "Material Density", None, -1))
        self.matMMLabel.setText(QW.QApplication.translate("MaterialView", "Material Molar Mass", None, -1))
