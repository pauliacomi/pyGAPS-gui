"""Compiled Qt resources (resources_rc) must provide the icons used by the main window."""

import pathlib
import re

import pytest
from qtpy import QtGui as QG

import pygapsgui

SOURCE = pathlib.Path(pygapsgui.__file__).with_name("MainWindowUI.py")
ICON_PATHS = sorted(set(re.findall(r'":(/res/icons/[^"]+)"', SOURCE.read_text(encoding="utf-8"))))


def test_icons_are_referenced():
    assert ICON_PATHS


@pytest.mark.parametrize("path", ICON_PATHS)
def test_resource_icon_loads(qapp, path):
    import pygapsgui.widgets.resources_rc  # noqa: F401

    assert not QG.QPixmap(":" + path).isNull()
