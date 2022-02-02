import pathlib
import sys

from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

# Scaling for high dpi screens # TODO deprecated in pyside6
QW.QApplication.setAttribute(QC.Qt.AA_EnableHighDpiScaling, True)
QW.QApplication.setAttribute(QC.Qt.AA_UseHighDpiPixmaps, True)


def exception_hook(exctype, exc, trace):
    """Catch qtpy exceptions."""
    # https://stackoverflow.com/questions/43039048/pyqt5-fails-with-cryptic-message
    import traceback

    trace_s = "".join(traceback.format_tb(trace))

    from pygapsgui.widgets.UtilityWidgets import error_detail_dialog
    error_detail_dialog(str(exc), trace_s)

    # Call the normal Exception hook after
    sys._excepthook(exctype, exc, trace)


# Resources
def get_resource(file):
    """Convenience function to locate resources"""
    return pathlib.Path(__file__).parent / 'resources' / file


def process_cl_args():
    """Process known arguments."""
    import argparse
    parser = argparse.ArgumentParser(description='Directly open isotherms.')
    parser.add_argument(
        '--file',
        '-f',
        action='store',
        nargs='+',
        help="Open one or more isotherms.",
    )
    parser.add_argument(
        '--folder',
        action='store',
        help="Open a folder of isotherms.",
    )

    parsed_args, unparsed_args = parser.parse_known_args()
    return parsed_args, unparsed_args


@QC.Slot()
def sync_theme_with_system() -> None:
    import darkdetect
    import qdarktheme
    theme = darkdetect.theme().lower()
    stylesheet = qdarktheme.load_stylesheet(theme)
    QW.QApplication.instance().setStyleSheet(stylesheet)


def main():
    """Main app entrypoint."""

    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook
    # Set the exception hook to our wrapping function
    sys.excepthook = exception_hook

    # Process cli arguments
    parsed_args, unparsed_args = process_cl_args()
    qt_args = sys.argv[:1] + unparsed_args

    # Create application
    app = QW.QApplication(qt_args)

    # Splashscreen
    from pygapsgui.SplashScreen import SplashScreen
    splash = SplashScreen()
    splash.show()
    app.processEvents()

    # Resources
    splash.showMessage("Loading resources...", 40)
    # app.paletteChanged.connect(sync_theme_with_system)
    # sync_theme_with_system()
    icon = QG.QIcon()
    icon.addFile('./pygapsgui/resources/main_icon.png', QC.QSize(48, 48))
    icon.addFile('./pygapsgui/resources/main_icon.png', QC.QSize(100, 100))
    app.setWindowIcon(icon)

    # Init pygaps
    splash.showMessage("Initiating backend...", 60)
    from pygapsgui.__init_pygaps__ import init_pygaps
    init_pygaps()

    # Create main window
    splash.showMessage("Starting...", 80)
    from .MainWindow import MainWindow
    mainwnd = MainWindow(None)

    # Load files from cli if needed
    if parsed_args.file:
        filepaths = map(pathlib.Path, parsed_args.file)
        mainwnd.open_iso(filepaths)

    elif parsed_args.folder:
        folder = pathlib.Path(parsed_args.folder)
        filepaths = [x for x in folder.iterdir() if not x.is_dir()]
        mainwnd.open_iso(filepaths)

    # Show and finish
    mainwnd.show()
    splash.finish(mainwnd)
    # Execute
    sys.exit(app.exec_())
