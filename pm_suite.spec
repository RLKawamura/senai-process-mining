# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import glob
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

block_cipher = None
SPECPATH = os.path.dirname(os.path.abspath(SPEC))
SRC_DIR = os.path.join(SPECPATH, 'src')
ASSETS_DIR = os.path.join(SPECPATH, 'assets')

if not os.path.exists(SRC_DIR):
    raise FileNotFoundError(f"Diretório src não encontrado: {SRC_DIR}")
if not os.path.exists(ASSETS_DIR):
    raise FileNotFoundError(f"Diretório assets não encontrado: {ASSETS_DIR}")

datas_pm4py = collect_data_files('pm4py', include_py_files=True)
datas_matplotlib = collect_data_files('matplotlib')
datas_pandas = collect_data_files('pandas')
datas_setuptools = collect_data_files('setuptools')
datas_jaraco = collect_data_files('jaraco', include_py_files=True)

VENDOR_GRAPHVIZ = os.path.join(SPECPATH, 'vendor', 'graphviz')
vendor_datas = []

if os.path.exists(VENDOR_GRAPHVIZ):
    print(f"[INFO] Incluindo Graphviz portátil de: {VENDOR_GRAPHVIZ}")
    vendor_datas = [
        (os.path.join(VENDOR_GRAPHVIZ, 'bin'), 'vendor/graphviz/bin'),
        (os.path.join(VENDOR_GRAPHVIZ, 'lib'), 'vendor/graphviz/lib'),
    ]
else:
    print(f"[WARN] Graphviz não encontrado em vendor/")

binaries_numpy = collect_dynamic_libs('numpy')
binaries_pandas = collect_dynamic_libs('pandas')
binaries_scipy = collect_dynamic_libs('scipy')

python_dll = []
python_base = os.path.dirname(sys.executable)

for dll_name in ['python38.dll', 'python3.dll', f'python{sys.version_info.major}{sys.version_info.minor}.dll']:
    dll_paths = [
        os.path.join(python_base, dll_name),
        os.path.join(python_base, 'DLLs', dll_name),
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32', dll_name),
    ]
    for dll_path in dll_paths:
        if os.path.exists(dll_path):
            python_dll.append((dll_path, '.'))
            print(f"[INFO] Python DLL encontrado: {dll_path}")
            break
    if python_dll:
        break

vcruntime_dll = []
for vcrt in glob.glob(os.path.join(python_base, 'vcruntime*.dll')):
    vcruntime_dll.append((vcrt, '.'))

hiddenimports = [
    'tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox',
    'tkinter.scrolledtext', 'tkinter.font', 'runpy', 'importlib',
    'unittest', 'unittest.mock', 'pkg_resources', 'setuptools',
    'jaraco', 'jaraco.text', 'more_itertools',
    'pm4py', 'numpy', 'pandas', 'scipy', 'matplotlib',
    'requests', 'urllib3', 'certifi', 'aw_client', 'aw_core',
    'graphviz', 'lxml', 'openpyxl', 'xlrd',
]

hiddenimports += collect_submodules('pm4py')
hiddenimports += collect_submodules('numpy')
hiddenimports += collect_submodules('pandas')

a = Analysis(
    ['pm_suite_entry.py'],
    pathex=[SPECPATH],
    binaries=python_dll + vcruntime_dll + binaries_numpy + binaries_pandas + binaries_scipy,
    datas=datas_pm4py + datas_matplotlib + datas_pandas + datas_setuptools + datas_jaraco + vendor_datas + [
        (os.path.join(ASSETS_DIR, 'senai.ico'), 'assets')  # SEM o _internal/
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=['pandas.tests', 'numpy.tests', 'pytest', 'IPython', 'jupyter'],
    cipher=block_cipher,
)

src_tree = Tree(SRC_DIR, prefix='_internal/app', excludes=['__pycache__', '*.pyc', 'aw_watcher_uia.py'])
a.datas += src_tree

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz, a.scripts, [], exclude_binaries=True,
    name='SENAI_Mineracao_Processos', debug=False, strip=False,
    upx=True, console=False,
    icon=os.path.join(ASSETS_DIR, 'senai.ico'),
)

coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas,
               strip=False, upx=True, name='SENAI_Mineracao_Processos')
