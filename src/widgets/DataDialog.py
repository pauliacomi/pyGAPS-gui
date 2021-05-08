from qtpy import QtCore as QC
from qtpy import QtWidgets as QW


class DataDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("DataDialog")
        self.resize(400, 300)

        self.layout = QW.QVBoxLayout(self)
        self.layout.setObjectName("layout")

        # Table View
        self.tableView = QW.QTableView(self)
        self.tableView.setObjectName("tableView")
        self.layout.addWidget(self.tableView)

        # QTableView Headers
        self.horizontal_header = self.tableView.horizontalHeader()
        self.vertical_header = self.tableView.verticalHeader()
        self.horizontal_header.setSectionResizeMode(
            QW.QHeaderView.ResizeToContents
        )
        self.vertical_header.setSectionResizeMode(
            QW.QHeaderView.ResizeToContents
        )
        self.horizontal_header.setStretchLastSection(True)

        # Button box
        self.buttonBox = QW.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QC.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QW.QDialogButtonBox.Cancel | QW.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.layout.addWidget(self.buttonBox)

        self.retranslateUi()

        # Button box connections
        QC.QObject.connect(
            self.buttonBox, QC.SIGNAL("accepted()"), self.accept
        )
        QC.QObject.connect(
            self.buttonBox, QC.SIGNAL("rejected()"), self.reject
        )
        QC.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(
            QW.QApplication.translate("DataDialog", "Isotherm Data", None, -1)
        )
