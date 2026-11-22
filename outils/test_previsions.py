#!/usr/bin/env python3
"""Test de la notation des prévisions, calculé à la main.

Prévision sur Nestlé au cours de CHF 85.55 (relevé d'exemple, cours du 20.11.2026), horizon 30 jours,
seuils +4 % / −4 %, probabilités 40 / 35 / 25.
Un mois plus tard, cours de CHF 90.00 : 90 / 85.55 = +5.20 % → scénario favorable.
Note de Brier : (0.40 − 1)² + 0.35² + 0.25² = 0.36 + 0.1225 + 0.0625 = 0.5450
"""
import json, shutil, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import compta, previsions

RELEVE = Path(__file__).parent.parent / "docs/donnees-test/releve-exemple.json"
d = Path(tempfile.mkdtemp())
echecs = []


def attendu(quoi, obtenu, voulu):
    ok = str(obtenu) == str(voulu)
    print(("OK    " if ok else "ÉCHEC ") + f"{quoi} : {obtenu}" + ("" if ok else f" (attendu {voulu})"))
    if not ok:
        echecs.append(quoi)


def lancer(*args):
    try:
        previsions.main(list(args))
    except SystemExit as e:
        return str(e)


base = ["--titre", "CH0038863350", "--nom", "Nestlé", "--horizon-jours", "30", "--seuil-haut", "4", "--seuil-bas", "-4",
        "--p-favorable", "40", "--p-neutre", "35", "--p-defavorable", "25", "--decision", "ecartee"]
compta.maintenant = lambda: datetime(2026, 11, 22, 17, 0, tzinfo=timezone.utc)
lancer("ajouter", str(d), str(RELEVE), *base)
pr = previsions.lire(d / "previsions.jsonl")[0]
attendu("prix de départ pris dans le relevé", pr["prix_depart"], 85.55)
attendu("échéance à 30 jours", pr["echeance"], "20261220")
attendu("doublon refusé", "REFUS" in (lancer("ajouter", str(d), str(RELEVE), *base) or ""), True)
attendu("probabilités ne faisant pas 100 refusées", "REFUS" in (lancer("ajouter", str(d), str(RELEVE), *base[:-6], "--p-neutre", "50", "--p-defavorable", "25", "--decision", "ecartee") or ""), True)
lancer("noter", str(d), str(RELEVE))
attendu("pas de note avant l'échéance", len(previsions.lire(d / "previsions-notes.jsonl")), 0)
# Un mois plus tard : même relevé, mais daté du 21.12 avec Nestlé à 90.00
r = json.loads(RELEVE.read_text())
r["releve_utc"] = "2026-12-21T06:45:00Z"
for t in r["titres"]:
    t["date_cours"] = "20261218" if t["id"] != "CH0038863350" else "20261221"
    if t["id"] == "CH0038863350":
        t["cloture"] = 90.0
(d / "plus-tard.json").write_text(json.dumps(r))
compta.maintenant = lambda: datetime(2026, 12, 21, 7, 0, tzinfo=timezone.utc)
lancer("noter", str(d), str(d / "plus-tard.json"))
n = previsions.lire(d / "previsions-notes.jsonl")[0]
attendu("variation réelle", n["variation_pct"], "5.20")
attendu("scénario arrivé", n["arrive"], "favorable")
attendu("note de Brier", n["brier"], "0.5450")
lancer("noter", str(d), str(d / "plus-tard.json"))
attendu("une prévision n'est notée qu'une fois", len(previsions.lire(d / "previsions-notes.jsonl")), 1)
shutil.rmtree(d)
print(f"\n{'TOUT EST JUSTE' if not echecs else str(len(echecs)) + ' ÉCHEC(S)'}")
sys.exit(1 if echecs else 0)
