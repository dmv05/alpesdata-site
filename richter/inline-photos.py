#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intègre les photos de la fiche Richter directement dans index.html (base64),
pour un affichage garanti sur mobile (aucune requête d'image externe).
Usage : python3 inline-photos.py  — à relancer après chaque changement de photo.
"""
import base64
import io
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "index.html")
PHOTOS = os.path.join(BASE, "photos")
MAX_W = 900
QUALITY = 72

try:
    from PIL import Image
except ImportError:
    print("PIL absent — tentative pip install pillow")
    os.system("pip install --quiet pillow")
    from PIL import Image

def photo_to_data_uri(path):
    im = Image.open(path).convert("RGB")
    if im.width > MAX_W:
        h = round(im.height * MAX_W / im.width)
        im = im.resize((MAX_W, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/jpeg;base64,{b64}", len(buf.getvalue())

def main():
    with open(HTML, encoding="utf-8") as f:
        html = f.read()

    total_orig = 0
    total_b64 = 0
    def repl(m):
        nonlocal total_orig, total_b64
        n = m.group(1)
        path = os.path.join(PHOTOS, f"photo-{n}.jpg")
        if not os.path.exists(path):
            return m.group(0)
        uri, size = photo_to_data_uri(path)
        total_orig += os.path.getsize(path)
        total_b64 += size
        print(f"  photo-{n}.jpg : {size//1024} Ko (optimisée) intégrée")
        return f'src="{uri}"'

    new_html = re.sub(r'src="photos/photo-(\d)\.jpg"', repl, html)
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"\nPhotos optimisées : {total_orig//1024} Ko -> {total_b64//1024} Ko")
    print(f"Poids final index.html : {len(new_html.encode())//1024} Ko")

if __name__ == "__main__":
    main()
