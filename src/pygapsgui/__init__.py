import pathlib
import sys

import qtpy
from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

# Scaling for high dpi screens DEPRECATED in QT6
if qtpy.API in (qtpy.PYQT5_API + qtpy.PYSIDE2_API):
    QW.QApplication.setAttribute(QC.Qt.AA_EnableHighDpiScaling, True)
    QW.QApplication.setAttribute(QC.Qt.AA_UseHighDpiPixmaps, True)


def exception_hook(exctype, exc, trace):
    """Catch qtpy exceptions.
    https://stackoverflow.com/questions/43039048/pyqt5-fails-with-cryptic-message
    """
    import traceback
    trace_s = "".join(traceback.format_tb(trace))

    from pygapsgui.widgets.UtilityDialogs import error_detail_dialog
    error_detail_dialog(str(exc), trace_s)

    # Call the normal Exception hook after
    sys._excepthook(exctype, exc, trace)


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
    parser.add_argument(
        '--test',
        action="store_true",
        help="Attempt startup then exit.",
    )
    parser.add_argument(
        '--version',
        action="store_true",
        help="Print current version.",
    )

    parsed_args, unparsed_args = parser.parse_known_args()
    return parsed_args, unparsed_args


def main():
    """Main app entrypoint."""

    # Set custom exception hook
    sys._excepthook = sys.excepthook
    sys.excepthook = exception_hook

    # Process cli arguments
    parsed_args, unparsed_args = process_cl_args()
    qt_args = sys.argv[:1] + unparsed_args

    if parsed_args.version:
        from importlib.metadata import PackageNotFoundError
        from importlib.metadata import version as im_version
        try:
            version = im_version("pygapsgui")
        except PackageNotFoundError:
            import src.pygapsgui as pygapsgui
            version = pygapsgui.__version__
        print(version)
        sys.exit()

    # Create application
    app = QW.QApplication(qt_args)
    app.setOrganizationName("pyGAPS")
    app.setApplicationName("pyGAPS-gui")

    # Splashscreen
    from pygapsgui.SplashScreen import SplashScreen
    splash = SplashScreen()
    splash.show()
    app.processEvents()

    # Resources
    splash.showMessage("Loading resources...", 40)
    from pygapsgui.utilities.color_theme import set_theme
    set_theme()
    from pygapsgui.utilities.resources import get_resource
    icon = QG.QIcon()
    icon.addFile(get_resource('main_icon.png'), QC.QSize(48, 48))
    icon.addFile(get_resource('main_icon.png'), QC.QSize(100, 100))
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

    if parsed_args.test:
        sys.exit()

    # Execute
    sys.exit(app.exec_())
