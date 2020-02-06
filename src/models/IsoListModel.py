import os

from PySide2 import QtGui, QtCore

import pygaps

from src.models.IsoModel import IsoModel


class IsoListModel(QtGui.QStandardItemModel):
    """Overloading an item model to store list of isotherms."""

    current_iso_index = None
    selected_iso_indices = []
    iso_sel_change = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.itemChanged.connect(self.check_changed)

    def get_iso_current(self):
        return self.itemFromIndex(self.current_iso_index).data()

    def get_iso_index(self, index):
        return self.itemFromIndex(index).data()

    def select(self, index):
        self.current_iso_index = index
        self.iso_sel_change.emit()

    def checked(self, index):
        self.current_iso_index = index
        if index not in self.selected_iso_indices:
            self.selected_iso_indices.append(index)
        self.iso_sel_change.emit()

    def unchecked(self, index):
        self.selected_iso_indices.remove(index)
        self.iso_sel_change.emit()

    def check_changed(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            self.checked(item.index())
        if item.checkState() == QtCore.Qt.Unchecked:
            self.unchecked(item.index())

    def check_all(self):
        """Check all items and mark them for display."""
        if self.rowCount() > 0:
            self.blockSignals(True)
            for row in range(self.rowCount()):
                item = self.item(row)
                item.setCheckState(QtCore.Qt.Checked)
                index = item.index()
                if index not in self.selected_iso_indices:
                    self.selected_iso_indices.append(index)
            self.blockSignals(False)
            self.iso_sel_change.emit()

    def uncheck_all(self):
        """Un-check all items and update selection."""
        if self.rowCount() > 0:
            self.blockSignals(True)
            for row in range(self.rowCount()):
                item = self.item(row)
                item.setCheckState(QtCore.Qt.Unchecked)
            self.selected_iso_indices.clear()
            self.blockSignals(False)
            self.iso_sel_change.emit()

    def load(self, path, name, ext):
        """Load isotherm from disk."""
        if ext == '.csv':
            isotherm = pygaps.isotherm_from_csv(path)
        elif ext == '.json':
            isotherm = pygaps.isotherm_from_jsonf(path)
        elif ext == '.xls' or ext == '.xlsx':
            isotherm = pygaps.isotherm_from_xl(path)

        # Create the model to store the isotherm
        iso_model = IsoModel(name)
        # store data
        iso_model.setData(isotherm)
        # make checkable (default unchecked)
        iso_model.setCheckable(True)
        # Add to the list model
        self.appendRow(iso_model)

    def save(self, path, ext):
        """Save isotherm to disk."""
        isotherm = self.get_iso_current()

        if ext == '.csv':
            pygaps.isotherm_to_csv(isotherm, path)
        elif ext == '.json':
            pygaps.isotherm_to_jsonf(isotherm, path)
        elif ext == '.xls' or ext == '.xlsx':
            pygaps.isotherm_to_xl(isotherm, path)

    def remove_current(self):
        """Remove currently selected isotherm from list."""
        index = self.current_iso_index.row()
        self.removeRow(index)
        if index == self.rowCount() and index != 0:
            self.current_iso_index -= 1
        self.iso_sel_change.emit()
