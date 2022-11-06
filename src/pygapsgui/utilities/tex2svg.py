from io import BytesIO

import matplotlib.pyplot as plt


def tex2svg(formula, fontsize=12, dpi=300):
    """
    Render TeX formula to SVG.

    Thanks to gist:
        https://gist.github.com/gmarull/dcc8218385014559c1ca46047457c364

    Args:
        formula (str): TeX formula.
        fontsize (int, optional): Font size.
        dpi (int, optional): DPI.
    Returns:
        str: SVG render.
    """

    # matplotlib: force computer modern font set
    with plt.rc_context(rc={'mathtext.fontset': 'cm'}):

        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, r'${}$'.format(formula), fontsize=fontsize)

        output = BytesIO()
        fig.savefig(
            output,
            dpi=dpi,
            transparent=True,
            format='svg',
            bbox_inches='tight',
            pad_inches=0.0,
        )
        plt.close(fig)

    output.seek(0)
    return output.read()
