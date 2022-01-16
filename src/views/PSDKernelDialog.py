from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView

from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class PSDKernelDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("PSDKernelDialog")

        layout = QW.QGridLayout(self)
        layout.setObjectName("layout")

        self.optionsBox = QW.QGroupBox(self)
        layout.addWidget(self.optionsBox, 0, 0, 1, 1)
        self.rGraphsBox = QW.QGroupBox(self)
        layout.addWidget(self.rGraphsBox, 1, 0, 1, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)

        # Options box
        self.options_layout = QW.QHBoxLayout(self.optionsBox)

        ## Iso graph and slider
        self.isoGraph = IsoGraphView(x_range_select=True, parent=self)
        self.isoGraph.setObjectName("isoGraph")
        self.x_select = self.isoGraph.x_range_select
        self.options_layout.addWidget(self.isoGraph)

        ## Options sub box
        self.optionsSubLayout = QW.QGridLayout()
        self.options_layout.addLayout(self.optionsSubLayout)

        ## Branch used
        self.branchLabel = LabelAlignRight("Branch used:")
        self.optionsSubLayout.addWidget(self.branchLabel, 0, 0, 1, 1)
        self.branchDropdown = QW.QComboBox(self)
        self.optionsSubLayout.addWidget(self.branchDropdown, 0, 1, 1, 1)

        ## Kernel model
        self.kernelLabel = LabelAlignRight("Kernel used:")
        self.optionsSubLayout.addWidget(self.kernelLabel, 1, 0, 1, 1)
        self.kernelDropdown = QW.QComboBox(self)
        self.optionsSubLayout.addWidget(self.kernelDropdown, 1, 1, 1, 1)

        ## spline smoothing
        self.smoothLabel = LabelAlignRight("Spline fit order:")
        self.optionsSubLayout.addWidget(self.smoothLabel, 2, 0, 1, 1)
        self.smoothEdit = QW.QSpinBox(self)
        self.smoothEdit.setMinimum(0)
        self.optionsSubLayout.addWidget(self.smoothEdit, 2, 1, 1, 1)

        ## Autodetermine
        self.autoButton = QW.QPushButton(self)
        self.optionsSubLayout.addWidget(self.autoButton, 3, 0, 1, 2)

        # Results graph box
        self.rGraphsLayout = QW.QVBoxLayout(self.rGraphsBox)

        ## PSD graph
        self.res_graph = GraphView(parent=self)
        self.rGraphsLayout.addWidget(self.res_graph)

        # TODO Add a second graph that shows the fit of the kernel

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox(self)
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Close)
        layout.addWidget(self.button_box, 2, 0, 1, 1)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(800, 900)

    def connect_signals(self):
        pass

    def translate_UI(self):
        self.setWindowTitle(
            QW.QApplication.translate("PSDKernelDialog", "Calculate kernel fit PSD", None, -1)
        )
        self.optionsBox.setTitle(QW.QApplication.translate("PSDKernelDialog", "Options", None, -1))
        self.rGraphsBox.setTitle(QW.QApplication.translate("PSDKernelDialog", "Results", None, -1))
        self.autoButton.setText(QW.QApplication.translate("PSDKernelDialog", "Calculate", None, -1))
