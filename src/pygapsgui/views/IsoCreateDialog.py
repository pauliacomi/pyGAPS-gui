from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygapsgui.views.IsoEditModelDialog import IsoEditModelWidget
from pygapsgui.views.IsoEditPointDialog import IsoEditPointWidget
from pygapsgui.views.IsoGraphView import IsoGraphView
from pygapsgui.widgets.IsoPropWidget import IsoPropWidget
from pygapsgui.widgets.IsoUnitWidget import IsoUnitWidget
from pygapsgui.widgets.MetadataEditWidget import MetadataEditWidget
from pygapsgui.widgets.UtilityWidgets import LabelOutput


class IsoCreateDialog(QW.QDialog):
    """Manually create an isotherm: QT MVC Dialog."""

    paramWidgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        """Create and set-up static UI elements."""
        self.setObjectName("IsoCreateDialog")

        _layout = QW.QGridLayout(self)

        # Data/metadata tabs
        self.datatype_tab = QW.QTabWidget()
        _layout.addWidget(self.datatype_tab, 0, 0)

        # Metadata
        # Create tab
        self.metadata_widget = QW.QWidget()
        self.metadata_layout = QW.QVBoxLayout(self.metadata_widget)
        self.datatype_tab.addTab(self.metadata_widget, "Metadata")

        # at the top, base properties and units
        self.prop_base_widget = IsoPropWidget()
        self.material_input = self.prop_base_widget.m_input
        self.material_details = self.prop_base_widget.m_button
        self.adsorbate_input = self.prop_base_widget.a_input
        self.adsorbate_details = self.prop_base_widget.a_button
        self.temperature_input = self.prop_base_widget.t_input
        self.temperature_unit = self.prop_base_widget.t_unit
        self.metadata_layout.addWidget(self.prop_base_widget)
        self.unit_widget = IsoUnitWidget(self.temperature_unit)
        self.metadata_layout.addWidget(self.unit_widget)

        # metadata edit widget
        self.metadata_extra_group = QW.QGroupBox()
        self.metadata_extra_layout = QW.QVBoxLayout(self.metadata_extra_group)
        self.metadata_layout.addWidget(self.metadata_extra_group)
        self.metadata_extra_edit_widget = MetadataEditWidget()
        self.metadata_extra_layout.addWidget(self.metadata_extra_edit_widget)

        self.metadata_layout.addStretch()

        # Data
        # Create tab
        self.data_widget = QW.QWidget()
        self.data_layout = QW.QVBoxLayout(self.data_widget)
        self.datatype_tab.addTab(self.data_widget, "Data")

        # Type selection
        self.isotype_tab = QW.QTabWidget()
        self.data_layout.addWidget(self.isotype_tab)

        # FOR POINTS
        self.point_edit = IsoEditPointWidget()
        self.isotype_tab.addTab(self.point_edit, "Point Isotherm")

        # FOR MODEL
        self.model_edit = IsoEditModelWidget()
        self.isotype_tab.addTab(self.model_edit, "Model Isotherm")

        # Output
        self.output_layout = QW.QVBoxLayout()
        _layout.addLayout(self.output_layout, 0, 1)

        # Isotherm display
        self.iso_graph = IsoGraphView()
        self.output_layout.addWidget(self.iso_graph)

        # Output log
        self.output_label = QW.QLabel("Output log:")
        self.output = LabelOutput()
        self.output.setMaximumHeight(120)
        self.output_layout.addWidget(self.output_label)
        self.output_layout.addWidget(self.output)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Cancel)
        _layout.addWidget(self.button_box, 4, 0, 1, 2)

    def sizeHint(self) -> QC.QSize:
        """Suggest ideal dimensions."""
        return QC.QSize(1000, 800)

    def connect_signals(self):
        """Connect permanent signals."""
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("IsoCreateDialog", "Create new Isotherm", None, -1))
        self.metadata_extra_group.setTitle(QW.QApplication.translate("IsoCreateDialog", "Other metadata", None, -1))
        # yapf: enable
