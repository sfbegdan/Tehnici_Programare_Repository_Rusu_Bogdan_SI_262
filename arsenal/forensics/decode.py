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
else:
    continut = a.intrare

output_dir = Path("arsenal/forensics")
output_dir.mkdir(parents=True, exist_ok=True)

data = {
    "strat": a.intrare,
    "rezultat": rezultat
}

with open(output_dir / "fisa.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)


