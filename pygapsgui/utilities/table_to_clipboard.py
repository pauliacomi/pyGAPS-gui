import csv
import io

from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW


def clipboard_to_table(table):
    """Put a clipboard table into the selected range."""

    model = table.model()
    indexes = table.selectedIndexes()
    row0 = indexes[0].row()
    col0 = indexes[0].column()

    text = QW.QApplication.clipboard().text()

    # TODO Slow and does not work with numbers
    for i, row in enumerate(text.split('\n')):
        if not row:
            return
        for j, col in enumerate(row.split('\t')):
            model.setData(model.index(row0 + i, col0 + j), col)


def table_to_clipboard(table):
    """Copies selected table to keyboard."""
    mime = table_selection_to_mime_data(table)
    QW.QApplication.clipboard().setMimeData(mime, QG.QClipboard.Clipboard)


def mime_data_to_table(table):
    pass


def table_selection_to_mime_data(table):
    """Copy the current selection in a QTableView to the clipboard."""
    lines = table_selection_to_list(table)

    as_csv = lines_to_csv_string(lines, dialect="excel").encode("utf-8")
    as_tsv = lines_to_csv_string(lines, dialect="excel-tab").encode("utf-8")

    mime = QC.QMimeData()
    mime.setData("text/csv", QC.QByteArray(as_csv))
    mime.setData("text/tab-separated-values", QC.QByteArray(as_tsv))
    mime.setData("text/plain", QC.QByteArray(as_tsv))
    return mime


def table_selection_to_list(table):
    """Put a table selection into a two-dimensional list"""
    model = table.model()
    indexes = table.selectedIndexes()

    rows = sorted(set(index.row() for index in indexes))
    columns = sorted(set(index.column() for index in indexes))

    lines = []
    for row in rows:
        line = []
        for col in columns:
            val = model.index(row, col).data(role=QC.Qt.DisplayRole)
            line.append("" if val is None else str(val))
        lines.append(line)

    return lines


def lines_to_csv_string(lines, dialect="excel"):
    """Turn individual lines to a CSV."""
    stream = io.StringIO()
    writer = csv.writer(stream, dialect=dialect)
    writer.writerows(lines)
    return stream.getvalue()
