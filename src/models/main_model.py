from PySide2 import QtCore

import os
import pygaps

from src.models.explorer_model import ExplorerModel
from src.models.isotherm_model import IsothermModel


class MainModel(QtCore.QObject):
    """
    """
    current_iso_index = None
    selected_iso_indices = []

    iso_selected = QtCore.Signal()
    iso_deselected = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.explorer_model = ExplorerModel()

    def load(self, filenames):
        for filepath in filenames:
            dirpath, filename = os.path.split(filepath)
            filetitle, fileext = os.path.splitext(filename)
            with open(filepath) as file:
                new_iso_model = IsothermModel(filetitle)
                new_iso_model.setData(pygaps.isotherm_from_json(file.read()))
                self.explorer_model.appendRow(new_iso_model)

    def select(self, index):
        self.current_iso_index = index
        self.selected_iso_indices.append(index)
        self.iso_selected.emit()

    def deselect(self, index):
        self.iso_deselected.emit()
