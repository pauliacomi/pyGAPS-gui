"""Regression checks for the release archive and WiX input."""

import os
import xml.etree.ElementTree as ET
import zipfile

import pytest

from ci import collect_dist

WIX_NS = "{http://wixtoolset.org/schemas/v4/wxs}"


@pytest.fixture
def dist_dir(tmp_path):
    dist = tmp_path / "pyGAPS-gui test build"
    (dist / "resources").mkdir(parents=True)
    (dist / "pyGAPS-gui.exe").write_bytes(b"executable")
    (dist / "LICENSE.rtf").write_text("license", encoding="utf8")
    (dist / "resources" / "icon.ico").write_bytes(b"icon")
    return dist


def test_archive_is_rooted_at_distribution_folder(dist_dir):
    collect_dist.zipit(str(dist_dir), str(dist_dir.parent))

    with zipfile.ZipFile(f"{dist_dir}.zip") as archive:
        assert set(archive.namelist()) == {
            "pyGAPS-gui test build/pyGAPS-gui.exe",
            "pyGAPS-gui test build/LICENSE.rtf",
            "pyGAPS-gui test build/resources/icon.ico",
        }


@pytest.mark.parametrize(("version", "expected"), [("0.6", "0.6.0"), ("0.7.dev3+dirty", "0.7.0")])
def test_wix_input_accepts_short_and_development_versions(dist_dir, monkeypatch, version, expected):
    work_dir = dist_dir.parent
    monkeypatch.setattr(collect_dist, "pggversion", version)

    collect_dist.msi(str(dist_dir), str(work_dir))

    text = (work_dir / "pyGAPS-gui.wxs").read_text(encoding="utf8")
    assert f'ProductVersion="{expected}"' in text
    root = ET.fromstring(text)
    assert root.tag == WIX_NS + "Wix"
    for file in root.iter(WIX_NS + "File"):
        source = file.attrib["Source"].replace("\\", os.sep)
        assert (work_dir / source).is_file()
