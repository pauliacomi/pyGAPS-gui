from PySide2 import QtCore

import pygaps


class MainModel(QtCore.QObject):
    """
    """
    isotherms = []
    selected_isotherms = []

    iso_added = QtCore.Signal()
    iso_removed = QtCore.Signal(int)
    iso_selected = QtCore.Signal(int)
    iso_deselected = QtCore.Signal(int)
    plot_changed = QtCore.Signal()

    def __init__(self):
        super().__init__()

    def load(self, filenames):
        for filename in filenames:
            with open(filename) as file:
                self.isotherms.append(pygaps.isotherm_from_json(file.read()))

        self.iso_added.emit()

    def select(self, index):
        self.selected_isotherms.append(self.isotherms[index])
        self.iso_selected.emit()

    def deselect(self, index):
        self.selected_isotherms.append(self.isotherms[index])
        self.iso_deselected.emit()
