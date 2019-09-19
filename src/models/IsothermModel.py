from PySide2.QtGui import QStandardItem


class IsothermModel(QStandardItem):
    """Overloading a standard item to store an isotherm."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
