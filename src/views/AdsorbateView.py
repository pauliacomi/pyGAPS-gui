from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from qtpy import PYSIDE6
if PYSIDE6:
    import PySide6.QtSvgWidgets as QS
else:
    from qtpy import QtSvg as QS

from src.models.AdsPropTableModel import AdsPropTableModel

from src.widgets.MetadataEditWidget import MetadataEditWidget
from src.widgets.MetadataTableWidget import MetadataTableWidget
from src.utilities.tex2svg import tex2svg
from src.widgets.UtilityWidgets import error_dialog

from pygaps import ADSORBATE_LIST
from pygaps import Adsorbate


class AdsorbateView(QW.QWidget):

    adsorbate = None

    def __init__(self, adsorbate=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        if adsorbate:
            self.adsorbate = adsorbate
            self.setupModel()
            self.connect_signals()
        self.translate_UI()

    def setup_UI(self):
        self.setObjectName("AdsorbateView")
        self.resize(500, 500)

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
        self.adsFormulaValue.setMinimumSize(50, 15)
        self.adsFormulaValue.setMaximumSize(300, 30)
        self.adsBackendLabel = QW.QLabel(self.propertiesWidget)
        self.adsBackendValue = QW.QLabel(self.propertiesWidget)
        self.propertiesLayout.addRow(self.adsNameLabel, self.adsNameValue)
        self.propertiesLayout.addRow(self.adsAliasLabel, self.adsAliasValues)
        self.propertiesLayout.addRow(self.adsFormulaLabel, self.adsFormulaValue)
        self.propertiesLayout.addRow(self.adsBackendLabel, self.adsBackendValue)

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

    def setAdsorbate(self, adsorbate):
        if not adsorbate:
            return

        self.adsorbate = adsorbate
        self.setupModel()
        self.connect_signals()

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

        self.tableModel = AdsPropTableModel(self.adsorbate)
        self.tableView.setModel(self.tableModel)

    def connect_signals(self):

        self.tableView.selectionModel().selectionChanged.connect(self.extra_prop_select)
        self.metaButtonWidget.propButtonSave.clicked.connect(self.extra_prop_save)
        self.metaButtonWidget.propButtonDelete.clicked.connect(self.extra_prop_delete)

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
                error_dialog("Could not convert metadata value to number.")
                return

        self.tableModel.setOrInsertRow(data=[propName, propValue, propType])
        self.tableView.resizeColumns()

    def extra_prop_delete(self):

        index = self.tableView.selectionModel().currentIndex()
        self.tableModel.removeRow(index.row())

    def translate_UI(self):
        self.adsNameLabel.setText(
            QW.QApplication.translate("AdsorbateView", "Adsorbate Name", None, -1)
        )
        self.adsAliasLabel.setText(
            QW.QApplication.translate("AdsorbateView", "Adsorbate Aliases", None, -1)
        )
        self.adsFormulaLabel.setText(
            QW.QApplication.translate("AdsorbateView", "Adsorbate Formula", None, -1)
        )
        self.adsBackendLabel.setText(
            QW.QApplication.translate("AdsorbateView", "Thermodynamic backend", None, -1)
        )
        self.metaLabel.setText(
            QW.QApplication.translate("AdsorbateView", "Other Metadata", None, -1)
        )


class AdsorbateDialog(QW.QDialog):
    def __init__(self, adsorbate, parent=None, **kwargs) -> None:
        super().__init__(parent=parent, **kwargs)

        self.setup_UI()
        self.translate_UI()
        self.connect_signals()
        self.view.setAdsorbate(adsorbate)

    def setup_UI(self):

        layout = QW.QVBoxLayout(self)

        # View
        self.view = AdsorbateView(parent=self)
        layout.addWidget(self.view)

        # Button box
        self.button_box = QW.QDialogButtonBox(self)
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Cancel | QW.QDialogButtonBox.Ok)
        layout.addWidget(self.button_box)

    def connect_signals(self):
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def translate_UI(self):
        self.setWindowTitle(
            QW.QApplication.translate("AdsorbateDialog", "Adsorbate details", None, -1)
        )


class AdsorbateListView(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.setupModel()

    def setup_UI(self):

        layout = QW.QHBoxLayout(self)

        # list
        self.adsorbateList = QW.QListWidget(parent=self)
        layout.addWidget(self.adsorbateList)

        # details
        self.adsorbateDetails = AdsorbateView(parent=self)
        layout.addWidget(self.adsorbateDetails)

    def setupModel(self):
        self.adsorbateList.addItems([ads.name for ads in ADSORBATE_LIST])
        self.adsorbateList.currentItemChanged.connect(self.selectAdsorbate)

    def selectAdsorbate(self, item):
        self.adsorbateDetails.setAdsorbate(Adsorbate.find(item.text()))

    def translate_UI(self):
        self.setWindowTitle(
            QW.QApplication.translate("AdsorbateListView", "pyGAPS Adsorbate explorer", None, -1)
        )
