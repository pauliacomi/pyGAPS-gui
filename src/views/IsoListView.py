from qtpy import QtWidgets as QW
from qtpy import QtCore as QC


class IsoListView(QW.QListView):
    """List view that shows the opened list of isotherms."""
    def __init__(self, *args, **kwargs):

        # Initial init
        super().__init__(*args, **kwargs)

        # Setup properties
        self.setUniformItemSizes(True)
        self.setMovement(QW.QListView.Static)
        self.setEditTriggers(QW.QAbstractItemView.DoubleClicked)
        self.setSelectionBehavior(QW.QAbstractItemView.SelectItems)
        self.setSelectionMode(QW.QAbstractItemView.SingleSelection)
        self.setDragDropMode(QW.QAbstractItemView.NoDragDrop)

    def keyPressEvent(self, event):
        if event.key() == QC.Qt.Key_Delete:
            self.model().removeRow(self.currentIndex().row())
            return
        super().keyPressEvent(event)

    # If we want to move isotherms by drag and drop QT messes up the selection
    # This results in the item check / plot errors
    # So we just say it's impossible (for now)
    #
    # def rowsAboutToBeRemoved(self, parent: QC.QModelIndex, start: int, end: int) -> None:
    #     selection_model = self.selectionModel()
    #     selection_model.blockSignals(True)
    #     super().rowsAboutToBeRemoved(parent, start, end)
    #     selection_model.blockSignals(False)
    #     old_index = self.model().index(start - 1, 0)
    #     new_index = self.model().index(self.selection, 0)
    #     selection_model.select(new_index, QC.QItemSelectionModel.ClearAndSelect)
    #     selection_model.currentChanged.emit(new_index, old_index)

    # def rowsInserted(self, parent: QC.QModelIndex, start: int, end: int) -> None:
    #     self.selection = start
    #     if end > start:
    #         self.selection = start - 1
    #     self.model().item(self.selection).setCheckState(QC.Qt.Unchecked)
    #     return super().rowsInserted(parent, start, end)
