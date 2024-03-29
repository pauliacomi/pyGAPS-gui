from qtpy import QtCore as QC
from qtpy import QtWidgets as QW


class IsoGraphDataSel(QW.QDialog):
    """Dialog that allows a selection of what isotherm data will be plotted on the x/y1/y2 axes."""

    datas = None
    x_data = None
    y1_data = None
    y2_data = None

    changed = False

    def __init__(self, datas, x_data, y1_data, y2_data, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.datas = datas
        self.x_data = x_data
        self.y1_data = y1_data
        self.y2_data = y2_data

        self.setup_UI()
        self.setup_data(datas, x_data, y1_data, y2_data)
        self.connect_signals()

    def setup_UI(self):
        """Create and set-up static UI elements."""
        self.dataLayout = QW.QFormLayout(self)

        self.xCombo = QW.QComboBox()
        self.y1Combo = QW.QComboBox()
        self.y2Combo = QW.QComboBox()

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
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Ok | QW.QDialogButtonBox.Close)
        self.dataLayout.addWidget(self.button_box)

    def setup_data(self, datas, x_data, y1_data, y2_data):
        self.xCombo.addItems(datas)
        self.xCombo.setCurrentText(x_data)
        self.y1Combo.addItems(datas)
        self.y1Combo.setCurrentText(y1_data)

        if len(datas) > 2:
            self.y2Combo.addItems(["None"] + datas)
            self.y2Combo.setCurrentText(y2_data)
        else:
            self.y2Combo.setDisabled(True)

    def connect_signals(self):
        """Connect permanent signals."""
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.xCombo.currentIndexChanged.connect(self.handle_changed)
        self.y1Combo.currentIndexChanged.connect(self.handle_changed)
        self.y2Combo.currentIndexChanged.connect(self.handle_changed)

    def handle_changed(self):
        self.changed = True

        self.x_data = self.xCombo.currentText()
        self.y1_data = self.y1Combo.currentText()
        y2_data = self.y2Combo.currentText()
        if y2_data == "None":
            y2_data = None
        self.y2_data = y2_data
