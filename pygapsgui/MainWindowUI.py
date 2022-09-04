import qtpy
from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

import pygapsgui.widgets.resources_rc
from pygapsgui.views.IsoGraphView import IsoListGraphView
from pygapsgui.views.IsoListView import IsoListView
from pygapsgui.views.MetadataTableView import MetadataTableView
from pygapsgui.widgets.IsoUnitWidget import IsoUnitWidget
from pygapsgui.widgets.MetadataEditWidget import MetadataEditWidget
from pygapsgui.widgets.SciDoubleSpinbox import SciFloatDelegate
from pygapsgui.widgets.UtilityWidgets import LabelAlignRight


class MainWindowUI():
    """Main window user interface for pygaps."""
    def setup_UI(self, main_window):
        """Create the window and all its components."""

        # First setup
        main_window.setObjectName("MainWindow")

        # Central widget
        self.central_widget = QW.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")

        # Layout of central widget
        self.main_layout = QW.QHBoxLayout(self.central_widget)
        self.main_layout.setObjectName("main_layout")

        # Left Group
        self.setup_iso_explorer()
        # Middle Group
        self.setup_iso_details()
        # Right Group
        self.setup_iso_graph()

        # Now set central widget
        main_window.setCentralWidget(self.central_widget)

        # Menu and status bar
        self.setup_menu_status(main_window)

        # Translate
        self.translate_UI(main_window)
        QC.QMetaObject.connectSlotsByName(main_window)

        # Move on screen to reasonable location with 2:1 aspect ratio
        if qtpy.API in qtpy.PYQT6_API:
            screen = self.screen()
        else:
            screen = QG.QGuiApplication.primaryScreen()
        geometry = screen.availableGeometry()
        height = geometry.height() * 0.75
        width = geometry.width() * 0.8
        width = min(width, height * 2)
        main_window.setGeometry(0, 0, width, height)
        main_window.move(geometry.center() - main_window.frameGeometry().center())

    def setup_iso_explorer(self):
        """Setup all the components in the left isotherm explorer section."""

        # create a groupbox to contain the iso explorer
        self.explorer_group = QW.QGroupBox()
        self.explorer_group.setObjectName("explorer_group")
        size_policy = QW.QSizePolicy(QW.QSizePolicy.Expanding, QW.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(1)  # relative 1 col
        self.explorer_group.setSizePolicy(size_policy)
        self.main_layout.addWidget(self.explorer_group)

        # the grid layout that organises the iso explorer
        self.explorer_layout = QW.QGridLayout(self.explorer_group)
        self.explorer_layout.setObjectName("explorer_layout")

        # at the top, the isotherm list widget
        self.iso_explorer = IsoListView()
        self.iso_explorer.setObjectName("iso_explorer")
        self.explorer_layout.addWidget(self.iso_explorer, 0, 0, 1, 2)

        # at the bottom, some handy selection buttons
        self.explorer_buttons = QW.QHBoxLayout()

        self.exp_select_button = QW.QPushButton()
        self.exp_select_button.setObjectName("exp_select_button")
        self.explorer_buttons.addWidget(self.exp_select_button)

        self.exp_deselect_button = QW.QPushButton()
        self.exp_deselect_button.setObjectName("exp_deselect_button")
        self.explorer_buttons.addWidget(self.exp_deselect_button)

        self.exp_remove_button = QW.QPushButton()
        self.exp_remove_button.setObjectName("exp_remove_button")
        self.explorer_buttons.addWidget(self.exp_remove_button)
        self.explorer_layout.addLayout(self.explorer_buttons, 1, 0, 1, 2)

    def setup_iso_details(self):
        """Setup all the components in the middle isotherm details section."""

        # create a groupbox for details of one isotherm
        self.properties_group = QW.QGroupBox()
        self.properties_group.setObjectName("properties_group")
        size_policy = QW.QSizePolicy(QW.QSizePolicy.Expanding, QW.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(2)  # relative 2 col
        self.properties_group.setSizePolicy(size_policy)
        self.main_layout.addWidget(self.properties_group)

        # the grid layout that organises the iso details
        self.properties_layout = QW.QGridLayout(self.properties_group)
        self.properties_layout.setObjectName("properties_layout")

        # at the top, base properties
        self.prop_base_layout = QW.QGridLayout()
        self.properties_layout.addLayout(self.prop_base_layout, 0, 0, 1, 1)

        self.material_label = LabelAlignRight()
        self.material_label.setObjectName("material_label")
        self.material_input = QW.QComboBox()
        self.material_input.setInsertPolicy(QW.QComboBox.NoInsert)
        self.material_input.setObjectName("material_input")
        self.material_input.setEditable(True)
        self.material_details = QW.QPushButton()
        self.material_details.setObjectName("material_details")
        self.prop_base_layout.addWidget(self.material_label, 0, 0, 1, 1)
        self.prop_base_layout.addWidget(self.material_input, 0, 1, 1, 1)
        self.prop_base_layout.addWidget(self.material_details, 0, 2, 1, 1)

        self.adsorbate_label = LabelAlignRight()
        self.adsorbate_label.setObjectName("adsorbate_label")
        self.adsorbate_input = QW.QComboBox()
        self.adsorbate_input.setInsertPolicy(QW.QComboBox.NoInsert)
        self.adsorbate_input.setObjectName("adsorbate_input")
        self.adsorbate_input.setEditable(True)
        self.adsorbate_details = QW.QPushButton()
        self.adsorbate_details.setObjectName("adsorbate_details")
        self.prop_base_layout.addWidget(self.adsorbate_label, 1, 0, 1, 1)
        self.prop_base_layout.addWidget(self.adsorbate_input, 1, 1, 1, 1)
        self.prop_base_layout.addWidget(self.adsorbate_details, 1, 2, 1, 1)

        self.temperature_label = LabelAlignRight()
        self.temperature_label.setObjectName("temperature_label")
        self.temperature_input = QW.QDoubleSpinBox()
        self.temperature_input.setMinimum(-999)
        self.temperature_input.setMaximum(9999)
        self.temperature_input.setObjectName("temperature_input")
        self.prop_base_layout.addWidget(self.temperature_label, 2, 0, 1, 1)
        self.prop_base_layout.addWidget(self.temperature_input, 2, 1, 1, 1)

        # then, units for isotherm physical quantities
        # the temperature combo is "given" to the unitWidget
        self.temperature_unit = QW.QComboBox()
        self.temperature_unit.setObjectName("temperature_unit")
        self.prop_unit_widget = IsoUnitWidget(self.temperature_unit)
        self.prop_base_layout.addWidget(self.temperature_unit, 2, 2, 1, 1)
        self.properties_layout.addWidget(self.prop_unit_widget, 1, 0, 1, 2)

        # then, isotherm metadata
        self.prop_extra_group = QW.QGroupBox()
        self.properties_layout.addWidget(self.prop_extra_group, 2, 0, 1, 1)
        self.prop_extra_layout = QW.QVBoxLayout(self.prop_extra_group)

        # metadata edit widget
        self.prop_extra_edit_widget = MetadataEditWidget()
        self.prop_extra_layout.addWidget(self.prop_extra_edit_widget)

        # metadata table
        self.metadata_table_view = MetadataTableView()
        delegate = SciFloatDelegate()
        self.metadata_table_view.setItemDelegate(delegate)
        self.metadata_table_view.setObjectName("metadata_table_view")
        self.prop_extra_layout.addWidget(self.metadata_table_view)

        # bottom buttons
        self.details_button_layout = QW.QHBoxLayout()
        self.data_button = QW.QPushButton()
        self.data_button.setObjectName("data_button")
        self.details_button_layout.addWidget(self.data_button)
        self.properties_layout.addLayout(self.details_button_layout, 3, 0, 1, 3)

    def setup_iso_graph(self):
        """Setup all the components in the right isotherm graph section."""

        # create a groupbox for the isotherm plot
        self.graph_group = QW.QGroupBox(self.central_widget)
        self.graph_group.setObjectName("graph_group")
        size_policy = QW.QSizePolicy(QW.QSizePolicy.Preferred, QW.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(3)  # relative 3 columns
        self.graph_group.setSizePolicy(size_policy)
        self.main_layout.addWidget(self.graph_group)

        # the grid layout that organises the iso plot
        self.graph_layout = QW.QVBoxLayout(self.graph_group)
        self.graph_layout.setObjectName("graph_layout")

        # create the iso plot widget
        self.iso_graph = IsoListGraphView()
        self.iso_graph.setObjectName("iso_graph")
        self.graph_layout.addWidget(self.iso_graph)

    def setup_menu_status(self, main_window):
        """Setup the top menu/statusbar of the main window"""

        # Create menu bar
        self.menubar = QW.QMenuBar(main_window)
        self.menubar.setGeometry(QC.QRect(0, 0, 900, 30))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)

        # Create menu components
        self.menu_file = QW.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menubar.addAction(self.menu_file.menuAction())
        self.menu_recent = QW.QMenu(self.menubar)
        self.menu_recent.setObjectName("menu_openrecent")

        self.menu_charact = QW.QMenu(self.menubar)
        self.menu_charact.setObjectName("menu_charact")
        self.menubar.addAction(self.menu_charact.menuAction())

        self.menu_model = QW.QMenu(self.menubar)
        self.menu_model.setObjectName("menu_model")
        self.menubar.addAction(self.menu_model.menuAction())

        self.menu_predict = QW.QMenu(self.menubar)
        self.menu_predict.setObjectName("menu_predict")
        self.menubar.addAction(self.menu_predict.menuAction())
        # Submenu
        self.menu_iast = QW.QMenu(self.menubar)
        self.menu_iast.setObjectName("menu_iast")
        self.menu_predict.addAction(self.menu_iast.menuAction())

        self.menu_options = QW.QMenu(self.menubar)
        self.menu_options.setObjectName("menu_options")
        self.menubar.addAction(self.menu_options.menuAction())
        self.menu_help = QW.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        self.menubar.addAction(self.menu_help.menuAction())

        # Defining menu actions
        # new
        self.action_new = QW.QAction(main_window)
        icon = QG.QIcon()
        icon.addPixmap(QG.QPixmap(":/res/icons/05_Edit_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.action_new.setIcon(icon)
        self.action_new.setObjectName("action_new")
        self.action_new.setShortcut("Ctrl+N")

        # open
        self.action_open = QW.QAction(main_window)
        icon = QG.QIcon()
        icon.addPixmap(QG.QPixmap(":/res/icons/10_Search_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.action_open.setIcon(icon)
        self.action_open.setObjectName("action_open")
        self.action_open.setShortcut("Ctrl+O")

        # import
        self.action_import = QW.QAction(main_window)
        self.action_import.setObjectName("action_import")
        icon = QG.QIcon()
        icon.addPixmap(QG.QPixmap(":/res/icons/16_Copy_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.action_import.setIcon(icon)
        self.action_import.setShortcut("Ctrl+I")

        # save
        self.action_save = QW.QAction(main_window)
        icon = QG.QIcon()
        icon.addPixmap(QG.QPixmap(":/res/icons/04_Save_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.action_save.setIcon(icon)
        self.action_save.setObjectName("action_save")
        self.action_save.setShortcut("Ctrl+S")

        # quit
        self.action_quit = QW.QAction(main_window)
        icon = QG.QIcon()
        icon.addPixmap(QG.QPixmap(":/res/icons/14_Delete_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.action_quit.setIcon(icon)
        self.action_quit.setObjectName("action_quit")
        self.action_quit.setShortcut("Ctrl+Q")

        # characterisation
        self.action_area_bet = QW.QAction(main_window)
        self.action_area_bet.setObjectName("actionBET_Surface_Area")
        self.action_area_lang = QW.QAction(main_window)
        self.action_area_lang.setObjectName("actionLangmuir_Surface_Area")
        self.action_da_plot = QW.QAction(main_window)
        self.action_da_plot.setObjectName("action_da_plot")
        self.action_dr_plot = QW.QAction(main_window)
        self.action_dr_plot.setObjectName("action_dr_plot")
        self.action_t_plot = QW.QAction(main_window)
        self.action_t_plot.setObjectName("action_t_plot")
        self.action_alpha_s_plot = QW.QAction(main_window)
        self.action_alpha_s_plot.setObjectName("action_alpha_s_plot")
        self.action_psd_micro = QW.QAction(main_window)
        self.action_psd_micro.setObjectName("action_psd_micro")
        self.action_psd_meso = QW.QAction(main_window)
        self.action_psd_meso.setObjectName("action_psd_meso")
        self.action_psd_kernel = QW.QAction(main_window)
        self.action_psd_kernel.setObjectName("action_psd_kernel")
        self.action_isosteric = QW.QAction(main_window)
        self.action_isosteric.setObjectName("action_isosteric")

        # modelling
        self.action_model_by = QW.QAction(main_window)
        self.action_model_by.setObjectName("action_model_by")
        self.action_model_guess = QW.QAction(main_window)
        self.action_model_guess.setObjectName("action_model_guess")
        self.action_model_manual = QW.QAction(main_window)
        self.action_model_manual.setObjectName("action_model_manual")

        # prediction
        self.action_iast_binary_vle = QW.QAction(main_window)
        self.action_iast_binary_vle.setObjectName("action_iast_binary_vle")
        self.action_iast_binary_svp = QW.QAction(main_window)
        self.action_iast_binary_svp.setObjectName("action_iast_binary_svp")
        self.action_iast_multi_lvp = QW.QAction(main_window)
        self.action_iast_multi_lvp.setObjectName("action_iast_multi_lvp")

        # options
        self.action_adsorbates = QW.QAction(main_window)
        self.action_adsorbates.setObjectName("action_adsorbates")
        self.action_materials = QW.QAction(main_window)
        self.action_materials.setObjectName("action_materials")

        # about and example
        self.action_examples = QW.QAction(main_window)
        self.action_about = QW.QAction(main_window)
        icon = QG.QIcon()
        icon.addPixmap(QG.QPixmap(":/res/icons/15_Tick_48x48.png"), QG.QIcon.Normal, QG.QIcon.Off)
        self.action_about.setIcon(icon)
        self.action_about.setObjectName("action_about")

        # add all actions to menus
        self.menu_file.addActions([
            self.action_new,
            self.action_open,
            self.menu_recent.menuAction(),
            self.action_import,
            self.action_save,
        ])
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_quit)
        #
        self.menu_charact.addActions([
            self.action_area_bet,
            self.action_area_lang,
        ])
        self.menu_charact.addSeparator()
        self.menu_charact.addActions([
            self.action_t_plot,
            self.action_alpha_s_plot,
            self.action_dr_plot,
            self.action_da_plot,
        ])
        self.menu_charact.addSeparator()
        self.menu_charact.addActions([
            self.action_psd_micro,
            self.action_psd_meso,
            self.action_psd_kernel,
        ])
        self.menu_charact.addSeparator()
        self.menu_charact.addActions([self.action_isosteric])
        #
        self.menu_model.addActions((
            self.action_model_by,
            self.action_model_guess,
        ))
        self.menu_model.addSeparator()
        self.menu_model.addActions([self.action_model_manual])
        #
        self.menu_iast.addActions([
            self.action_iast_binary_vle,
            self.action_iast_binary_svp,
            self.action_iast_multi_lvp,
        ])
        self.menu_options.addActions([
            self.action_adsorbates,
            self.action_materials,
        ])
        self.menu_help.addAction(self.action_examples)
        self.menu_help.addAction(self.action_about)

        # Create status bar
        self.statusbar = QW.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

    def translate_UI(self, main_window):
        """Set UI text."""
        # yapf: disable
        # pylint: disable=line-too-long
        main_window.setWindowTitle(QW.QApplication.translate("MainWindow", "pyGAPS-gui", None, -1))
        #
        self.explorer_group.setTitle(QW.QApplication.translate("MainWindow", "Isotherm Explorer", None, -1))
        self.exp_select_button.setText(QW.QApplication.translate("MainWindow", "Select All", None, -1))
        self.exp_deselect_button.setText(QW.QApplication.translate("MainWindow", "Deselect All", None, -1))
        self.exp_remove_button.setText(QW.QApplication.translate("MainWindow", "Delete", None, -1))
        #
        self.properties_group.setTitle(QW.QApplication.translate("MainWindow", "Isotherm Properties", None, -1))
        self.material_label.setText(QW.QApplication.translate("MainWindow", "Material", None, -1))
        self.material_details.setText(QW.QApplication.translate("MainWindow", "Details", None, -1))
        self.adsorbate_label.setText(QW.QApplication.translate("MainWindow", "Adsorbate", None, -1))
        self.adsorbate_details.setText(QW.QApplication.translate("MainWindow", "Details", None, -1))
        self.temperature_label.setText(QW.QApplication.translate("MainWindow", "Temperature", None, -1))
        self.prop_extra_group.setTitle(QW.QApplication.translate("MainWindow", "Metadata", None, -1))
        self.data_button.setText(QW.QApplication.translate("MainWindow", "Isotherm Points", None, -1))
        #
        self.graph_group.setTitle(QW.QApplication.translate("MainWindow", "Isotherm Display", None, -1))
        #
        self.menu_file.setTitle(QW.QApplication.translate("MainWindow", "File", None, -1))
        self.menu_recent.setTitle(QW.QApplication.translate("MainWindow", "Open recent", None, -1))
        self.menu_charact.setTitle(QW.QApplication.translate("MainWindow", "Characterization", None, -1))
        self.menu_help.setTitle(QW.QApplication.translate("MainWindow", "Help", None, -1))
        self.menu_model.setTitle(QW.QApplication.translate("MainWindow", "Model Fitting", None, -1))
        self.menu_predict.setTitle(QW.QApplication.translate("MainWindow", "Predict", None, -1))
        self.menu_options.setTitle(QW.QApplication.translate("MainWindow", "Options", None, -1))
        self.action_new.setText(QW.QApplication.translate("MainWindow", "New", None, -1))
        self.action_open.setText(QW.QApplication.translate("MainWindow", "Open", None, -1))
        self.action_import.setText(QW.QApplication.translate("MainWindow", "Import", None, -1))
        self.action_save.setText(QW.QApplication.translate("MainWindow", "Save", None, -1))
        self.action_quit.setText(QW.QApplication.translate("MainWindow", "Quit", None, -1))
        self.action_examples.setText(QW.QApplication.translate("MainWindow", "Load example data", None, -1))
        self.action_about.setText(QW.QApplication.translate("MainWindow", "About", None, -1))
        self.action_area_bet.setText(QW.QApplication.translate("MainWindow", "BET surface area", None, -1))
        self.action_area_lang.setText(QW.QApplication.translate("MainWindow", "Langmuir surface area", None, -1))
        self.action_t_plot.setText(QW.QApplication.translate("MainWindow", "t-plot", None, -1))
        self.action_alpha_s_plot.setText(QW.QApplication.translate("MainWindow", "Alpha-s plot", None, -1))
        self.action_da_plot.setText(QW.QApplication.translate("MainWindow", "Dubinin-Astakov plot", None, -1))
        self.action_dr_plot.setText(QW.QApplication.translate("MainWindow", "Dubinin-Radushkevich plot", None, -1))
        self.action_psd_micro.setText(QW.QApplication.translate("MainWindow", "Microporous PSD", None, -1))
        self.action_psd_meso.setText(QW.QApplication.translate("MainWindow", "Mesoporous PSD", None, -1))
        self.action_psd_kernel.setText(QW.QApplication.translate("MainWindow", "Kernel Fit PSD", None, -1))
        self.action_isosteric.setText(QW.QApplication.translate("MainWindow", "Isosteric enthalpy", None, -1))
        self.action_model_by.setText(QW.QApplication.translate("MainWindow", "Fit a model", None, -1))
        self.action_model_guess.setText(QW.QApplication.translate("MainWindow", "Guess best model", None, -1))
        self.action_model_manual.setText(QW.QApplication.translate("MainWindow", "Manually create a model", None, -1))
        self.menu_iast.setTitle(QW.QApplication.translate("MainWindow", "IAST", None, -1))
        self.action_iast_binary_vle.setText(QW.QApplication.translate("MainWindow", "Binary phase equilibrium", None, -1))
        self.action_iast_binary_svp.setText(QW.QApplication.translate("MainWindow", "Binary selectivity v. pressure", None, -1))
        self.action_iast_multi_lvp.setText(QW.QApplication.translate("MainWindow", "Multicomponent uptake v. pressure", None, -1))
        self.action_adsorbates.setText(QW.QApplication.translate("MainWindow", "pyGAPS Adsorbates", None, -1))
        self.action_materials.setText(QW.QApplication.translate("MainWindow", "pyGAPS Materials", None, -1))
        # yapf: enable
