
from PySide2.QtCore import Signal


class ExplorerController():

    def __init__(self, view, model):

        self.view = view
        self.model = model

        self.create_subscriptions()

    def create_subscriptions(self):

        # Data subscriptions
        self.view.setModel(self.model)
