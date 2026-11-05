import threading

from qtpy import QtCore as QC

from pygapsgui.utilities import color_theme


def test_system_theme(qapp):
    assert color_theme.system_theme() in ("dark", "light")


def test_auto_theme_follows_system_without_threads(qapp, monkeypatch):
    threads = threading.active_count()
    monkeypatch.setattr(color_theme, "system_theme", lambda: "light")
    color_theme.set_theme()

    assert color_theme.COLORS is color_theme.COLORS_LIGHT
    assert color_theme.THEME_LISTENING
    assert threading.active_count() == threads

    monkeypatch.setattr(color_theme, "system_theme", lambda: "dark")
    color_theme.theme_callback(QC.Qt.ColorScheme.Dark)

    assert color_theme.COLORS is color_theme.COLORS_DARK
    assert qapp.styleSheet()


def test_fixed_theme_ignores_system_changes(qapp, monkeypatch):
    QC.QSettings().setValue("theme", "light")
    color_theme.set_theme()
    monkeypatch.setattr(color_theme, "system_theme", lambda: "dark")
    color_theme.theme_callback(QC.Qt.ColorScheme.Dark)

    assert color_theme.COLORS is color_theme.COLORS_LIGHT


def test_menu_switches_theme(main_window):
    main_window.ui.action_theme_light.trigger()
    assert QC.QSettings().value("theme") == "light"
    assert color_theme.COLORS is color_theme.COLORS_LIGHT
    assert main_window.ui.action_theme_light.isChecked()
    assert not main_window.ui.action_theme_auto.isChecked()

    main_window.ui.action_theme_dark.trigger()
    assert QC.QSettings().value("theme") == "dark"
    assert color_theme.COLORS is color_theme.COLORS_DARK
    assert main_window.ui.action_theme_dark.isChecked()
    assert not main_window.ui.action_theme_light.isChecked()


def test_existing_graph_restyles_without_losing_state(main_window, qtbot):
    from matplotlib.colors import to_rgba

    from pygapsgui.views.GraphView import GraphView

    main_window.color_theme("light")
    graph = GraphView(x_range_select=True, parent=main_window)
    qtbot.addWidget(graph)
    graph.ax.set_xlabel("Pressure")
    graph.ax.set_ylabel("Loading")
    line, = graph.ax.plot([1, 2, 3], [3, 5, 6], color="black", label="data")
    fit, = graph.ax.plot([1, 2, 3], [3, 4, 5], color=color_theme.COLORS["primary"], gid="pygapsgui-fit")
    secondary = graph.ax.twinx()
    secondary.set_ylabel("Secondary")
    scatter = secondary.scatter([1, 2], [4, 5], color="black")
    legend = graph.ax.legend()
    graph.ax.set_xlim(1.2, 2.8)
    graph.ax.set_ylim(2, 7)
    graph.draw_xlimits(1.4, 2.5)
    limits = graph.ax.get_xlim(), graph.ax.get_ylim()
    lines = tuple(graph.ax.lines)

    for theme in ("dark", "light", "dark"):
        main_window.color_theme(theme)
        foreground = "white" if theme == "dark" else "black"
        assert graph.figure.get_facecolor() == to_rgba(color_theme.COLORS["dark"] if theme == "dark" else "white")
        assert to_rgba(graph.ax.xaxis.label.get_color()) == to_rgba(foreground)
        assert to_rgba(secondary.yaxis.label.get_color()) == to_rgba(foreground)
        assert to_rgba(legend.get_texts()[0].get_color()) == to_rgba(foreground)
        assert to_rgba(line.get_color()) == to_rgba(foreground)
        assert tuple(scatter.get_facecolors()[0]) == to_rgba("black")
        assert fit.get_color() == color_theme.COLORS["primary"]
        assert tuple(graph.ax.lines) == lines
        assert (graph.ax.get_xlim(), graph.ax.get_ylim()) == limits
        assert list(graph.x_lower.get_xdata()) == [1.4, 1.4]


def test_existing_and_new_model_items_follow_theme(main_window, data_dir):
    from pygaps import ModelIsotherm
    from pygaps.parsing import isotherm_from_json

    iso = isotherm_from_json(data_dir / "json" / "SiO2 N2 77.json")
    model_iso = ModelIsotherm.from_pointisotherm(iso, model="Henry", branch="ads")
    main_window.color_theme("light")
    main_window.iso_controller.add_isotherm("model", model_iso)
    item = main_window.iso_model.item(0)
    assert item.foreground().color().name() == color_theme.COLORS["primary"].lower()

    main_window.color_theme("dark")
    assert item.foreground().color().name() == color_theme.COLORS["primary"].lower()
    main_window.iso_controller.add_isotherm("new model", model_iso)
    assert main_window.iso_model.item(1).foreground() == item.foreground()


def test_theme_preserves_multi_isotherm_zoom(main_window, data_dir, qtbot):
    main_window.open_iso([
        data_dir / "json" / "SiO2 N2 77.json",
        data_dir / "json" / "Takeda 5A N2 77.json",
    ])
    main_window.iso_model.check_all()
    graph = main_window.ui.iso_graph
    graph.ax.set_xlim(0.05, 0.3)
    graph.ax.set_ylim(1, 3)
    limits = graph.ax.get_xlim(), graph.ax.get_ylim()
    lines = tuple(graph.ax.lines)
    with qtbot.assertNotEmitted(main_window.iso_model.checked_changed):
        for theme in ("light", "dark", "light"):
            main_window.color_theme(theme)
            assert (graph.ax.get_xlim(), graph.ax.get_ylim()) == limits
            assert tuple(graph.ax.lines) == lines
    with qtbot.waitSignal(main_window.iso_model.checked_changed):
        main_window.iso_model.item(0).setCheckState(QC.Qt.CheckState.Unchecked)


def test_theme_preserves_semantic_marker_colours(main_window):
    graph = main_window.ui.iso_graph
    line, = graph.ax.plot(
        [1, 2], [3, 4], color="blue", marker="o",
        markerfacecolor="white", markeredgecolor="blue", label="desorption",
    )
    scatter = graph.ax.scatter([1, 2], [4, 5], c=[0, 1], cmap="gray")
    graph.canvas.draw()
    colours = scatter.get_facecolors().copy()
    legend = graph.ax.legend()
    for theme in ("dark", "light", "dark"):
        main_window.color_theme(theme)
        graph.canvas.draw()
        assert line.get_markerfacecolor() == "white"
        assert line.get_markeredgecolor() == "blue"
        assert legend.get_lines()[0].get_markerfacecolor() == "white"
        assert (scatter.get_facecolors() == colours).all()
