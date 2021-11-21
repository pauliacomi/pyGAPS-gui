from src.views.IsoGraphView import IsoGraphView


class IsoListGraphView(IsoGraphView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setModel(self, model):
        self.model = model

    def update(self):
        self.setIsotherms(self.model.get_iso_checked())
        self.plot()
