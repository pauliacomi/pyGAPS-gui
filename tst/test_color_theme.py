import os
import tempfile
import threading
import unittest
from unittest import mock

os.environ.setdefault("QT_API", "pyside6")
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.utilities import color_theme


class ColorThemeTest(unittest.TestCase):
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

    def test_system_theme(self):
        self.assertIn(color_theme.system_theme(), ("dark", "light"))

    def test_auto_theme_follows_system_without_threads(self):
        threads = threading.active_count()
        with mock.patch.object(color_theme, "system_theme", return_value="light"):
            color_theme.set_theme()
        self.assertIs(color_theme.COLORS, color_theme.COLORS_LIGHT)
        self.assertTrue(color_theme.THEME_LISTENING)
        self.assertEqual(threading.active_count(), threads)

        with mock.patch.object(color_theme, "system_theme", return_value="dark"):
            color_theme.theme_callback(QC.Qt.ColorScheme.Dark)
        self.assertIs(color_theme.COLORS, color_theme.COLORS_DARK)
        self.assertTrue(self.app.styleSheet())

    def test_fixed_theme_ignores_system_changes(self):
        QC.QSettings().setValue("theme", "light")
        color_theme.set_theme()
        with mock.patch.object(color_theme, "system_theme", return_value="dark"):
            color_theme.theme_callback(QC.Qt.ColorScheme.Dark)
        self.assertIs(color_theme.COLORS, color_theme.COLORS_LIGHT)


if __name__ == "__main__":
    unittest.main()
