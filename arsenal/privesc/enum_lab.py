#------A1------

import argparse, json, os

BAZA = os.path.dirname(os.path.abspath(__file__))



def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        # TODO: intoarce lista liniilor .strip(), fara cele goale si fara cele cu #
        linii = []
        for linie in f:
            linie_curata = linie.strip()
            if linie_curata and not linie_curata.startswith("#"):
                linii.append(linie_curata)
        return linii


#------A2------

def nume(cale):
    # TODO: intoarce ce e dupa ultimul "/"  (vezi rsplit)
    return cale.rsplit('/', 1)[-1]




#------A3------

GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}


def suid_constatari(cale):
    cai = citeste_linii(cale)
    # TODO: pentru fiecare cale UNICA, in ordine sortata, un dict:
    #   {"cale": c, "nume": nume(c),
    #    "risc": "mare" daca nume(c) in GTFO, altfel "normal"}
    cai_unice = sorted(set(cai))

    rezultat = []
    for c in cai_unice:
        nume_fisier = nume(c)
        risc_val = "mare" if nume_fisier in GTFO else "normal"

        rezultat.append({
            "cale": c,
            "nume": nume_fisier,
            "risc": risc_val
        })

    return rezultat

#-------A4------

def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)  # despachetare in tuplu
        # TODO: adauga {"user": user.strip(), "drept": drept.strip(),
        #   "risc": "mare" daca "NOPASSWD" in drept, altfel "normal"}
        out.append({
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": "mare" if "NOPASSWD" in drept else "normal"
        })
    return out


def cron_constatari(cale):
    # TODO: campuri = ln.split(); user = campuri[5];
    #   comanda = " ".join(campuri[6:]); dict cu user si comanda
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        user = campuri[5]
        comanda = " ".join(campuri[6:])
        out.append({
            "user": user,
            "comanda": comanda
        })
    return out

def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }

#------A5------

def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    raport = enumereaza(a.capturi)
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False));
        return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")
    # TODO: utilizatorii implicati = multimea userilor din sudo REUNITA cu cei din cron
    users_sudo = {item["user"] for item in raport.get("sudo", [])}
    users_cron = {item["user"] for item in raport.get("cron", [])}
    utilizatori_unici = sorted(users_sudo.union(users_cron))

    print(f"utilizatori implicati: {', '.join(utilizatori_unici)}")

    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")


if __name__ == "__main__":
    print("------A1------")
    cai = citeste_linii(os.path.join(BAZA, "start", "suid.txt"))
    print("linii SUID:", len(cai))

    print("------A2------")
    nume_unice = {nume(c) for c in cai}
    print("SUID distincte:", len(nume_unice))

    print("------A3------")
    suid = suid_constatari(os.path.join(BAZA, "start", "suid.txt"))
    mari = [c for c in suid if c["risc"] == "mare"]
    print(len(suid), "SUID,", len(mari), "cu risc mare")
    print(sorted(c["nume"] for c in mari))

    main()

