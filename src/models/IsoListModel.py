from qtpy import QtCore as QC
from qtpy import QtGui as QG

from src.models.IsoModel import IsoModel


class IsoListModel(QG.QStandardItemModel):
    """
    Overload an item model to store a list of isotherms.

    There are two main isotherm states:
        "selected" - isotherm details will be displayed
        "checked" - isotherm will be plotted (for comparisons)

        The "selected" isotherm will automatically be "checked".

    Changing states:
        selected isotherm is changed by clicking the item/arrow keys
        checked items are changed by clicking the checkmark

    """

    checkedChanged = QC.Signal()  # emits when any checked are changed
    indexCurrent = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itemChanged.connect(self.handle_item_change)
        self.setItemPrototype(IsoModel())

    def get_item_index(self, index):
        """Return an isotherm given an index."""
        iso = self.itemFromIndex(index)
        return iso.data() if iso else None

    def get_item_checked(self):
        """Return list of checked isotherms."""
        # There is no standard method for this
        return [
            self.item(row).data()
            for row in range(self.rowCount())
            if self.item(row).checkState() == QC.Qt.Checked
        ]

    def handle_item_change(self, item):
        """If an item changed, we need to check why."""
        # Can never uncheck a selected item
        # if it is selected then we re-mark it as checked
        if item.index() == self.indexCurrent:
            self.blockSignals(True)
            item.setCheckState(QC.Qt.Checked)
            self.blockSignals(False)
            return
        # Otherwise emit change
        self.checkedChanged.emit()

    def handle_item_select(self, index):
        """When isotherm is selected, ensure it is marked checked."""

        # Restore previous item check state to user state
        oldItem = None
        if self.indexCurrent:
            oldItem = self.itemFromIndex(self.indexCurrent)
            if oldItem:
                self.blockSignals(True)
                oldItem.setCheckState(oldItem.userCheckState)
                oldItem.userCheckState = QC.Qt.Unchecked
                self.blockSignals(False)

        # Save user check state and mark selected item as checked
        newItem = self.itemFromIndex(index)
        if newItem:
            # Before any changes, store old state
            newItem.userCheckState = newItem.checkState()

            self.blockSignals(True)
            newItem.setCheckState(QC.Qt.Checked)
            self.blockSignals(False)

            # store index
            self.indexCurrent = index

            # improve performance by emitting check change if something changed
            if oldItem:
                if (
                    oldItem.checkState() == QC.Qt.Checked
                    and newItem.userCheckState == QC.Qt.Checked
                ):
                    return

        self.checkedChanged.emit()

    def tick_all(self):
        """Tick all items and mark them for display."""
        nrows = self.rowCount()
        if nrows > 0:
            self.blockSignals(True)
            for row in range(nrows):
                item = self.item(row)
                item.setCheckState(QC.Qt.Checked)
            self.blockSignals(False)

            self.layoutChanged.emit()  # let models know something changed
            self.checkedChanged.emit()  # and that checked state changed

    def untick_all(self):
        """Un-tick all items and update selection."""
        nrows = self.rowCount()
        if nrows > 0:
            self.blockSignals(True)
            for row in range(nrows):
                item = self.item(row)
                # only untick non-selected isotherms
                if item.index() != self.indexCurrent:
                    item.setCheckState(QC.Qt.Unchecked)
            self.blockSignals(False)

            self.layoutChanged.emit()  # let models know something changed
            self.checkedChanged.emit()  # and that checked state changed

    def delete(self, index):
        """Remove isotherm from model."""
        # LayoutChanged called automatically BEFORE actual removal
        # Therefore must ensure old isotherm is not ticked
        self.blockSignals(True)
        self.itemFromIndex(index).setCheckState(QC.Qt.Unchecked)
        self.blockSignals(False)

        # Remove reference to old isotherm
        self.indexCurrent = None
        # Call method for removal
        self.removeRow(index.row())
