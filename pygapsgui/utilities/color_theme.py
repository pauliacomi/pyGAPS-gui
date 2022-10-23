import typing

from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

THEME_DAEMON = None


@QC.Slot()
def theme_apply(theme) -> None:
    """Apply a custom theme."""
    import qdarktheme

    theme = theme.lower()
    stylesheet = qdarktheme.load_stylesheet(theme)
    QW.QApplication.instance().setStyleSheet(stylesheet)

    # import matplotlib.pyplot as plt
    # if theme == "dark":
    #     plt.style.use('dark_background')
    # elif theme == "light":
    #     plt.style.use('default')


def theme_callback(theme) -> None:
    settings = QC.QSettings()
    theme_setting = settings.value("theme", "auto")
    if theme_setting == "auto":
        theme_apply(theme)


def theme_listener(callback: typing.Callable[[str], None]) -> None:
    """Add a listener that automatically changes theme."""
    global THEME_DAEMON

    import threading
    import darkdetect

    THEME_DAEMON = threading.Thread(target=darkdetect.listener, args=(callback, ))
    THEME_DAEMON.daemon = True
    THEME_DAEMON.start()


def set_theme():
    """Starts/sets all theming components."""

    settings = QC.QSettings()
    theme_setting = settings.value("theme", "auto")

    if theme_setting not in ["dark", "light", "auto"]:
        return

    if theme_setting == "auto":
        import darkdetect
        theme_apply(darkdetect.theme())
        theme_listener(theme_callback)
    else:
        theme_apply(theme_setting)
