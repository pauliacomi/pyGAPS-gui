from qtpy import QtCore as QC


class IsoDataTableModel(QC.QAbstractTableModel):
    """Overloading a table model to display isotherm adsorption data."""
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QC.Qt.DisplayRole):
        if index.isValid():
            if role == QC.Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role=QC.Qt.DisplayRole):
        if role != QC.Qt.DisplayRole:
            return None

        if orientation == QC.Qt.Horizontal:
            try:
                label = self._data.columns.tolist()[section]
                if label == section:
                    label = section
                return label
            except (IndexError, ):
                return None
        elif orientation == QC.Qt.Vertical:
            return section
