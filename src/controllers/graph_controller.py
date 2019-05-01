import pygaps


class GraphController():
    def __init__(self, view, model):

        self.view = view
        self.model = model

        self.create_subscriptions()

    def create_subscriptions(self):

        # Data subscriptions
        self.model.plot_changed.connect(self.plot_iso)

    def plot_iso(self):
        pygaps.plot_iso(
            self.model.isotherms,
            ax=self.view.ax
        )
        self.view.ax.figure.canvas.draw()

    def update_gui(self):
        pass
