import os

from PySide2 import QtGui, QtCore

import pygaps

from src.views.UtilityWidgets import ErrorMessageBox
from src.models.IsothermModel import IsothermModel


class IsothermListModel(QtGui.QStandardItemModel):
    """Overloading an item model to store list of isotherms."""

    current_iso_index = None
    selected_iso_indices = []
    iso_sel_change = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.itemChanged.connect(self.check_changed)

    def current_iso(self):
        return self.itemFromIndex(self.current_iso_index).data()

    def data_from_iso(self, index):
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

    def load(self, path, name, ext):

        if ext == '.csv':
            isotherm = pygaps.isotherm_from_csv(path)
        elif ext == '.json':
            isotherm = pygaps.isotherm_from_jsonf(path)
        elif ext == '.xls' or ext == '.xlsx':
            isotherm = pygaps.isotherm_from_xl(path)

        # Create the model to store the isotherm
        iso_model = IsothermModel(name)
        # store data
        iso_model.setData(isotherm)
        # make checkable and set unchecked
        iso_model.setCheckable(True)
        iso_model.setCheckState(QtCore.Qt.Unchecked)
        # Add to the list model
        self.appendRow(iso_model)

    def save(self, path, ext):
        isotherm = self.current_iso()

        if ext == '.csv':
            pygaps.isotherm_to_csv(isotherm, path)
        elif ext == '.json':
            pygaps.isotherm_to_jsonf(isotherm, path)
        elif ext == '.xls' or ext == '.xlsx':
            pygaps.isotherm_to_xl(isotherm, path)
