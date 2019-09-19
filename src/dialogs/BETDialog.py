from PySide2 import QtCore, QtGui, QtWidgets

from src.views.IsoGraphView import IsoGraphView


class BETDialog(QtWidgets.QDialog):

    isotherm = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("BETDialog")
        Dialog.resize(800, 600)

        self.layout = QtWidgets.QVBoxLayout(Dialog)
        self.layout.setObjectName("layout")

        self.isoGraph = IsoGraphView(Dialog)
        self.isoGraph.setObjectName("isoGraph")
        self.layout.addWidget(self.isoGraph)

        # BET plot
        self.betGraph = IsoGraphView(Dialog)
        self.betGraph.setObjectName("betGraph")
        self.layout.addWidget(self.betGraph)

        # Rouquerol plot
        self.rouqGraph = IsoGraphView(Dialog)
        self.rouqGraph.setObjectName("rouqGraph")
        self.layout.addWidget(self.rouqGraph)

        # Bottom buttons
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(
            self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(
            self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate(
            "BETDialog", "BET area calculation", None, -1))
