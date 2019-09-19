from PySide2 import QtCore, QtGui, QtWidgets

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView
from src.views.RangeSlider import QHSpinBoxRangeSlider


class BETDialog(QtWidgets.QDialog):

    isotherm = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("BETDialog")
        Dialog.resize(1000, 800)

        self.layout = QtWidgets.QGridLayout(Dialog)
        self.layout.setObjectName("layout")

        # Isotherm display
        self.isoGraph = GraphView(Dialog)
        self.isoGraph.setObjectName("isoGraph")
        self.layout.addWidget(self.isoGraph, 0, 0, 1, 1)

        # BET plot
        self.betGraph = GraphView(Dialog)
        self.betGraph.setObjectName("betGraph")
        self.layout.addWidget(self.betGraph, 1, 0, 1, 1)

        # Rouquerol plot
        self.rouqGraph = GraphView(Dialog)
        self.rouqGraph.setObjectName("rouqGraph")
        self.layout.addWidget(self.rouqGraph, 1, 1, 1, 1)

        # Tweaking parameters
        # self.tweakingLayout = QtWidgets.QHBoxLayout(self)

        self.pSlider = QHSpinBoxRangeSlider(
            slider_range=[0, 1, 0.02], values=[0, 1])
        self.pSlider.setEmitWhileMoving(False)
        self.layout.addWidget(self.pSlider, 0, 1, 1, 1)

        # self.lSlider = QHSpinBoxRangeSlider(
        #     slider_range=[-5.0, 5.0, 0.5], values=[-2.5, 2.5])
        # self.lSlider.setEmitWhileMoving(True)
        # self.tweakingLayout.addWidget(self.lSlider)

        # self.layout.addWidget(self.tweakingLayout, 0, 1, 1, 1)

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
