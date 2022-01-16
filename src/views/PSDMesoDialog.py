from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView

from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class PSDMesoDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("PSDMesoDialog")

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

        ## PSD model
        self.tmodelLabel = LabelAlignRight("PSD model used:")
        self.optionsSubLayout.addWidget(self.tmodelLabel, 1, 0, 1, 1)
        self.tmodelDropdown = QW.QComboBox(self)
        self.optionsSubLayout.addWidget(self.tmodelDropdown, 1, 1, 1, 1)

        ## Thickness function
        self.thicknessLabel = LabelAlignRight("Thickness function:")
        self.optionsSubLayout.addWidget(self.thicknessLabel, 2, 0, 1, 1)
        self.thicknessDropdown = QW.QComboBox(self)
        self.optionsSubLayout.addWidget(self.thicknessDropdown, 2, 1, 1, 1)

        ## Pore geometry
        self.geometryLabel = LabelAlignRight("Pore geometry:")
        self.optionsSubLayout.addWidget(self.geometryLabel, 3, 0, 1, 1)
        self.geometryDropdown = QW.QComboBox(self)
        self.optionsSubLayout.addWidget(self.geometryDropdown, 3, 1, 1, 1)

        ## Kelvin model
        self.kmodelLabel = LabelAlignRight("Kelvin model:")
        self.optionsSubLayout.addWidget(self.kmodelLabel, 4, 0, 1, 1)
        self.kmodelDropdown = QW.QComboBox(self)
        self.optionsSubLayout.addWidget(self.kmodelDropdown, 4, 1, 1, 1)

        # Autodetermine
        self.autoButton = QW.QPushButton(self)
        self.optionsSubLayout.addWidget(self.autoButton, 5, 0, 1, 2)

        # Results graph box
        self.rGraphsLayout = QW.QVBoxLayout(self.rGraphsBox)

        ## PSD graph
        self.res_graph = GraphView(parent=self)
        self.rGraphsLayout.addWidget(self.res_graph)

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
            QW.QApplication.translate("PSDMesoDialog", "Calculate mesoporous PSD", None, -1)
        )
        self.optionsBox.setTitle(QW.QApplication.translate("PSDMesoDialog", "Options", None, -1))
        self.rGraphsBox.setTitle(QW.QApplication.translate("PSDMesoDialog", "Results", None, -1))
        self.autoButton.setText(QW.QApplication.translate("PSDMesoDialog", "Calculate", None, -1))
