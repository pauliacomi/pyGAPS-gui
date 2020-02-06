from PySide2 import QtCore


class IsoInfoTableModel(QtCore.QAbstractTableModel):
    """Overloading a table model to display isotherm adsorption data."""

    def __init__(self, isotherm, parent=None):
        super().__init__(parent)
        self.isotherm = isotherm
        self.params = []

        for prop in vars(isotherm):
            if prop not in isotherm._required_params + list(isotherm._named_params) + \
                    list(isotherm._unit_params) + isotherm._reserved_params:
                self.params.append([prop, str(getattr(isotherm, prop))])

    def rowCount(self, parent=None):
        return len(self.params)

    def columnCount(self, parent=None):
        return 2

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return self.params[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:
            if section == 0:
                return "Parameter"
            elif section == 1:
                return "Value"
            else:
                return ""
        elif orientation == QtCore.Qt.Vertical:
            return section

    def setData(self, index, value, role):
        if index.isValid() and role == QtCore.Qt.EditRole:
            self.params[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
