################################################################################
##
## Original design: WANDERSON M.PIMENTA
## V: 1.0.0
## https://github.com/Wanderson-Magalhaes/Splash_Screen_Python_PySide2
##
## Adapted by Paul Iacomi
##
################################################################################

import qtpy
from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW


class SplashScreen(QW.QSplashScreen):
    """A general purpose splashscreen."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setGeometry(0, 0, 680, 400)
        self.setup_UI()
        if qtpy.API in qtpy.PYQT6_API:
            screen = self.screen()
        else:
            screen = QG.QGuiApplication.primaryScreen()
        self.move(screen.availableGeometry().center() - self.frameGeometry().center())

    def drawContents(self, painter: QG.QPainter) -> None:
        """Do nothing on draw."""

    def showMessage(self, text: str, progress: int):
        """Message to show on paint."""
        self.label_loading.setText(text)
        self.progressbar.setValue(progress)
        self.repaint()

    def setup_UI(self):
        """Create all UI components."""
        if self.objectName():
            self.setObjectName("SplashScreen")

        # General window formats
        self.setWindowFlag(QC.Qt.FramelessWindowHint)
        self.setAttribute(QC.Qt.WA_TranslucentBackground)

        # Declare fonts
        font_large = QG.QFont()
        font_large.setFamily("Segoe UI")
        font_large.setPointSize(40)
        font_med1 = QG.QFont()
        font_med1.setFamily("Segoe UI")
        font_med1.setPointSize(14)
        font_med2 = QG.QFont()
        font_med2.setFamily("Segoe UI")
        font_med2.setPointSize(12)
        font_small = QG.QFont()
        font_small.setFamily("Segoe UI")
        font_small.setPointSize(10)

        ## Drop shadow effect
        self.dropShadowFrame = QW.QFrame(self)
        self.dropShadowFrame.setObjectName("dropShadowFrame")
        self.dropShadowFrame.setStyleSheet(
            "QFrame {	\n"
            "	background-color: rgb(56, 58, 89);	\n"
            "	color: rgb(220, 220, 220);\n"
            "	border-radius: 10px;\n"
            "}"
        )
        self.dropShadowFrame.setFrameShape(QW.QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QW.QFrame.Raised)
        self.shadow = QW.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QG.QColor(0, 0, 0, 60))
        self.dropShadowFrame.setGraphicsEffect(self.shadow)

        self.label_title = QW.QLabel(self.dropShadowFrame)
        self.label_title.setObjectName("label_title")
        self.label_title.setGeometry(QC.QRect(0, 90, 661, 90))
        self.label_title.setFont(font_large)
        self.label_title.setStyleSheet("color: rgb(254, 121, 199);")
        self.label_title.setAlignment(QC.Qt.AlignCenter)

        self.label_description = QW.QLabel(self.dropShadowFrame)
        self.label_description.setObjectName("label_description")
        self.label_description.setGeometry(QC.QRect(0, 180, 661, 31))
        self.label_description.setFont(font_med1)
        self.label_description.setStyleSheet("color: rgb(98, 114, 164);")
        self.label_description.setAlignment(QC.Qt.AlignCenter)

        self.progressbar = QW.QProgressBar(self.dropShadowFrame)
        self.progressbar.setObjectName("progressbar")
        self.progressbar.setGeometry(QC.QRect(50, 280, 561, 23))
        self.progressbar.setStyleSheet(
            "QProgressBar {\n"
            "	\n"
            "	background-color: rgb(98, 114, 164);\n"
            "	color: rgb(200, 200, 200);\n"
            "	border-style: none;\n"
            "	border-radius: 10px;\n"
            "	text-align: center;\n"
            "}\n"
            "QProgressBar::chunk{\n"
            "	border-radius: 10px;\n"
            "	background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(254, 121, 199, 255), stop:1 rgba(170, 85, 255, 255));\n"
            "}"
        )
        self.progressbar.setValue(20)
        self.label_loading = QW.QLabel(self.dropShadowFrame)
        self.label_loading.setObjectName("label_loading")
        self.label_loading.setGeometry(QC.QRect(0, 320, 661, 21))
        self.label_loading.setFont(font_med2)
        self.label_loading.setStyleSheet("color: rgb(98, 114, 164);")
        self.label_loading.setAlignment(QC.Qt.AlignCenter)
        self.label_credits = QW.QLabel(self.dropShadowFrame)
        self.label_credits.setObjectName("label_credits")
        self.label_credits.setGeometry(QC.QRect(20, 350, 621, 21))
        self.label_credits.setFont(font_small)
        self.label_credits.setStyleSheet("color: rgb(98, 114, 164);")
        self.label_credits.setAlignment(QC.Qt.AlignRight | QC.Qt.AlignTrailing | QC.Qt.AlignVCenter)

        # Layout
        self._layout = QW.QVBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setObjectName("_layout")
        self._layout.setContentsMargins(10, 10, 10, 10)
        self._layout.addWidget(self.dropShadowFrame)

        self.translate_UI()

        QC.QMetaObject.connectSlotsByName(self)

    # setupUi

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QC.QCoreApplication.translate("SplashScreen", "MainWindow", None))
        self.label_title.setText(QC.QCoreApplication.translate("SplashScreen", "<strong>py</strong>GAPS", None))
        self.label_description.setText(QC.QCoreApplication.translate("SplashScreen", "General Adsorption Processing Suite", None))
        self.label_loading.setText(QC.QCoreApplication.translate("SplashScreen", "loading...", None))
        self.label_credits.setText(QC.QCoreApplication.translate("SplashScreen", "<strong>Created by</strong>: Paul Iacomi", None))
        # yapf: enable

    # retranslateUi
