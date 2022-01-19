from qtpy import QtWidgets as QW

from functools import partial

from src.widgets.UtilityWidgets import open_files_dialog

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
        self.last_dir = None

        self.setup_UI()
        self.translate_UI()

    def setup_UI(self):
        self.setObjectName("ImportDialog")

        # Create/set layout
        _layout = QW.QVBoxLayout(self)

        # Create widgets
        self.label = QW.QLabel("Select source file type:")
        _layout.addWidget(self.label)

        self.choice_radio = []
        for ind, tp in enumerate(IMPORT_FILES):
            radio = QW.QRadioButton(f"{tp['name']} (.{', .'.join(tp['ext'])})")
            radio.toggled.connect(partial(self.set_ftype, tp=ind))
            _layout.addWidget(radio)
            self.choice_radio.append(radio)

        self.import_button = QW.QPushButton("Select file(s)")
        self.import_button.setVisible(False)
        self.import_button.clicked.connect(self.import_form)
        _layout.addWidget(self.import_button)

    def set_ftype(self, act: bool, tp: int):
        if act:
            self.ftype = tp
            self.import_button.setVisible(True)

    def import_form(self):
        sel = IMPORT_FILES[self.ftype]
        self.filepaths = open_files_dialog(
            parent=self,
            caption="Import an isotherm from a manufacturer file",
            directory=str(self.last_dir) if self.last_dir else '.',
            filter=f"{sel['name']} (*.{' *.'.join(sel['ext'])})"
        )
        if self.filepaths:
            self.close()

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("ImportDialog", "Import from manufacturer file", None, -1))
        # yapf: enable
