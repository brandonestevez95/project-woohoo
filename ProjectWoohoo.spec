# -*- mode: python ; coding: utf-8 -*-
import sys
from PyInstaller.utils.hooks import collect_all

# Create a runtime hook to suppress pkg_resources warnings
runtime_hook = '''
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources")
warnings.filterwarnings("ignore", category=DeprecationWarning)
'''

with open('suppress_warnings.py', 'w') as f:
    f.write(runtime_hook)

block_cipher = None

# Collect all necessary data and binaries
data = []
binaries = []
hiddenimports = [
    'streamlit',
    'ollama',
    'torch',
    'transformers',
    'gtts',
    'soundfile',
    'setuptools',
    'pkg_resources.py2_warn',
    'PyPDF2',  # Add PDF support
]

# Add additional data files
datas = [
    ('app', 'app'),  # Include our app directory
    ('README.md', '.'),  # Include README
    ('requirements.txt', '.'),  # Include requirements
]

a = Analysis(
    ['launch.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['suppress_warnings.py'],  # Add our warning suppression
    excludes=['_tkinter', 'Tkinter', 'tkinter'],  # Exclude unnecessary packages
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove any duplicate data files
a.datas = list(set(a.datas))

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ProjectWoohoo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ProjectWoohoo',
) 