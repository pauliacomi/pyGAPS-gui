from PySide2.QtGui import QStandardItemModel


class IsothermListModel(QStandardItemModel):
    """Overloading an item model to store list of isotherms."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
