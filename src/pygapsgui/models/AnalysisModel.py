from functools import wraps

from qtpy import QtWidgets as QW

from pygaps.utilities.exceptions import CalculationError
from pygapsgui.widgets.UtilityDialogs import error_dialog


class AnalysisModel:
    """Track whether the current calculation can be saved or exported."""

    has_result = False

    def set_result_valid(self, valid):
        self.has_result = valid
        if not valid:
            self.results = None
            self.model_isotherm = None
            if hasattr(self.view, "iso_graph") and hasattr(self.view.iso_graph, "model_isotherm"):
                self.view.iso_graph.model_isotherm = None
            for name, widget in vars(self.view).items():
                if name.startswith("result_") and isinstance(widget, QW.QLabel):
                    widget.clear()
        for button in self.view.button_box.buttons():
            if self.view.button_box.buttonRole(button) == QW.QDialogButtonBox.ButtonRole.AcceptRole:
                button.setEnabled(valid)
        if hasattr(self.view, "export_btn"):
            self.view.export_btn.setEnabled(valid)


def calculation(method):
    @wraps(method)
    def run(self, *args, **kwargs):
        self.set_result_valid(False)
        valid = bool(method(self, *args, **kwargs))
        self.set_result_valid(valid)
        return valid
    return run


def result_dictionary(method):
    @wraps(method)
    def checked(self, *args, **kwargs):
        if not self.has_result:
            raise CalculationError("No valid calculation results to save.")
        return method(self, *args, **kwargs)
    return checked


def result_export(method):
    @wraps(method)
    def checked(self, *args, **kwargs):
        if not self.has_result:
            error_dialog("No valid calculation results to export.")
            return False
        return method(self, *args, **kwargs)
    return checked
