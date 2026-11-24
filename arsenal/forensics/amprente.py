#------A1------

MAGIC = {b"\x89PNG": "PNG", b"%PDF": "PDF", b"PK\x03\x04": "ZIP"}


def tip(head):
    # TODO: pentru fiecare (semnatura, nume) din MAGIC,
    #   daca head.startswith(semnatura) intoarce nume;
    #   dupa bucla, intoarce "necunoscut"
    for semnatura, nume in MAGIC.items():
        if head.startswith(semnatura):
            return nume
    return "necunoscut"

#------A2------

import os, hashlib

def amprenta_fisier(cale):
    with open(cale, "rb") as f:  # "rb" = binar; with = inchide singur
        date = f.read()
        # TODO: intoarce {"nume": os.path.basename(cale),
        #   "tip": tip(date[:8]),
        #   "sha256": hashlib.sha256(date).hexdigest()[:16]}
        return {
            "nume": os.path.basename(cale),
            "tip": tip(date[:8]),
            "sha256": hashlib.sha256(date).hexdigest()[:16]
        }

#------A3------

def scaneaza(folder):
    rez = []
    for nume in sorted(os.listdir(folder)):
        cale = os.path.join(folder, nume)
        if os.path.isfile(cale):
            # TODO: adauga amprenta_fisier(cale) la rez
            rez.append(amprenta_fisier(cale))
    return rez

# TODO: main() cu argparse (un argument: folder) care tipareste
#       fiecare fisa cu f"{nume:14} {tip:11} {sha256}"

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    args = parser.parse_args()

    for fisa in scaneaza(args.folder):
        print(f"{fisa['nume']:14} {fisa['tip']:11} {fisa['sha256']}")

if __name__ == "__main__":
    main()












