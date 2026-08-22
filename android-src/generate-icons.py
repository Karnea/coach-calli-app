#!/usr/bin/env python3
"""Génère les icônes Android (mipmap-*) à partir de resources/icon.png."""
import os, sys
from PIL import Image, ImageDraw

SRC = sys.argv[1] if len(sys.argv) > 1 else "resources/icon.png"
RES = sys.argv[2] if len(sys.argv) > 2 else "android/app/src/main/res"

DENSITIES = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192,
}

src = Image.open(SRC).convert("RGBA")

import glob
for pat in [
    os.path.join(RES, "drawable*", "ic_launcher_foreground.xml"),
    os.path.join(RES, "drawable*", "ic_launcher_background.xml"),
    os.path.join(RES, "values*", "ic_launcher_background.xml"),
    os.path.join(RES, "mipmap-*", "ic_launcher.webp"),
    os.path.join(RES, "mipmap-*", "ic_launcher_round.webp"),
    os.path.join(RES, "mipmap-*", "ic_launcher_foreground.webp"),
]:
    for f in glob.glob(pat):
        try:
            os.remove(f)
            print("supprimé (ancien) :", f)
        except OSError:
            pass


def square_icon(size):
    return src.resize((size, size), Image.LANCZOS)


def round_icon(size):
    img = src.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((0, 0, size, size), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def foreground_icon(size):
    w, h = src.size
    m = int(w * 0.13)
    cropped = src.crop((m, m, w - m, h - m))
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    inner = int(size * 0.72)
    logo = cropped.resize((inner, inner), Image.LANCZOS)
    off = (size - inner) // 2
    canvas.paste(logo, (off, off), logo)
    return canvas


for dens, size in DENSITIES.items():
    d = os.path.join(RES, "mipmap-" + dens)
    os.makedirs(d, exist_ok=True)
    square_icon(size).save(os.path.join(d, "ic_launcher.png"))
    round_icon(size).save(os.path.join(d, "ic_launcher_round.png"))
    fg = int(size * 2.25)
    foreground_icon(fg).save(os.path.join(d, "ic_launcher_foreground.png"))
    print("mipmap-%s : %dpx (fg %dpx)" % (dens, size, fg))

values = os.path.join(RES, "values")
os.makedirs(values, exist_ok=True)
with open(os.path.join(values, "ic_launcher_background.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<resources>\n')
    f.write('    <color name="ic_launcher_background">#171C24</color>\n')
    f.write('</resources>\n')

for folder in ["mipmap-anydpi-v26"]:
    d = os.path.join(RES, folder)
    os.makedirs(d, exist_ok=True)
    for name in ["ic_launcher", "ic_launcher_round"]:
        with open(os.path.join(d, name + ".xml"), "w") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n')
            f.write('    <background android:drawable="@color/ic_launcher_background" />\n')
            f.write('    <foreground android:drawable="@mipmap/ic_launcher_foreground" />\n')
            f.write('</adaptive-icon>\n')

print("Icônes générées avec succès")
