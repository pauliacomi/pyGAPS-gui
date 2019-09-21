from PySide2 import QtCore, QtGui, QtWidgets

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView
from src.views.RangeSlider import QHSpinBoxRangeSlider

from src.dialogs.UtilityDialogs import LabelAlignRight


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
        self.layout.addWidget(self.betGraph, 0, 1, 1, 1)

        # Rouquerol plot
        self.rouqGraph = GraphView(Dialog)
        self.rouqGraph.setObjectName("rouqGraph")
        self.layout.addWidget(self.rouqGraph, 1, 1, 1, 1)

        # Options/results box

        self.optionsBox = QtWidgets.QGroupBox('Range and results', Dialog)
        self.layout.addWidget(self.optionsBox, 1, 0, 1, 1)

        self.optionsLayout = QtWidgets.QGridLayout(self.optionsBox)
        self.optionsLayout.addWidget(
            QtWidgets.QLabel("Pressure range:"), 0, 0, 1, 2)
        self.pSlider = QHSpinBoxRangeSlider(parent=self, dec_pnts=2,
                                            slider_range=[0, 1, 0.01], values=[0, 1])
        self.pSlider.setGeometry(200, 200, 200, 100)
        self.pSlider.setEmitWhileMoving(False)
        self.optionsLayout.addWidget(self.pSlider, 1, 0, 1, 4)
        self.optionsLayout.addWidget(
            QtWidgets.QLabel("Calculated results:"), 2, 0, 1, 2)
        self.optionsLayout.addWidget(
            LabelAlignRight("BET area:"), 3, 0, 1, 1)
        self.optionsLayout.addWidget(
            LabelAlignRight("C constant:"), 4, 0, 1, 1)
        self.optionsLayout.addWidget(
            LabelAlignRight("Monolayer uptake:"), 5, 0, 1, 1)
        self.optionsLayout.addWidget(
            LabelAlignRight("Monolayer pressure:"), 6, 0, 1, 1)

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
