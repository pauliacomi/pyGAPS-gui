from qtpy import QtCore as QC
from qtpy import QtWidgets as QW
from qtpy import QtSvg as QS
from src.models.AdsPropTableModel import AdsPropTableModel

from src.widgets.MetadataEditWidget import MetadataEditWidget
from src.utilities.tex2svg import tex2svg


class AdsorbateView(QW.QDialog):
    def __init__(self, adsorbate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adsorbate = adsorbate
        self.setupUi()
        self.setupModel()
        self.connectSignals()
        self.retranslateUi()

    def setupUi(self):
        self.setObjectName("AdsorbateView")
        self.resize(400, 500)

        # Create/set layout
        layout = QW.QVBoxLayout(self)

        # Create widgets
        #
        # Named properties
        self.propertiesWidget = QW.QWidget(self)
        self.propertiesLayout = QW.QFormLayout(self.propertiesWidget)
        self.propertiesLayout.setObjectName("propertiesLayout")

        self.adsNameLabel = QW.QLabel(self.propertiesWidget)
        self.adsNameValue = QW.QLabel(self.propertiesWidget)
        self.adsAliasLabel = QW.QLabel(self.propertiesWidget)
        self.adsAliasValues = QW.QListWidget(self.propertiesWidget)
        self.adsFormulaLabel = QW.QLabel(self.propertiesWidget)
        self.adsFormulaValue = QS.QSvgWidget(self.propertiesWidget)
        self.adsBackendLabel = QW.QLabel(self.propertiesWidget)
        self.adsBackendValue = QW.QLabel(self.propertiesWidget)
        self.propertiesLayout.addRow(self.adsNameLabel, self.adsNameValue)
        self.propertiesLayout.addRow(self.adsAliasLabel, self.adsAliasValues)
        self.propertiesLayout.addRow(self.adsFormulaLabel, self.adsFormulaValue)
        self.propertiesLayout.addRow(self.adsBackendLabel, self.adsBackendValue)

        layout.addWidget(self.propertiesWidget)

        # metadata edit widget
        self.metaButtonWidget = MetadataEditWidget(self)
        layout.addWidget(self.metaButtonWidget)

        # Table view
        self.tableWidget = QW.QTableWidget(self)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Metadata", "Value", "Type"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QW.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QW.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QW.QHeaderView.ResizeToContents)
        layout.addWidget(self.tableWidget)

        # Button box
        self.buttonBox = QW.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QC.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QW.QDialogButtonBox.Cancel | QW.QDialogButtonBox.Ok)
        layout.addWidget(self.buttonBox)

    def setupModel(self):
        self.adsNameValue.setText(self.adsorbate.name)
        self.adsAliasValues.addItems(self.adsorbate.alias)
        self.adsAliasValues.setFixedHeight(
            self.adsAliasValues.sizeHintForRow(0) * 4 + 2 * self.adsAliasValues.frameWidth()
        )
        self.adsFormulaValue.load(tex2svg(self.adsorbate.formula))
        aspectRatioMode = QC.Qt.AspectRatioMode(QC.Qt.KeepAspectRatio)
        self.adsFormulaValue.renderer().setAspectRatioMode(aspectRatioMode)
        if self.adsorbate.properties.get("backend_name"):
            backend = "Yes"
        else:
            backend = "No"
        self.adsBackendValue.setText(backend)

        props = [(prop, self.adsorbate.properties[prop])
                 for prop in self.adsorbate.properties
                 if prop not in self.adsorbate._reserved_params]
        self.tableWidget.setRowCount(len(props))
        for row, prop in enumerate(props):
            metaItem = QW.QTableWidgetItem()
            metaItem.setText(str(prop[0]))
            self.tableWidget.setItem(row, 0, metaItem)
            nameItem = QW.QTableWidgetItem()
            nameItem.setText(str(prop[1]))
            self.tableWidget.setItem(row, 1, nameItem)
            typeBox = QW.QComboBox()
            typeBox.addItems(["text", "number"])
            if type(prop[1]) == str:
                typeBox.setCurrentIndex(0)
            else:
                typeBox.setCurrentIndex(1)
            self.tableWidget.setCellWidget(row, 2, typeBox)
        self.tableWidget.verticalHeader().setVisible(False)

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
        nrows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(nrows)
        self.tableWidget.setItem(nrows, 0, QW.QTableWidgetItem(str(propName)))
        self.tableWidget.scrollToBottom()
        typeBox = QW.QComboBox()
        typeBox.addItems(["text", "number"])
        self.tableWidget.setCellWidget(nrows, 2, typeBox)
        self.tableWidget.selectRow(nrows)

        # self.tableModel.insertRows(self.tableModel.rowCount(), val=propName)
        # self.tableView.scrollToBottom()
        # self.tableView.selectRow(self.tableModel.rowCount() - 1)

    def extra_prop_edit(self):
        index = self.tableWidget.selectionModel().currentIndex()
        if index:
            self.tableWidget.edit(index)

        # index = self.tableView.selectionModel().currentIndex()
        # if index:
        #     self.tableView.edit(index)

    def extra_prop_delete(self):
        index = self.tableWidget.selectionModel().currentIndex()
        self.tableWidget.removeRow(index)
        # index = self.tableView.selectionModel().currentIndex()
        # self.tableModel.removeRow(index.row())

    def retranslateUi(self):
        self.setWindowTitle(QW.QApplication.translate("AdsorbateView", "Adsorbate details", None, -1))
        self.adsNameLabel.setText(QW.QApplication.translate("AdsorbateView", "Adsorbate Name", None, -1))
        self.adsAliasLabel.setText(QW.QApplication.translate("AdsorbateView", "Adsorbate Aliases", None, -1))
        self.adsFormulaLabel.setText(QW.QApplication.translate("AdsorbateView", "Adsorbate Formula", None, -1))
        self.adsBackendLabel.setText(QW.QApplication.translate("AdsorbateView", "Thermodynamic backend", None, -1))
