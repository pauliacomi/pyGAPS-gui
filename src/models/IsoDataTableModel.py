from qtpy import QtCore as QC

from src.models.dfTableModel import dfTableModel
from src.widgets.UtilityWidgets import error_dialog


class IsoDataTableModel(dfTableModel):
    """Overload a dataframe table model to display isotherm adsorption data."""
    def data(self, index=QC.QModelIndex(), role=QC.Qt.DisplayRole):

        if role in [QC.Qt.DisplayRole, QC.Qt.EditRole]:
            val = self._data.values[index.row()][index.column()]
            if self._data.columns[index.column()] == "branch":
                return "des" if val else "ads"

        return super().data(index, role)

    def setData(self, index, value, role: int = QC.Qt.EditRole) -> bool:

        if role == QC.Qt.EditRole:
            if self._data.columns[index.column()] == "branch":
                if value in ["ads", "des"]:
                    choice = {"ads": False, "des": True}
                    self._data.iloc[index.row(), index.column()] = choice[value]
                    self.dataChanged.emit(index, index)
                    return True
                else:
                    error_dialog("Branch can only be 'ads' or 'des'.")
                    return False

        return super().setData(index, value, role)
