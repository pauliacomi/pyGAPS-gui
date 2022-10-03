from qtpy import QtCore as QC
from qtpy import QtWidgets as QW


class IsoGraphLegendSel(QW.QDialog):
    """Dialog that allows a selection of what isotherm data will be plotted on the x/y1/y2 axes."""

    changed = False

    def __init__(self, current, available, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.current = current if current else []
        self.available = available

        self.setup_UI()
        self.setupData()
        self.connect_signals()

    def setup_UI(self):
        """Create and set-up static UI elements."""
        self.data_layout = QW.QFormLayout(self)
        self.list_options = QW.QListWidget()
        # self.list_options.setDragDropMode(QW.QAbstractItemView.InternalMove) # TODO drag and drop to arrange?
        self.top_label = QW.QLabel("Select which keys are part of the legend.")

        for text in self.available:
            item = QW.QListWidgetItem(text)
            item.setFlags(item.flags() | QC.Qt.ItemIsUserCheckable)
            if text in self.current:
                item.setCheckState(QC.Qt.Checked)
            else:
                item.setCheckState(QC.Qt.Unchecked)
            self.list_options.addItem(item)

        self.data_layout.addWidget(self.top_label)
        self.data_layout.addWidget(self.list_options)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Ok | QW.QDialogButtonBox.Close)
        self.data_layout.addWidget(self.button_box)

    def setupData(self):
        pass

    def connect_signals(self):
        """Connect permanent signals."""
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_checked(self):
        lw = self.list_options
        checked = [
            lw.item(x).text() for x in range(lw.count()) if lw.item(x).checkState() is QC.Qt.Checked
        ]
        return checked
