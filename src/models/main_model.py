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
            new_iso_model = IsothermModel(filetitle)
            try:
                if fileext == '.csv':
                    new_iso_model.setData(pygaps.isotherm_from_csv(filepath))
                elif fileext == '.json':
                    new_iso_model.setData(pygaps.isotherm_from_jsonf(filepath))
                elif fileext == '.xls' or fileext == '.xlsx':
                    new_iso_model.setData(pygaps.isotherm_from_xl(filepath))
                self.explorer_model.appendRow(new_iso_model)
            except Exception as e:
                # TODO Print out error details
                print(e)
                pass

    def save(self, filepath):
        isotherm = self.explorer_model.itemFromIndex(
            self.current_iso_index).data()
        fileroot, fileext = os.path.splitext(filepath)
        try:
            if fileext == '.csv':
                pygaps.isotherm_to_csv(isotherm, filepath)
            elif fileext == '.json':
                pygaps.isotherm_to_jsonf(isotherm, filepath)
            elif fileext == '.xls' or fileext == '.xlsx':
                pygaps.isotherm_to_xl(isotherm, filepath)
        except Exception as e:
            # TODO Print error details
            print(e)
            pass

    def select(self, index):
        self.current_iso_index = index
        self.selected_iso_indices = [index]
        self.iso_selected.emit()

    def deselect(self, index):
        self.iso_deselected.emit()
