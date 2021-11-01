from qtpy import QtWidgets as QW
from qtpy import QtGui as QG
from qtpy import QtCore as QC


class MetadataTableWidget(QW.QTableView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setSelectionMode(QW.QTableView.SingleSelection)
        self.setSelectionBehavior(QW.QTableView.SelectRows)
        self.verticalHeader().setVisible(False)

        self.verticalHeader().setSectionResizeMode(QW.QHeaderView.ResizeToContents)

    def setModel(self, model: QC.QAbstractItemModel) -> None:
        ret = super().setModel(model)
        self.resizeColumns()
        return ret

    def resizeColumns(self) -> None:
        self.horizontalHeader().setSectionResizeMode(QW.QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QW.QHeaderView.Stretch)
