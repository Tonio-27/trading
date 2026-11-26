#!/usr/bin/env python3
"""D'où vient l'écart entre les agents et la référence ?

Chaque soir, « noter » ajoute une ligne (valeur et part investie des deux portefeuilles). « rapport » sépare ensuite l'écart en deux :
  - effet de la part investie : ce que les agents ont gagné ou perdu en étant plus ou moins investis que la référence
    (par exemple en restant en liquidités pendant que le marché monte ou baisse) ;
  - effet du choix des titres et des frais : ce que la partie investie des agents a fait de mieux ou de moins bien que
    le même montant placé dans l'ETF de référence, frais compris.
Calcul jour par jour : écart du jour = (part agents − part référence) × variation de l'ETF + (variation agents − part agents × variation de l'ETF).
Les parts sont celles de la veille au soir. La somme des jours diffère un peu de l'écart total (effet de composition) : c'est le « reste ».

  noter DOSSIER      lit DOSSIER/etat.json et ajoute une ligne à DOSSIER/origine.csv (une ligne par jour de cours)
  rapport DOSSIER [--depuis AAAA-MM-JJ]
"""
import csv, json, sys
from decimal import Decimal
from pathlib import Path

ENTETE = ["date_cours", "valeur_agents_chf", "valeur_reference_chf", "part_investie_agents", "part_investie_reference"]


def decomposer(lignes):
    """`lignes` : dictionnaires triés par date. Rend (écart total, effet part investie, effet titres et frais, reste), en points."""
    D = Decimal
    part = titres = D(0)
    for hier, jour in zip(lignes, lignes[1:]):
        ra = D(jour["valeur_agents_chf"]) / D(hier["valeur_agents_chf"]) - 1
        rr = D(jour["valeur_reference_chf"]) / D(hier["valeur_reference_chf"]) - 1
        wa, wr = D(hier["part_investie_agents"]), D(hier["part_investie_reference"])
        etf = rr / wr if wr > 0 else D(0)          # variation de l'ETF seul, sans les liquidités de la référence
        part += (wa - wr) * etf
        titres += ra - wa * etf
    total = (D(lignes[-1]["valeur_agents_chf"]) / D(lignes[0]["valeur_agents_chf"])
             - D(lignes[-1]["valeur_reference_chf"]) / D(lignes[0]["valeur_reference_chf"]))
    return tuple(round(float(x * 100), 2) for x in (total, part, titres, total - part - titres))


def lire(dossier):
    f = Path(dossier) / "origine.csv"
    return list(csv.DictReader(open(f))) if f.exists() else []


def cmd_noter(dossier):
    e = json.loads((Path(dossier) / "etat.json").read_text())
    investie = lambda p: (1 - Decimal(p["liquidites_chf"]) / Decimal(p["valeur_chf"])).quantize(Decimal("0.0001"))
    deja = lire(dossier)
    if any(l["date_cours"] == e["date_cours"] for l in deja):
        print(f"Origine : cours du {e['date_cours']} déjà notés.")
        return
    f = Path(dossier) / "origine.csv"
    nouveau = not f.exists()
    with open(f, "a", newline="") as h:
        w = csv.writer(h)
        if nouveau:
            w.writerow(ENTETE)
        w.writerow([e["date_cours"], e["agents"]["valeur_chf"], e["reference"]["valeur_chf"], investie(e["agents"]), investie(e["reference"])])
    print(f"Origine : cours du {e['date_cours']} notés (agents investis à {float(investie(e['agents'])) * 100:.0f} %).")


def cmd_rapport(dossier, depuis=None):
    lignes = [l for l in lire(dossier) if not depuis or l["date_cours"] >= depuis]
    if len(lignes) < 2:
        print("Origine du résultat : pas encore assez de jours notés (il en faut au moins 2).")
        return
    total, part, titres, reste = decomposer(lignes)
    s = lambda x: f"{x:+.2f}"
    print(f"Origine de l'écart entre les agents et la référence, du {lignes[0]['date_cours']} au {lignes[-1]['date_cours']} :")
    print(f"  écart total                         : {s(total)} point(s)")
    print(f"  dont effet de la part investie      : {s(part)} point(s)")
    print(f"  dont choix des titres et frais      : {s(titres)} point(s)")
    print(f"  reste de calcul                     : {s(reste)} point(s)")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "noter":
        cmd_noter(sys.argv[2])
    elif len(sys.argv) >= 3 and sys.argv[1] == "rapport":
        cmd_rapport(sys.argv[2], sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--depuis" else None)
    else:
        sys.exit(__doc__)
