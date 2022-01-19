from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.models.MatPropTableModel import MatPropTableModel
from src.widgets.MetadataEditWidget import MetadataEditWidget
from src.widgets.MetadataTableWidget import MetadataTableWidget
from src.widgets.UtilityWidgets import error_dialog

from pygaps import MATERIAL_LIST
from pygaps import Material


class MaterialView(QW.QWidget):

    _material = None

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

        self.tableModel = MatPropTableModel(self.material)
        self.table_view.setModel(self.tableModel)

    def connect_signals(self):
        self.table_view.selectionModel().selectionChanged.connect(self.extra_prop_select)
        self.meta_edit_widget.save_button.clicked.connect(self.extra_prop_save)
        self.meta_edit_widget.delete_button.clicked.connect(self.extra_prop_delete)

    def accept(self) -> None:

        if self.name_value.text() != self.material.name:
            self.material.name = self.name_value.text()

        if self.density_value.text() != self.material.density:
            self.material.density = self.density_value.text()

        if self.mm_value.text() != self.material.molar_mass:
            self.material.molar_mass = self.mm_value.text()

    def extra_prop_select(self):
        index = self.table_view.selectionModel().currentIndex()
        if index:
            data = self.tableModel.rowData(index)
            if data:
                self.meta_edit_widget.display(*data)
            else:
                self.meta_edit_widget.clear()

    def extra_prop_save(self):

        propName = self.meta_edit_widget.name_input.text()
        propValue = self.meta_edit_widget.value_input.text()
        propType = self.meta_edit_widget.type_input.currentText()
        if not propName:
            return

        if propType == "number":
            try:
                propValue = float(propValue)
            except ValueError:
                error_dialog("Could not convert metadata value to number.")
                return

        self.tableModel.setOrInsertRow(data=[propName, propValue, propType])
        self.table_view.resizeColumns()

    def extra_prop_delete(self):
        index = self.table_view.selectionModel().currentIndex()
        self.tableModel.removeRow(index.row())

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
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
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Close)
        _layout.addWidget(self.button_box)

    def connect_signals(self):
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def setup_model(self):
        self.materialList.addItems([mat.name for mat in MATERIAL_LIST])
        self.materialList.currentItemChanged.connect(self.selectMaterial)

    def selectMaterial(self, item):
        self.material_details.material = Material.find(item.text())

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("MaterialListDialog", "pyGAPS Material explorer", None, -1))
        # yapf: enable
