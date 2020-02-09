from PySide2 import QtGui, QtCore


class IsoListModel(QtGui.QStandardItemModel):
    """Overloading an item model to store a list of isotherms."""

    checkedChanged = QtCore.Signal()
    selected_iso_indices = []
    old_check_state = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itemChanged.connect(self.check_ticked)

    def get_iso_index(self, index):
        iso = self.itemFromIndex(index)
        return iso.data() if iso else None

    def check_ticked(self, item):
        """If an item was changed, verify it was a tick mark and add to list."""
        index = item.index()
        if item.checkState() == QtCore.Qt.Checked:
            if index not in self.selected_iso_indices:
                self.selected_iso_indices.append(index)
                self.checkedChanged.emit()
        elif item.checkState() == QtCore.Qt.Unchecked:
            if index in self.selected_iso_indices:
                self.selected_iso_indices.remove(index)
                self.checkedChanged.emit()

    def check(self, index):
        """Check one isotherm while restoring previous state."""
        if self.old_check_state:
            item = self.itemFromIndex(self.old_check_state[0])
            if item:
                item.setCheckState(self.old_check_state[1])
        item = self.itemFromIndex(index)
        if item:
            self.old_check_state = (index, item.checkState())
            item.setCheckState(QtCore.Qt.Checked)

    def check_all(self):
        """Check all items and mark them for display."""
        if self.rowCount() > 0:
            self.blockSignals(True)
            for row in range(self.rowCount()):
                item = self.item(row)
                item.setCheckState(QtCore.Qt.Checked)
                index = item.index()
                if index not in self.selected_iso_indices:
                    self.selected_iso_indices.append(index)
            self.blockSignals(False)
            self.checkedChanged.emit()

    def uncheck_all(self):
        """Un-check all items and update selection."""
        if self.rowCount() > 0:
            self.blockSignals(True)
            for row in range(self.rowCount()):
                item = self.item(row)
                item.setCheckState(QtCore.Qt.Unchecked)
            self.selected_iso_indices.clear()
            self.blockSignals(False)
            self.checkedChanged.emit()
