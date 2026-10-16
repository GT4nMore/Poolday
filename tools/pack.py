"""Build the Poolday-only NZP web build in ../docs from the official NZP web files.

    python tools/pack.py

- upstream/ holds the official files from github.com/nzp-team/nzp-team.github.io
- game.pk3 is copied without the stock maps and their map-specific music
- poolday.pk3 holds nz_Poolday (bsp + zombie waypoints) and its two radio songs
"""
import os
import shutil
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.join(HERE, '..', 'upstream')
OUT = os.path.join(HERE, '..', 'docs')
NZP = r'C:/Users/gt4/Desktop/nzp/nzp'
KEEP_TRACKS = {'tracks/tensioned_by_the_damned.wav', 'tracks/readme.txt'}

os.makedirs(os.path.join(OUT, 'nzp'), exist_ok=True)
for f in ('ftewebgl.js', 'ftewebgl.wasm', 'default.fmf', 'nzp/progs.pk3'):
    shutil.copy(os.path.join(UP, f), os.path.join(OUT, f))

src = zipfile.ZipFile(os.path.join(UP, 'nzp/game.pk3'))
with zipfile.ZipFile(os.path.join(OUT, 'nzp/game.pk3'), 'w', zipfile.ZIP_DEFLATED) as dst:
    for info in src.infolist():
        n = info.filename
        if n.startswith('maps/') and n != 'maps/':
            continue
        if n.startswith('tracks/') and not n.endswith('/') and n not in KEEP_TRACKS:
            continue
        dst.writestr(info, src.read(info), compress_type=info.compress_type)

with zipfile.ZipFile(os.path.join(OUT, 'nzp/poolday.pk3'), 'w', zipfile.ZIP_DEFLATED) as z:
    for f in ('maps/nz_Poolday.bsp', 'maps/nz_Poolday.way',
              'sounds/music/DieWoodys.wav', 'sounds/music/ThankYouUSA.wav'):
        z.write(os.path.join(NZP, f), f)

for f in ('nzp/game.pk3', 'nzp/progs.pk3', 'nzp/poolday.pk3', 'ftewebgl.wasm'):
    print(f, round(os.path.getsize(os.path.join(OUT, f)) / 1e6, 1), 'MB')
