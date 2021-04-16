from qtpy import QtCore, QtGui, QtWidgets


class DataDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("DataDialog")
        Dialog.resize(400, 300)

        self.layout = QtWidgets.QVBoxLayout(Dialog)
        self.layout.setObjectName("layout")

        # Table View
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setObjectName("tableView")
        self.layout.addWidget(self.tableView)

        # QTableView Headers
        self.horizontal_header = self.tableView.horizontalHeader()
        self.vertical_header = self.tableView.verticalHeader()
        self.horizontal_header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        self.vertical_header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        self.horizontal_header.setStretchLastSection(True)

        # Button box
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.layout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)

        # Button box connections
        QtCore.QObject.connect(
            self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept
        )
        QtCore.QObject.connect(
            self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject
        )
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QtWidgets.QApplication.translate(
                "DataDialog", "Isotherm Data", None, -1
            )
        )
