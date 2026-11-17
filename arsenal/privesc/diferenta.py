#------B1-------
import os
from arsenal.privesc.enum_lab import citeste_linii

BAZA_DIR = os.path.dirname(os.path.abspath(__file__))


def cai(fisier):
    # intoarce MULTIMEA cailor din fisier
    return set(citeste_linii(fisier))


if __name__ == "__main__":
    baza = cai(os.path.join(BAZA_DIR, "start", "baza_suid.txt"))
    acum = cai(os.path.join(BAZA_DIR, "start", "suid.txt"))
    print("baza:", len(baza), " acum:", len(acum))
    #------B2------
    noi = acum - baza
    print(len(noi), "SUID noi fata de sistemul curat")
    for c in sorted(noi):
        print(" ", c)
    #------B3-------
    from arsenal.privesc.enum_lab import nume, GTFO

    risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
    periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
    print("periculoase NOI:", periculoase)
