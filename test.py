import sys

from qtpy.QtCore import Qt

from qtpy.QtWidgets import QApplication, QLabel

if __name__ == "__main__":

    app = QApplication(sys.argv)

    label = QLabel("Hello World", alignment=Qt.AlignCenter)

    label.show()

    sys.exit(app.exec_())