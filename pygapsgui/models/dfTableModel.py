import numpy as np
import pandas as pd
from qtpy import QtCore as QC


class dfTableModel(QC.QAbstractTableModel):
    """Table model to display/edit a Pandas dataframe."""
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        if data is None:
            data = pd.DataFrame({"pressure": [0], "loading": [0], "branch": [0]})
        self._data = data

    def rowCount(self, index=QC.QModelIndex()):
        """Rows are df rows."""
        return self._data.shape[0]

    def columnCount(self, index=QC.QModelIndex()):
        """Columns are df columns."""
        return self._data.shape[1]

    def setRowCount(self, nrows):
        """Slice existing rows or insert new ones by appending a new df."""
        if nrows == self.rowCount():
            return
        if nrows < self.rowCount():
            self._data = self._data.iloc[0:nrows]
        if nrows > self.rowCount():
            newrows = pd.DataFrame(
                columns=self._data.columns,
                data=np.empty((nrows - self.rowCount(), self.columnCount())),
            )
            self._data = self._data.append(newrows, ignore_index=True)
        self.dataChanged.emit(QC.QModelIndex(), QC.QModelIndex())
        self.layoutChanged.emit()

    def data(self, index=QC.QModelIndex(), role=QC.Qt.DisplayRole):
        """Gets data at a specific index."""
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

    def setColumnData(self, col, values, role: int = QC.Qt.EditRole) -> bool:
        """Set data of a whole column."""
        start = self.index(0, col)
        end = self.index(self._data.shape[0] - 1, col)
        if not start.isValid() or not end.isValid():
            return False

        if role == QC.Qt.EditRole:
            colname = self._data.columns[col]
            self._data[colname] = values
            self.dataChanged.emit(start, end)
            return True

        return False

    def setColumnDtype(self, col, dtype) -> bool:
        """Set the dtype of a column"""
        colname = self._data.columns[col]
        self._data = self._data.astype({colname: dtype})
        return True

    def headerData(self, section, orientation, role=QC.Qt.DisplayRole):
        """Get data from the header."""
        if role != QC.Qt.DisplayRole:
            return None
        if orientation == QC.Qt.Horizontal:
            return self._data.columns[section]
        if orientation == QC.Qt.Vertical:
            return self._data.index[section] + 1

    def setHeaderData(self, section, orientation, value, role=QC.Qt.EditRole) -> bool:
        """Set data in the header as df columns, only horizontal."""
        if role in [QC.Qt.DisplayRole, QC.Qt.EditRole]:
            if orientation == QC.Qt.Horizontal:
                old_col = self._data.columns[section]
                self._data.rename(columns={old_col: value}, inplace=True)
                self.headerDataChanged.emit(QC.Qt.Horizontal, section, section)

    def insertRows(self, row: int, count: int, parent=QC.QModelIndex()) -> bool:
        """Convenience/fast function for row insertion"""
        self.beginInsertRows(parent, row, row + count - 1)
        # line = pd.DataFrame(self._data.iloc[row])
        line = pd.DataFrame([self._data.iloc[row].values],
                            index=range(count),
                            columns=self._data.columns)
        self._data = pd.concat([self._data.iloc[:row], line,
                                self._data.iloc[row:]]).reset_index(drop=True)
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent=QC.QModelIndex()) -> bool:
        """Convenience/fast function for row deletion."""
        self.beginRemoveRows(parent, row, row + count - 1)
        self._data.drop(self._data.index[row:row + count], inplace=True)
        self._data.reset_index(drop=True, inplace=True)
        self.endRemoveRows()
        return True

    def insertColumns(self, column: int, count: int, parent=QC.QModelIndex()) -> bool:
        """Convenience/fast function for column insertion."""
        self.beginInsertColumns(parent, column, column + count - 1)
        self._data.insert(column, "newcol", np.nan)
        self.endInsertColumns()
        return True

    def removeColumns(self, column: int, count: int, parent=QC.QModelIndex()) -> bool:
        """Convenience/fast function for column deletion."""
        self.beginRemoveColumns(parent, column, column + count - 1)
        self._data.drop(self._data.columns[column:column + count], axis=1, inplace=True)
        self.endRemoveColumns()
        return True

    def flags(self, index=QC.QModelIndex()):
        """Set flags for the model."""
        return QC.Qt.ItemIsEnabled | QC.Qt.ItemIsSelectable | QC.Qt.ItemIsEditable
