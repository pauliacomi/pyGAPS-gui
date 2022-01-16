from qtpy import QtCore as QC
from qtpy import QtWidgets as QW


class IsoDataDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("IsoDataDialog")

        # Create/set layout
        layout = QW.QVBoxLayout(self)

        # Table View
        self.table_view = QW.QTableView(self)
        layout.addWidget(self.table_view)

        # Qtable_view Headers
        self.horizontal_header = self.table_view.horizontalHeader()
        self.vertical_header = self.table_view.verticalHeader()
        self.horizontal_header.setSectionResizeMode(QW.QHeaderView.Stretch)
        self.vertical_header.setSectionResizeMode(QW.QHeaderView.Stretch)

        # Button box
        self.button_box = QW.QDialogButtonBox(self)
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Cancel | QW.QDialogButtonBox.Ok)
        layout.addWidget(self.button_box)

    def connect_signals(self):
        # Button box connections
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(self.table_view.model().columnCount() * 100, 300)

    def translate_UI(self):
        self.setWindowTitle(QW.QApplication.translate("IsoDataDialog", "Isotherm Data", None, -1))
