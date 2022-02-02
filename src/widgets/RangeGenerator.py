import numpy as np
import pandas as pd
from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.models.dfTableModel import dfTableModel
from src.widgets.SciDoubleSpinbox import SciFloatDelegate
from src.widgets.UtilityWidgets import HeightHeaderView


class RangeGenWidget(QW.QWidget):
    data = None

    def __init__(self, props=None, data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        props = props if props else ["Property"]
        data = data if data is not None else []
        self.data = pd.DataFrame(columns=props, data=data)
        self.setup_UI()
        self.translate_UI()
        self.handle_propchange()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("RangeGenWidget")

        # Create/set layout
        _layout = QW.QVBoxLayout(self)

        # Create widgets
        #
        # Options
        self.options_widget = QW.QWidget()
        _layout.addWidget(self.options_widget)
        self.options_layout = QW.QFormLayout(self.options_widget)
        self.options_layout.setObjectName("options_layout")

        self.prop_label = QW.QLabel()
        self.prop_value = QW.QComboBox()
        self.prop_value.addItems(self.data.columns)
        self.start_label = QW.QLabel()
        self.start_value = QW.QDoubleSpinBox()
        self.start_value.setSingleStep(0.1)
        self.start_value.setMinimum(0)
        self.start_value.setMaximum(1000)
        self.end_label = QW.QLabel()
        self.end_value = QW.QDoubleSpinBox()
        self.end_value.setSingleStep(0.1)
        self.end_value.setMinimum(0)
        self.end_value.setMaximum(1000)
        self.points_label = QW.QLabel()
        self.points_value = QW.QSpinBox()
        self.points_value.setMinimum(1)
        self.points_value.setMaximum(500)
        self.dist_label = QW.QLabel()
        self.dist_value = QW.QComboBox()
        self.dist_value.addItems(["Linear", "Logarithmic"])
        self.options_layout.addRow(self.prop_label, self.prop_value)
        self.options_layout.addRow(self.points_label, self.points_value)
        self.options_layout.addRow(self.start_label, self.start_value)
        self.options_layout.addRow(self.end_label, self.end_value)
        self.options_layout.addRow(self.dist_label, self.dist_value)

        self.generate_btn = QW.QPushButton()
        self.erase_btn = QW.QPushButton()
        self.options_layout.addRow(self.generate_btn, self.erase_btn)

        # Range Table
        self.range_label = QW.QLabel()
        self.range_table = QW.QTableView(self)
        self.range_model = dfTableModel(self.data)
        self.range_table.setModel(self.range_model)
        delegate = SciFloatDelegate()
        self.range_table.setItemDelegate(delegate)
        h_header = HeightHeaderView()
        self.range_table.setHorizontalHeader(h_header)
        vertical_header = self.range_table.verticalHeader()
        vertical_header.setSectionResizeMode(QW.QHeaderView.ResizeToContents)
        _layout.addWidget(self.range_label)
        _layout.addWidget(self.range_table)

    def connect_signals(self):
        self.prop_value.currentIndexChanged.connect(self.handle_propchange)
        self.generate_btn.clicked.connect(self.generate)
        self.erase_btn.clicked.connect(self.erase)
        self.range_model.dataChanged.connect(self.save)

    def set_data(self, props=None, data=None):
        props = props if props else ["Property"]
        data = data if data is not None else []
        self.data = pd.DataFrame(columns=props, data=data)
        self.prop_value.clear()
        self.prop_value.addItems(self.data.columns)
        self.range_model = dfTableModel(self.data)
        self.range_table.setModel(self.range_model)
        self.range_model.dataChanged.connect(self.save)

    def handle_propchange(self):
        prop = self.prop_value.currentIndex()
        start = 0.1
        end = 1.0
        points = 5
        if self.data is not None and self.data.shape[0] > 0:
            start = self.data.iloc[0, prop]
            end = self.data.iloc[-1, prop]
            points = self.data.shape[0]
        # TODO handle empty columns
        self.start_value.setValue(start)
        self.end_value.setValue(end)
        self.points_value.setValue(points)

    def erase(self):
        self.range_model.setRowCount(0)

    def generate(self):
        # generate range
        prop = self.prop_value.currentIndex()
        start = self.start_value.value()
        end = self.end_value.value()
        npoints = self.points_value.value()

        dist = self.dist_value.currentText().lower()
        if dist == "linear":
            distfn = np.linspace
        elif dist == "logarithmic":
            distfn = np.logspace
            start = np.log10(start)
            end = np.log10(end)

        rng = distfn(start, end, npoints)

        # populate table
        self.range_model.setRowCount(npoints)
        index = self.range_model.index(0, prop)
        self.range_model.setColumnData(index.column(), rng, role=QC.Qt.EditRole)

    def save(self):
        self.data = self.range_model._data

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.prop_label.setText(QW.QApplication.translate("RangeGenWidget", "Column", None, -1))
        self.start_label.setText(QW.QApplication.translate("RangeGenWidget", "Start", None, -1))
        self.end_label.setText(QW.QApplication.translate("RangeGenWidget", "End", None, -1))
        self.points_label.setText(QW.QApplication.translate("RangeGenWidget", "Total points", None, -1))
        self.dist_label.setText(QW.QApplication.translate("RangeGenWidget", "Distribution", None, -1))
        self.generate_btn.setText(QW.QApplication.translate("RangeGenWidget", "Generate", None, -1))
        self.erase_btn.setText(QW.QApplication.translate("RangeGenWidget", "Clear", None, -1))
        self.range_label.setText(QW.QApplication.translate("RangeGenWidget", "Range", None, -1))
        # yapf: enable


class RangeGenDialog(QW.QDialog):
    def __init__(self, props=None, data=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setup_UI(props=props, data=data)
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self, props, data):

        _layout = QW.QVBoxLayout(self)

        # View
        self.widget = RangeGenWidget(props=props, data=data)
        _layout.addWidget(self.widget)

        # Button box
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Cancel | QW.QDialogButtonBox.Ok)
        _layout.addWidget(self.button_box)

    def connect_signals(self):
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("RangeGenDialog", "Range generator", None, -1))
        # yapf: enable
