def init_matplotlib():
    # Tweak pyGAPS graph settings for a GUI
    from pygaps.graphing.mpl_styles import BASE_STYLE
    from pygaps.graphing.mpl_styles import ISO_STYLE
    ISO_STYLE.update({
        'lines.markersize': 6,
        'legend.fontsize': 9,
    })
    BASE_STYLE.update({
        'lines.markersize': 6,
        'legend.fontsize': 7,
    })


def init_pygaps():
    import pygaps
    init_matplotlib()
