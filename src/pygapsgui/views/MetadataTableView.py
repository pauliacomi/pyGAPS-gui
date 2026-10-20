from qtpy import QtCore as QC
from qtpy import QtWidgets as QW


class MetadataTableView(QW.QTableView):
    """A TableView optimised to display core class (Isotherm, Adsorbate, Material) metadata."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setSelectionMode(QW.QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QW.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setWordWrap(True)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setSectionResizeMode(QW.QHeaderView.ResizeMode.ResizeToContents)

    def setModel(self, model: QC.QAbstractItemModel) -> None:
        super().setModel(model)
        self.resizeColumns()

    def resizeColumns(self) -> None:
        #     # TODO may be a better way to do this
        self.horizontalHeader().setSectionResizeMode(2, QW.QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QW.QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QW.QHeaderView.ResizeMode.Interactive)
