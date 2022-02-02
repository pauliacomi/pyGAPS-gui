from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from pygaps import MATERIAL_LIST
from pygaps import Material
from pygapsgui.models.MatPropTableModel import MatPropTableModel
from pygapsgui.widgets.MetadataEditWidget import MetadataEditWidget
from pygapsgui.widgets.MetadataTableView import MetadataTableWidget
from pygapsgui.widgets.UtilityWidgets import error_dialog


class MaterialView(QW.QWidget):

    _material = None
    material_changed = QC.Signal(str)

    def __init__(self, material=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.material = material

    def setup_UI(self):
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

        # Table view
        self.table_view = MetadataTableWidget()
        self.metadata_layout.addWidget(self.table_view)

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, material):
        if not material:
            return

        self._material = material
        self.setup_model()
        self.connect_signals()

    def setup_model(self):
        self.name_value.setText(self.material.name)
        density = self.material.density
        density = str(density) if density else density
        self.density_value.setText(density)
        mmass = self.material.molar_mass
        mmass = str(mmass) if mmass else mmass
        self.mm_value.setText(mmass)

        self.table_model = MatPropTableModel(self.material)
        self.table_view.setModel(self.table_model)

    def connect_signals(self):
        self.table_view.selectionModel().selectionChanged.connect(self.metadata_select)
        self.meta_edit_widget.save_button.clicked.connect(self.metadata_save)
        self.meta_edit_widget.delete_button.clicked.connect(self.metadata_delete)

    def accept(self) -> None:
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
        self.material_changed.emit(str(self.material))
        self.table_view.resizeColumns()

    def metadata_delete(self):
        index = self.table_view.currentIndex()
        self.table_model.removeRow(index.row())
        self.material_changed.emit(str(self.material))

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.properties_box.setTitle(QW.QApplication.translate("AdsorbateView", "Main properties", None, -1))
        self.name_label.setText(QW.QApplication.translate("MaterialView", "Name", None, -1))
        self.density_label.setText(QW.QApplication.translate("MaterialView", "Density", None, -1))
        self.mm_label.setText(QW.QApplication.translate("MaterialView", "Molar Mass", None, -1))
        self.metadata_box.setTitle(QW.QApplication.translate("MaterialView", "Other Metadata", None, -1))
        # yapf: enable


class MaterialDialog(QW.QDialog):
    material_changed = QC.Signal(str)

    def __init__(self, material, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setup_UI()
        self.translate_UI()
        self.connect_signals()
        self.view.material = material

    def setup_UI(self):

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
        self.view.material_changed.connect(self.material_changed)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def accept(self) -> None:
        self.view.accept()
        return super().accept()

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("MaterialDialog", "Material details", None, -1))
        # yapf: enable


class MaterialListDialog(QW.QDialog):
    material_changed = QC.Signal(str)

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
        self.materialList = QW.QListWidget()
        layout_top.addWidget(self.materialList)

        # details
        self.material_details = MaterialView()
        layout_top.addWidget(self.material_details)

        # Button box
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Ok)
        _layout.addWidget(self.button_box)

    def connect_signals(self):
        self.material_details.material_changed.connect(self.material_changed)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def setup_model(self):
        self.materialList.addItems([mat.name for mat in MATERIAL_LIST])
        self.materialList.currentItemChanged.connect(self.selectMaterial)

    def selectMaterial(self, item):
        self.material_details.material = Material.find(item.text())

    def accept(self) -> None:
        self.material_details.accept()
        return super().accept()

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("MaterialListDialog", "pyGAPS Material explorer", None, -1))
        # yapf: enable
