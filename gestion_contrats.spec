# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['manage.py'],
    pathex=['.'],  # Chemin vers votre projet
    binaries=[],
    datas=[
        ('gestion_contrats/templates', 'gestion_contrats/templates'),  # Inclut les templates
        ('gestion_contrats/static', 'gestion_contrats/static'),        # Inclut les fichiers statiques
        ('gestion_contrats/*.py', 'gestion_contrats'),                 # Inclut tous les fichiers Python du projet
        ('media', 'media'),                                            # Inclut le répertoire des médias
        ('db.sqlite3', '.'),                                           # Inclut la base de données SQLite si nécessaire
        # Ajoutez d'autres fichiers nécessaires ici
    ],
    hiddenimports=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Ajoutez d'autres modules si nécessaires
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='gestion_contrats',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='gestion_contrats',
)
