import argparse
import pathlib
import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication
# from qtconsole.inprocess import QtInProcessKernelManager

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    """Catch qtpy exceptions."""
    # https://stackoverflow.com/questions/43039048/pyqt5-fails-with-cryptic-message

    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


def process_cl_args():
    """Process known arguments."""
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


def main():
    """Main app entrypoint."""
    # Set the exception hook to our wrapping function
    sys.excepthook = exception_hook

    # Create application
    parsed_args, unparsed_args = process_cl_args()
    qt_args = sys.argv[:1] + unparsed_args
    app = QApplication(qt_args)

    # Create kernel
    # kernel_manager = QtInProcessKernelManager()
    # kernel_manager.start_kernel(show_banner=True)
    # kernel = kernel_manager.kernel
    # kernel.gui = 'qt'

    # Create main window and show
    from .MainWindow import MainWindow
    application = MainWindow(None)  # (kernel_manager)
    application.show()

    if parsed_args.file:
        filepaths = [pathlib.Path(x) for x in parsed_args.file]
        application.load(filepaths)

    elif parsed_args.folder:
        folder = pathlib.Path(parsed_args.folder)
        filepaths = [x for x in folder.iterdir() if not x.is_dir()]
        application.load(filepaths)

    # Execute
    sys.exit(app.exec_())
