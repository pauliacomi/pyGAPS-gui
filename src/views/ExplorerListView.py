
from PySide2 import QtWidgets


class ExplorerListView(QtWidgets.QListView):
    """List view that shows the opened list of isotherms."""

    def __init__(self, parent=None):

        # Initial init
        super().__init__(parent)
