from qtpy import QtWidgets as QW

from functools import partial

from src.widgets.UtilityWidgets import ErrorMessageBox, open_files_dialog

IMPORT_FILES = [
    {
        "ind": "bel_dat",
        "name": "BELSORP MAX raw",
        "ext": ("DAT", )
    },
    {
        "ind": "bel_xl",
        "name": "BELSORP MAX report",
        "ext": ("xls", "xlxs")
    },
    {
        "ind": "mic_rep",
        "name": "Micromeritics report",
        "ext": ("xls", "xlxs")
    },
    {
        "ind": "qnt_rep",
        "name": "Quantachrome report",
        "ext": ("txt", )
    },
]


class ImportDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filepaths = None
        self.ftype = None
        self.fext = None

        self.setupUi()
        self.retranslateUi()

    def setupUi(self):
        self.setObjectName("ImportDialog")

        # Create/set layout
        layout = QW.QVBoxLayout(self)

        # Create widgets
        self.label = QW.QLabel("Select source file type")
        layout.addWidget(self.label)
        self.btns = []

        for ind, tp in enumerate(IMPORT_FILES):
            btn = QW.QRadioButton(f"{tp['name']} (.{', .'.join(tp['ext'])})")
            btn.toggled.connect(partial(self.setftype, tp=ind))
            layout.addWidget(btn)
            self.btns.append(btn)

        self.buttonImport = QW.QPushButton("Select file(s)")
        self.buttonImport.setVisible(False)
        self.buttonImport.clicked.connect(self.importForm)
        layout.addWidget(self.buttonImport)

    def setftype(self, act: bool, tp: int):
        if act:
            self.ftype = tp
            self.buttonImport.setVisible(True)

    def importForm(self):
        sel = IMPORT_FILES[self.ftype]
        self.filepaths = open_files_dialog(
            parent_widget=self,
            caption="Import an isotherm from a manufacturer file",
            directory='.',
            filter=f"{sel['name']} (*.{', *.'.join(sel['ext'])})"
        )
        if self.filepaths:
            self.close()

    def retranslateUi(self):
        self.setWindowTitle(
            QW.QApplication.translate("BEImportDialogTDialog", "Import from manufacturer file", None, -1)
        )
