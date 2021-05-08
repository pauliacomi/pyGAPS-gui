from qtpy import QtCore as QC


class IsoInfoTableModel(QC.QAbstractTableModel):
    """Table model to display various isotherm properties."""
    def __init__(self, isotherm, parent=None):
        super().__init__(parent)
        self.isotherm = isotherm
        self.params = []

        for prop in vars(isotherm):
            if prop not in isotherm._required_params + \
                    list(isotherm._unit_params) + isotherm._reserved_params:
                self.params.append([prop, str(getattr(isotherm, prop))])

    def rowCount(self, parent=QC.QModelIndex()):
        """Number of rows."""
        return len(self.params)

    def columnCount(self, parent=QC.QModelIndex()):
        """Number of columns, always two."""
        return 2

    def data(self, index, role=QC.Qt.DisplayRole):
        """Data display function."""
        if index.isValid():
            if role == QC.Qt.DisplayRole or role == QC.Qt.EditRole:
                return self.params[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=QC.Qt.DisplayRole):
        """Header display function."""
        if role != QC.Qt.DisplayRole:
            return None

        if orientation == QC.Qt.Horizontal:
            if section == 0:
                return "Parameter"
            elif section == 1:
                return "Value"
            else:
                return ""
        elif orientation == QC.Qt.Vertical:
            return section

    def setData(self, index, value, role):
        """Number of columns, always two."""
        if index.isValid() and role == QC.Qt.EditRole:
            self.params[index.row()][index.column()] = value
            if index.column() == 1:
                setattr(self.isotherm, self.params[index.row()][0], value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        """Set flags for the model."""
        if index.column() == 0:
            return QC.Qt.ItemIsSelectable
        return QC.Qt.ItemIsEnabled | QC.Qt.ItemIsSelectable | QC.Qt.ItemIsEditable

    def removeRows(self, position, rows=1, index=QC.QModelIndex()):
        """Deletes a row from the model. Removes attribute from isotherm."""
        self.beginRemoveRows(index, position, position + rows - 1)
        for row in range(rows):
            delattr(self.isotherm, self.params[position + row][0])
        del self.params[position:position + rows]
        self.endRemoveRows()
        return True

    def insertRows(self, position, rows=1, index=QC.QModelIndex(), val=None):
        """Insert a row into the model. Adds new attribute to isotherm."""
        if val:
            self.beginInsertRows(index, position, position + rows - 1)
            for row in range(rows):
                if not hasattr(self.isotherm, val):
                    self.params.insert(position + row, [val, None])
            self.endInsertRows()
            return True
        return False
