#!/usr/bin/env python3
"""Comptabilité du portefeuille fictif. Les agents décident ; ce programme calcule.

Le journal (donnees/journal.jsonl) est la seule vérité : on y ajoute des lignes, on n'en modifie jamais.
Chaque ligne porte une empreinte qui dépend de toutes les lignes précédentes : toute retouche se voit
avec la commande « verifier ». Positions, liquidités et performance sont recalculées en relisant le journal.

Commandes :
  init --capital 10000 --date AAAA-MM-JJ
  ordre --portefeuille agents|reference --sens achat|vente --titre ID --nom NOM --quantite N
        --date-decision AAAA-MM-JJ --justification TEXTE
  executer RELEVE.json     exécute les ordres en attente au prix d'ouverture du relevé
  etat RELEVE.json         valorise les deux portefeuilles et ajoute une ligne à la performance
  verifier                 contrôle que le journal n'a pas été retouché
Option commune : --dossier (défaut : donnees), --frais (défaut : outils/frais.json)
"""
import argparse, hashlib, json, sys
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

PORTEFEUILLES = ("agents", "reference")
EXPIRATION_JOURS = 5


def D(x):
    return Decimal(str(x))


def centime(x):
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class Refus(Exception):
    pass


# ---------- journal ----------

def lire_journal(dossier):
    f = Path(dossier) / "journal.jsonl"
    return [json.loads(l) for l in f.read_text().splitlines() if l.strip()] if f.exists() else []


def empreinte(precedente, ligne):
    corps = json.dumps({k: v for k, v in ligne.items() if k != "empreinte"}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256((precedente + corps).encode()).hexdigest()[:16]


def ajouter(dossier, ligne):
    journal = lire_journal(dossier)
    ligne = {"n": len(journal) + 1, "enregistre_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), **ligne}
    ligne["empreinte"] = empreinte(journal[-1]["empreinte"] if journal else "", ligne)
    Path(dossier).mkdir(parents=True, exist_ok=True)
    with open(Path(dossier) / "journal.jsonl", "a") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return ligne


def verifier(dossier):
    prec = ""
    for i, l in enumerate(lire_journal(dossier), 1):
        if l["n"] != i or l["empreinte"] != empreinte(prec, l):
            raise Refus(f"journal retouché ou abîmé à la ligne {i}")
        prec = l["empreinte"]
    return i if prec else 0


# ---------- calculs ----------

def frais_ordre(marche, quantite, prix, monnaie, taux, F):
    """Frais d'un ordre, en CHF. Tous les paramètres viennent du fichier de frais."""
    montant_dev = D(quantite) * D(prix)
    montant = centime(montant_dev * taux)
    if marche == "six":
        commission = centime(max(montant * D(F["six"]["taux"]), D(F["six"]["min_chf"])))
    else:
        c = max(D(quantite) * D(F["us"]["par_action_usd"]), D(F["us"]["min_usd"]))
        c = min(c, montant_dev * D(F["us"]["max_part"]))
        commission = centime(c * taux)
    change = D(0)
    if monnaie != "CHF":
        usd = D(F["_taux_usd"])
        change = centime(max(montant * D(F["change"]["taux"]), D(F["change"]["min_usd"]) * usd))
    timbre = centime(montant * D(F["timbre"]["suisse" if monnaie == "CHF" and marche == "six" else "etranger"]))
    return montant, commission, change, timbre


def situation(journal):
    """Rejoue le journal : liquidités et positions de chaque portefeuille, ordres en attente."""
    s = {p: {"liquidites": D(0), "positions": {}, "frais": D(0)} for p in PORTEFEUILLES}
    ordres, clos = {}, set()
    for l in journal:
        t = l["type"]
        if t == "depot":
            s[l["portefeuille"]]["liquidites"] += D(l["montant_chf"])
        elif t == "ordre":
            ordres[l["id"]] = l
        elif t == "rejet":
            clos.add(l["ordre"])
        elif t == "execution":
            clos.add(l["ordre"])
            o, pf = ordres[l["ordre"]], s[ordres[l["ordre"]]["portefeuille"]]
            signe = 1 if o["sens"] == "achat" else -1
            pos = pf["positions"].setdefault(o["titre"], {"nom": o["nom"], "quantite": 0})
            pos["quantite"] += signe * o["quantite"]
            if pos["quantite"] == 0:
                del pf["positions"][o["titre"]]
            pf["liquidites"] -= D(l["total_chf"]) if signe == 1 else -D(l["net_chf"])
            pf["frais"] += D(l["commission_chf"]) + D(l["frais_change_chf"]) + D(l["timbre_chf"])
        elif t == "dividende":
            s[l["portefeuille"]]["liquidites"] += D(l["net_chf"])
    return s, [o for i, o in ordres.items() if i not in clos]


def charger_releve(chemin, F):
    r = json.loads(Path(chemin).read_text())
    if not r.get("change_en_chf"):
        raise Refus("relevé sans taux de change : aucune opération possible")
    F["_taux_usd"] = r["change_en_chf"]["USD"]
    return r, {t["id"]: t for t in r["titres"]}


# ---------- commandes ----------

def cmd_init(a, F):
    if lire_journal(a.dossier):
        raise Refus("le journal existe déjà : on ne repart jamais de zéro sur un journal existant")
    for p in PORTEFEUILLES:
        ajouter(a.dossier, {"type": "depot", "portefeuille": p, "date": a.date, "montant_chf": str(centime(D(a.capital)))})
    print(f"Départ : CHF {a.capital} fictifs dans chaque portefeuille ({', '.join(PORTEFEUILLES)}).")


def cmd_ordre(a, F):
    verifier(a.dossier)
    journal = lire_journal(a.dossier)
    if not journal:
        raise Refus("journal vide : lancer d'abord « init »")
    if a.quantite <= 0:
        raise Refus("la quantité doit être un nombre entier positif")
    if len(a.justification.strip()) < 20:
        raise Refus("justification trop courte : chaque ordre doit être justifié par écrit")
    date.fromisoformat(a.date_decision)
    n = sum(1 for l in journal if l["type"] == "ordre") + 1
    l = ajouter(a.dossier, {"type": "ordre", "id": f"O-{n:04d}", "portefeuille": a.portefeuille, "sens": a.sens,
                            "titre": a.titre, "nom": a.nom, "quantite": a.quantite,
                            "date_decision": a.date_decision, "justification": a.justification.strip()})
    print(f"Ordre {l['id']} enregistré : {a.sens} {a.quantite} × {a.nom}, exécution au prochain prix d'ouverture.")


def cmd_executer(a, F):
    verifier(a.dossier)
    releve, prix = charger_releve(a.releve, F)
    _, attente = situation(lire_journal(a.dossier))
    jour_releve = date.fromisoformat(releve["releve_utc"][:10])
    for o in sorted(attente, key=lambda o: (o["sens"] != "vente", o["id"])):  # les ventes d'abord
        s, _ = situation(lire_journal(a.dossier))
        pf, p = s[o["portefeuille"]], prix.get(o["titre"])
        decision = date.fromisoformat(o["date_decision"])

        def rejet(raison):
            ajouter(a.dossier, {"type": "rejet", "ordre": o["id"], "raison": raison, "releve": Path(a.releve).name})
            print(f"{o['id']} REJETÉ : {raison}")

        if not p or not p["utilisable"] or p["date_cours"] < decision.strftime("%Y%m%d"):
            if (jour_releve - decision).days > EXPIRATION_JOURS:
                rejet(f"aucun prix d'ouverture utilisable dans les {EXPIRATION_JOURS} jours après la décision")
            else:
                print(f"{o['id']} en attente : pas encore de prix d'ouverture utilisable après le {o['date_decision']}")
            continue
        taux = D(releve["change_en_chf"][p["monnaie"]])
        marche = "six" if p["source"].startswith("SIX") else "us"
        montant, commission, change, timbre = frais_ordre(marche, o["quantite"], p["ouverture"], p["monnaie"], taux, F)
        frais = commission + change + timbre
        if o["sens"] == "vente":
            if pf["positions"].get(o["titre"], {"quantite": 0})["quantite"] < o["quantite"]:
                rejet("vente à découvert interdite : quantité détenue insuffisante")
                continue
            montants = {"net_chf": str(montant - frais)}
        else:
            if montant + frais > pf["liquidites"]:
                rejet(f"liquidités insuffisantes (CHF {pf['liquidites']} disponibles, CHF {montant + frais} nécessaires) : pas d'effet de levier")
                continue
            montants = {"total_chf": str(montant + frais)}
        ajouter(a.dossier, {"type": "execution", "ordre": o["id"], "date_cours": p["date_cours"],
                            "prix": p["ouverture"], "monnaie": p["monnaie"], "taux_chf": str(taux),
                            "date_taux": releve["change_en_chf"]["date"], "montant_chf": str(montant),
                            "commission_chf": str(commission), "frais_change_chf": str(change),
                            "timbre_chf": str(timbre), **montants,
                            "source_prix": p["source"], "releve": Path(a.releve).name})
        print(f"{o['id']} EXÉCUTÉ : {o['sens']} {o['quantite']} × {o['nom']} à {p['ouverture']} {p['monnaie']}, "
              f"montant CHF {montant}, frais CHF {frais}")


def cmd_etat(a, F):
    verifier(a.dossier)
    releve, prix = charger_releve(a.releve, F)
    journal = lire_journal(a.dossier)
    s, attente = situation(journal)
    depart = {p: sum(D(l["montant_chf"]) for l in journal if l["type"] == "depot" and l["portefeuille"] == p) for p in PORTEFEUILLES}
    etat = {"releve": Path(a.releve).name, "releve_utc": releve["releve_utc"], "ordres_en_attente": len(attente)}
    for nom, pf in s.items():
        lignes, total = [], pf["liquidites"]
        for titre, pos in sorted(pf["positions"].items()):
            p = prix.get(titre)
            if not p:
                raise Refus(f"{pos['nom']} est en portefeuille mais absent du relevé : valorisation impossible")
            v = centime(D(pos["quantite"]) * D(p["cloture"]) * D(releve["change_en_chf"][p["monnaie"]]))
            total += v
            lignes.append({"titre": titre, "nom": pos["nom"], "quantite": pos["quantite"], "cloture": p["cloture"],
                           "monnaie": p["monnaie"], "date_cours": p["date_cours"], "valeur_chf": str(v),
                           "prix_douteux": not p["utilisable"]})
        etat[nom] = {"valeur_chf": str(total), "liquidites_chf": str(pf["liquidites"]), "frais_cumules_chf": str(pf["frais"]),
                     "performance_pct": str((total / depart[nom] * 100 - 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                     "positions": lignes}
    etat["ecart_points"] = str(D(etat["agents"]["performance_pct"]) - D(etat["reference"]["performance_pct"]))
    dossier = Path(a.dossier)
    (dossier / "etat.json").write_text(json.dumps(etat, ensure_ascii=False, indent=2) + "\n")
    perf, jour = dossier / "performance.csv", releve["releve_utc"][:10]
    deja = perf.read_text().splitlines() if perf.exists() else ["date,valeur_agents_chf,valeur_reference_chf,ecart_points"]
    if any(l.startswith(jour + ",") for l in deja):
        print(f"Performance du {jour} déjà notée : ligne non réécrite.")
    else:
        deja.append(f"{jour},{etat['agents']['valeur_chf']},{etat['reference']['valeur_chf']},{etat['ecart_points']}")
        perf.write_text("\n".join(deja) + "\n")
    for nom in PORTEFEUILLES:
        e = etat[nom]
        print(f"{nom:10} valeur CHF {e['valeur_chf']:>10}  ({e['performance_pct']} %)  liquidités CHF {e['liquidites_chf']}  frais cumulés CHF {e['frais_cumules_chf']}")
    print(f"Écart agents − référence : {etat['ecart_points']} point(s)")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Comptabilité du portefeuille fictif")
    ap.add_argument("--dossier", default="donnees")
    ap.add_argument("--frais", default="outils/frais.json")
    sp = ap.add_subparsers(dest="commande", required=True)
    p = sp.add_parser("init"); p.add_argument("--capital", required=True); p.add_argument("--date", required=True)
    p = sp.add_parser("ordre")
    p.add_argument("--portefeuille", choices=PORTEFEUILLES, required=True)
    p.add_argument("--sens", choices=("achat", "vente"), required=True)
    p.add_argument("--titre", required=True); p.add_argument("--nom", required=True)
    p.add_argument("--quantite", type=int, required=True)
    p.add_argument("--date-decision", required=True); p.add_argument("--justification", required=True)
    for c in ("executer", "etat"):
        p = sp.add_parser(c); p.add_argument("releve")
    sp.add_parser("verifier")
    a = ap.parse_args(argv)
    F = json.loads(Path(a.frais).read_text())
    try:
        if a.commande == "verifier":
            print(f"Journal intact : {verifier(a.dossier)} ligne(s) contrôlée(s).")
        else:
            {"init": cmd_init, "ordre": cmd_ordre, "executer": cmd_executer, "etat": cmd_etat}[a.commande](a, F)
    except Refus as e:
        sys.exit(f"REFUS : {e}")


if __name__ == "__main__":
    main()
