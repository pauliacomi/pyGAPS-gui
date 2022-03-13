import sys

import numpy as np
from qtpy import QtWidgets as QW

import pygaps
from pygapsgui.views.IsoGraphView import IsoGraphView

if __name__ == "__main__":

    app = QW.QApplication(sys.argv)
    wnd = IsoGraphView(
        x_range_select=True,
        y_range_select=True,
    )

    p = np.linspace(1e-3, 10)
    n = p / (1 + p)

    iso = pygaps.PointIsotherm(
        pressure=p,
        loading=n,
        m="Test",
        a="N2",
        t=77,
    )
    wnd.set_isotherms([iso])
    wnd.draw_isotherms()

    wnd.show()
    sys.exit(app.exec_())
