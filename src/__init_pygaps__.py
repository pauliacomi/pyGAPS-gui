def init_pygaps():
    import pygaps

    # Tweak pyGAPS graph settings for a GUI
    from pygaps.graphing.mpl_styles import ISO_STYLE
    from pygaps.graphing.mpl_styles import BASE_STYLE
    ISO_STYLE.update({
        'lines.markersize': 6,
        'legend.fontsize': 10,
    })
    BASE_STYLE.update({
        'lines.markersize': 6,
        'legend.fontsize': 8,
    })
