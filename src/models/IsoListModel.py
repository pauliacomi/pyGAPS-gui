from PySide2 import QtGui, QtCore


class IsoListModel(QtGui.QStandardItemModel):
    """Overloading an item model to store a list of isotherms."""

    checkedChanged = QtCore.Signal()
    oldCurrent = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itemChanged.connect(self.check_ticked)

    def get_iso_index(self, index):
        iso = self.itemFromIndex(index)
        return iso.data() if iso else None

    def get_iso_checked(self):
        return [
            self.item(row, 0).data() for row in range(self.rowCount())
            if self.item(row, 0).checkState() == QtCore.Qt.Checked
        ]

    def check_ticked(self, item):
        """If an item was changed, verify it was a tick mark."""
        if item.index() == self.oldCurrent:
            self.blockSignals(True)
            item.setCheckState(QtCore.Qt.Checked)
            self.blockSignals(False)
            return
        if item.checkState() != item.oldCheckState:
            item.oldCheckState = QtCore.Qt.Checked if item.checkState() else QtCore.Qt.Unchecked
            self.checkedChanged.emit()

    def check_selected(self, index):
        """Check one isotherm while restoring previous state."""
        if self.oldCurrent:
            oldItem = self.itemFromIndex(self.oldCurrent)
            if oldItem:
                self.blockSignals(True)
                oldItem.setCheckState(oldItem.userCheckState)
                if oldItem.checkState() != oldItem.oldCheckState:
                    oldItem.oldCheckState = QtCore.Qt.Checked if oldItem.checkState() else QtCore.Qt.Unchecked
                self.blockSignals(False)
        newItem = self.itemFromIndex(index)
        if newItem:
            newItem.userCheckState = newItem.checkState()
            newItem.setCheckState(QtCore.Qt.Checked)
            if newItem.userCheckState == QtCore.Qt.Checked:
                self.checkedChanged.emit()
            self.oldCurrent = index

    def tick_all(self):
        """Tick all items and mark them for display."""
        if self.rowCount() > 0:
            self.blockSignals(True)
            for row in range(self.rowCount()):
                item = self.item(row)
                item.setCheckState(QtCore.Qt.Checked)
                item.oldCheckState = QtCore.Qt.Checked
                if item.index() != self.oldCurrent:
                    item.userCheckState = QtCore.Qt.Unchecked
                else:
                    item.userCheckState = QtCore.Qt.Checked
            self.blockSignals(False)
            self.layoutChanged.emit()
            self.checkedChanged.emit()

    def untick_all(self):
        """Un-tick all items and update selection."""
        if self.rowCount() > 0:
            self.blockSignals(True)
            for row in range(self.rowCount()):
                item = self.item(row)
                if item.index() != self.oldCurrent:
                    item.setCheckState(QtCore.Qt.Unchecked)
                    item.oldCheckState = QtCore.Qt.Unchecked
                item.userCheckState = QtCore.Qt.Unchecked
            self.blockSignals(False)
            self.layoutChanged.emit()
            self.checkedChanged.emit()
