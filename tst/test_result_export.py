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
