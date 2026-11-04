"""Functional tests for loading, importing and saving isotherms through the main window."""

import pathlib

import pygaps
import pygaps.parsing as pgp
import pytest

DATA_DIR = pathlib.Path(__file__).parent
ISOTHERM_FILES = sorted(DATA_DIR.glob("json/*.json")) + sorted(DATA_DIR.glob("aif/*.aif"))
COMMERCIAL_FILES = [
    ("mic_xl/Sample_A.xls", {"manufacturer": "mic", "fmt": "xl"}),
    ("bel_xl/Sample_C.xls", {"manufacturer": "bel", "fmt": "xl"}),
    ("bel_xl/Sample_D.xls", {"manufacturer": "bel", "fmt": "xl"}),
    ("bel_dat/1.DAT", {"manufacturer": "bel", "fmt": "dat"}),
    ("bel_dat/Sample_E.DAT", {"manufacturer": "bel", "fmt": "dat"}),
    ("3p_xl/AC_ref_filter_Ar_87K_run 3_rep.xlsx", {"manufacturer": "3p", "fmt": "xl"}),
    ("qnt_rep/1.txt", {"manufacturer": "qnt", "fmt": "txt-raw"}),
]


def iso_count(window):
    return window.iso_model.rowCount()


@pytest.mark.parametrize("path", ISOTHERM_FILES, ids=lambda path: f"{path.parent.name}/{path.name}")
def test_open_isotherm(main_window, dialog_errors, path):
    main_window.open_iso([path])

    assert dialog_errors == []
    assert iso_count(main_window) == 1
    assert main_window.iso_controller.iso_current is not None
    assert main_window.get_recent_paths() == [str(path)]
    assert main_window.ui.iso_graph.ax.lines


def test_open_multiple_and_delete(main_window):
    main_window.open_iso(ISOTHERM_FILES[:3])
    assert iso_count(main_window) == 3

    main_window.iso_controller.delete_current_iso()
    assert iso_count(main_window) == 2


def test_delete_last_isotherm_clears_display(main_window):
    main_window.open_iso(ISOTHERM_FILES[:1])
    editor = main_window.ui.prop_extra_edit_widget
    assert editor.metadata_table_model is not None

    main_window.iso_controller.delete_current_iso()

    assert iso_count(main_window) == 0
    assert main_window.iso_controller.iso_current is None
    assert editor.metadata_table_model is None
    assert editor.metadata_table_view.model() is None
    assert not editor.save_button.isEnabled()
    assert not main_window.ui.iso_graph.ax.lines
    main_window.iso_controller.delete_current_iso()

    main_window.open_iso(ISOTHERM_FILES[:1])
    assert editor.metadata_table_model is not None
    assert editor.save_button.isEnabled()
    assert main_window.ui.iso_graph.ax.lines


def test_example_data(main_window, monkeypatch):
    from qtpy import QtWidgets as QW
    monkeypatch.setattr(QW.QMessageBox, "question", lambda *args, **kwargs: QW.QMessageBox.StandardButton.Yes)

    main_window.ui.action_examples.trigger()

    assert iso_count(main_window) > 0


@pytest.mark.parametrize(("relpath", "ftype"), COMMERCIAL_FILES, ids=[item[0] for item in COMMERCIAL_FILES])
def test_import_commercial(main_window, dialog_errors, relpath, ftype):
    path = DATA_DIR / relpath
    main_window.import_iso([path], ftype)

    assert dialog_errors == []
    assert iso_count(main_window) == 1


@pytest.mark.parametrize("ext", [".aif", ".json", ".csv", ".xlsx"])
def test_save_roundtrip(main_window, tmp_path, ext):
    source = DATA_DIR / "json" / "SiO2 N2 77.json"
    main_window.open_iso([source])
    original = main_window.iso_controller.iso_current

    target = tmp_path / f"saved{ext}"
    main_window.save_iso(target)

    assert target.is_file()
    reloaded = {
        ".aif": pgp.isotherm_from_aif,
        ".json": pgp.isotherm_from_json,
        ".csv": pgp.isotherm_from_csv,
        ".xlsx": pgp.isotherm_from_xl,
    }[ext](target)
    assert isinstance(reloaded, pygaps.PointIsotherm)
    assert str(reloaded.material) == str(original.material)
    assert str(reloaded.adsorbate) == str(original.adsorbate)
    assert len(reloaded.data()) == len(original.data())


def test_mixed_open_continues_and_records_only_successes(main_window, tmp_path, dialog_errors):
    source = DATA_DIR / "json" / "SiO2 N2 77.json"
    uppercase = tmp_path / "UPPER.JSON"
    uppercase.write_bytes(source.read_bytes())
    broken = tmp_path / "broken.json"
    broken.write_text("invalid json", encoding="utf-8")
    unsupported = tmp_path / "notes.txt"
    unsupported.write_text("notes", encoding="utf-8")

    main_window.open_iso([broken, unsupported, uppercase])

    assert iso_count(main_window) == 1
    assert main_window.get_recent_paths() == [str(uppercase)]
    assert len(dialog_errors) == 1
    assert "2 failed" in dialog_errors[0]
    assert "broken.json" in dialog_errors[0]
    assert "notes.txt" in dialog_errors[0]


def test_folder_filters_non_isotherm_files(main_window, tmp_path, dialog_errors):
    source = DATA_DIR / "json" / "SiO2 N2 77.json"
    (tmp_path / "isotherm.JSON").write_bytes(source.read_bytes())
    (tmp_path / "readme.txt").write_text("notes", encoding="utf-8")
    (tmp_path / "subdirectory").mkdir()

    main_window.open_folder(tmp_path)

    assert iso_count(main_window) == 1
    assert not dialog_errors
    main_window.open_folder(tmp_path / "missing")
    assert "Cannot open folder" in dialog_errors[0]


def test_import_recent_preserves_parser_settings(main_window, dialog_errors):
    path = DATA_DIR / "bel_dat" / "1.DAT"
    main_window.import_iso([path], {"manufacturer": "bel", "fmt": "dat"})
    assert main_window.get_recent_paths() == [str(path)]

    main_window.open_recent(0)

    assert iso_count(main_window) == 2
    assert not dialog_errors


def test_batch_import_continues_after_failure(main_window, tmp_path, dialog_errors):
    path = DATA_DIR / "bel_dat" / "1.DAT"
    main_window.import_iso([tmp_path / "missing.DAT", path], {"manufacturer": "bel", "fmt": "dat"})
    assert iso_count(main_window) == 1
    assert main_window.get_recent_paths() == [str(path)]
    assert len(dialog_errors) == 1


def test_save_write_error_is_reported(main_window, tmp_path, monkeypatch, dialog_errors):
    main_window.open_iso(ISOTHERM_FILES[:1])

    def denied(*args):
        raise PermissionError("file is locked")

    monkeypatch.setattr(pgp, "isotherm_to_json", denied)
    main_window.save_iso(tmp_path / "locked.json")
    assert "file is locked" in dialog_errors[0]


def test_save_without_suffix_uses_selected_filter(main_window, tmp_path, monkeypatch):
    from qtpy import QtWidgets as QW

    main_window.open_iso(ISOTHERM_FILES[:1])
    target = tmp_path / "saved"
    monkeypatch.setattr(QW.QFileDialog, "getSaveFileName", lambda **kwargs: (str(target), "pyGAPS Excel Isotherm (*.xlsx)"))

    main_window.save_iso()

    assert target.with_suffix(".xlsx").is_file()
