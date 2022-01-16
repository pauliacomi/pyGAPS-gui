from qtpy import QtWidgets as QW

from functools import partial

from src.widgets.UtilityWidgets import error_dialog, open_files_dialog

IMPORT_FILES = [
    {
        "ind": "bel_dat",
        "name": "BELSORP MAX raw",
        "ext": ("DAT", )
    },
    {
        "ind": "bel_xl",
        "name": "BELSORP MAX report",
        "ext": ("xls", "xlsx")
    },
    {
        "ind": "mic_rep",
        "name": "Micromeritics report",
        "ext": ("xls", "xlsx")
    },
    {
        "ind": "qnt_rep",
        "name": "Quantachrome report",
        "ext": ("txt", )
    },
    {
        "ind": "3p_rep",
        "name": "3P report",
        "ext": ("xls", "xlsx")
    },
]


class ImportDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filepaths = None
        self.ftype = None
        self.fext = None

        self.setup_UI()
        self.translate_UI()

    def setup_UI(self):
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
            filter=f"{sel['name']} (*.{' *.'.join(sel['ext'])})"
        )
        if self.filepaths:
            self.close()

    def translate_UI(self):
        self.setWindowTitle(
            QW.QApplication.translate("ImportDialog", "Import from manufacturer file", None, -1)
        )
