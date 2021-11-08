from qtpy import QtWidgets as QW

from src.views.AdsorbateView import AdsorbateView

from pygaps import ADSORBATE_LIST
from pygaps import Adsorbate


class AdsorbatesView(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()
        self.retranslateUi()
        self.setupModel()

    def setupUi(self):

        layout = QW.QHBoxLayout(self)

        # list
        self.adsorbateList = QW.QListWidget(parent=self)
        layout.addWidget(self.adsorbateList)

        # details
        self.adsorbateDetails = AdsorbateView(parent=self)
        layout.addWidget(self.adsorbateDetails)

    def setupModel(self):
        self.adsorbateList.addItems([ads.name for ads in ADSORBATE_LIST])
        self.adsorbateList.currentItemChanged.connect(self.selectAdsorbate)

    def selectAdsorbate(self, item):
        self.adsorbateDetails.setAdsorbate(Adsorbate.find(item.text()))

    def retranslateUi(self):
        self.setWindowTitle(QW.QApplication.translate("AdsorbatesView", "pyGAPS Adsorbate explorer", None, -1))
