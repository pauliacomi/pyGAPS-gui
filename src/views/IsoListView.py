from PySide2 import QtWidgets, QtCore


class IsoListView(QtWidgets.QListView):
    """List view that shows the opened list of isotherms."""

    # Ask to delete current isotherm
    delete_current = QtCore.Signal()

    def __init__(self, parent=None):

        # Initial init
        super().__init__(parent)

        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setMovement(QtWidgets.QListView.Free)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.delete_current.emit()
            return
        super().keyPressEvent(event)
