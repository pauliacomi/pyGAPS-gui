import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from qtconsole.inprocess import QtInProcessKernelManager
from .MainWindow import MainWindow

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    """Catch PySide2 exceptions."""
    # https://stackoverflow.com/questions/43039048/pyqt5-fails-with-cryptic-message

    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


def main():
    """Main app entrypoint."""
    # Set the exception hook to our wrapping function
    sys.excepthook = exception_hook

    # Create application
    app = QApplication(sys.argv)

    # Create kernel
    # kernel_manager = QtInProcessKernelManager()
    # kernel_manager.start_kernel(show_banner=True)
    # kernel = kernel_manager.kernel
    # kernel.gui = 'qt'

    # Create main window and show
    application = MainWindow(None)  # (kernel_manager)
    application.show()

    # Execute
    sys.exit(app.exec_())
