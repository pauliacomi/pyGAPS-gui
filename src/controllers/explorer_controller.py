
class ExplorerController():
    def __init__(self, view, model):

        self.view = view
        self.model = model

        self.create_subscriptions()

    def create_subscriptions(self):

        # Data subscriptions
        self.view.setModel(self.model)
        self.view.clicked.connect(self.info_iso)

        # self.model.iso_added.connect(self.info_iso)

        # treeView = QTreeView(self)
        # treeView.setModel(myStandardItemModel)
        # treeView.clicked[QModelIndex].connect(self.clicked)
    def info_iso(self, index):
        print(f'Clicked with {index} ')
