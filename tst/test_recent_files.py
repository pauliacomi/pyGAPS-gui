import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

os.environ.setdefault("QT_API", "pyside6")
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6 import __version_info__ as PYSIDE_VERSION_INFO
from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.MainWindow import LEGACY_RECENT_FILES_KEY
from pygapsgui.MainWindow import RECENT_FILES_KEY
from pygapsgui.MainWindow import MainWindow


class RecentFilesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QW.QApplication.instance() or QW.QApplication([])
        cls.app.setOrganizationName("pyGAPS-test")
        cls.app.setApplicationName("pyGAPS-gui-test")
        cls.settings_dir = tempfile.TemporaryDirectory()
        QC.QSettings.setDefaultFormat(QC.QSettings.IniFormat)
        QC.QSettings.setPath(QC.QSettings.IniFormat, QC.QSettings.UserScope, cls.settings_dir.name)

    @classmethod
    def tearDownClass(cls):
        cls.settings_dir.cleanup()

    def setUp(self):
        QC.QSettings().clear()

    def make_window(self):
        window = MainWindow()
        self.addCleanup(window.deleteLater)
        return window

    def visible_actions(self, window):
        return [action for action in window.recent_file_actions if action.isVisible()]

    def test_single_recent_file_is_a_list(self):
        window = self.make_window()
        window.update_recent_files([pathlib.Path("C:/data/one.json")])

        self.assertEqual(window.get_recent_paths(), [str(pathlib.Path("C:/data/one.json"))])
        self.assertEqual([action.text() for action in self.visible_actions(window)], ["one.json"])

    def test_updates_reuse_menu_actions(self):
        window = self.make_window()
        window.update_recent_files([pathlib.Path("a.json")])
        window.update_recent_files([pathlib.Path("b.json"), pathlib.Path("a.json")])

        self.assertEqual(len(window.ui.menu_recent.actions()), window.recent_files_no)
        self.assertEqual([action.text() for action in self.visible_actions(window)], ["a.json", "b.json"])

    def test_legacy_value_is_migrated(self):
        # Write from another process so the value is deserialized from disk, as on upgrade.
        ini_path = QC.QSettings().fileName()
        writer = (
            "import pathlib, sys\n"
            "from qtpy import QtCore as QC\n"
            "settings = QC.QSettings(sys.argv[1], QC.QSettings.IniFormat)\n"
            f"settings.setValue({LEGACY_RECENT_FILES_KEY!r}, [pathlib.Path('legacy.aif')])\n"
            "settings.sync()\n"
        )
        subprocess.run([sys.executable, "-c", writer, ini_path], check=True)
        QC.QSettings().sync()
        self.assertTrue(QC.QSettings().contains(LEGACY_RECENT_FILES_KEY))

        window = self.make_window()
        settings = QC.QSettings()

        self.assertFalse(settings.contains(LEGACY_RECENT_FILES_KEY))
        self.assertTrue(settings.contains(RECENT_FILES_KEY))
        # PySide6 >= 6.12 refuses to read the legacy pickles (PYSIDE-3331).
        expected = [] if PYSIDE_VERSION_INFO >= (6, 12) else ["legacy.aif"]
        self.assertEqual(window.get_recent_paths(), expected)


if __name__ == "__main__":
    unittest.main()
