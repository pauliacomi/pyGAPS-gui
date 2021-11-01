from qtpy import QtCore as QC


class MetadataTableModel(QC.QAbstractTableModel):
    """Table model to display various adsorbate properties."""
    def __init__(self, metadata: dict, parent=None):
        super().__init__(parent)

        self.params = []
        for prop, propval in metadata.items():
            tp = type(propval)
            if tp == str:
                tpstr = "text"
            else:
                tpstr = "number"
            self.params.append([prop, propval, tpstr])

    def rowCount(self, parent=QC.QModelIndex()):
        """Number of rows."""
        return len(self.params)

    def columnCount(self, parent=QC.QModelIndex()):
        """Number of columns, always two."""
        return 3

    def data(self, index, role=QC.Qt.DisplayRole):
        """Data display function."""
        if index.isValid():
            if role in [QC.Qt.DisplayRole, QC.Qt.EditRole]:
                return str(self.params[index.row()][index.column()])
        return None

    def rowData(self, index, role=QC.Qt.DisplayRole):
        """Row data return function."""
        if index.isValid():
            if role in [QC.Qt.DisplayRole, QC.Qt.EditRole]:
                return self.params[index.row()]
        return None

    def insertRow(self, position, data, parent=QC.QModelIndex()):
        """Insert a single row into the model"""
        return self.insertRows(position, 1, data=[data], parent=parent)

    def insertRows(self, position, count=1, parent=QC.QModelIndex(), data=None):
        """Insert a row into the model."""
        if not data or count != len(data):
            return False

        for row, datarow in enumerate(data):
            self.beginInsertRows(parent, position + row, position + row + count - 1)
            self.setRowData(position + row, datarow)
            self.endInsertRows()
        return True

    def setRowData(self, row, data):
        """Set data of a whole row."""

        for col in range(len(data)):
            index = self.createIndex(row, col)
            self.setData(index, data[col], role=QC.Qt.EditRole)

    def setOrInsertRow(self, data, parent=QC.QModelIndex()):
        metaNames = [p[0] for p in self.params]
        if data[0] in metaNames:
            position = metaNames.index(data[0])
            return self.setRowData(position, data)

        return self.insertRow(self.rowCount(), data, parent=parent)

    def headerData(self, section, orientation, role=QC.Qt.DisplayRole):
        """Header display function."""
        if role != QC.Qt.DisplayRole:
            return None

        if orientation == QC.Qt.Horizontal:
            if section == 0:
                return "Name"
            elif section == 1:
                return "Value"
            elif section == 2:
                return "Type"
            else:
                return ""
        elif orientation == QC.Qt.Vertical:
            return section

    def flags(self, index):
        """Set flags for the model."""
        if index.column() == 2:
            return QC.Qt.ItemIsSelectable
        return QC.Qt.ItemIsEnabled | QC.Qt.ItemIsSelectable | QC.Qt.ItemIsEditable
