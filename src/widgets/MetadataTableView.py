from qtpy import QtWidgets as QW
from qtpy import QtGui as QG
from qtpy import QtCore as QC


class MetadataTableWidget(QW.QTableView):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setSelectionMode(QW.QTableView.SingleSelection)
        self.setSelectionBehavior(QW.QTableView.SelectRows)
        self.verticalHeader().setVisible(False)

        self.verticalHeader().setSectionResizeMode(QW.QHeaderView.ResizeToContents)

    def setModel(self, model: QC.QAbstractItemModel) -> None:
        super().setModel(model)
        self.resizeColumns()

    def resizeColumns(self) -> None:
        # TODO may be a better way to do this
        self.horizontalHeader().setSectionResizeMode(QW.QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QW.QHeaderView.Stretch)
