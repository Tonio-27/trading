#!/usr/bin/env python3
"""Prépare les données du tableau de bord à partir du journal, de l'état et de la performance.
Usage : python3 outils/tableau.py DOSSIER   → écrit DOSSIER/tableau.json (fichier dérivé, recréé à chaque fois)."""
import csv, json, sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import compta

d = Path(sys.argv[1])
config = json.loads((Path(__file__).parent.parent / "equipe/config.json").read_text())
etat = json.loads((d / "etat.json").read_text())
journal = compta.lire_journal(d)
capital = sum(Decimal(l["montant_chf"]) for l in journal if l["type"] == "depot" and l["portefeuille"] == "agents")  # le capital vient du journal
pct = lambda v: float((Decimal(v) / capital * 100 - 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

# Portefeuille « deux poches » : une part confiée aux agents, le reste dans l'ETF de référence, sans rééquilibrage.
# Il se déduit des deux autres : aucun ordre, aucune ligne de journal en plus.
part = Decimal(str(config.get("deux_poches_part_agents", 0.5)))
mixte = lambda a, r: (Decimal(a) * part + Decimal(r) * (1 - part)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

performance = []
with open(d / "performance.csv") as h:
    for r in csv.DictReader(h):
        performance.append({"date": r["date_cours"], "agents_pct": pct(r["valeur_agents_chf"]), "reference_pct": pct(r["valeur_reference_chf"]),
                            "mixte_pct": pct(mixte(r["valeur_agents_chf"], r["valeur_reference_chf"])),
                            "agents_chf": float(r["valeur_agents_chf"]), "reference_chf": float(r["valeur_reference_chf"])})

total = Decimal(etat["agents"]["valeur_chf"])
positions = [{"nom": p["nom"], "quantite": p["quantite"], "cours": p["cloture"], "monnaie": p["monnaie"],
              "valeur_chf": float(p["valeur_chf"]),
              "poids_pct": float((Decimal(p["valeur_chf"]) / total * 100).quantize(Decimal("0.1")))}
             for p in etat["agents"]["positions"]]
positions.append({"nom": "Liquidités", "quantite": None, "cours": None, "monnaie": "CHF",
                  "valeur_chf": float(etat["agents"]["liquidites_chf"]),
                  "poids_pct": float((Decimal(etat["agents"]["liquidites_chf"]) / total * 100).quantize(Decimal("0.1")))})
positions.sort(key=lambda p: -p["valeur_chf"])

ordres = {l["id"]: l for l in journal if l["type"] == "ordre" and l["portefeuille"] == "agents"}
suites = {l["ordre"]: l for l in journal if l["type"] in ("execution", "rejet")}
operations = []
for i, o in ordres.items():
    s = suites.get(i)
    ligne = {"ordre": i, "date_decision": o["date_decision"], "sens": o["sens"], "nom": o["nom"], "quantite": o["quantite"],
             "statut": "en attente", "date_execution": None, "prix": None, "monnaie": None, "montant_chf": None, "frais_chf": None,
             "justification": o["justification"]}
    if s and s["type"] == "execution":
        dc = s["date_cours"]
        frais = Decimal(s["commission_chf"]) + Decimal(s["frais_change_chf"]) + Decimal(s["timbre_chf"])
        ligne.update(statut="exécuté", quantite=s.get("quantite", o["quantite"]), date_execution=f"{dc[:4]}-{dc[4:6]}-{dc[6:]}", prix=s["prix"], monnaie=s["monnaie"],
                     montant_chf=float(s["montant_chf"]), frais_chf=float(frais))
    elif s:
        ligne.update(statut="rejeté", justification=f"Rejeté : {s['raison']}")
    operations.append(ligne)
operations.reverse()

routines = {"ok": 0, "panne": 0}
f = d / "routines.csv"
if f.exists():
    with open(f) as h:
        for r in csv.DictReader(h):
            routines[r["statut"]] += 1

resume = [{
    "date": etat["date_cours"], "phase": config["phase"], "debut_compteur": config.get("debut_compteur"),
    "valeur_agents_chf": float(etat["agents"]["valeur_chf"]), "perf_agents_pct": float(etat["agents"]["performance_pct"]),
    "valeur_reference_chf": float(etat["reference"]["valeur_chf"]), "perf_reference_pct": float(etat["reference"]["performance_pct"]),
    "valeur_mixte_chf": float(mixte(etat["agents"]["valeur_chf"], etat["reference"]["valeur_chf"])),
    "perf_mixte_pct": pct(mixte(etat["agents"]["valeur_chf"], etat["reference"]["valeur_chf"])),
    "part_agents_pct": float(part * 100),
    "ecart_points": float(etat["ecart_points"]), "objectif_points": 2.0,
    "liquidites_chf": float(etat["agents"]["liquidites_chf"]), "frais_cumules_chf": float(etat["agents"]["frais_cumules_chf"]),
    "positions": len(etat["agents"]["positions"]), "ordres_en_attente": sum(1 for o in operations if o["statut"] == "en attente"),
    "operations_executees": sum(1 for o in operations if o["statut"] == "exécuté"),
    "routines_reussies": routines["ok"], "routines_en_panne": routines["panne"],
}]
(d / "tableau.json").write_text(json.dumps({"resume": resume, "performance": performance, "positions": positions,
                                           "operations": operations}, ensure_ascii=False, indent=1) + "\n")
print(f"Tableau de bord : données écrites dans {d / 'tableau.json'} ({len(performance)} jour(s), {len(positions)} ligne(s), {len(operations)} opération(s))")
