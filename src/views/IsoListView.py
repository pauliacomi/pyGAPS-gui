from qtpy import QtWidgets as QW
from qtpy import QtCore as QC


class IsoListView(QW.QListView):
    """List view that shows the opened list of isotherms."""

    # Ask to delete current isotherm
    delete_current_iso = QC.Signal()

    def __init__(self, parent=None):

        # Initial init
        super().__init__(parent)

        self.setEditTriggers(QW.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QW.QAbstractItemView.SingleSelection)
        self.setMovement(QW.QListView.Snap)
        self.setDragDropMode(QW.QAbstractItemView.InternalMove)

    def keyPressEvent(self, event):
        if event.key() == QC.Qt.Key_Delete:
            self.delete_current_iso.emit()
            return
        super().keyPressEvent(event)
