# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec to bundle the app into a stand-alone executable.
# Build it with: pyinstaller weather-app.spec

block_cipher = None


a = Analysis(
    ['weather_app/__main__.py'],
    pathex=[],
    binaries=[],
    # Bundle the API key config so the packaged app works without any setup.
    datas=[('config.ini', '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='weather-app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,
)
