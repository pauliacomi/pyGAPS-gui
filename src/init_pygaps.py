def init_pygaps():
    import pygaps.graphing.mpl_styles as pgs

    pgs.FIG_STYLE = {
        'figsize': (6, 6),
    }
    pgs.TITLE_STYLE = {
        'horizontalalignment': 'center',
        # 'fontsize': 20,
        'y': 1.01,
    }
    pgs.LABEL_STYLE = {
        'horizontalalignment': 'center',
        # 'fontsize': 15,
    }
    pgs.TICK_STYLE = {
        # 'labelsize': 13,
    }
    pgs.LEGEND_STYLE = {
        'handlelength': 2,
        # 'fontsize': 12,
        'frameon': False,
    }

    pgs.ISO_STYLES = {
        'fig_style': pgs.FIG_STYLE,
        'title_style': pgs.TITLE_STYLE,
        'label_style': pgs.LABEL_STYLE,
        'lgd_style': pgs.LEGEND_STYLE,
        'y1_line_style': {
            'linewidth': 1.5,
            # 'markersize': 6
        },
        'y2_line_style': {
            'linewidth': 0,
            # 'markersize': 6
        },
        'tick_style': pgs.TICK_STYLE,
        'save_style': {},
    }

    pgs.IAST_STYLES = {
        'fig_style': pgs.FIG_STYLE,
        'title_style': pgs.TITLE_STYLE,
        'label_style': pgs.LABEL_STYLE,
        'tick_style': pgs.TICK_STYLE,
        'lgd_style': pgs.LEGEND_STYLE,
    }
    pgs.POINTS_ALL_STYLE = {
        'color': 'grey',
        'marker': 'o',
        'mfc': 'none',
        # 'markersize': 6,
        'markeredgewidth': 1.5,
        'linewidth': 0,
    }
    pgs.POINTS_SEL_STYLE = {
        'marker': 'o',
        'linestyle': '',
        'color': 'r',
    }
