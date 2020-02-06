
from PySide2 import QtWidgets


class IsoListView(QtWidgets.QListView):
    """List view that shows the opened list of isotherms."""

    def __init__(self, parent=None):

        # Initial init
        super().__init__(parent)

    def remove_current(self):
        """Remove currently selected isotherm from list."""
        index = self.current_iso_index.row()
        self.removeRow(index)
        if index == self.rowCount() and index != 0:
            self.current_iso_index -= 1
        self.iso_sel_change.emit()
