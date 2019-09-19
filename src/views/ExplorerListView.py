
from PySide2 import QtWidgets
from PySide2 import QtCore


class ExplorerListView(QtWidgets.QListView):
    """List view that shows the opened list of isotherms."""

    iso_sel_change = QtCore.Signal()

    def __init__(self, parent=None):

        # Initial init
        super().__init__(parent)

        # Connect clicking and selecting
        self.clicked.connect(self.venue_selected)
