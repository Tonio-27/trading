#!/usr/bin/env python3
"""Tests des ordres à cours limité, du financement par vente d'ETF et de l'achat maximal, calculés à la main.

Relevé d'exemple (cours du 20.11.2026) : ETF MSCI World ouverture USD 136.50, Nestlé CHF 85.00, Zurich CHF 640.60 ; 1 USD = CHF 0.839217.
1. Agents : achat --maximum de l'ETF : 87 parts (comme la référence) → total CHF 9'972.80, liquidités 27.20.
2. Nestlé 10, limite CHF 84 : ouverture 85 > 84 → attend ; 6 jours plus tard toujours 85 → rejeté.
3. Zurich 1, limite CHF 650, financé par l'ETF : coût 640.60 + 5.00 = 645.60 ; il manque 645.60 − 27.20 = 618.40.
   Vente de 5 parts : 682.50 USD = 572.77 − 6.68 = 566.09 (trop peu) ; de 6 parts : 819 USD = 687.32 − 6.68 = 680.64 (suffit).
   → vente automatique de 6 parts ; liquidités 27.20 + 680.64 − 645.60 = 62.24 ; restent 81 parts.
"""
import json, shutil, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import compta

RELEVE = Path(__file__).parent.parent / "docs/donnees-test/releve-exemple.json"
FRAIS = {"six": {"taux": "0.0005", "min_chf": "5.00"}, "us": {"par_action_usd": "0.005", "min_usd": "1.00", "max_part": "0.01"},
         "change": {"taux": "0.00002", "min_usd": "2.00"}, "timbre": {"suisse": "0", "etranger": "0"}}
J = "Opération d'exemple pour le test des ordres."
d = tempfile.mkdtemp(); f = str(Path(d) / "frais.json"); Path(f).write_text(json.dumps(FRAIS))
echecs = []


def attendu(quoi, obtenu, voulu):
    ok = str(obtenu) == str(voulu)
    print(("OK    " if ok else "ÉCHEC ") + f"{quoi} : {obtenu}" + ("" if ok else f" (attendu {voulu})"))
    if not ok:
        echecs.append(quoi)


def lancer(*args):
    try:
        compta.main(["--dossier", d, "--frais", f, *args])
    except SystemExit as e:
        return str(e)


horloge = lambda t: setattr(compta, "maintenant", lambda: t)
ordre = lambda *x: lancer("ordre", "--portefeuille", "agents", "--sens", "achat", "--justification", J, *x)
horloge(datetime(2026, 11, 20, 6, 0, tzinfo=timezone.utc))
lancer("init", "--capital", "10000")
ordre("--titre", "IE00B4L5Y983", "--nom", "ETF MSCI World", "--maximum")
ordre("--titre", "CH0038863350", "--nom", "Nestlé", "--quantite", "10", "--limite", "84")
ordre("--titre", "CH0011075394", "--nom", "Zurich Assurances", "--quantite", "1", "--limite", "650", "--financer-par", "IE00B4L5Y983")
attendu("--maximum refusé sur un autre titre que la référence", "REFUS" in (ordre("--titre", "AAPL", "--nom", "Apple", "--maximum") or ""), True)
horloge(datetime(2026, 11, 22, 17, 0, tzinfo=timezone.utc))
lancer("executer", str(RELEVE))
j = compta.lire_journal(d)
ex = {l["ordre"]: l for l in j if l["type"] == "execution"}
s, attente = compta.situation(j)
attendu("1. achat maximal de l'ETF par les agents", ex["O-0001"]["quantite"], 87)
attendu("2. Nestlé au-dessus de la limite : en attente", [o["id"] for o in attente], ["O-0002"])
attendu("3. vente automatique de 6 parts", [(l["quantite"], l["net_chf"]) for l in j if l["type"] == "execution" and l["ordre"] == "O-0004"], [(6, "680.64")])
attendu("3. Zurich exécuté", ex["O-0003"]["total_chf"], "645.60")
attendu("3. liquidités après financement", s["agents"]["liquidites"], "62.24")
attendu("3. parts d'ETF restantes", s["agents"]["positions"]["IE00B4L5Y983"]["quantite"], 81)
plus_tard = json.loads(RELEVE.read_text())
plus_tard["releve_utc"] = "2026-11-26T21:40:00Z"
for t in plus_tard["titres"]:
    t["date_cours"] = "20261126"
(Path(d) / "plus-tard.json").write_text(json.dumps(plus_tard))
horloge(datetime(2026, 11, 26, 22, 0, tzinfo=timezone.utc))
lancer("executer", str(Path(d) / "plus-tard.json"))
attendu("2. limite non atteinte en 5 jours : rejeté", [l["raison"][:12] for l in compta.lire_journal(d) if l["type"] == "rejet"], ["cours limite"])
shutil.rmtree(d)
print(f"\n{'TOUT EST JUSTE' if not echecs else str(len(echecs)) + ' ÉCHEC(S)'}")
sys.exit(1 if echecs else 0)
