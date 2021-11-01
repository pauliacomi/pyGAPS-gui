import src.widgets.resources_rc

from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from src.views.IsoGraphView import IsoGraphView
from src.views.IsoListView import IsoListView
from src.widgets.IsoUnitWidget import IsoUnitWidget
from src.widgets.MetadataEditWidget import MetadataEditWidget
from src.widgets.MetadataTableWidget import MetadataTableWidget


class MainWindowUI():
    """Main window user interface for pygaps."""
    def setupUi(self, MainWindowUI):
        """Create the window and all its components."""

        # First setup
        MainWindowUI.setObjectName("MainWindowUI")
        MainWindowUI.resize(1200, 700)

        # Icon
        icon = QG.QIcon()
        icon.addPixmap(QG.QPixmap(":/res/designer/icons/01_Warning_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        MainWindowUI.setWindowIcon(icon)

        # Central widget
        self.centralwidget = QW.QWidget(MainWindowUI)
        self.centralwidget.setObjectName("centralwidget")

        # Layout of central widget
        self.mainLayout = QW.QHBoxLayout(self.centralwidget)
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
        QC.QMetaObject.connectSlotsByName(MainWindowUI)

    def setup_iso_explorer(self):
        """Setup all the components in the left isotherm explorer section."""

        # create a groupbox to contain the iso explorer
        self.explorerGroup = QW.QGroupBox(self.centralwidget)
        self.explorerGroup.setObjectName("explorerGroup")
        sizePolicy = QW.QSizePolicy(QW.QSizePolicy.Expanding, QW.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)  # relative 1 col
        self.explorerGroup.setSizePolicy(sizePolicy)

        # the grid layout that organises the iso explorer
        self.explorerLayout = QW.QGridLayout(self.explorerGroup)
        self.explorerLayout.setObjectName("explorerLayout")

        # at the top, the isotherm list widget
        self.isoExplorer = IsoListView(self.explorerGroup)
        self.isoExplorer.setObjectName("isoExplorer")
        self.explorerLayout.addWidget(self.isoExplorer, 0, 0, 1, 2)

        # at the bottom, some handy selection buttons
        self.explorerBottomButtons = QW.QHBoxLayout()

        self.selectAllButton = QW.QPushButton(self.explorerGroup)
        self.selectAllButton.setObjectName("selectAllButton")
        self.explorerBottomButtons.addWidget(self.selectAllButton)

        self.deselectAllButton = QW.QPushButton(self.explorerGroup)
        self.deselectAllButton.setObjectName("deselectAllButton")
        self.explorerBottomButtons.addWidget(self.deselectAllButton)

        self.removeButton = QW.QPushButton(self.explorerGroup)
        self.removeButton.setObjectName("removeButton")
        self.explorerBottomButtons.addWidget(self.removeButton)
        self.explorerLayout.addLayout(self.explorerBottomButtons, 1, 0, 1, 2)

        # all done
        self.mainLayout.addWidget(self.explorerGroup)

    def setup_iso_details(self):
        """Setup all the components in the middle isotherm details section."""

        # create a groupbox for details of one isotherm
        self.propertiesGroup = QW.QGroupBox(self.centralwidget)
        self.propertiesGroup.setObjectName("propertiesGroup")
        sizePolicy = QW.QSizePolicy(QW.QSizePolicy.Expanding, QW.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)  # relative 2 col
        self.propertiesGroup.setSizePolicy(sizePolicy)

        # the grid layout that organises the iso details
        self.propertiesLayout = QW.QGridLayout(self.propertiesGroup)
        self.propertiesLayout.setObjectName("propertiesLayout")

        # at the top, base properties
        self.basePropButtonWidget = QW.QWidget(self.propertiesGroup)
        self.propertiesLayout.addWidget(self.basePropButtonWidget, 0, 0, 1, 1)
        self.basePropLayout = QW.QGridLayout(self.basePropButtonWidget)

        self.materialLabel = QW.QLabel(self.basePropButtonWidget)
        self.materialLabel.setObjectName("materialLabel")
        self.basePropLayout.addWidget(self.materialLabel, 0, 0, 1, 1)
        self.materialEdit = QW.QComboBox(self.basePropButtonWidget)
        self.materialEdit.setInsertPolicy(QW.QComboBox.NoInsert)
        self.materialEdit.setObjectName("materialEdit")
        self.materialEdit.setEditable(True)
        self.basePropLayout.addWidget(self.materialEdit, 0, 1, 1, 1)
        self.materialDetails = QW.QPushButton(self.basePropButtonWidget)
        self.materialDetails.setObjectName("materialDetails")
        self.basePropLayout.addWidget(self.materialDetails, 0, 2, 1, 1)

        self.adsorbateLabel = QW.QLabel(self.basePropButtonWidget)
        self.adsorbateLabel.setObjectName("adsorbateLabel")
        self.basePropLayout.addWidget(self.adsorbateLabel, 1, 0, 1, 1)
        self.adsorbateEdit = QW.QComboBox(self.basePropButtonWidget)
        self.adsorbateEdit.setInsertPolicy(QW.QComboBox.NoInsert)
        self.adsorbateEdit.setObjectName("adsorbateEdit")
        self.adsorbateEdit.setEditable(True)
        self.basePropLayout.addWidget(self.adsorbateEdit, 1, 1, 1, 1)
        self.adsorbateDetails = QW.QPushButton(self.basePropButtonWidget)
        self.adsorbateDetails.setObjectName("adsorbateDetails")
        self.basePropLayout.addWidget(self.adsorbateDetails, 1, 2, 1, 1)

        self.temperatureLabel = QW.QLabel(self.basePropButtonWidget)
        self.temperatureLabel.setObjectName("temperatureLabel")
        self.basePropLayout.addWidget(self.temperatureLabel, 2, 0, 1, 1)
        self.temperatureEdit = QW.QLineEdit(self.basePropButtonWidget)
        self.temperatureEdit.setObjectName("temperatureEdit")
        self.basePropLayout.addWidget(self.temperatureEdit, 2, 1, 1, 1)

        # then, units for isotherm physical quantities
        # the temperature combo is "given" to the unitWidget
        self.temperatureUnit = QW.QComboBox(self.basePropButtonWidget)
        self.temperatureUnit.setObjectName("temperatureUnit")
        self.basePropLayout.addWidget(self.temperatureUnit, 2, 2, 1, 1)
        self.unitPropButtonWidget = IsoUnitWidget(self.temperatureUnit, parent=self.propertiesGroup)
        self.propertiesLayout.addWidget(self.unitPropButtonWidget, 1, 0, 1, 2)

        # then, isotherm metadata
        self.extraPropWidget = QW.QGroupBox(self.propertiesGroup)
        self.propertiesLayout.addWidget(self.extraPropWidget, 2, 0, 1, 2)
        self.extraPropLayout = QW.QVBoxLayout(self.extraPropWidget)

        # metadata edit widget
        self.extraPropButtonWidget = MetadataEditWidget(self.extraPropWidget)
        self.extraPropLayout.addWidget(self.extraPropButtonWidget)

        # metadata table
        self.extraPropTableView = MetadataTableWidget(self.propertiesGroup)
        self.extraPropTableView.setObjectName("extraPropTableView")
        self.extraPropLayout.addWidget(self.extraPropTableView)

        # bottom buttons
        self.detailsBottomButtons = QW.QHBoxLayout()
        self.dataButton = QW.QPushButton(self.propertiesGroup)
        self.dataButton.setObjectName("dataButton")
        self.detailsBottomButtons.addWidget(self.dataButton)
        self.propertiesLayout.addLayout(self.detailsBottomButtons, 3, 0, 1, 3)

        # all done
        self.mainLayout.addWidget(self.propertiesGroup)

    def setup_iso_graph(self):
        """Setup all the components in the right isotherm graph section."""

        # create a groupbox for the isotherm plot
        self.graphGroup = QW.QGroupBox(self.centralwidget)
        self.graphGroup.setObjectName("graphGroup")
        sizePolicy = QW.QSizePolicy(QW.QSizePolicy.Preferred, QW.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)  # relative 3 columns
        self.graphGroup.setSizePolicy(sizePolicy)

        # the grid layout that organises the iso plot
        self.graphGrid = QW.QGridLayout(self.graphGroup)
        self.graphGrid.setObjectName("graphGrid")

        # create the iso plot widget
        self.isoGraph = IsoGraphView(self.graphGroup)
        self.isoGraph.setObjectName("isoGraph")
        self.graphGrid.addWidget(self.isoGraph, 0, 0, 1, 1)

        # all done
        self.mainLayout.addWidget(self.graphGroup)

    def setup_menu_status(self, MainWindowUI):
        """Setup the top menu/statusbar of the main window"""

        # Create menu bar
        self.menubar = QW.QMenuBar(MainWindowUI)
        self.menubar.setGeometry(QC.QRect(0, 0, 900, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QW.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFileImport = QW.QMenu(self.menubar)
        self.menuFileImport.setObjectName("menuFileImport")
        self.menuCharact = QW.QMenu(self.menubar)
        self.menuCharact.setObjectName("menuCharact")
        self.menuHelp = QW.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuModel = QW.QMenu(self.menubar)
        self.menuModel.setObjectName("menuModel")
        MainWindowUI.setMenuBar(self.menubar)

        # Create status bar
        self.statusbar = QW.QStatusBar(MainWindowUI)
        self.statusbar.setObjectName("statusbar")
        MainWindowUI.setStatusBar(self.statusbar)

        # Defining menu actions
        # open
        self.actionOpen = QW.QAction(MainWindowUI)
        icon1 = QG.QIcon()
        icon1.addPixmap(QG.QPixmap(":/res/icons/10_Search_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setShortcut("Ctrl+O")

        # import
        self.actionImport = QW.QAction(MainWindowUI)
        self.actionImport.setObjectName("actionImport")
        icon1 = QG.QIcon()
        icon1.addPixmap(QG.QPixmap(":/res/icons/16_Copy_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.actionImport.setIcon(icon1)
        self.actionImport.setShortcut("Ctrl+I")

        # save
        self.actionSave = QW.QAction(MainWindowUI)
        icon2 = QG.QIcon()
        icon2.addPixmap(QG.QPixmap(":/res/icons/04_Save_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setShortcut("Ctrl+S")

        # quit
        self.actionQuit = QW.QAction(MainWindowUI)
        icon3 = QG.QIcon()
        icon3.addPixmap(QG.QPixmap(":/res/icons/14_Delete_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.actionQuit.setIcon(icon3)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.setShortcut("Ctrl+Q")

        # about
        self.actionAbout = QW.QAction(MainWindowUI)
        icon4 = QG.QIcon()
        icon4.addPixmap(QG.QPixmap(":/res/icons/15_Tick_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.actionAbout.setIcon(icon4)
        self.actionAbout.setObjectName("actionAbout")

        # characterisation
        self.actionBET_SA = QW.QAction(MainWindowUI)
        self.actionBET_SA.setObjectName("actionBET_Surface_Area")
        self.actionLangmuir_SA = QW.QAction(MainWindowUI)
        self.actionLangmuir_SA.setObjectName("actionLangmuir_Surface_Area")
        self.actiont_plot = QW.QAction(MainWindowUI)
        self.actiont_plot.setObjectName("actiont_plot")
        self.actionalpha_s_plot = QW.QAction(MainWindowUI)
        self.actionalpha_s_plot.setObjectName("actionalpha_s_plot")
        self.actionMicroporous_PSD = QW.QAction(MainWindowUI)
        self.actionMicroporous_PSD.setObjectName("actionMicroporous_PSD")
        self.actionMesoporous_PSD = QW.QAction(MainWindowUI)
        self.actionMesoporous_PSD.setObjectName("actionMesoporous_PSD")
        self.actionDFT_Kernel_PSD = QW.QAction(MainWindowUI)
        self.actionDFT_Kernel_PSD.setObjectName("actionDFT_Kernel_PSD")
        self.actionModel_By = QW.QAction(MainWindowUI)
        self.actionModel_By.setObjectName("actionModel_By")
        self.actionGuess_Model = QW.QAction(MainWindowUI)
        self.actionGuess_Model.setObjectName("actionGuess_Model")

        # add all actions to menus
        self.menuFile.addActions([
            self.actionOpen,
            self.actionImport,
            self.actionSave,
        ])
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuCharact.addAction(self.actionBET_SA)
        self.menuCharact.addAction(self.actionLangmuir_SA)
        self.menuCharact.addSeparator()
        self.menuCharact.addAction(self.actiont_plot)
        self.menuCharact.addAction(self.actionalpha_s_plot)
        self.menuCharact.addSeparator()
        self.menuCharact.addActions([
            self.actionMicroporous_PSD,
            self.actionMesoporous_PSD,
            self.actionDFT_Kernel_PSD,
        ])
        self.menuModel.addActions((
            self.actionModel_By,
            self.actionGuess_Model,
        ))
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCharact.menuAction())
        self.menubar.addAction(self.menuModel.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

    def retranslateUi(self, MainWindowUI):
        """Set UI text."""
        MainWindowUI.setWindowTitle(QW.QApplication.translate("MainWindowUI", "pyGAPS-gui", None, -1))
        #
        self.explorerGroup.setTitle(QW.QApplication.translate("MainWindowUI", "Isotherm Explorer", None, -1))
        self.selectAllButton.setText(QW.QApplication.translate("MainWindowUI", "Select All", None, -1))
        self.deselectAllButton.setText(QW.QApplication.translate("MainWindowUI", "Deselect All", None, -1))
        self.removeButton.setText(QW.QApplication.translate("MainWindowUI", "Remove", None, -1))
        #
        self.propertiesGroup.setTitle(QW.QApplication.translate("MainWindowUI", "Isotherm Properties", None, -1))
        self.materialLabel.setText(QW.QApplication.translate("MainWindowUI", "Material", None, -1))
        self.materialDetails.setText(QW.QApplication.translate("MainWindowUI", "Details", None, -1))
        self.adsorbateLabel.setText(QW.QApplication.translate("MainWindowUI", "Adsorbate", None, -1))
        self.adsorbateDetails.setText(QW.QApplication.translate("MainWindowUI", "Details", None, -1))
        self.temperatureLabel.setText(QW.QApplication.translate("MainWindowUI", "Temperature", None, -1))
        self.extraPropWidget.setTitle(QW.QApplication.translate("MainWindowUI", "Metadata", None, -1))
        self.dataButton.setText(QW.QApplication.translate("MainWindowUI", "Isotherm Points", None, -1))
        #
        self.graphGroup.setTitle(QW.QApplication.translate("MainWindowUI", "Isotherm Display", None, -1))
        #
        self.menuFile.setTitle(QW.QApplication.translate("MainWindowUI", "File", None, -1))
        self.menuCharact.setTitle(QW.QApplication.translate("MainWindowUI", "Characterization", None, -1))
        self.menuHelp.setTitle(QW.QApplication.translate("MainWindowUI", "Help", None, -1))
        self.menuModel.setTitle(QW.QApplication.translate("MainWindowUI", "Model", None, -1))
        self.actionOpen.setText(QW.QApplication.translate("MainWindowUI", "Open", None, -1))
        self.actionImport.setText(QW.QApplication.translate("MainWindowUI", "Import", None, -1))
        self.actionSave.setText(QW.QApplication.translate("MainWindowUI", "Save", None, -1))
        self.actionQuit.setText(QW.QApplication.translate("MainWindowUI", "Quit", None, -1))
        self.actionAbout.setText(QW.QApplication.translate("MainWindowUI", "About", None, -1))
        self.actionBET_SA.setText(QW.QApplication.translate("MainWindowUI", "BET Surface Area", None, -1))
        self.actionLangmuir_SA.setText(QW.QApplication.translate("MainWindowUI", "Langmuir Surface Area", None, -1))
        self.actiont_plot.setText(QW.QApplication.translate("MainWindowUI", "t-plot", None, -1))
        self.actionalpha_s_plot.setText(QW.QApplication.translate("MainWindowUI", "alpha-s plot", None, -1))
        self.actionMicroporous_PSD.setText(QW.QApplication.translate("MainWindowUI", "Microporous PSD", None, -1))
        self.actionMesoporous_PSD.setText(QW.QApplication.translate("MainWindowUI", "Mesoporous PSD", None, -1))
        self.actionDFT_Kernel_PSD.setText(QW.QApplication.translate("MainWindowUI", "DFT Kernel PSD", None, -1))
        self.actionModel_By.setText(QW.QApplication.translate("MainWindowUI", "Model Using", None, -1))
        self.actionGuess_Model.setText(QW.QApplication.translate("MainWindowUI", "Model Guess", None, -1))
