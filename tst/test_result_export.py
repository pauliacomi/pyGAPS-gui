import json

import pytest
from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.utilities.result_export import serialize


@pytest.mark.parametrize("suffix", [".csv", ".json", ".JSON"])
def test_result_export_suffix_and_directory(tmp_path, monkeypatch, suffix):
    target = tmp_path / ("results" if suffix != ".JSON" else "results.JSON")
    monkeypatch.setattr(
        QW.QFileDialog, "getSaveFileName",
        lambda **kwargs: (str(target), f"Results (*{suffix})"),
    )
    assert serialize({"test": 5})
    actual = target if target.suffix else target.with_suffix(suffix)
    assert actual.is_file()
    if suffix.lower() == ".json":
        assert json.loads(actual.read_text()) == {"test": 5}
    assert QC.QSettings().value("resultExportDirectory") == str(tmp_path)


@pytest.mark.parametrize("confirm", [False, True])
def test_inferred_suffix_requires_overwrite_confirmation(tmp_path, monkeypatch, confirm):
    target = tmp_path / "results.json"
    target.write_text('{"original": true}', encoding="utf-8")
    monkeypatch.setattr(
        QW.QFileDialog, "getSaveFileName",
        lambda **kwargs: (str(target.with_suffix("")), "JSON (*.json)"),
    )
    prompts = []

    def answer(*args):
        prompts.append(args)
        return QW.QMessageBox.StandardButton.Yes if confirm else QW.QMessageBox.StandardButton.No

    monkeypatch.setattr(QW.QMessageBox, "question", answer)
    assert serialize({"test": 5}) == confirm
    assert len(prompts) == 1
    assert json.loads(target.read_text()) == ({"test": 5} if confirm else {"original": True})


@pytest.mark.parametrize("cancel", [False, True])
def test_native_save_confirmation_is_not_duplicated(tmp_path, monkeypatch, cancel):
    target = tmp_path / "results.json"
    target.write_text('{"original": true}', encoding="utf-8")
    monkeypatch.setattr(
        QW.QFileDialog, "getSaveFileName",
        lambda **kwargs: ("" if cancel else str(target), "JSON (*.json)"),
    )

    def unexpected_confirmation(*args):
        pytest.fail("Only inferred filenames need additional confirmation")

    monkeypatch.setattr(QW.QMessageBox, "question", unexpected_confirmation)
    assert serialize({"test": 5}) == (not cancel)
    assert json.loads(target.read_text()) == ({"original": True} if cancel else {"test": 5})
