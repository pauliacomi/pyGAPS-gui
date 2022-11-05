from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygaps import MATERIAL_LIST
from pygaps import Material
from pygapsgui.utilities.string_match import fuzzy_match_list_choice
from pygapsgui.widgets.MetadataEditWidget import MetadataEditWidget


class MaterialView(QW.QWidget):
    """QT MVC View for displaying and editing Material properties/metadata."""

    _material = None
    material_changed = QC.Signal(str)

    def __init__(self, material=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.material = material

    def setup_UI(self):
        """Create and set-up static UI elements."""
        self.setObjectName("MaterialView")
        self.resize(400, 500)

        # Create/set layout
        _layout = QW.QVBoxLayout(self)

        # Create widgets
        #
        # Named properties
        self.properties_box = QW.QGroupBox()
        _layout.addWidget(self.properties_box)
        self.properties_layout = QW.QFormLayout(self.properties_box)

        self.name_label = QW.QLabel()
        self.name_value = QW.QLineEdit()
        self.density_label = QW.QLabel()
        self.density_value = QW.QLineEdit()
        self.mm_label = QW.QLabel()
        self.mm_value = QW.QLineEdit()
        self.properties_layout.addRow(self.name_label, self.name_value)
        self.properties_layout.addRow(self.density_label, self.density_value)
        self.properties_layout.addRow(self.mm_label, self.mm_value)

        # metadata
        self.metadata_box = QW.QGroupBox()
        _layout.addWidget(self.metadata_box)
        self.metadata_layout = QW.QVBoxLayout(self.metadata_box)

        # metadata edit widget
        self.meta_edit_widget = MetadataEditWidget()
        self.metadata_layout.addWidget(self.meta_edit_widget)

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, material):
        if not material:
            return

        self._material = material
        self.setup_view()
        self.connect_signals()

    def setup_view(self):
        """Sets up the display of various properties/metadata."""
        self.name_value.setText(self.material.name)
        density = self.material.density
        density = str(density) if density else density
        self.density_value.setText(density)
        mmass = self.material.molar_mass
        mmass = str(mmass) if mmass else mmass
        self.mm_value.setText(mmass)

        self.meta_edit_widget.set_model(self.material)

    def connect_signals(self):
        """Connect permanent signals."""
        self.meta_edit_widget.changed.connect(self.handle_changed)

    def accept(self) -> None:
        """See if any changes were made and emit signal."""
        if not self._material:
            return
        changed = False
        if self.name_value.text() != self.material.name:
            self.material.name = self.name_value.text()
            changed = True
        if self.density_value.text() != self.material.density:
            self.material.density = self.density_value.text()
            changed = True
        if self.mm_value.text() != self.material.molar_mass:
            self.material.molar_mass = self.mm_value.text()
            changed = True
        if changed:
            self.material_changed.emit(str(self.material))

    def handle_changed(self):
        """Handle saving of a metadata in the TableView."""
        self.material_changed.emit(str(self.material))

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.properties_box.setTitle(QW.QApplication.translate("AdsorbateView", "Main properties", None, -1))
        self.name_label.setText(QW.QApplication.translate("MaterialView", "Name", None, -1))
        self.density_label.setText(QW.QApplication.translate("MaterialView", "Density [cm3/g]", None, -1))
        self.mm_label.setText(QW.QApplication.translate("MaterialView", "Molar Mass [mol/g]", None, -1))
        self.metadata_box.setTitle(QW.QApplication.translate("MaterialView", "Other Metadata", None, -1))
        # yapf: enable


class MaterialDialog(QW.QDialog):
    """Dialog with a MaterialView."""
    material_changed = QC.Signal(str)

    def __init__(self, material, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setup_UI()
        self.translate_UI()
        self.connect_signals()
        self.view.material = material

    def setup_UI(self):
        """Create and set-up static UI elements."""

        _layout = QW.QVBoxLayout(self)

        # View
        self.view = MaterialView()
        _layout.addWidget(self.view)

        # Button box
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Ok)
        _layout.addWidget(self.button_box)

    def connect_signals(self):
        """Connect permanent signals."""
        self.view.material_changed.connect(self.material_changed)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def accept(self) -> None:
        self.view.accept()
        return super().accept()

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("MaterialDialog", "Material details", None, -1))
        # yapf: enable


class MaterialListDialog(QW.QDialog):
    """Dialog with a list of Materials and a MaterialView."""
    materials = None
    material_changed = QC.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()
        self.setup_view()

    def setup_UI(self):
        """Create and set-up static UI elements."""

        _layout = QW.QVBoxLayout(self)
        layout_top = QW.QHBoxLayout()
        layout_top_left = QW.QVBoxLayout()
        _layout.addLayout(layout_top)
        layout_top.addLayout(layout_top_left)

        # search + list
        self.search_bar = QW.QLineEdit()
        self.material_list = QW.QListWidget()
        layout_top_left.addWidget(QW.QLabel("Search:"))
        layout_top_left.addWidget(self.search_bar)
        layout_top_left.addWidget(self.material_list)

        # details
        self.material_details = MaterialView()
        layout_top.addWidget(self.material_details)

        # Button box
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Ok | QW.QDialogButtonBox.Close)
        _layout.addWidget(self.button_box)

    def connect_signals(self):
        """Connect permanent signals."""
        self.search_bar.textChanged.connect(self.search_filter)
        self.material_details.material_changed.connect(self.material_changed)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def setup_view(self):
        """Set up the display of various properties/metadata."""
        self.materials = [mat.name for mat in MATERIAL_LIST]
        self.material_list.addItems(self.materials)
        self.material_list.currentItemChanged.connect(self.select_material)

    def select_material(self, item):
        """Select the material for the view."""
        if item:
            self.material_details.material = Material.find(item.text())

    def search_filter(self, text):
        """Filter the material list based on a text."""
        self.material_list.clear()
        if text == "":
            self.material_list.addItems(self.materials)
        else:
            self.material_list.addItems(fuzzy_match_list_choice(text, self.materials))

    def accept(self) -> None:
        """Select a material."""
        self.material_details.accept()
        return super().accept()

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("MaterialListDialog", "pyGAPS Material explorer", None, -1))
        # yapf: enable
