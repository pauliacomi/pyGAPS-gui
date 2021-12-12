from qtpy import QtWidgets as QW

from src.widgets.RangeSlider import QHSpinBoxRangeSlider


class HSelectorToolbar(QW.QToolBar):
    def __init__(
        self, title: str, ax, slider_range: "list[float, float]" = None, parent=None
    ) -> None:
        super().__init__(title, parent=parent)
        self.ax = ax
        if not slider_range:
            slider_range = [0, 1, None]
        self.setupUi(slider_range)

    def setupUi(self, slider_range):
        self.slider = QHSpinBoxRangeSlider(
            parent=self, dec_pnts=2, slider_range=slider_range, values=slider_range[:-1]
        )
        self.slider.setFixedHeight(35)
        self.slider.setEmitWhileMoving(False)
        self.addWidget(self.slider)

    def setRange(self, slider_range):
        self.slider.setRange([slider_range[0], slider_range[1], None])

    def setLogScale(self, is_set: bool):
        self.slider.setLogScale(is_set)
