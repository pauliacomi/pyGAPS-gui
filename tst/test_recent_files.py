import pathlib
import subprocess
import sys

from PySide6 import __version_info__ as PYSIDE_VERSION_INFO
from qtpy import QtCore as QC

from pygapsgui.MainWindow import LEGACY_RECENT_FILES_KEY
from pygapsgui.MainWindow import RECENT_FILES_KEY


def visible_names(window):
    return [action.text() for action in window.recent_file_actions if action.isVisible()]


def test_single_recent_file_is_a_list(main_window):
    path = pathlib.Path("C:/data/one.json")
    main_window.update_recent_files([path])

    assert main_window.get_recent_paths() == [str(path)]
    assert visible_names(main_window) == ["one.json"]


def test_updates_reuse_menu_actions(main_window):
    main_window.update_recent_files([pathlib.Path("a.json")])
    main_window.update_recent_files([pathlib.Path("b.json"), pathlib.Path("a.json")])

    assert len(main_window.ui.menu_recent.actions()) == main_window.recent_files_no
    assert visible_names(main_window) == ["a.json", "b.json"]


def test_recent_files_are_capped(main_window):
    main_window.update_recent_files([pathlib.Path(f"{ind}.json") for ind in range(12)])

    assert len(main_window.get_recent_paths()) == main_window.recent_files_no
    assert visible_names(main_window)[0] == "11.json"


def test_legacy_value_is_migrated(qtbot):
    # Write from another process so the value is deserialized from disk, as on upgrade.
    writer = (
        "import pathlib, sys\n"
        "from qtpy import QtCore as QC\n"
        "settings = QC.QSettings(sys.argv[1], QC.QSettings.IniFormat)\n"
        f"settings.setValue({LEGACY_RECENT_FILES_KEY!r}, [pathlib.Path('legacy.aif')])\n"
        "settings.sync()\n"
    )
    subprocess.run([sys.executable, "-c", writer, QC.QSettings().fileName()], check=True)
    QC.QSettings().sync()
    assert QC.QSettings().contains(LEGACY_RECENT_FILES_KEY)

    from pygapsgui.MainWindow import MainWindow
    window = MainWindow()
    qtbot.addWidget(window)

    settings = QC.QSettings()
    assert not settings.contains(LEGACY_RECENT_FILES_KEY)
    assert settings.contains(RECENT_FILES_KEY)
    # PySide6 >= 6.12 refuses to read the legacy pickles (PYSIDE-3331).
    expected = [] if PYSIDE_VERSION_INFO >= (6, 12) else ["legacy.aif"]
    assert window.get_recent_paths() == expected
