from functools import partial

from qtpy import QtWidgets as QW

from pygapsgui.widgets.UtilityDialogs import open_files_dialog

IMPORT_FILES = [
    {
        "ind": {
            "manufacturer": 'smsdvs',
            "fmt": 'xlsx'
        },
        "name": "SMS DVS Excel workbook",
        "ext": ("xlsx", )
    },
    {
        "ind": {
            "manufacturer": "bel",
            "fmt": "dat"
        },
        "name": "BEL japan",
        "ext": ("DAT", )
    },
    {
        "ind": {
            "manufacturer": "bel",
            "fmt": "xl"
        },
        "name": "BEL japan report",
        "ext": ("xls", )
    },
    {
        "ind": {
            "manufacturer": "bel",
            "fmt": "csv"
        },
        "name": "BEL japan CSV",
        "ext": ("csv", )
    },
    {
        "ind": {
            "manufacturer": "bel",
            "fmt": "csv",
            "lang": "JPN"
        },
        "name": "BEL japan JIS CSV",
        "ext": ("csv", )
    },
    {
        "ind": {
            "manufacturer": "mic",
            "fmt": "xl"
        },
        "name": "Micromeritics report",
        "ext": ("xls", )
    },
    {
        "ind": {
            "manufacturer": "3p",
            "fmt": "xl"
        },
        "name": "3P report",
        "ext": ("xlsx", )
    },
    {
        "ind": {
            "manufacturer": 'qnt',
            "fmt": 'txt-raw'
        },
        "name": "Quantachrome (Raw Analysis Data)",
        "ext": ("txt", )
    },
]


class ImportDialog(QW.QDialog):
    """Pop-up dialog prompting allowing for selection of manufacturer import type."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filepaths = None
        self.ftype = None
        self.fext = None
        self.last_dir = None

        self.setup_UI()
        self.translate_UI()

    def setup_UI(self):
        """Creates and sets-up static UI elements"""
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
        """Handle file type setting."""
        if act:
            self.ftype = IMPORT_FILES[tp]['ind']
            self.import_button.setVisible(True)

    def import_form(self):
        """Pop-up to select files."""
        sel = next(v for v in IMPORT_FILES if v['ind'] == self.ftype)
        self.filepaths = open_files_dialog(
            parent=self,
            caption="Import an isotherm from a manufacturer file",
            directory=str(self.last_dir) if self.last_dir else '.',
            filter=f"{sel['name']} (*.{' *.'.join(sel['ext'])})"
        )
        if self.filepaths:
            self.close()

    def translate_UI(self):
        """Set static UI text through QT translation."""
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("ImportDialog", "Import from manufacturer file", None, -1))
        # yapf: enable
