# -*- mode: python ; coding: utf-8 -*-

import pathlib

folder = pathlib.Path.cwd()

import pygaps

pgversion = pygaps.__version__
from importlib.metadata import version, PackageNotFoundError

try:
    pggversion = version("pygapsgui")
except PackageNotFoundError:
    import pygapsgui
    pggversion = pygapsgui.__version__

pygaps_dir = pathlib.Path(pygaps.__file__).parent

extra_datas = [
    ("LICENSE", "."),
    ("LICENSE.rtf", "."),
    ("pygapsgui/resources", "pygapsgui/resources"),
    (str(pygaps_dir / "data"), "pygaps/data"),
    (str(pygaps_dir / "characterisation/kernels"), "pygaps/characterisation/kernels"),
]

# Modules that should not be in the distribution
extra_excludes = [
    # installed in path
    'pyinstaller',
    'setuptools'
]

# DLLs that should not be in the distribution
extra_exclude_dll = [
    # 'Qt6dbus.dll',
    # 'Qt6Network.dll',
    # 'Qt6Qml.dll',
    # 'Qt6Quick.dll',
    # 'Qt6WebSockets.dll',
]

# Modules that SHOULD be in the distribution but may not get picked up
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

block_cipher = None

a = Analysis(['pyGAPS-gui.py'],
             pathex=[folder],
             binaries=[],
             datas=extra_datas,
             hiddenimports=extra_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=extra_excludes,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

to_keep = []

# Iterate through the list of included binaries.
for (dest, source, kind) in a.binaries:
    # Skip anything we don't need.
    if pathlib.Path(dest).name in extra_exclude_dll:
        continue
    to_keep.append((dest, source, kind))

# Replace list of data files with filtered one.
a.binaries = to_keep

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

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
    icon="pygapsgui/resources/main_icon.ico",
)

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
