import src.widgets.resources_rc

from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from src.views.IsoGraphView import IsoListGraphView
from src.views.IsoListView import IsoListView
from src.widgets.IsoUnitWidget import IsoUnitWidget
from src.widgets.MetadataEditWidget import MetadataEditWidget
from src.widgets.MetadataTableWidget import MetadataTableWidget


class MainWindowUI():
    """Main window user interface for pygaps."""
    def setup_UI(self, MainWindowUI):
        """Create the window and all its components."""

        # First setup
        MainWindowUI.setObjectName("MainWindow")

        # TODO This code is borked for pyside6
        # # remove after finalizing
        # monitor = QW.QDesktopWidget().screenGeometry(0)
        # MainWindowUI.move(monitor.left(), monitor.top())
        # MainWindowUI.resize(monitor.width() * 0.9, monitor.height() * 0.8)

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
        self.translate_UI(MainWindowUI)
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

        self.adsorbate_label = QW.QLabel(self.basePropButtonWidget)
        self.adsorbate_label.setObjectName("adsorbate_label")
        self.basePropLayout.addWidget(self.adsorbate_label, 1, 0, 1, 1)
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
        self.isoGraph = IsoListGraphView(self.graphGroup)
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
        MainWindowUI.setMenuBar(self.menubar)

        # Create menu components
        self.menuFile = QW.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menubar.addAction(self.menuFile.menuAction())
        self.menuCharact = QW.QMenu(self.menubar)
        self.menuCharact.setObjectName("menuCharact")
        self.menubar.addAction(self.menuCharact.menuAction())
        self.menuModel = QW.QMenu(self.menubar)
        self.menuModel.setObjectName("menuModel")
        self.menubar.addAction(self.menuModel.menuAction())
        self.menuPredict = QW.QMenu(self.menubar)
        self.menuPredict.setObjectName("menuPredict")
        self.menubar.addAction(self.menuPredict.menuAction())
        # Submenu
        self.menuIAST = QW.QMenu(self.menubar)
        self.menuIAST.setObjectName("menuPredict")
        self.menuPredict.addAction(self.menuIAST.menuAction())
        self.menuOptions = QW.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menuHelp = QW.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menubar.addAction(self.menuHelp.menuAction())

        # Defining menu actions
        # new
        self.actionNew = QW.QAction(MainWindowUI)
        icon = QG.QIcon()
        icon.addPixmap(QG.QPixmap(":/res/icons/05_Edit_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.actionNew.setIcon(icon)
        self.actionNew.setObjectName("actionNew")
        self.actionNew.setShortcut("Ctrl+O")

        # open
        self.actionOpen = QW.QAction(MainWindowUI)
        icon = QG.QIcon()
        icon.addPixmap(QG.QPixmap(":/res/icons/10_Search_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setShortcut("Ctrl+O")

        # import
        self.actionImport = QW.QAction(MainWindowUI)
        self.actionImport.setObjectName("actionImport")
        icon = QG.QIcon()
        icon.addPixmap(QG.QPixmap(":/res/icons/16_Copy_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.actionImport.setIcon(icon)
        self.actionImport.setShortcut("Ctrl+I")

        # save
        self.actionSave = QW.QAction(MainWindowUI)
        icon = QG.QIcon()
        icon.addPixmap(QG.QPixmap(":/res/icons/04_Save_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.actionSave.setIcon(icon)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setShortcut("Ctrl+S")

        # quit
        self.actionQuit = QW.QAction(MainWindowUI)
        icon = QG.QIcon()
        icon.addPixmap(QG.QPixmap(":/res/icons/14_Delete_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.actionQuit.setIcon(icon)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.setShortcut("Ctrl+Q")

        # characterisation
        self.actionBET_SA = QW.QAction(MainWindowUI)
        self.actionBET_SA.setObjectName("actionBET_Surface_Area")
        self.actionLangmuir_SA = QW.QAction(MainWindowUI)
        self.actionLangmuir_SA.setObjectName("actionLangmuir_Surface_Area")
        self.action_da_plot = QW.QAction(MainWindowUI)
        self.action_da_plot.setObjectName("action_da_plot")
        self.action_dr_plot = QW.QAction(MainWindowUI)
        self.action_dr_plot.setObjectName("action_dr_plot")
        self.action_t_plot = QW.QAction(MainWindowUI)
        self.action_t_plot.setObjectName("action_t_plot")
        self.action_alpha_s_plot = QW.QAction(MainWindowUI)
        self.action_alpha_s_plot.setObjectName("action_alpha_s_plot")
        self.actionMicroporous_PSD = QW.QAction(MainWindowUI)
        self.actionMicroporous_PSD.setObjectName("actionMicroporous_PSD")
        self.actionMesoporous_PSD = QW.QAction(MainWindowUI)
        self.actionMesoporous_PSD.setObjectName("actionMesoporous_PSD")
        self.actionDFT_Kernel_PSD = QW.QAction(MainWindowUI)
        self.actionDFT_Kernel_PSD.setObjectName("actionDFT_Kernel_PSD")
        self.actionIsosteric = QW.QAction(MainWindowUI)
        self.actionIsosteric.setObjectName("actionIsosteric")

        # modelling
        self.actionModelBy = QW.QAction(MainWindowUI)
        self.actionModelBy.setObjectName("actionModelBy")
        self.actionModelGuess = QW.QAction(MainWindowUI)
        self.actionModelGuess.setObjectName("actionModelGuess")
        self.actionModelCreate = QW.QAction(MainWindowUI)
        self.actionModelCreate.setObjectName("actionModelCreate")

        # prediction
        self.actionIASTvle = QW.QAction(MainWindowUI)
        self.actionIASTvle.setObjectName("actionIASTvle")
        self.actionIASTsvp = QW.QAction(MainWindowUI)
        self.actionIASTsvp.setObjectName("actionIASTsvp")
        self.actionIASTgeneral = QW.QAction(MainWindowUI)
        self.actionIASTgeneral.setObjectName("actionIASTgeneral")

        # options
        self.actionAdsorbates = QW.QAction(MainWindowUI)
        self.actionAdsorbates.setObjectName("actionAdsorbates")
        self.actionMaterials = QW.QAction(MainWindowUI)
        self.actionMaterials.setObjectName("actionMaterials")

        # about
        self.actionAbout = QW.QAction(MainWindowUI)
        icon = QG.QIcon()
        icon.addPixmap(QG.QPixmap(":/res/icons/15_Tick_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.actionAbout.setIcon(icon)
        self.actionAbout.setObjectName("actionAbout")

        # add all actions to menus
        self.menuFile.addActions([
            self.actionNew,
            self.actionOpen,
            self.actionImport,
            self.actionSave,
        ])
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        #
        self.menuCharact.addActions([
            self.actionBET_SA,
            self.actionLangmuir_SA,
        ])
        self.menuCharact.addSeparator()
        self.menuCharact.addActions([
            self.action_t_plot,
            self.action_alpha_s_plot,
            self.action_dr_plot,
            self.action_da_plot,
        ])
        self.menuCharact.addSeparator()
        self.menuCharact.addActions([
            self.actionMicroporous_PSD,
            self.actionMesoporous_PSD,
            self.actionDFT_Kernel_PSD,
        ])
        self.menuCharact.addSeparator()
        self.menuCharact.addActions([self.actionIsosteric])
        #
        self.menuModel.addActions((
            self.actionModelBy,
            self.actionModelGuess,
        ))
        self.menuModel.addSeparator()
        self.menuModel.addActions([self.actionModelCreate])
        #
        self.menuIAST.addActions([
            self.actionIASTvle,
            self.actionIASTsvp,
            self.actionIASTgeneral,
        ])
        self.menuOptions.addActions([
            self.actionAdsorbates,
            self.actionMaterials,
        ])
        self.menuHelp.addAction(self.actionAbout)

        # Create status bar
        self.statusbar = QW.QStatusBar(MainWindowUI)
        self.statusbar.setObjectName("statusbar")
        MainWindowUI.setStatusBar(self.statusbar)

    def translate_UI(self, MainWindowUI):
        """Set UI text."""
        MainWindowUI.setWindowTitle(
            QW.QApplication.translate("MainWindowUI", "pyGAPS-gui", None, -1)
        )
        #
        self.explorerGroup.setTitle(
            QW.QApplication.translate("MainWindowUI", "Isotherm Explorer", None, -1)
        )
        self.selectAllButton.setText(
            QW.QApplication.translate("MainWindowUI", "Select All", None, -1)
        )
        self.deselectAllButton.setText(
            QW.QApplication.translate("MainWindowUI", "Deselect All", None, -1)
        )
        self.removeButton.setText(QW.QApplication.translate("MainWindowUI", "Remove", None, -1))
        #
        self.propertiesGroup.setTitle(
            QW.QApplication.translate("MainWindowUI", "Isotherm Properties", None, -1)
        )
        self.materialLabel.setText(QW.QApplication.translate("MainWindowUI", "Material", None, -1))
        self.materialDetails.setText(QW.QApplication.translate("MainWindowUI", "Details", None, -1))
        self.adsorbate_label.setText(
            QW.QApplication.translate("MainWindowUI", "Adsorbate", None, -1)
        )
        self.adsorbateDetails.setText(
            QW.QApplication.translate("MainWindowUI", "Details", None, -1)
        )
        self.temperatureLabel.setText(
            QW.QApplication.translate("MainWindowUI", "Temperature", None, -1)
        )
        self.extraPropWidget.setTitle(
            QW.QApplication.translate("MainWindowUI", "Metadata", None, -1)
        )
        self.dataButton.setText(
            QW.QApplication.translate("MainWindowUI", "Isotherm Points", None, -1)
        )
        #
        self.graphGroup.setTitle(
            QW.QApplication.translate("MainWindowUI", "Isotherm Display", None, -1)
        )
        #
        self.menuFile.setTitle(QW.QApplication.translate("MainWindowUI", "File", None, -1))
        self.menuCharact.setTitle(
            QW.QApplication.translate("MainWindowUI", "Characterization", None, -1)
        )
        self.menuHelp.setTitle(QW.QApplication.translate("MainWindowUI", "Help", None, -1))
        self.menuModel.setTitle(
            QW.QApplication.translate("MainWindowUI", "Model Fitting", None, -1)
        )
        self.menuPredict.setTitle(QW.QApplication.translate("MainWindowUI", "Predict", None, -1))
        self.menuOptions.setTitle(QW.QApplication.translate("MainWindowUI", "Options", None, -1))
        self.actionNew.setText(QW.QApplication.translate("MainWindowUI", "New", None, -1))
        self.actionOpen.setText(QW.QApplication.translate("MainWindowUI", "Open", None, -1))
        self.actionImport.setText(QW.QApplication.translate("MainWindowUI", "Import", None, -1))
        self.actionSave.setText(QW.QApplication.translate("MainWindowUI", "Save", None, -1))
        self.actionQuit.setText(QW.QApplication.translate("MainWindowUI", "Quit", None, -1))
        self.actionAbout.setText(QW.QApplication.translate("MainWindowUI", "About", None, -1))
        self.actionBET_SA.setText(
            QW.QApplication.translate("MainWindowUI", "BET surface area", None, -1)
        )
        self.actionLangmuir_SA.setText(
            QW.QApplication.translate("MainWindowUI", "Langmuir surface area", None, -1)
        )
        self.action_t_plot.setText(QW.QApplication.translate("MainWindowUI", "T-plot", None, -1))
        self.action_alpha_s_plot.setText(
            QW.QApplication.translate("MainWindowUI", "Alpha-s plot", None, -1)
        )
        self.action_da_plot.setText(
            QW.QApplication.translate("MainWindowUI", "Dubinin-Astakov plot", None, -1)
        )
        self.action_dr_plot.setText(
            QW.QApplication.translate("MainWindowUI", "Dubinin-Radushkevich plot", None, -1)
        )
        self.actionMicroporous_PSD.setText(
            QW.QApplication.translate("MainWindowUI", "Microporous PSD", None, -1)
        )
        self.actionMesoporous_PSD.setText(
            QW.QApplication.translate("MainWindowUI", "Mesoporous PSD", None, -1)
        )
        self.actionDFT_Kernel_PSD.setText(
            QW.QApplication.translate("MainWindowUI", "DFT Kernel PSD", None, -1)
        )
        self.actionIsosteric.setText(
            QW.QApplication.translate("MainWindowUI", "Isosteric enthalpy", None, -1)
        )
        self.actionModelBy.setText(
            QW.QApplication.translate("MainWindowUI", "Fit a model", None, -1)
        )
        self.actionModelGuess.setText(
            QW.QApplication.translate("MainWindowUI", "Guess best model", None, -1)
        )
        self.actionModelCreate.setText(
            QW.QApplication.translate("MainWindowUI", "Manually create a model", None, -1)
        )
        self.menuIAST.setTitle(QW.QApplication.translate("MainWindowUI", "IAST", None, -1))
        self.actionIASTvle.setText(
            QW.QApplication.translate("MainWindowUI", "Binary phase equilibrium", None, -1)
        )
        self.actionIASTsvp.setText(
            QW.QApplication.translate("MainWindowUI", "Binary selectivity v. pressure", None, -1)
        )
        self.actionIASTgeneral.setText(
            QW.QApplication.translate(
                "MainWindowUI", "Multicomponent uptake v. pressure", None, -1
            )
        )
        self.actionAdsorbates.setText(
            QW.QApplication.translate("MainWindowUI", "pyGAPS Adsorbates", None, -1)
        )
        self.actionMaterials.setText(
            QW.QApplication.translate("MainWindowUI", "pyGAPS Materials", None, -1)
        )
