from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import _devicePixelRatioF
from matplotlib.backends.qt_compat import _setDevicePixelRatio
from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from pygapsgui import get_res_path


class IsoGraphToolbar(NavigationToolbar):
    """Subclass a MPL navigation toolbar to add extra buttons."""

    logx = QC.Signal(bool)
    logy = QC.Signal(bool)
    axis_data_sel = QC.Signal()

    toolitems = [*NavigationToolbar.toolitems]

    pos = [name for name, *_ in toolitems].index("Subplots") + 2

    toolitems.insert(pos, ("Data X", "Data to plot on X/Y1/Y2 axis", "pg_btn_data", "axis_data"))
    toolitems.insert(pos + 1, ("Log(x)", "Log the X axis", "pg_btn_logx", "log_x"))
    toolitems.insert(pos + 2, ("Log(y)", "Log the Y axis", "pg_btn_logy", "log_y"))

    def __init__(self, canvas, parent, coordinates=True):
        super().__init__(canvas, parent, coordinates=coordinates)
        self._actions['log_x'].setCheckable(True)
        self._actions['log_y'].setCheckable(True)

    def _icon(self, name):
        """
        We override a matplotlib NavigationToolbar2QT function.
        If the name of an icon starts with pg, we go find it locally,
        Otherwas pass it to the main function.
        """
        if name.startswith("pg"):
            pm = QG.QPixmap(get_res_path(name[3:], "icons"))
            _setDevicePixelRatio(pm, _devicePixelRatioF(self))
            if self.palette().color(self.backgroundRole()).value() < 128:
                icon_color = self.palette().color(self.foregroundRole())
                mask = pm.createMaskFromColor(QG.QColor('black'), QC.Qt.MaskOutColor)
                pm.fill(icon_color)
                pm.setMask(mask)
            return QG.QIcon(pm)
        else:
            return super()._icon(name)

    def get_main_ax(self):
        """Get the first ax in figure axes."""
        axes = self.canvas.figure.get_axes()
        if not axes:
            QW.QMessageBox.warning(self.canvas.parent(), "Error", "There are no axes to edit.")
            return
        else:
            ax = axes[0]
        return ax

    def get_ax(self):
        """Interactive popup for the user to select one ax."""
        axes = self.canvas.figure.get_axes()
        if not axes:
            QW.QMessageBox.warning(self.canvas.parent(), "Error", "There are no axes to edit.")
            return
        elif len(axes) == 1:
            ax, = axes
        else:
            titles = [
                ax.get_label() or ax.get_title()
                or " - ".join(filter(None, [ax.get_xlabel(), ax.get_ylabel()]))
                or f"<anonymous {type(ax).__name__}>" for ax in axes
            ]
            duplicate_titles = [title for title in titles if titles.count(title) > 1]
            for i, ax in enumerate(axes):
                if titles[i] in duplicate_titles:
                    titles[i] += f" (id: {id(ax):#x})"  # Deduplicate titles.
            item, ok = QW.QInputDialog.getItem(
                self.canvas.parent(), 'Customize', 'Select axes:', titles, 0, False
            )
            if not ok:
                return None, None
            ax = axes[titles.index(item)]
        return ax, len(axes)

    def axis_data(self):
        """Functionality to select which data is plotted on an axes."""
        self.axis_data_sel.emit()

    def log_x(self):
        """Functionality to log the x-axis."""
        # Get axis
        axes = self.get_main_ax()

        xmin, xmax = map(float, axes.get_xlim())

        # Change to log
        if axes.get_xscale() != 'log':
            logx = True
            axes.set_xscale('log')
        elif axes.get_xscale() != 'linear':
            axes.set_xscale('linear')
            logx = False

        axes.set_xlim(xmin, xmax)

        # set checkable
        self._actions['log_x'].setChecked(logx)

        # draw
        self.canvas.draw_idle()

        # Emit change
        self.logx.emit(logx)

    def log_y(self):
        """Functionality to log one of the y-axes."""
        # Get axis
        axes, naxes = self.get_ax()
        if not axes:
            return

        ymin, ymax = map(float, axes.get_ylim())

        # Change to log
        if axes.get_yscale() != 'log':
            axes.set_yscale('log')
            logy = True
        elif axes.get_yscale() != 'linear':
            axes.set_yscale('linear')
            logy = False

        axes.set_ylim(ymin, ymax)

        if naxes == 1:
            self._actions['log_y'].setChecked(logy)
        else:
            self._actions['log_y'].setChecked(False)

        # draw
        self.canvas.draw_idle()

        # Emit change
        self.logy.emit(logy)
