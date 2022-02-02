from qtpy import PYSIDE6
from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

if PYSIDE6:
    import PySide6.QtSvgWidgets as QS
else:
    from qtpy import QtSvg as QS

from pygaps import ADSORBATE_LIST
from pygaps import Adsorbate
from pygapsgui.models.AdsPropTableModel import AdsPropTableModel
from pygapsgui.utilities.tex2svg import tex2svg
from pygapsgui.widgets.MetadataEditWidget import MetadataEditWidget
from pygapsgui.widgets.MetadataTableView import MetadataTableWidget
from pygapsgui.widgets.UtilityWidgets import LabelAlignCenter
from pygapsgui.widgets.UtilityWidgets import error_dialog


class AdsorbateView(QW.QWidget):

    _adsorbate = None
    adsorbate_changed = QC.Signal(str)

    def __init__(self, adsorbate=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.adsorbate = adsorbate

    def setup_UI(self):
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

        # Table view
        self.table_view = MetadataTableWidget()
        self.metadata_layout.addWidget(self.table_view)

    @property
    def adsorbate(self):
        return self._adsorbate

    @adsorbate.setter
    def adsorbate(self, adsorbate):
        if not adsorbate:
            return

        self._adsorbate = adsorbate
        self.setup_model()
        self.connect_signals()

    def setup_model(self):
        self.name_value.setText(self.adsorbate.name)
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

        self.table_model = AdsPropTableModel(self.adsorbate)
        self.table_view.setModel(self.table_model)

    def connect_signals(self):

        self.table_view.selectionModel().selectionChanged.connect(self.metadata_select)
        self.meta_edit_widget.save_button.clicked.connect(self.metadata_save)
        self.meta_edit_widget.delete_button.clicked.connect(self.metadata_delete)

    def metadata_select(self):
        index = self.table_view.currentIndex()
        if index:
            data = self.table_model.rowData(index)
            if data:
                self.meta_edit_widget.display(*data)
            else:
                self.meta_edit_widget.clear()

    def metadata_save(self):

        meta_name = self.meta_edit_widget.name_input.text()
        meta_value = self.meta_edit_widget.value_input.text()
        meta_type = self.meta_edit_widget.type_input.currentText()
        if not meta_name:
            return

        if meta_type == "number":
            try:
                meta_value = float(meta_value)
            except ValueError:
                error_dialog("Could not convert metadata value to number.")
                return

        self.table_model.setOrInsertRow(data=[meta_name, meta_value, meta_type])
        self.adsorbate_changed.emit(self.adsorbate.name)
        self.table_view.resizeColumns()

    def metadata_delete(self):

        index = self.table_view.currentIndex()
        self.table_model.removeRow(index.row())
        self.adsorbate_changed.emit(self.adsorbate.name)

    def translate_UI(self):
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
    adsorbate_changed = QC.Signal(str)

    def __init__(self, adsorbate, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setup_UI()
        self.translate_UI()
        self.connect_signals()
        self.view.adsorbate = adsorbate

    def setup_UI(self):

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
        self.view.adsorbate_changed.connect(self.adsorbate_changed)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("AdsorbateDialog", "Adsorbate details", None, -1))
        # yapf: enable


class AdsorbateListDialog(QW.QDialog):
    adsorbate_changed = QC.Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()
        self.setup_model()

    def setup_UI(self):

        _layout = QW.QVBoxLayout(self)
        layout_top = QW.QHBoxLayout()
        _layout.addLayout(layout_top)

        # list
        self.adsorbate_list = QW.QListWidget()
        layout_top.addWidget(self.adsorbate_list)

        # details
        self.adsorbate_details = AdsorbateView()
        layout_top.addWidget(self.adsorbate_details)

        # Button box
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Close)
        _layout.addWidget(self.button_box)

    def connect_signals(self):
        self.adsorbate_details.adsorbate_changed.connect(self.adsorbate_changed)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def setup_model(self):
        self.adsorbate_list.addItems([ads.name for ads in ADSORBATE_LIST])
        self.adsorbate_list.currentItemChanged.connect(self.selectAdsorbate)

    def selectAdsorbate(self, item):
        self.adsorbate_details.adsorbate = Adsorbate.find(item.text())

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("AdsorbateListDialog", "pyGAPS Adsorbate explorer", None, -1))
        # yapf: enable
