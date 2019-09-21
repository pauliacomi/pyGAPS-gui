from qtconsole.qt import QtGui
from qtconsole.rich_jupyter_widget import RichJupyterWidget


class ConsoleView(RichJupyterWidget):

    def __init__(self, manager, client, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.kernel_manager = manager
        self.kernel_client = client
