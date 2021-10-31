from qtpy import QtWidgets as QW
from qtpy import QtGui as QG
from qtpy import QtCore as QC
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import _setDevicePixelRatio, _devicePixelRatioF
from .. import get_resource


class IsoGraphToolbar(NavigationToolbar):

    toolitems = [*NavigationToolbar.toolitems]
    toolitems.insert([name for name, *_ in toolitems].index("Subplots") + 2,
                     ("Log(x)", "Log the X axis", "pg_btn_logx", "log_x"))
    toolitems.insert([name for name, *_ in toolitems].index("Subplots") + 3,
                     ("Log(y)", "Log the Y axis", "pg_btn_logy", "log_y"))

    def _icon(self, name):
        """
        Construct a `.QIcon` from an image file *name*, including the extension
        and relative to Matplotlib's "images" data directory.
        """
        if name.startswith("pg"):
            pm = QG.QPixmap(str(get_resource(name[3:])))
            _setDevicePixelRatio(pm, _devicePixelRatioF(self))
            if self.palette().color(self.backgroundRole()).value() < 128:
                icon_color = self.palette().color(self.foregroundRole())
                mask = pm.createMaskFromColor(QG.QColor('black'), QC.Qt.MaskOutColor)
                pm.fill(icon_color)
                pm.setMask(mask)
            return QG.QIcon(pm)
        else:
            return super()._icon(name)

    def get_ax(self):
        axes = self.canvas.figure.get_axes()
        if not axes:
            QW.QMessageBox.warning(self.canvas.parent(), "Error", "There are no axes to edit.")
            return
        elif len(axes) == 1:
            ax, = axes
        else:
            titles = [
                ax.get_label() or ax.get_title()
                or " - ".join(filter(None, [ax.get_xlabel(), ax.get_ylabel()])) or f"<anonymous {type(ax).__name__}>"
                for ax in axes
            ]
            duplicate_titles = [title for title in titles if titles.count(title) > 1]
            for i, ax in enumerate(axes):
                if titles[i] in duplicate_titles:
                    titles[i] += f" (id: {id(ax):#x})"  # Deduplicate titles.
            item, ok = QW.QInputDialog.getItem(self.canvas.parent(), 'Customize', 'Select axes:', titles, 0, False)
            if not ok:
                return
            ax = axes[titles.index(item)]
        return ax

    def log_x(self):
        # Get axis
        axes = self.get_ax()

        xmin, xmax = map(float, axes.get_xlim())

        # Change to log
        if axes.get_xscale() != 'log':
            axes.set_xscale('log')
        elif axes.get_xscale() != 'linear':
            axes.set_xscale('linear')

        axes.set_xlim(xmin, xmax)

        # Redraw
        figure = axes.get_figure()
        figure.canvas.draw()

    def log_y(self):
        # Get axis
        axes = self.get_ax()

        ymin, ymax = map(float, axes.get_ylim())

        # Change to log
        if axes.get_yscale() != 'log':
            axes.set_yscale('log')
        elif axes.get_yscale() != 'linear':
            axes.set_yscale('linear')

        axes.set_ylim(ymin, ymax)

        # Redraw
        figure = axes.get_figure()
        figure.canvas.draw()
