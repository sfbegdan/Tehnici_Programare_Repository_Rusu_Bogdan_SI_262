s = "Salut"
b = s.encode() # bytes
print(b, b[0]) # b"Salut" 83
# TODO: tipareste b.hex() si refa bytes din hex
# cu bytes.fromhex(...)

hex_string = b.hex()
print(hex_string)

b2 = bytes.fromhex(hex_string)
print(b2)

import re

def ghici_strat(s):
    if re.search(r'%[0-9a-fA-F]{2}', s):
        return "url"

    if re.fullmatch(r'[0-9a-fA-F]+', s) and len(s) % 2 == 0:
        return "hex"

    if re.fullmatch(r'[A-Za-z0-9+/=]+', s):
        return "base64"

    return "necunoscut"

print(ghici_strat("%2Fetc")) # url
print(ghici_strat("48656c6c6f")) # hex

import base64
from urllib.parse import unquote
def desfa(s):
    strat = ghici_strat(s)
    # TODO: pentru fiecare strat, decodeaza
    # base64 -> base64.b64decode(s)
    if strat == "base64":
        result = base64.b64decode(s)
    # hex -> bytes.fromhex(s)
    if strat == "hex":
        result = bytes.fromhex(s).decode()
    # url -> unquote(s).encode()
    if strat == "url":
        result = unquote(s).encode()
    # intoarce (strat, rezultat_bytes)
    return strat, result

def citibil(b):
    # TODO: True daca toti octetii sunt 32..126
    return all(32 <= c < 127 for c in b)
val = "NTM1OTU3NTk="
for _ in range(8):
    strat, b = desfa(val)
    # TODO: daca citibil(b): opreste si tipareste
    if citibil(b):
        print(b)
        break
    else:
        val = b.decode()
    # altfel val = b.decode(); continua

date = open("probe/xor.bin", "rb").read()
for k in range(256):
    clar = bytes(b ^ k for b in date)
    # TODO: daca citibil(clar):
    # print("cheie:", k, clar.decode())
    if citibil(clar):
        print("cheie:", k, clar.decode())

import hashlib
tinta = open("probe/hashuri.txt").readline().strip()
print(len(tinta)) # 32 md5 / 40 sha1 / 64 sha256
for cuv in open("probe/wordlist.txt", encoding="latin1"):
    cuv = cuv.strip()
    # TODO: daca hashlib.md5(cuv.encode()).hexdigest()
    # == tinta: print("gasit:", cuv); break
    if hashlib.md5(cuv.encode()).hexdigest() == tinta:
        print("gasit:", cuv); break

import argparse, json
from pathlib import Path
from PIL.ExifTags import TAGS, GPSTAGS
p = argparse.ArgumentParser()
p.add_argument("intrare") # sir sau cale
p.add_argument("--fisier", action="store_true")
a = p.parse_args()
# TODO: daca a.fisier, citeste octetii din cale;
# altfel trateaza intrarea ca sir
# TODO: salveaza {strat, rezultat} in
# arsenal/forensics/fisa.json
if a.fisier:
    with open(a.intrare, "rb") as f:
        continut = f.read()
    rezultat = continut.hex()
else:
    continut = a.intrare
    rezultat = continut

output_dir = Path("arsenal/forensics")
output_dir.mkdir(parents=True, exist_ok=True)

data = {
    "strat": a.intrare,
    "rezultat": rezultat
}

with open(output_dir / "fisa.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

def tip_real(cale):
    cap = open(cale, "rb").read(8)
    # TODO: daca cap incepe cu b"%PDF" -> "pdf"
    # b"\x89PNG" -> "png" ; b"\xff\xd8" -> "jpeg"
    # b"PK\x03\x04" -> "zip/docx"
    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()
print(tip_real("probe/foto.jpg"))

import re
date = open("probe/ascuns.png", "rb").read()
# TODO: for m in re.findall(rb"[ -~]{4,}", date):
# print(m.decode())
# cauta un indiciu: o cale, un mesaj, un nume de fisier
for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())

from PIL import Image
from PIL.ExifTags import TAGS
exif = Image.open("probe/foto.jpg")._getexif() or {}
for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)
# TODO: ia blocul GPS (tag 34853) si tipareste
# latitudinea si longitudinea
gps_raw = exif.get(34853)
if gps_raw:
    gps = {GPSTAGS.get(k, k): v for k, v in gps_raw.items()}

    g, m, s = (float(x) for x in gps["GPSLatitude"])
    lat = g + m / 60 + s / 3600
    if gps["GPSLatitudeRef"] == "S":
        lat = -lat

    g, m, s = (float(x) for x in gps["GPSLongitude"])
    lon = g + m / 60 + s / 3600
    if gps["GPSLongitudeRef"] == "W":
        lon = -lon

    print("Latitudine:", lat)
    print("Longitudine:", lon)
else:
    print("Fotografia nu conține date GPS.")

date = open("probe/ascuns.png", "rb").read()
i = date.find(b"PK\x03\x04")
# TODO: daca i != -1:
# open("gasit.zip","wb").write(date[i:])
# print("arhiva extrasa de la octetul", i)
# apoi dezarhiveaza si vezi ce era inauntru
if i != -1:
    open("gasit.zip", "wb").write(date[i:])
    print("arhiva extrasa de la octetul", i)

from PIL import Image
img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.get_flattened_data())
mesaj = b"FLAG{ascuns_in_pixeli}" + b"\x00"
biti = "".join(f"{x:08b}" for x in mesaj)
# TODO: pentru fiecare bit, ia un canal si pune
# canal = (canal & ~1) | int(bit)
# TODO: img.putdata(px_nou); img.save("stego.png")
if len(biti) > len(px) * 3:
    raise SystemExit("Poza este prea mică pentru mesaj")

px_nou = []
i = 0
for (r, g, b) in px:
    canale = [r, g, b]
    for j in range(3):
        if i < len(biti):
            canale[j] = (canale[j] & ~1) | int(biti[i])
            i += 1
    px_nou.append(tuple(canale))

img.putdata(px_nou)
img.save("stego.png")

px = list(Image.open("stego.png").convert("RGB").get_flattened_data())
biti = ""
for (r, g, b) in px:
    # TODO: aduna ultimii biti (r&1, g&1, b&1)
    biti += str(r & 1)
    biti += str(g & 1)
    biti += str(b & 1)

# TODO: grupeaza cate 8 biti -> octeti -> text
# opreste-te la primul octet 0 (final de mesaj)
caractere = []
for i in range(0, len(biti), 8):
    octet_biti = biti[i:i + 8]
    if len(octet_biti) < 8:
        break

    valoare_octet = int(octet_biti, 2)

    if valoare_octet == 0:
        break

    caractere.append(chr(valoare_octet))

mesaj_reconstituit = "".join(caractere)
print("Mesajul ascuns:", mesaj_reconstituit)













