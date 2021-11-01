from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.models.MetadataTableModel import MetadataTableModel


class MatPropTableModel(MetadataTableModel):
    """Table model to display various material properties."""
    def __init__(self, material, parent=None):
        self.material = material
        metadata = {
            prop: material.properties[prop]
            for prop in material.properties
            if prop not in material._reserved_params
        }
        super().__init__(metadata, parent)

    def setData(self, index, value, role):
        """Set data of a cell."""
        if index.isValid() and role == QC.Qt.EditRole:
            if index.column() == 0:
                if value not in [p[0] for p in self.params]:
                    self.params.insert(index.row(), [value, None, None])

            if index.column() == 1:
                self.material.properties[self.params[index.row()][0]] = value

            self.params[index.row()][index.column()] = value

            self.dataChanged.emit(index, index)
            return True
        return False

    def removeRows(self, position, rows=1, index=QC.QModelIndex()):
        """Deletes a row from the model. Removes attribute from material."""
        self.beginRemoveRows(index, position, position + rows - 1)
        for row in range(rows):
            del self.material.properties[self.params[position + row][0]]
        del self.params[position:position + rows]
        self.endRemoveRows()
        return True
