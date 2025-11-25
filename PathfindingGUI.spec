# -*- mode: python ; coding: utf-8 -*-

# Внешние данные, которые нужно включить в сборку
datas = [
    ('config/config.yaml', 'config'),
]

# Скрытые импорты для PyQt6 (обязательно)
hiddenimports = [
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
]

a = Analysis(
    ['src/gui/app.py'],    # точка входа
    pathex=['.'],          # корень проекта
    binaries=[],
    datas=datas,           # <--- ВАЖНО: datas передаём сюда
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,             # должен включать бинарники PyQt6
    a.zipfiles,
    a.datas,
    name='PathfindingGUI',
    console=False,
    debug=False,
    strip=False,
    upx=False,
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='PathfindingGUI',
)
