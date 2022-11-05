# -*- mode: python ; coding: utf-8 -*-
# This file tells pyinstaller how to collect the program

import pathlib
from sys import platform
from importlib.metadata import version, PackageNotFoundError

# we need to deterimine the versions of the two components (pygaps and pygapsgui)
# this will allow us to set executable title appropriately

import pygaps

pgversion = version("pygaps")

try:
    pggversion = version("pygapsgui")
except PackageNotFoundError:
    import pygapsgui
    pggversion = pygapsgui.__version__

pygaps_dir = pathlib.Path(pygaps.__file__).parent

#
# Pyinstaller may miss some imports.
# Here we manually list some that may get lost.
extra_imports = [
    'numpy',
    'pandas',
    'matplotlib',
    'scipy',
    'requests',
    'gemmi',
]
extra_models = [f"pygaps.modelling.{m.stem}" for m in (pygaps_dir / "modelling").glob("*.py")]
extra_imports = extra_imports + extra_models

#
# Pyinstaller loses track of non-python resources.
# To addres this we manually specify important stuff.
extra_datas = [
    ("LICENSE", "."),
    ("LICENSE.rtf", "."),
    ("src/pygapsgui/resources", "pygapsgui/resources"),
    (str(pygaps_dir / "data"), "pygaps/data"),
]

#
# Pyinstaller often includes packages it shouldn't.
# Normally the collection takes place in a virtual
# environment with no extraneous python packages.
# However, there are a few which are needed for collection
# but not for the final bundle. Those are removed here.
extra_excludes = [
    # installed in path
    'pyinstaller',
    'setuptools'
]

#
# Pyinstaller includes all DLLs it can.
# Often we might not want some functionality from QT
# We can remove the specific DLLs here, if needed.
extra_exclude_dll = [
    # 'Qt6dbus.dll',
    # 'Qt6Network.dll',
    # 'Qt6Qml.dll',
    # 'Qt6Quick.dll',
    # 'Qt6WebSockets.dll',
]

#
# Some variables
folder = pathlib.Path.cwd()
block_cipher = None

#
# Run analysis script
a = Analysis(
    ['pyGAPS-gui.py'],
    pathex=[folder],
    binaries=[],
    datas=extra_datas,
    hiddenimports=extra_imports,
    hookspath=[],
    runtime_hooks=[],
    hooksconfig={
        "matplotlib": {
            "backends": [
                "QtAgg",
                "PDF",
                "SVG",
                "PS",
            ],  # collect the correct backend
        },
    },
    excludes=extra_excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

#
# Iteratively remove unneeded binaries
to_keep = []

# Iterate through the list of included binaries.
for (dest, source, kind) in a.binaries:
    # Skip anything we don't need.
    if pathlib.Path(dest).name in extra_exclude_dll:
        continue
    to_keep.append((dest, source, kind))

# Replace list of data files with filtered one.
a.binaries = to_keep

#
# run compression
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

#
# run exe creation
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pyGAPS-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="src/pygapsgui/resources/main_icon.ico",
)

#
# run collection
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name=f'pyGAPS-gui v{pggversion} (with pyGAPS v{pgversion})',
)

#
# run mac specific
if platform == "darwin":
    app = BUNDLE(
        coll,
        name=f'pyGAPS-gui v{pggversion}.app',
        icon="src/pygapsgui/resources/main_icon.ico",
    )
