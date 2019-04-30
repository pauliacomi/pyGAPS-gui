from PySide2 import QtWidgets


def open_file_dialog(parent_widget, caption, directory, filter=None):
    filename = QtWidgets.QFileDialog.getOpenFileName(parent_widget, caption=caption,
                                                     directory=directory,
                                                     filter=filter)
    if isinstance(filename, tuple):  # PyQt5 returns a tuple...
        return str(filename[0])
    return str(filename)


def open_files_dialog(parent_widget, caption, directory, filter=None):
    filenames = QtWidgets.QFileDialog.getOpenFileNames(parent_widget, caption=caption,
                                                       directory=directory,
                                                       filter=filter)
    if isinstance(filenames, tuple):  # PyQt5 returns a tuple...
        filenames = filenames[0]
    return filenames


def save_file_dialog(parent_widget, caption, directory, filter=None):
    filename = QtWidgets.QFileDialog.getSaveFileName(parent_widget, caption,
                                                     directory=directory,
                                                     filter=filter)
    if isinstance(filename, tuple):  # PyQt5 returns a tuple...
        return str(filename[0])
    return str(filename)
