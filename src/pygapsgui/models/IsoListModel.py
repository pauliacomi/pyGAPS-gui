from qtpy import QtCore as QC
from qtpy import QtGui as QG


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

    checked_changed = QC.Signal()
    index_selected = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # this emits when any checked are changed
        self.itemChanged.connect(self.handle_check_change)

    def handle_check_change(self, item):
        """If an item got checked, we need to check why."""
        # Can never uncheck a selected item so we re-mark it as checked
        if item.index() == self.index_selected:
            self.blockSignals(True)
            item.setCheckState(QC.Qt.Checked)
            self.blockSignals(False)
            return
        # Otherwise emit change
        self.checked_changed.emit()

    def handle_item_select(self, new_index, old_index):
        """When isotherm is selected, ensure it is marked checked."""

        # Restore previous item check state to user state
        old_item = self.itemFromIndex(old_index)
        if old_item:
            self.blockSignals(True)
            old_item.setCheckState(old_item.userCheckState)
            self.blockSignals(False)

        # Save user check state and mark selected item as checked
        new_item = self.itemFromIndex(new_index)
        if new_item:
            # Before any changes, store old state
            new_item.userCheckState = new_item.checkState()

            self.blockSignals(True)
            new_item.setCheckState(QC.Qt.Checked)
            self.blockSignals(False)

            # store index
            self.index_selected = new_index

            # improve performance by emitting check change only if something changed
            # TODO what about when it is deleted?
            if (
                old_item and old_item.checkState() == QC.Qt.Checked
                and new_item.userCheckState == QC.Qt.Checked
            ):
                return
            self.checked_changed.emit()

    def get_checked(self):
        """Return list of checked isotherms."""
        # There is no standard method for this
        return [
            self.item(row).data()
            for row in range(self.rowCount())
            if self.item(row).checkState() == QC.Qt.Checked
        ]

    def check_all(self):
        """Tick all items and mark them for display."""
        nrows = self.rowCount()
        if not nrows:
            return

        self.blockSignals(True)
        for row in range(nrows):
            item = self.item(row)
            item.setCheckState(QC.Qt.Checked)
        self.blockSignals(False)

        self.layoutChanged.emit()  # let models know something changed
        self.checked_changed.emit()  # and that checked state changed

    def uncheck_all(self):
        """Un-tick all items and update selection."""
        nrows = self.rowCount()
        if not nrows:
            return

        self.blockSignals(True)
        for row in range(nrows):
            item = self.item(row)
            # only untick non-selected isotherms
            if item.index() != self.index_selected:
                item.setCheckState(QC.Qt.Unchecked)
        self.blockSignals(False)

        self.layoutChanged.emit()  # let models know something changed
        self.checked_changed.emit()  # and that checked state changed

    def removeRow(self, row, parent=QC.QModelIndex()):
        """Remove isotherm from model."""
        # LayoutChanged called automatically BEFORE actual removal
        # Therefore must ensure old isotherm is not ticked
        self.blockSignals(True)
        self.item(row).setCheckState(QC.Qt.Unchecked)
        self.blockSignals(False)

        # Call method for removal
        super().removeRow(row, parent)
