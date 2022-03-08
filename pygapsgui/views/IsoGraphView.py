import itertools

import pygaps.graphing as pgg
import pygaps.utilities.exceptions as pge
from pygapsgui.views.GraphView import GraphView
from pygapsgui.widgets.IsoGraphToolbar import IsoGraphToolbar
from pygapsgui.widgets.UtilityDialogs import error_dialog


class IsoGraphView(GraphView):
    """A canvas specifically designed to display isotherms.

    It extends GraphView and adds functionality consistent with pyGAPS isotherms.
    In particular:

    - store reference to isotherms to be displayed
    - can display selectable isotherm data on an x/y1/y2 axis
    - stores reference to branch to select
    - stores units/bases for plotting
    - has functionality to linearize/log one or more axes
    - integrates with ``IsoGraphToolbar`` to provide custom isotherm actions
    - integrates with ``SelectorToolbar`` to allow data range selection

    """

    isotherms = None
    _branch: str = "all"
    logx: bool = False
    logy: bool = False
    data_types: list = ["pressure", "loading"]
    x_data: str = "pressure"
    y1_data: str = "loading"
    y2_data: str = None

    x_range: list = None
    y1_range: list = None

    pressure_mode: str = None
    pressure_unit: str = None
    loading_basis: str = None
    loading_unit: str = None
    material_basis: str = None
    material_unit: str = None

    lgd_keys: list = None
    lgd_pos: str = "best"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # anything less and it looks too cramped
        self.setMinimumSize(400, 400)

    def setupNav(self):
        """Override parent nav to add custom toolbar."""
        self.navbar = IsoGraphToolbar(self.canvas, self)
        self.navbar.logx.connect(self.handle_logx)
        self.navbar.logy.connect(self.handle_logy)
        self.navbar.axis_data_sel.connect(self.handle_data_sel)

    def set_isotherms(self, isotherms):
        """Set one or more isotherms to be displayed by this graph."""
        self.isotherms = isotherms
        if not isotherms:
            return

        # data
        keys = list(iso.other_keys for iso in isotherms)
        self.data_types = ["pressure", "loading"]
        self.y2_data = None
        if any(keys):
            self.data_types = self.data_types + list(set(itertools.chain.from_iterable(keys)))
        if self.y1_data not in self.data_types:
            self.y1_data = "loading"
        if self.x_data not in self.data_types:
            self.x_data = "pressure"

        # range
        self.find_xrange()

    def draw_isotherms(self, clear=True):
        """Redraws the current isotherms."""
        if clear:
            self.clear()
        if self.isotherms:
            try:
                self._pg_plot_isotherms()
                self.ax.autoscale()
            except pge.GraphingError:
                error_dialog(
                    "X-axis and Y1-axis must display data that is shared by all isotherms (i.e. pressure or loading)."
                )
            except pge.CalculationError:
                error_dialog(
                    "Cannot plot multiple isotherms that are impossible to convert to the same units / modes."
                )
        self.canvas.draw_idle()

    def _pg_plot_isotherms(self):
        """Calls the pygaps plot function with all View state."""
        pgg.plot_iso(
            self.isotherms,
            ax=self.ax,
            branch=self._branch,
            logx=self.logx,
            logy1=self.logy,
            x_data=self.x_data,
            y1_data=self.y1_data,
            y2_data=self.y2_data,
            pressure_mode=self.pressure_mode,
            pressure_unit=self.pressure_unit,
            loading_basis=self.loading_basis,
            loading_unit=self.loading_unit,
            lgd_keys=self.lgd_keys,
        )

    @property
    def branch(self):
        return self._branch

    @branch.setter
    def branch(self, branch):
        self._branch = branch
        # have to reset selector range
        self.find_xrange()

    def find_xrange(self):
        """Find minimum and maximum of the x axis range for isotherms. Used in selectors."""
        # TODO this considers that "pressure" is always on the x axis
        if not self.isotherms:
            return
        self.x_range = (
            min([min(self.state_pressure(i)) for i in self.isotherms]),
            max([max(self.state_pressure(i)) for i in self.isotherms]),
        )
        if self.x_range_select:
            self.x_range_select.setRange(self.x_range)
            self.x_range_select.setValues(self.x_range, emit=False)
            self.xlow.set_xdata([self.x_range[0], self.x_range[0]])
            self.xhigh.set_xdata([self.x_range[1], self.x_range[1]])

    def state_pressure(self, iso):
        """Shortcut function to get isotherm pressure."""
        return iso.pressure(
            branch=self._branch,
            pressure_mode=self.pressure_mode,
            pressure_unit=self.pressure_unit,
        )

    def state_loading(self, iso):
        """Shortcut function to get isotherm loading."""
        return iso.loading(
            branch=self._branch,
            loading_basis=self.loading_basis,
            loading_unit=self.loading_unit,
            material_basis=self.material_basis,
            material_unit=self.material_unit,
        )

    def handle_logx(self, is_set: bool):
        """Makes sure log state is propagated to other components."""
        self.logx = is_set
        # TODO autoscaling on log resets the limits
        # this is good in that it nicely frames the whole isotherm
        # on the other hand, we lose nice features like keeping the same range while zoomed
        # could we set a flag to determing when the user "moved" the isotherm?
        self.ax.autoscale(axis="x")
        if self.x_range_select:
            self.x_range_select.setLogScale(is_set)

    def handle_logy(self, is_set: bool):
        """Makes sure log state is propagated to other components."""
        self.logy = is_set
        self.ax.autoscale(axis="y")
        if self.y_range_select:
            self.y_range_select.setLogScale(is_set)

    def handle_data_sel(self):
        """Dialog to ask user which data to display on each axis."""
        from pygapsgui.widgets.IsoGraphDataSel import IsoGraphDataSel
        dialog = IsoGraphDataSel(
            self.data_types,
            self.x_data,
            self.y1_data,
            self.y2_data,
            parent=self,
        )
        if dialog.exec():
            if dialog.changed:
                self.x_data = dialog.x_data
                self.y1_data = dialog.y1_data
                self.y2_data = dialog.y2_data
                self.draw_isotherms()


class IsoListGraphView(IsoGraphView):
    """IsoGraphView sublass which adds the ability to connect to a IsoListModel"""

    model = None

    def setModel(self, model):
        """Connects the IsoListModel to the View."""
        self.model = model
        self.model.checked_changed.connect(self.update)

    def update(self):
        """Updates the isotherms to those selected by the model."""
        self.set_isotherms(self.model.get_checked())
        self.draw_isotherms()


class IsoModelGraphView(IsoGraphView):
    """Subclass that plots an extra model isotherm."""

    model_isotherm = None
    _branch: str = "ads"
    lgd_pos: str = None

    def draw_isotherms(self, clear=True):
        """Overwrite the main draw function to plot the extra model isotherm."""

        if clear:
            self.clear()
        if self.isotherms:
            self._pg_plot_isotherms()
            if self.model_isotherm:
                points_dict = {}
                if self.model_isotherm.model.calculates == "loading":
                    points_dict['x_points'] = self.isotherms[0].pressure(
                        branch=self._branch,
                        limits=self.model_isotherm.model.pressure_range,
                    )
                else:
                    points_dict['y1_points'] = self.isotherms[0].loading(
                        branch=self._branch,
                        limits=self.model_isotherm.model.loading_range,
                    )
                pgg.plot_iso(
                    self.model_isotherm,
                    ax=self.ax,
                    branch=self._branch,
                    logx=self.logx,
                    logy1=self.logy,
                    lgd_pos=None,
                    color="r",
                    **points_dict,
                )
            self.ax.autoscale()
        self.canvas.draw_idle()
