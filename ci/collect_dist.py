#
# Lightning Python Distribution System
#
# Copyright (C) 2014 Jeffrey Armstrong
#                    <jeffrey.armstrong@approximatrix.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This script will deploy the python distribution to a folder, laid out just like
# reference Python, and then zip up the result or create XML inputs for WiX.

import os
import os.path
import zipfile
import argparse
import xml.dom.minidom
import uuid
from io import StringIO

from importlib.metadata import version, PackageNotFoundError

try:
    pggversion = version("pygapsgui")
except PackageNotFoundError:
    import pygapsgui
    pggversion = pygapsgui.__version__


def zipit(dist_dir, work_dir):
    """Zip folder."""
    print("Zipping...")
    if os.path.exists(dist_dir + '.zip'):
        os.remove(dist_dir + '.zip')

    with zipfile.ZipFile(dist_dir + '.zip', 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(dist_dir):
            for f in files:
                diskname = os.path.join(root, f)
                zipname = os.path.relpath(diskname)
                zf.write(diskname, arcname=zipname)

    print("Distribution is located at {0}".format(dist_dir + '.zip'))


def gen_wix_id():
    """Make UUID for wix."""
    return "_" + str(uuid.uuid4()).replace("-", "")


def construct_msi_strings(dist_dir, work_dir):
    """Make strings for MSI."""

    doc = xml.dom.minidom.Document()

    # We'll now construct
    curdir = []
    curdir.append((dist_dir, doc))

    topElement = doc.createElement("Root")
    doc.appendChild(topElement)
    curdir.append((dist_dir, topElement))

    # need to return a component id list
    components = []

    for root, dirs, files in os.walk(dist_dir, topdown=True):

        # Create a basic path to our source
        start = root.replace(work_dir + '\\', '')

        parent, thisdir = os.path.split(root)
        while parent != curdir[-1][0] and curdir[-1][1] != topElement:
            curdir.pop()

        if root != dist_dir:
            # Create a Directory node
            thisnode = doc.createElement("Directory")
            thisnode.setAttribute("Name", thisdir)
            did = gen_wix_id()

            thisnode.setAttribute("Id", did)
            curdir[-1][1].appendChild(thisnode)
            curdir.append((root, thisnode))

        # Create a component for the files in said directory
        cnode = doc.createElement('Component')
        cnode.setAttribute('Id', gen_wix_id())
        cnode.setAttribute("DiskId", "1")
        cnode.setAttribute("Guid", str(uuid.uuid4()))

        # If there are files, append the component node
        if files is not None and len(files) > 0:
            if root != dist_dir:
                thisnode.appendChild(cnode)
            else:
                curdir[-1][1].appendChild(cnode)
            components.append(cnode)

        # Add each file to the component (not recommended, but meh...)
        for name in files:
            fnode = doc.createElement('File')
            fnode.setAttribute("Name", name)
            fnode.setAttribute("Source", os.path.join(start, name))

            # We treat the main executable separately
            if name == 'pyGAPS-gui.exe':
                continue
            else:
                fnode.setAttribute("Id", gen_wix_id())

            cnode.appendChild(fnode)

    # Create an XML fragment
    filesxml = topElement.toprettyxml(indent='    ')
    filesxml = filesxml.replace("<Root>", "").replace("</Root>", "")

    # Build a list of ComponentRefs, but don't bother using a DOM
    componentsSIO = StringIO()
    for x in components:
        componentsSIO.write(
            '                <ComponentRef Id="{0}" />\n'.format(x.getAttribute("Id"))
        )
    componentRefs = componentsSIO.getvalue()
    componentsSIO.close()

    return filesxml, componentRefs


def msi(dist_dir, work_dir):
    """Create an WXS input file."""

    # First build the XML components
    print("Constructing WiX Components XML")
    print("Distribution dir:", dist_dir)
    print("Target dir:", work_dir)
    _, distdirname = os.path.split(dist_dir)
    print("Distribution dir name:", distdirname)
    files, refs = construct_msi_strings(dist_dir, work_dir)

    # Read in the WiX template
    template = ""
    base_wix_path = os.path.join(os.path.dirname(__file__), 'base_wix.wxs')
    with open(base_wix_path, "r", encoding="utf8") as f:
        template = f.read()

    # Write out the WiX file to the parent directory of the distro
    print("Generating WiX Input File")
    out_wix_path = os.path.join(work_dir, 'pyGAPS-gui.wxs')
    version_tuple = pggversion.split(".")
    print(
        f"Generated WiX file for version: {version_tuple[0]}.{version_tuple[1]}.{version_tuple[2]}"
    )
    with open(out_wix_path, "w", encoding="utf8") as f:
        f.write(
            template.format(
                major=version_tuple[0],
                minor=version_tuple[1],
                micro=version_tuple[2],
                distdir=distdirname,
                distfiles=files,
                distcomponents=refs,
            )
        )


def main(cmds, dist_dir):
    """Main entrypoint."""

    # The working dir is where our file will be written
    work_dir, _ = os.path.split(dist_dir)

    for cmd in cmds:
        if cmd == 'zip':
            zipit(dist_dir, work_dir)
        elif cmd == 'msi':
            msi(dist_dir, work_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a ZIP or an WIX MSI.')
    parser.add_argument(
        'command',
        metavar='cmd',
        type=str,
        nargs='*',
        help='command for this script, either "zip" or "msi"',
    )
    parser.add_argument(
        'distpath',
        metavar='dist',
        type=str,
        help='path to the location of the distribution',
    )
    args = parser.parse_args()
    main(args.command, args.distpath)
