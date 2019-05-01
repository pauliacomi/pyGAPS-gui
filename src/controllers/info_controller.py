
class TextInfoController():
    def __init__(self, view, model):

        self.view = view
        self.model = model

        self.create_subscriptions()

    def create_subscriptions(self):
        pass
        # Data subscriptions
        # self.model.iso_added.connect(self.info_iso)

    def info_iso(self):
        pass
