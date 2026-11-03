import threading

from qtpy import QtCore as QC

from pygapsgui.utilities import color_theme


def test_system_theme(qapp):
    assert color_theme.system_theme() in ("dark", "light")


def test_auto_theme_follows_system_without_threads(qapp, monkeypatch):
    threads = threading.active_count()
    monkeypatch.setattr(color_theme, "system_theme", lambda: "light")
    color_theme.set_theme()

    assert color_theme.COLORS is color_theme.COLORS_LIGHT
    assert color_theme.THEME_LISTENING
    assert threading.active_count() == threads

    monkeypatch.setattr(color_theme, "system_theme", lambda: "dark")
    color_theme.theme_callback(QC.Qt.ColorScheme.Dark)

    assert color_theme.COLORS is color_theme.COLORS_DARK
    assert qapp.styleSheet()


def test_fixed_theme_ignores_system_changes(qapp, monkeypatch):
    QC.QSettings().setValue("theme", "light")
    color_theme.set_theme()
    monkeypatch.setattr(color_theme, "system_theme", lambda: "dark")
    color_theme.theme_callback(QC.Qt.ColorScheme.Dark)

    assert color_theme.COLORS is color_theme.COLORS_LIGHT


def test_menu_switches_theme(main_window):
    main_window.ui.action_theme_light.trigger()
    assert QC.QSettings().value("theme") == "light"
    assert color_theme.COLORS is color_theme.COLORS_LIGHT

    main_window.ui.action_theme_dark.trigger()
    assert QC.QSettings().value("theme") == "dark"
    assert color_theme.COLORS is color_theme.COLORS_DARK
