from qtpy import QtWidgets as QW

from src.views.MaterialView import MaterialView

from pygaps import MATERIAL_LIST
from pygaps import Material


class MaterialsView(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()
        self.retranslateUi()
        self.setupModel()

    def setupUi(self):

        layout = QW.QHBoxLayout(self)

        # list
        self.materialList = QW.QListWidget(parent=self)
        layout.addWidget(self.materialList)

        # details
        self.materialDetails = MaterialView(parent=self)
        layout.addWidget(self.materialDetails)

    def setupModel(self):
        self.materialList.addItems([mat.name for mat in MATERIAL_LIST])
        self.materialList.currentItemChanged.connect(self.selectMaterial)

    def selectMaterial(self, item):
        self.materialDetails.setMaterial(Material.find(item.text()))

    def retranslateUi(self):
        self.setWindowTitle(QW.QApplication.translate("MaterialsView", "pyGAPS Material explorer", None, -1))
