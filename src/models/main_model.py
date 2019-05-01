from PySide2 import QtCore

import os
import pygaps

from src.models.explorer_model import ExplorerModel
from src.models.isotherm_model import IsothermModel


class MainModel(QtCore.QObject):
    """
    """
    iso_selected = QtCore.Signal(int)
    iso_deselected = QtCore.Signal(int)
    plot_changed = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self._explorer_model = ExplorerModel()

        self.connect_models()

    def connect_models(self):
        pass

    def load(self, filenames):
        for filepath in filenames:
            dirpath, filename = os.path.split(filepath)
            filetitle, fileext = os.path.splitext(filename)
            with open(filepath) as file:
                new_iso_model = IsothermModel(filetitle)
                new_iso_model.setData(pygaps.isotherm_from_json(file.read()))
                self._explorer_model.appendRow(new_iso_model)

    def select(self, index):
        self.iso_selected.emit()

    def deselect(self, index):
        self.iso_deselected.emit()
