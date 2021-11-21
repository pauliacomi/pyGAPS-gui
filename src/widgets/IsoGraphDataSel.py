from itertools import chain

from qtpy import QtWidgets as QW
from qtpy import QtCore as QC


class IsoGraphDataSel(QW.QDialog):

    datas = None
    x_data = None
    y1_data = None
    y2_data = None

    changed = False

    def __init__(self, datas, x_data, y1_data, y2_data, parent=None) -> None:
        super().__init__(parent=parent)

        self.datas = datas
        self.x_data = x_data
        self.y1_data = y1_data
        self.y2_data = y2_data

        self.setupUI()
        self.setupData()
        self.connectSignals()

    def setupUI(self):
        self.dataLayout = QW.QFormLayout(self)

        self.xCombo = QW.QComboBox(self)
        self.y1Combo = QW.QComboBox(self)
        self.y2Combo = QW.QComboBox(self)

        self.dataLayout.addRow(
            QW.QLabel("X Axis Data"),
            self.xCombo,
        )
        self.dataLayout.addRow(
            QW.QLabel("Y1 Axis Data"),
            self.y1Combo,
        )
        self.dataLayout.addRow(
            QW.QLabel("Y2 Axis Data"),
            self.y2Combo,
        )

        # Bottom buttons
        self.buttonBox = QW.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QC.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QW.QDialogButtonBox.Ok | QW.QDialogButtonBox.Close
        )
        self.buttonBox.setObjectName("buttonBox")
        self.dataLayout.addWidget(self.buttonBox)

    def setupData(self):
        self.xCombo.addItems(self.datas)
        self.xCombo.setCurrentText(self.x_data)
        self.y1Combo.addItems(self.datas)
        self.y1Combo.setCurrentText(self.y1_data)

        if self.y2_data:
            self.y2Combo.addItems(self.datas)
            self.y2Combo.setCurrentText(self.y2_data)
        else:
            self.y2Combo.setDisabled(True)

    def connectSignals(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.xCombo.currentIndexChanged.connect(self.handleChanged)
        self.y1Combo.currentIndexChanged.connect(self.handleChanged)
        self.y2Combo.currentIndexChanged.connect(self.handleChanged)

    def handleChanged(self):
        self.changed = True

        self.x_data = self.xCombo.currentText()
        self.y1_data = self.y1Combo.currentText()
        self.y2_data = self.y2Combo.currentText()
