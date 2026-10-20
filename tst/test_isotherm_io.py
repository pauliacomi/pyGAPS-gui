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


@pytest.mark.qt_no_exception_capture
@pytest.mark.xfail(strict=True, reason="MainWindow.examples uses QMessageBox.Yes on an instance, removed in Qt6")
def test_example_data(main_window, monkeypatch):
    from qtpy import QtWidgets as QW
    monkeypatch.setattr(QW.QMessageBox, "question", lambda *args, **kwargs: QW.QMessageBox.Yes)

    main_window.ui.action_examples.trigger()

    assert iso_count(main_window) > 0


@pytest.mark.parametrize(("relpath", "ftype"), COMMERCIAL_FILES, ids=[item[0] for item in COMMERCIAL_FILES])
def test_import_commercial(main_window, dialog_errors, relpath, ftype):
    path = DATA_DIR / relpath
    main_window.import_iso([path], ftype)

    assert dialog_errors == []
    assert iso_count(main_window) == 1


@pytest.mark.parametrize("ext", [".aif", ".json", ".csv"])
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
    }[ext](target)
    assert isinstance(reloaded, pygaps.PointIsotherm)
    assert str(reloaded.material) == str(original.material)
    assert str(reloaded.adsorbate) == str(original.adsorbate)
    assert len(reloaded.data()) == len(original.data())
