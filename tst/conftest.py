import os

os.environ.setdefault("QT_API", "pyside6")
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("MPLBACKEND", "Agg")

import pathlib

import pytest
from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

DATA_DIR = pathlib.Path(__file__).parent


@pytest.fixture(autouse=True)
def isolated_settings(qapp, tmp_path):
    """Keep QSettings away from the developer's real application settings."""
    qapp.setOrganizationName("pyGAPS-test")
    qapp.setApplicationName("pyGAPS-gui-test")
    QC.QSettings.setDefaultFormat(QC.QSettings.Format.IniFormat)
    QC.QSettings.setPath(QC.QSettings.Format.IniFormat, QC.QSettings.Scope.UserScope, str(tmp_path / "settings"))
    QC.QSettings().clear()
    yield
    QC.QSettings().clear()


@pytest.fixture(autouse=True)
def dialog_errors(monkeypatch):
    """Accept modal dialogs immediately and collect error dialog messages."""
    from pygapsgui.widgets.UtilityDialogs import ErrorMessageBox

    errors = []

    def fake_exec(self, *args, **kwargs):
        if isinstance(self, ErrorMessageBox):
            errors.append(self.text_label.text())
            return QW.QDialog.DialogCode.Rejected
        return QW.QDialog.DialogCode.Accepted

    for name in ("exec", "exec_"):
        if hasattr(QW.QDialog, name):
            monkeypatch.setattr(QW.QDialog, name, fake_exec)
    return errors


@pytest.fixture
def main_window(qtbot):
    from pygapsgui.MainWindow import MainWindow

    window = MainWindow()
    qtbot.addWidget(window)
    return window


@pytest.fixture
def data_dir():
    return DATA_DIR
