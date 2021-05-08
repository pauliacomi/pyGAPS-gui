from qtpy import QtCore as QC
from qtpy import QtGui as QG


class IsoListModel(QG.QStandardItemModel):
    """Overloading an item model to store a list of isotherms."""

    checkedChanged = QC.Signal()
    oldCurrent = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itemChanged.connect(self.check_ticked)

    def get_iso_index(self, index):
        """Return an isotherm given an index."""
        iso = self.itemFromIndex(index)
        return iso.data() if iso else None

    def get_iso_checked(self):
        """Return list of checked isotherms."""
        return [
            self.item(row).data()
            for row in range(self.rowCount())
            if self.item(row).checkState() == QC.Qt.Checked
        ]

    def check_ticked(self, item):
        """If an item changed, verify if it was a tick change."""
        # Can never uncheck a selected item
        if item.index() == self.oldCurrent:
            self.blockSignals(True)
            item.setCheckState(QC.Qt.Checked)
            self.blockSignals(False)
            return
        # Mirror state in backup, then emit change
        if item.checkState() != item.oldCheckState:
            item.oldCheckState = item.checkState()
            self.checkedChanged.emit()

    def check_selected(self, index):
        """When isotherm is selected, ensure it is marked checked."""
        # Restore user check state to previous item
        oldItem = None
        if self.oldCurrent:
            oldItem = self.itemFromIndex(self.oldCurrent)
            if oldItem:
                self.blockSignals(True)
                oldItem.setCheckState(oldItem.userCheckState)
                oldItem.oldCheckState = oldItem.userCheckState
                self.blockSignals(False)
        # Save user check state and mark selected item as checked
        newItem = self.itemFromIndex(index)
        if newItem:
            newItem.userCheckState = newItem.checkState()
            # Depending on the previous state
            # we either change to checked or just refresh
            if newItem.userCheckState == QC.Qt.Unchecked:
                newItem.setCheckState(QC.Qt.Checked)
            # refresh is done when we change the isotherms
            elif oldItem and oldItem.oldCheckState == QC.Qt.Unchecked:
                self.checkedChanged.emit()
            self.oldCurrent = index
        else:
            self.checkedChanged.emit()

    def tick_all(self):
        """Tick all items and mark them for display."""
        if self.rowCount() > 0:
            self.blockSignals(True)
            for row in range(self.rowCount()):
                item = self.item(row)
                item.setCheckState(QC.Qt.Checked)
                item.oldCheckState = QC.Qt.Checked
                # make sure that the selected isotherm is marked
                if item.index() == self.oldCurrent:
                    item.userCheckState = QC.Qt.Checked
            self.blockSignals(False)
            self.layoutChanged.emit()
            self.checkedChanged.emit()

    def untick_all(self):
        """Un-tick all items and update selection."""
        if self.rowCount() > 0:
            self.blockSignals(True)
            for row in range(self.rowCount()):
                item = self.item(row)
                # only untick non-selected isotherms
                if item.index() != self.oldCurrent:
                    item.setCheckState(QC.Qt.Unchecked)
                    item.oldCheckState = QC.Qt.Unchecked
                item.userCheckState = QC.Qt.Unchecked
            self.blockSignals(False)
            self.layoutChanged.emit()
            self.checkedChanged.emit()

    def delete(self, index):
        """Remove isotherm from model."""
        # LayoutChanged called automatically BEFORE actual removal
        # Therefore must ensure old isotherm is not ticked
        self.blockSignals(True)
        self.itemFromIndex(index).setCheckState(QC.Qt.Unchecked)
        self.blockSignals(False)
        # Remove reference to old isotherm
        self.oldCurrent = None
        # Call method for removal
        self.removeRow(index.row())
        # Remove reference again
        self.oldCurrent = None

    # TODO delete does not update selection when deleting checked isotherms
    # TODO delete keeps one item ticked
