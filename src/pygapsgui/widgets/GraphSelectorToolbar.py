from qtpy import QtWidgets as QW

from pygapsgui.widgets.RangeSlider import QHSpinBoxRangeSlider
from pygapsgui.widgets.RangeSlider import QVSpinBoxRangeSlider


class SelectorToolbar(QW.QToolBar):
    """A base class that allows selection of ranges on a graph."""
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

    def setRange(self, slider_range):
        """Set the underlying range for the slider."""
        self.slider.setRange([slider_range[0], slider_range[1], None])

    def setValues(self, slider_values, emit=True):
        """Set the underlying range for the slider."""
        self.slider.setValues(slider_values, emit=emit)

    def getValues(self):
        """Pass-through to slider function."""
        return self.slider.getValues()

    def setLogScale(self, is_set: bool):
        """Pass-through to slider function."""
        self.slider.setLogScale(is_set)


class HSelectorToolbar(SelectorToolbar):
    """Horizontal implementation of graph data selector."""
    def setup_UI(self, slider_range):
        """Setup the UI horizontally."""
        self.slider = QHSpinBoxRangeSlider(
            slider_range=slider_range,
            values=slider_range[:-1],
            dec_pnts=2,
        )
        self.slider.setFixedHeight(35)
        self.slider.setEmitWhileMoving(False)
        self.addWidget(self.slider)


class VSelectorToolbar(SelectorToolbar):
    """Vertical implementation of graph data selector."""
    def setup_UI(self, slider_range):
        """Setup the UI vertically."""
        self.slider = QVSpinBoxRangeSlider(
            slider_range=slider_range,
            values=slider_range[:-1],
            dec_pnts=2,
        )
        self.slider.range_slider.setFixedWidth(20)
        self.slider.setEmitWhileMoving(False)
        self.addWidget(self.slider)

        size_policy = QW.QSizePolicy(
            QW.QSizePolicy.MinimumExpanding,
            QW.QSizePolicy.MinimumExpanding,
        )
        self.setSizePolicy(size_policy)
