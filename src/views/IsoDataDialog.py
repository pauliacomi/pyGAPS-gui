from qtpy import QtCore as QC
from qtpy import QtWidgets as QW


class IsoDataDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()
        self.retranslateUi()
        self.connectSignals()

    def setupUi(self):
        self.setObjectName("IsoDataDialog")
        self.resize(400, 300)

        # Create/set layout
        layout = QW.QVBoxLayout(self)

        # Table View
        self.tableView = QW.QTableView(self)
        layout.addWidget(self.tableView)

        # QTableView Headers
        self.horizontal_header = self.tableView.horizontalHeader()
        self.vertical_header = self.tableView.verticalHeader()
        self.horizontal_header.setSectionResizeMode(QW.QHeaderView.ResizeToContents)
        self.vertical_header.setSectionResizeMode(QW.QHeaderView.ResizeToContents)
        self.horizontal_header.setStretchLastSection(True)

        # Button box
        self.buttonBox = QW.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QC.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QW.QDialogButtonBox.Cancel | QW.QDialogButtonBox.Ok)
        layout.addWidget(self.buttonBox)

    def connectSignals(self):
        # Button box connections
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        self.setWindowTitle(QW.QApplication.translate("IsoDataDialog", "Isotherm Data", None, -1))
