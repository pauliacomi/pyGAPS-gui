from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from pygapsgui.widgets.UtilityWidgets import MovableListWidget


class IsoGraphLegendSel(QW.QDialog):
    """Dialog that allows a selection of what isotherm data will be plotted on the x/y1/y2 axes."""

    changed: bool = False
    default: "list[str]" = [
        "material",
        "adsorbate",
        "temperature",
        "branch",
        "key",
    ]  # do not modify
    available: "list[str]" = None

    def __init__(self, current, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.current = current if current else self.default.copy()

        self.setupData()
        self.setup_UI()
        self.connect_signals()

    def setup_UI(self):
        """Create and set-up static UI elements."""
        self.data_layout = QW.QFormLayout(self)
        self.list_widget = MovableListWidget()
        self.list_widget.label.setText("Metadata:")
        self.top_label = QW.QLabel("Select which keys are part of the legend.")

        for text in self.available:
            item = QW.QListWidgetItem(text)
            item.setFlags(item.flags() | QC.Qt.ItemIsUserCheckable)
            if text in self.current:
                item.setCheckState(QC.Qt.Checked)
            else:
                item.setCheckState(QC.Qt.Unchecked)
            self.list_widget.list.addItem(item)

        self.data_layout.addWidget(self.top_label)
        self.data_layout.addWidget(self.list_widget)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Ok | QW.QDialogButtonBox.Close)
        self.data_layout.addWidget(self.button_box)

    def setupData(self):
        """Refresh or select available keys."""
        self.available = self.current + [key for key in self.default if key not in self.current]

    def connect_signals(self):
        """Connect permanent signals."""
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_checked(self):
        """Get a list of all list checked items."""
        lw = self.list_widget.list
        checked = [
            lw.item(x).text() for x in range(lw.count()) if lw.item(x).checkState() is QC.Qt.Checked
        ]
        return checked
