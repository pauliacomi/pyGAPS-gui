from qtpy import QtCore as QC


class MetadataTableModel(QC.QAbstractTableModel):
    """Table model to display various coreclass (Isotherm, Adsorbate, Material) properties."""
    def __init__(self, coreclass, parent=None):
        super().__init__(parent)

        self.coreclass = coreclass
        metadata = {
            prop: coreclass.properties[prop]
            for prop in coreclass.properties
            if prop not in coreclass._reserved_params
        }
        self.params = []
        for prop, propval in metadata.items():
            tp = type(propval)
            if tp == str:
                tpstr = "text"
            else:
                tpstr = "number"
            self.params.append([prop, propval, tpstr])

    def rowCount(self, index=QC.QModelIndex()):
        """Get number of rows."""
        return len(self.params)

    def columnCount(self, index=QC.QModelIndex()):
        """Get number of columns, always three."""
        return 3

    def data(self, index, role=QC.Qt.DisplayRole):
        """Data display function."""
        if not index.isValid():
            return

        if role in [QC.Qt.DisplayRole, QC.Qt.EditRole]:
            return self.params[index.row()][index.column()]

        if role == QC.Qt.TextAlignmentRole:
            return QC.Qt.AlignCenter

    def rowData(self, index, role=QC.Qt.DisplayRole):
        """Row data return function."""
        if not index.isValid():
            return
        if role in [QC.Qt.DisplayRole, QC.Qt.EditRole]:
            return self.params[index.row()]

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

    def setData(self, index, value, role):
        """Set data of a cell."""
        if not index.isValid():
            return False

        if role == QC.Qt.EditRole:
            if index.column() == 0:
                if value not in [p[0] for p in self.params]:
                    self.params.insert(index.row(), [value, None, None])

            if index.column() == 1:
                self.coreclass.properties[self.params[index.row()][0]] = value

            self.params[index.row()][index.column()] = value

            self.dataChanged.emit(index, index)
            return True

        return False

    def setRowData(self, row, data):
        """Set data of a whole row."""
        for col in range(len(data)):
            index = self.createIndex(row, col)
            self.setData(index, data[col], role=QC.Qt.EditRole)

    def removeRows(self, position, rows=1, index=QC.QModelIndex()):
        """Delete a row from the model. Removes attribute from coreclass."""
        self.beginRemoveRows(index, position, position + rows - 1)
        for row in range(rows):
            del self.coreclass.properties[self.params[position + row][0]]
        del self.params[position:position + rows]
        self.endRemoveRows()
        return True

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

    def setOrInsertRow(self, data, parent=QC.QModelIndex()):
        """Convenience for combined row set/insert."""
        metaNames = [p[0] for p in self.params]
        if data[0] in metaNames:
            position = metaNames.index(data[0])
            return self.setRowData(position, data)

        return self.insertRow(self.rowCount(), data, parent=parent)

    def flags(self, index):
        """Set flags for the model."""
        if index.column() == 2:
            return QC.Qt.ItemIsSelectable
        return QC.Qt.ItemIsEnabled | QC.Qt.ItemIsSelectable
