from qtpy import QtCore as QC
from qtpy import QtCore as QW

from pygapsgui.models.dfTableModel import dfTableModel
from pygapsgui.widgets.UtilityDialogs import error_dialog

_BRANCH_CHOICES = {"ads": False, "des": True, "0": False, "1": True, "False": False, "True": True}


class IsoDataTableModel(dfTableModel):
    """Overload a dataframe table model to display isotherm adsorption data."""
    def data(self, index=QC.QModelIndex(), role=QC.Qt.DisplayRole):
        """Intercept data to display ads/des for branches"""
        if role in [QC.Qt.DisplayRole, QC.Qt.EditRole]:
            if self._data.columns[index.column()] == "branch":
                val = self._data.values[index.row()][index.column()]
                return "des" if val else "ads"
        return super().data(index, role)

    def setData(self, index, value, role: int = QC.Qt.EditRole) -> bool:
        """Intercept setdata to correctly set ads/des for branches"""
        if not index.isValid():
            return False

        if role == QC.Qt.EditRole:
            if self._data.columns[index.column()] == "branch":
                if value in ("ads", "des", "0", "1", "False", "True"):
                    self._data.iloc[index.row(), index.column()] = _BRANCH_CHOICES[value]
                    self.dataChanged.emit(index, index)
                    return True
                else:
                    error_dialog("Branch can only be 'ads'/0/True or 'des'/1/False.")
                    return False

        return super().setData(index, value, role)

    def insertColumns(self, column: int, count: int, parent=None) -> bool:
        """Ensure only insert at the end."""
        return super().insertColumns(max(column, 2), count, parent)

    def removeColumns(self, column: int, count: int, parent=None) -> bool:
        """Ensure base parameters cant be deleted."""
        if any(
            self._data.columns[column + c] in ["pressure", "loading", "branch"]
            for c in range(count)
        ):
            error_dialog("Cannot remove basic data types (pressure, loading or branch).")
            return False
        return super().removeColumns(column, count, parent)
