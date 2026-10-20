"""Regression checks for the release archive and WiX input."""

import contextlib
import io
import os
import pathlib
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile

from ci import collect_dist


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work_dir = pathlib.Path(self.temp.name)
        self.dist_dir = self.work_dir / "pyGAPS-gui test build"
        self.dist_dir.mkdir()
        (self.dist_dir / "pyGAPS-gui.exe").write_bytes(b"executable")
        (self.dist_dir / "LICENSE.rtf").write_text("license", encoding="utf8")
        (self.dist_dir / "resources").mkdir()
        (self.dist_dir / "resources" / "icon.ico").write_bytes(b"icon")

    def test_archive_is_rooted_at_distribution_folder(self):
        with contextlib.redirect_stdout(io.StringIO()):
            collect_dist.zipit(str(self.dist_dir), str(self.work_dir))
        with zipfile.ZipFile(str(self.dist_dir) + ".zip") as archive:
            self.assertEqual(
                set(archive.namelist()),
                {
                    "pyGAPS-gui test build/pyGAPS-gui.exe",
                    "pyGAPS-gui test build/LICENSE.rtf",
                    "pyGAPS-gui test build/resources/icon.ico",
                },
            )

    def test_wix_input_accepts_short_and_development_versions(self):
        for version, expected in (("0.6", "0.6.0"), ("0.7.dev3+dirty", "0.7.0")):
            with self.subTest(version=version):
                with patch.object(collect_dist, "pggversion", version):
                    with contextlib.redirect_stdout(io.StringIO()):
                        collect_dist.msi(str(self.dist_dir), str(self.work_dir))
                text = (self.work_dir / "pyGAPS-gui.wxs").read_text(encoding="utf8")
                self.assertIn(f'ProductVersion="{expected}"', text)
                root = ET.fromstring(text)
                namespace = "{http://wixtoolset.org/schemas/v4/wxs}"
                self.assertEqual(root.tag, namespace + "Wix")
                for file in root.iter(namespace + "File"):
                    source = file.attrib["Source"].replace("\\", os.sep)
                    self.assertTrue((self.work_dir / source).is_file())


if __name__ == "__main__":
    unittest.main()
