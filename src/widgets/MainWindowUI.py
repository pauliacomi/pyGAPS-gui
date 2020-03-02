import src.widgets.resources_rc

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox
from PySide2.QtWidgets import QSizePolicy, QAbstractItemView
from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton, QComboBox, QFrame
from PySide2.QtWidgets import QMenu, QMenuBar, QAction, QStatusBar

from src.views.IsoGraphView import IsoGraphView
from src.views.IsoListView import IsoListView


class MainWindowUI(object):
    """Main window user interface for pygaps."""

    def setupUi(self, MainWindowUI):
        """Create the window and all its components."""

        # First setup
        MainWindowUI.setObjectName("MainWindowUI")
        MainWindowUI.resize(1200, 700)

        # Icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            ":/res/designer/icons/01_Warning_48x48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindowUI.setWindowIcon(icon)

        # Central widget
        self.centralwidget = QWidget(MainWindowUI)
        self.centralwidget.setObjectName("centralwidget")

        # Layout of central widget
        self.mainLayout = QHBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName("mainLayout")

        # Left Group
        self.setup_iso_explorer()
        # Middle Group
        self.setup_iso_details()
        # Right Group
        self.setup_iso_graph()

        # Now set central widget
        MainWindowUI.setCentralWidget(self.centralwidget)

        # Menu and status bar
        self.setup_menu_status(MainWindowUI)

        # Finally
        self.retranslateUi(MainWindowUI)
        QtCore.QMetaObject.connectSlotsByName(MainWindowUI)

    def setup_iso_explorer(self):
        """
        Setup all the components in the left isotherm explorer section.
        """

        self.explorerGroup = QGroupBox(self.centralwidget)
        self.explorerGroup.setObjectName("explorerGroup")
        sizePolicy = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        self.explorerGroup.setSizePolicy(sizePolicy)

        self.explorerLayout = QGridLayout(self.explorerGroup)
        self.explorerLayout.setObjectName("explorerLayout")
        self.isoExplorer = IsoListView(self.explorerGroup)
        self.isoExplorer.setObjectName("isoExplorer")
        self.explorerLayout.addWidget(self.isoExplorer, 0, 0, 1, 2)

        self.explorerBottomButtons = QHBoxLayout()

        self.selectAllButton = QPushButton(self.explorerGroup)
        self.selectAllButton.setObjectName("selectAllButton")
        self.explorerBottomButtons.addWidget(self.selectAllButton)

        self.deselectAllButton = QPushButton(self.explorerGroup)
        self.deselectAllButton.setObjectName("deselectAllButton")
        self.explorerBottomButtons.addWidget(self.deselectAllButton)

        self.removeButton = QPushButton(self.explorerGroup)
        self.removeButton.setObjectName("removeButton")
        self.explorerBottomButtons.addWidget(self.removeButton)
        self.explorerLayout.addLayout(self.explorerBottomButtons, 1, 0, 1, 2)

        self.mainLayout.addWidget(self.explorerGroup)

    def setup_iso_details(self):
        """
        Setup all the components in the middle isotherm details section.
        """

        self.propertiesGroup = QGroupBox(self.centralwidget)
        self.propertiesGroup.setObjectName("propertiesGroup")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        self.propertiesGroup.setSizePolicy(sizePolicy)
        self.propertiesLayout = QGridLayout(self.propertiesGroup)
        self.propertiesLayout.setObjectName("propertiesLayout")

        self.materialLabel = QLabel(self.propertiesGroup)
        self.materialLabel.setObjectName("materialLabel")
        self.propertiesLayout.addWidget(self.materialLabel, 0, 0, 1, 1)
        self.materialEdit = QLineEdit(self.propertiesGroup)
        self.materialEdit.setObjectName("materialEdit")
        self.propertiesLayout.addWidget(self.materialEdit, 0, 1, 1, 1)
        self.adsorbateLabel = QLabel(self.propertiesGroup)
        self.adsorbateLabel.setObjectName("adsorbateLabel")
        self.propertiesLayout.addWidget(self.adsorbateLabel, 1, 0, 1, 1)
        self.adsorbateEdit = QComboBox(self.propertiesGroup)
        self.adsorbateEdit.setInsertPolicy(QComboBox.NoInsert)
        self.adsorbateEdit.setObjectName("adsorbateEdit")
        self.adsorbateEdit.setEditable(True)
        self.propertiesLayout.addWidget(self.adsorbateEdit, 1, 1, 1, 1)
        self.temperatureLabel = QLabel(self.propertiesGroup)
        self.temperatureLabel.setObjectName("temperatureLabel")
        self.propertiesLayout.addWidget(self.temperatureLabel, 2, 0, 1, 1)
        self.temperatureEdit = QLineEdit(self.propertiesGroup)
        self.temperatureEdit.setObjectName("temperatureEdit")
        self.propertiesLayout.addWidget(self.temperatureEdit, 2, 1, 1, 1)

        # Modes, bases and modes for isotherm physical quantities.
        self.unitGroup = QHBoxLayout()
        self.pressureMode = QComboBox(self.propertiesGroup)
        self.pressureMode.setObjectName("pressureMode")
        self.unitGroup.addWidget(self.pressureMode)
        self.pressureUnit = QComboBox(self.propertiesGroup)
        self.pressureUnit.setObjectName("pressureUnit")
        self.unitGroup.addWidget(self.pressureUnit)
        self.loadingBasis = QComboBox(self.propertiesGroup)
        self.loadingBasis.setObjectName("loadingBasis")
        self.unitGroup.addWidget(self.loadingBasis)
        self.loadingUnit = QComboBox(self.propertiesGroup)
        self.loadingUnit.setObjectName("loadingUnit")
        self.unitGroup.addWidget(self.loadingUnit)
        self.adsorbentBasis = QComboBox(self.propertiesGroup)
        self.adsorbentBasis.setObjectName("adsorbentBasis")
        self.unitGroup.addWidget(self.adsorbentBasis)
        self.adsorbentUnit = QComboBox(self.propertiesGroup)
        self.adsorbentUnit.setObjectName("adsorbentUnit")
        self.unitGroup.addWidget(self.adsorbentUnit)
        self.propertiesLayout.addLayout(self.unitGroup, 3, 0, 1, 2)

        #
        # Other isotherm information
        self.extraPropLayout = QVBoxLayout()
        self.propertiesLayout.addLayout(self.extraPropLayout, 4, 0, 1, 2)

        # Top button layout
        self.extraPropButtonWidget = QtWidgets.QWidget(self.propertiesGroup)
        self.extraPropButtonLayout = QHBoxLayout(self.extraPropButtonWidget)

        self.extraPropLabelAdd = QLabel(self.propertiesGroup)
        self.extraPropLabelAdd.setObjectName("extraPropLabelAdd")
        self.extraPropButtonLayout.addWidget(self.extraPropLabelAdd)

        self.extraPropLineEditAdd = QLineEdit(self.propertiesGroup)
        self.extraPropLineEditAdd.setObjectName("extraPropLineEditAdd")
        self.extraPropButtonLayout.addWidget(self.extraPropLineEditAdd)

        self.extraPropButtonAdd = QPushButton(self.propertiesGroup)
        self.extraPropButtonAdd.setObjectName("extraPropButtonAdd")
        self.extraPropButtonLayout.addWidget(self.extraPropButtonAdd)

        extraPropDivideLine = QFrame(self.propertiesGroup)
        extraPropDivideLine.setFrameShape(QFrame.VLine)
        extraPropDivideLine.setFrameShadow(QFrame.Sunken)
        self.extraPropButtonLayout.addWidget(extraPropDivideLine)

        self.extraPropButtonEdit = QPushButton(self.propertiesGroup)
        self.extraPropButtonEdit.setObjectName("extraPropButtonEdit")
        self.extraPropButtonLayout.addWidget(self.extraPropButtonEdit)

        extraPropDivideLine = QFrame(self.propertiesGroup)
        extraPropDivideLine.setFrameShape(QFrame.VLine)
        extraPropDivideLine.setFrameShadow(QFrame.Sunken)
        self.extraPropButtonLayout.addWidget(extraPropDivideLine)

        self.extraPropButtonDelete = QPushButton(self.propertiesGroup)
        self.extraPropButtonDelete.setObjectName("extraPropButtonDelete")
        self.extraPropButtonLayout.addWidget(self.extraPropButtonDelete)

        self.extraPropLayout.addWidget(self.extraPropButtonWidget)

        # Table View & properties
        self.extraPropTableView = QtWidgets.QTableView(self.propertiesGroup)
        self.extraPropTableView.setSelectionBehavior(
            QtWidgets.QTableView.SelectRows)
        self.extraPropTableView.verticalHeader().setVisible(False)
        self.extraPropTableView.setObjectName("extraPropTableView")
        self.extraPropLayout.addWidget(self.extraPropTableView)

        # TableView Headers
        self.horizontalHTable = self.extraPropTableView.horizontalHeader()
        self.verticalHTable = self.extraPropTableView.verticalHeader()
        self.horizontalHTable.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)
        self.verticalHTable.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)
        self.horizontalHTable.setStretchLastSection(True)

        # self.textInfo = QTextBrowser(self.propertiesGroup)
        # self.textInfo.setObjectName("textInfo")
        # self.propertiesLayout.addWidget(self.textInfo, 4, 0, 1, 2)

        # Bottom buttons
        self.detailsBottomButtons = QHBoxLayout()
        self.dataButton = QPushButton(self.propertiesGroup)
        self.dataButton.setObjectName("dataButton")
        self.detailsBottomButtons.addWidget(self.dataButton)
        self.detailsBottomButtons.addStretch(1)
        self.propertiesLayout.addLayout(self.detailsBottomButtons, 5, 0, 1, 2)
        self.mainLayout.addWidget(self.propertiesGroup)

    def setup_iso_graph(self):
        """
        Setup all the components in the right isotherm graph section.
        """

        self.graphGroup = QGroupBox(self.centralwidget)
        self.graphGroup.setObjectName("graphGroup")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        self.graphGroup.setSizePolicy(sizePolicy)

        self.graphGrid = QGridLayout(self.graphGroup)
        self.graphGrid.setObjectName("graphGrid")
        self.isoGraph = IsoGraphView(self.graphGroup)
        self.isoGraph.setObjectName("isoGraph")
        self.graphGrid.addWidget(self.isoGraph, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.graphGroup)

    def setup_menu_status(self, MainWindowUI):

        # Create menu bar
        self.menubar = QMenuBar(MainWindowUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuCharact = QMenu(self.menubar)
        self.menuCharact.setObjectName("menuCharact")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuModel = QMenu(self.menubar)
        self.menuModel.setObjectName("menuModel")
        MainWindowUI.setMenuBar(self.menubar)

        # Create status bar
        self.statusbar = QStatusBar(MainWindowUI)
        self.statusbar.setObjectName("statusbar")
        MainWindowUI.setStatusBar(self.statusbar)

        # Defining menu actions

        self.actionOpen = QAction(MainWindowUI)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(
            ":/res/icons/10_Search_48x48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setShortcut("Ctrl+O")

        self.actionSave = QAction(MainWindowUI)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/res/icons/04_Save_48x48.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setShortcut("Ctrl+S")

        self.actionQuit = QAction(MainWindowUI)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(
            ":/res/icons/14_Delete_48x48.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon3)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.setShortcut("Ctrl+Q")

        self.actionAbout = QAction(MainWindowUI)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/res/icons/15_Tick_48x48.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon4)
        self.actionAbout.setObjectName("actionAbout")

        self.actionBET_Surface_Area = QAction(MainWindowUI)
        self.actionBET_Surface_Area.setObjectName("actionBET_Surface_Area")
        self.actionLangmuir_Surface_Area = QAction(MainWindowUI)
        self.actionLangmuir_Surface_Area.setObjectName(
            "actionLangmuir_Surface_Area")
        self.actiont_plot = QAction(MainWindowUI)
        self.actiont_plot.setObjectName("actiont_plot")
        self.actionalpha_s_plot = QAction(MainWindowUI)
        self.actionalpha_s_plot.setObjectName("actionalpha_s_plot")
        self.actionMicroporous_PSD = QAction(MainWindowUI)
        self.actionMicroporous_PSD.setObjectName("actionMicroporous_PSD")
        self.actionMesoporous_PSD = QAction(MainWindowUI)
        self.actionMesoporous_PSD.setObjectName("actionMesoporous_PSD")
        self.actionDFT_Kernel_PSD = QAction(MainWindowUI)
        self.actionDFT_Kernel_PSD.setObjectName("actionDFT_Kernel_PSD")
        self.actionModel_By = QAction(MainWindowUI)
        self.actionModel_By.setObjectName("actionModel_By")
        self.actionGuess_Model = QAction(MainWindowUI)
        self.actionGuess_Model.setObjectName("actionGuess_Model")

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuCharact.addAction(self.actionBET_Surface_Area)
        self.menuCharact.addAction(self.actionLangmuir_Surface_Area)
        self.menuCharact.addSeparator()
        self.menuCharact.addAction(self.actiont_plot)
        self.menuCharact.addAction(self.actionalpha_s_plot)
        self.menuCharact.addSeparator()
        self.menuCharact.addAction(self.actionMicroporous_PSD)
        self.menuCharact.addAction(self.actionMesoporous_PSD)
        self.menuCharact.addAction(self.actionDFT_Kernel_PSD)
        self.menuModel.addAction(self.actionModel_By)
        self.menuModel.addAction(self.actionGuess_Model)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCharact.menuAction())
        self.menubar.addAction(self.menuModel.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

    def retranslateUi(self, MainWindowUI):
        MainWindowUI.setWindowTitle(QApplication.translate(
            "MainWindowUI", "pyGAPS-gui", None, -1))
        self.explorerGroup.setTitle(QApplication.translate(
            "MainWindowUI", "Isotherm Explorer", None, -1))
        self.propertiesGroup.setTitle(QApplication.translate(
            "MainWindowUI", "Isotherm Properties", None, -1))
        self.temperatureLabel.setText(QApplication.translate(
            "MainWindowUI", "Temperature (K)", None, -1))
        self.adsorbateLabel.setText(QApplication.translate(
            "MainWindowUI", "Adsorbate", None, -1))
        self.materialLabel.setText(QApplication.translate(
            "MainWindowUI", "Material", None, -1))
        self.selectAllButton.setText(QApplication.translate(
            "MainWindowUI", "Select All", None, -1))
        self.deselectAllButton.setText(QApplication.translate(
            "MainWindowUI", "Deselect All", None, -1))
        self.extraPropLabelAdd.setText(QApplication.translate(
            "MainWindowUI", "Property", None, -1))
        self.extraPropButtonAdd.setText(QApplication.translate(
            "MainWindowUI", "+", None, -1))
        self.extraPropButtonEdit.setText(QApplication.translate(
            "MainWindowUI", "edt", None, -1))
        self.extraPropButtonDelete.setText(QApplication.translate(
            "MainWindowUI", "del", None, -1))
        self.dataButton.setText(QApplication.translate(
            "MainWindowUI", "Data", None, -1))
        self.removeButton.setText(QApplication.translate(
            "MainWindowUI", "Remove", None, -1))
        self.graphGroup.setTitle(QApplication.translate(
            "MainWindowUI", "Isotherm Overlay", None, -1))
        self.menuFile.setTitle(QApplication.translate(
            "MainWindowUI", "File", None, -1))
        self.menuCharact.setTitle(QApplication.translate(
            "MainWindowUI", "Characterization", None, -1))
        self.menuHelp.setTitle(QApplication.translate(
            "MainWindowUI", "Help", None, -1))
        self.menuModel.setTitle(QApplication.translate(
            "MainWindowUI", "Model", None, -1))
        self.actionOpen.setText(QApplication.translate(
            "MainWindowUI", "Open", None, -1))
        self.actionSave.setText(QApplication.translate(
            "MainWindowUI", "Save", None, -1))
        self.actionQuit.setText(QApplication.translate(
            "MainWindowUI", "Quit", None, -1))
        self.actionAbout.setText(QApplication.translate(
            "MainWindowUI", "About", None, -1))
        self.actionBET_Surface_Area.setText(QApplication.translate(
            "MainWindowUI", "BET Surface Area", None, -1))
        self.actionLangmuir_Surface_Area.setText(QApplication.translate(
            "MainWindowUI", "Langmuir Surface Area", None, -1))
        self.actiont_plot.setText(QApplication.translate(
            "MainWindowUI", "t-plot", None, -1))
        self.actionalpha_s_plot.setText(QApplication.translate(
            "MainWindowUI", "alpha-s plot", None, -1))
        self.actionMicroporous_PSD.setText(QApplication.translate(
            "MainWindowUI", "Microporous PSD", None, -1))
        self.actionMesoporous_PSD.setText(QApplication.translate(
            "MainWindowUI", "Mesoporous PSD", None, -1))
        self.actionDFT_Kernel_PSD.setText(QApplication.translate(
            "MainWindowUI", "DFT Kernel PSD", None, -1))
        self.actionModel_By.setText(QApplication.translate(
            "MainWindowUI", "Model Using", None, -1))
        self.actionGuess_Model.setText(QApplication.translate(
            "MainWindowUI", "Model Guess", None, -1))
