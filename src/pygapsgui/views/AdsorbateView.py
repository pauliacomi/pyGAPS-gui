from qtpy import PYSIDE6
from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

if PYSIDE6:
    import PySide6.QtSvgWidgets as QS
else:
    from qtpy import QtSvg as QS

from pygaps import ADSORBATE_LIST
from pygaps import Adsorbate
from pygapsgui.utilities.string_match import fuzzy_match_list
from pygapsgui.utilities.tex2svg import tex2svg
from pygapsgui.widgets.MetadataEditWidget import MetadataEditWidget
from pygapsgui.widgets.UtilityWidgets import LabelAlignCenter


class AdsorbateView(QW.QWidget):
    """QT MVC View for displaying and editing Adsorbate properties/metadata."""

    _adsorbate = None
    adsorbate_changed = QC.Signal(str)

    def __init__(self, adsorbate=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.adsorbate = adsorbate

    def setup_UI(self):
        """Create and set-up static UI elements."""
        self.setObjectName("AdsorbateView")
        self.resize(500, 500)

        # Create/set layout
        _layout = QW.QVBoxLayout(self)

        # Create widgets
        #
        # Named properties
        self.properties_box = QW.QGroupBox()
        _layout.addWidget(self.properties_box)
        self.properties_layout = QW.QFormLayout(self.properties_box)

        self.name_label = QW.QLabel()
        self.name_value = LabelAlignCenter()
        self.alias_label = QW.QLabel()
        self.alias_value = QW.QListWidget()
        self.alias_value.setSizePolicy(
            QW.QSizePolicy(QW.QSizePolicy.Minimum, QW.QSizePolicy.Minimum)
        )
        self.formula_label = QW.QLabel()
        self.formula_value = QS.QSvgWidget()
        self.formula_value.setMinimumSize(50, 15)
        self.formula_value.setMaximumSize(300, 30)
        self.backend_label = QW.QLabel()
        self.backend_value = LabelAlignCenter()
        self.properties_layout.addRow(self.name_label, self.name_value)
        self.properties_layout.addRow(self.alias_label, self.alias_value)
        self.properties_layout.addRow(self.formula_label, self.formula_value)
        self.properties_layout.addRow(self.backend_label, self.backend_value)

        # metadata
        self.metadata_box = QW.QGroupBox()
        _layout.addWidget(self.metadata_box)
        self.metadata_layout = QW.QVBoxLayout(self.metadata_box)

        # metadata edit widget
        self.meta_edit_widget = MetadataEditWidget()
        self.metadata_layout.addWidget(self.meta_edit_widget)

    @property
    def adsorbate(self):
        return self._adsorbate

    @adsorbate.setter
    def adsorbate(self, adsorbate):
        if not adsorbate:
            return

        self._adsorbate = adsorbate
        self.setup_view()
        self.connect_signals()

    def setup_view(self):
        """Sets up the display of various properties/metadata."""
        self.name_value.setText(self.adsorbate.name)
        self.alias_value.clear()
        self.alias_value.addItems(self.adsorbate.alias)
        self.alias_value.setFixedHeight(
            self.alias_value.sizeHintForRow(0) * 4 + 2 * self.alias_value.frameWidth()
        )
        self.formula_value.load(tex2svg(self.adsorbate.formula))
        aspectRatioMode = QC.Qt.AspectRatioMode(QC.Qt.KeepAspectRatio)
        self.formula_value.renderer().setAspectRatioMode(aspectRatioMode)
        if self.adsorbate.properties.get("backend_name"):
            backend = "Yes"
        else:
            backend = "No"
        self.backend_value.setText(backend)

        self.meta_edit_widget.set_model(self.adsorbate)

    def connect_signals(self):
        """Connect permanent signals."""
        self.meta_edit_widget.changed.connect(self.handle_changed)

    def handle_changed(self):
        """Handle changes in EditWidget."""
        self.adsorbate_changed.emit(self.adsorbate.name)

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.properties_box.setTitle(QW.QApplication.translate("AdsorbateView", "Main properties", None, -1))
        self.name_label.setText(QW.QApplication.translate("AdsorbateView", "Name", None, -1))
        self.alias_label.setText(QW.QApplication.translate("AdsorbateView", "Aliases", None, -1))
        self.formula_label.setText(QW.QApplication.translate("AdsorbateView", "Formula", None, -1))
        self.backend_label.setText(QW.QApplication.translate("AdsorbateView", "Thermodynamic backend", None, -1))
        self.metadata_box.setTitle(QW.QApplication.translate("AdsorbateView", "Other Metadata", None, -1))
        # yapf: enable


class AdsorbateDialog(QW.QDialog):
    """Dialog with an AdsorbateView."""
    adsorbate_changed = QC.Signal(str)

    def __init__(self, adsorbate, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setup_UI()
        self.translate_UI()
        self.connect_signals()
        self.view.adsorbate = adsorbate

    def setup_UI(self):
        """Create and set-up static UI elements."""

        _layout = QW.QVBoxLayout(self)

        # View
        self.view = AdsorbateView()
        _layout.addWidget(self.view)

        # Button box
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Ok)
        _layout.addWidget(self.button_box)

    def connect_signals(self):
        """Connect permanent signals."""
        self.view.adsorbate_changed.connect(self.adsorbate_changed)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("AdsorbateDialog", "Adsorbate details", None, -1))
        # yapf: enable


class AdsorbateListDialog(QW.QDialog):
    """Dialog with a list of Adsorbates and an AdsorbateView."""

    adsorbates: dict = None  # all aliases of adsorbates
    adsorbate_changed = QC.Signal(str)

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
        self.adsorbate_list = QW.QListWidget()
        layout_top_left.addWidget(QW.QLabel("Search:"))
        layout_top_left.addWidget(self.search_bar)
        layout_top_left.addWidget(self.adsorbate_list)

        # details
        self.adsorbate_details = AdsorbateView()
        layout_top.addWidget(self.adsorbate_details)

        # Button box
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Ok | QW.QDialogButtonBox.Close)
        _layout.addWidget(self.button_box)

    def connect_signals(self):
        """Connect permanent signals."""
        self.search_bar.textChanged.connect(self.search_filter)
        self.adsorbate_details.adsorbate_changed.connect(self.adsorbate_changed)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def setup_view(self):
        """Add all adsorbates to the view list."""
        self.adsorbates = {ads.name: ads.alias for ads in ADSORBATE_LIST}
        self.adsorbate_list.addItems(self.adsorbates.keys())
        self.adsorbate_list.currentItemChanged.connect(self.select_adsorbate)

    def select_adsorbate(self, item):
        """Select an adsorbate for the view."""
        if item:
            self.adsorbate_details.adsorbate = Adsorbate.find(item.text())

    def search_filter(self, text):
        """Filter the adsorbate list based on a text."""
        self.adsorbate_list.clear()
        if text == "":
            self.adsorbate_list.addItems(self.adsorbates.keys())
        else:
            self.adsorbate_list.addItems([
                k for (k, v) in self.adsorbates.items() if fuzzy_match_list(text, v)
            ])

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("AdsorbateListDialog", "pyGAPS Adsorbate explorer", None, -1))
        # yapf: enable
