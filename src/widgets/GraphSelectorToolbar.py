from qtpy import QtWidgets as QW

from src.widgets.RangeSlider import QHSpinBoxRangeSlider


class HSelectorToolbar(QW.QToolBar):
    def __init__(
        self,
        title: str,
        ax,
        slider_range: "list[float, float]" = None,
        parent=None,
    ) -> None:
        super().__init__(title, parent=parent)
        self.ax = ax
        if not slider_range:
            slider_range = [0, 1, None]
        self.setup_UI(slider_range)

    def setup_UI(self, slider_range):
        self.slider = QHSpinBoxRangeSlider(
            slider_range=slider_range,
            values=slider_range[:-1],
            dec_pnts=2,
        )
        self.slider.setFixedHeight(35)
        self.slider.setEmitWhileMoving(False)
        self.addWidget(self.slider)

    def setRange(self, slider_range):
        self.slider.setRange([slider_range[0], slider_range[1], None])

    def setValues(self, slider_values, emit=True):
        self.slider.setValues(slider_values, emit=emit)

    def getValues(self):
        return self.slider.getValues()

    def setLogScale(self, is_set: bool):
        self.slider.setLogScale(is_set)
