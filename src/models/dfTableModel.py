import pandas as pd
import numpy as np

from qtpy import QtCore as QC

from src.widgets.UtilityWidgets import error_dialog


class dfTableModel(QC.QAbstractTableModel):
    """Table model to display/edit a Pandas dataframe."""
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data

    def rowCount(self, index=QC.QModelIndex()):
        return self._data.shape[0]

    def columnCount(self, index=QC.QModelIndex()):
        return self._data.shape[1]

    def setRowCount(self, nrows):
        if nrows == self.rowCount():
            return
        if nrows < self.rowCount():
            self._data = self._data.iloc[0:nrows]
        if nrows > self.rowCount():
            newrows = pd.DataFrame(
                columns=self._data.columns,
                data=np.zeros((nrows - self.rowCount(), self.columnCount())),
            )
            self._data = self._data.append(newrows, ignore_index=True)
        self.dataChanged.emit(QC.QModelIndex(), QC.QModelIndex())
        self.layoutChanged.emit()

    def data(self, index=QC.QModelIndex(), role=QC.Qt.DisplayRole):
        if not index.isValid():
            return None

        if role in [QC.Qt.DisplayRole, QC.Qt.EditRole]:
            return self._data.values[index.row()][index.column()]

        if role == QC.Qt.TextAlignmentRole:
            return QC.Qt.AlignCenter

    def setData(self, index, value, role: int = QC.Qt.EditRole) -> bool:
        """Set data of a cell."""
        if not index.isValid():
            return False

        if role == QC.Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index)
            return True

        return False

    def headerData(self, section, orientation, role=QC.Qt.DisplayRole):
        if role != QC.Qt.DisplayRole:
            return None
        if orientation == QC.Qt.Horizontal:
            return self._data.columns[section]
        if orientation == QC.Qt.Vertical:
            return self._data.index[section] + 1

    def setHeaderData(self, section, orientation, value, role=QC.Qt.EditRole) -> bool:
        if role in [QC.Qt.DisplayRole, QC.Qt.EditRole]:
            if orientation == QC.Qt.Horizontal:
                old_col = self._data.columns[section]
                self._data.rename(columns={old_col: value}, inplace=True)
                self.headerDataChanged.emit(QC.Qt.Horizontal, section, section)

    def insertRows(self, row: int, count: int, parent=QC.QModelIndex()) -> bool:
        self.beginInsertRows(parent, row, row + count - 1)
        line = pd.DataFrame(0, index=np.arange(count), columns=self._data.columns)
        line['branch'] = self._data.iloc[row]['branch']
        self._data = pd.concat([self._data.iloc[:row], line,
                                self._data.iloc[row:]]).reset_index(drop=True)
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent=QC.QModelIndex()) -> bool:
        self.beginRemoveRows(parent, row, row + count - 1)
        self._data.drop(self._data.index[row:row + count], inplace=True)
        self._data.reset_index(drop=True, inplace=True)
        self.endRemoveRows()
        return True

    def insertColumns(self, column: int, count: int, parent=QC.QModelIndex()) -> bool:
        self.beginInsertColumns(parent, column, column + count - 1)
        self._data.insert(column, "newcol", 0)
        self.endInsertColumns()
        return True

    def removeColumns(self, column: int, count: int, parent=QC.QModelIndex()) -> bool:
        self.beginRemoveColumns(parent, column, column + count - 1)
        self._data.drop(self._data.columns[column:column + count], axis=1, inplace=True)
        self.endRemoveColumns()
        return True

    def flags(self, index=QC.QModelIndex()):
        """Set flags for the model."""
        return QC.Qt.ItemIsEnabled | QC.Qt.ItemIsSelectable | QC.Qt.ItemIsEditable
