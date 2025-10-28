# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os

# Get escpos package path
try:
    import escpos
    escpos_path = os.path.dirname(escpos.__file__)
except ImportError:
    escpos_path = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('restaurant_billing.db', '.'),
    ] + (
        [(f'{escpos_path}/capabilities.json', 'escpos')] if escpos_path else []
    ),
    hiddenimports=[
        'telegram_notifier',
        'thermal_printer',
        'admin_panel',
        'inventory_manager',
        'accounting',
        'purchase_management',
        'staff_management',
        'analytics',
        'backup_manager',
        'automation',
        'telegram_bot',
        'escpos',
        'escpos.printer',
        'database',
    ],
    hookspath=[],
    hooksconfig={},
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
    name='HUNGER_Billing_Software',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='restaurant_icon.ico',
)
