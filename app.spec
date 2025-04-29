# app.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=['.'],
    binaries=[],
	datas=[
		('assets/player/*.png', 'assets/player'),
		('assets/gui/*.png', 'assets/gui'),
		('assets/destroy_stages/*.png', 'assets/destroy_stages'),
		('assets/font/*.ttf', 'assets/font'),
		('assets/sound_effects/*.mp3', 'assets/sound_effects'),
		('assets/cursors/*.png', 'assets/cursors'),
		('assets/furnace/*.png', 'assets/furnace'),
		('assets/heart/*.png', 'assets/heart'),
		('assets/items/*.png', 'assets/items'),
		('assets/sound_effects/*.mp3', 'assets/sound_effects'),
		('assets/*.png', 'assets'),  # for menu_background.png, menu_background2.png
		('recipes/crafting_table/*.json', 'recipes/crafting_table'),
		('recipes/inventory_crafting_table/*.json', 'recipes/inventory_crafting_table'),
		('commands/*.py', 'commands'),
		('config.json', '.'),
	],
    hiddenimports=[
        'commands',  # to make sure your dynamic imports work
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TerrMine',
    debug=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,   # Extracts to random temp folder at runtime
    console=False,         # No black console window
)