# -*- mode: python ; coding: utf-8 -*-

import os

folder = os.getcwd()

import pygaps

pygaps_path = os.path.dirname(pygaps.__file__)

extra_datas = [
    ("src/resources", "pyGAPS/gui"),
    (os.path.join(pygaps_path, "data"), "pyGAPS/data"),
]

hiddenimports = [
    'numpy',
    'pandas',
    'matplotlib',
    'scipy',
    'requests',
    'gemmi',
]

block_cipher = None

a = Analysis(['pyGAPS-gui.py'],
             pathex=[folder],
             binaries=[],
             datas=extra_datas,
             hiddenimports=hiddenimports,
             hookspath=[],
             runtime_hooks=[],
             excludes=['pyinstaller', 'setuptools'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

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
    console=True,
    icon="src/resources/main_icon.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='pyGAPS-gui',
)
