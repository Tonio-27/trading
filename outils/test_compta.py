#!/usr/bin/env python3
"""5 opérations d'exemple, calculées à la main, sur le vrai relevé du 22.11.2026 (cours du 20.11.2026).

Taux du relevé : 1 USD = CHF 0.839217 ; 1 EUR = CHF 0.9223.
Frais du test (figés ici pour que le test reste valable si les tarifs changent) :
bourse suisse 0,05 % min CHF 5 ; US USD 0.005/action min USD 1 max 1 % ; change 0,002 % min USD 2 (= CHF 1.68).

1. Achat 10 Nestlé à l'ouverture CHF 85        : 850.00 + commission 5.00                    = 855.00
2. Achat 3 Apple à USD 352.87                  : 1058.61 USD × 0.839217 = 888.40
                                                 + commission USD 1 = 0.84 + change 1.68      = 890.92
3. Achat 2 ETF Euro Stoxx 50 à EUR 236.05      : 472.10 EUR × 0.9223 = 435.42 + 5.00 + 1.68   = 442.10
4. Vente 5 Nestlé à CHF 85 (le lendemain)      : 425.00 − commission 5.00                     = 420.00 net
5. Référence : achat 87 ETF MSCI World à USD 136.5 : 11875.50 USD × 0.839217 = 9966.12
                                                 + 5.00 (0,05 % = 4.98, minimum 5) + 1.68     = 9972.80
Liquidités agents après 1 à 4 : 10000 − 855.00 − 890.92 − 442.10 + 420.00 = 8231.98
Liquidités référence après 5  : 10000 − 9972.80 = 27.20
Valeur agents à la clôture : 8231.98 + 5 × 85.55 (427.75) + 3 × 342.56 × 0.839217 (862.45)
                             + 2 × 232 × 0.9223 (427.95) = 9950.13  → −0.50 %
Valeur référence : 27.20 + 87 × 134.82 × 0.839217 (9843.46) = 9870.66 → −1.29 %
"""
import json, shutil, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import compta

ICI = Path(__file__).parent
RELEVE = ICI.parent / "docs/donnees-test/releve-exemple.json"
FRAIS = {"six": {"taux": "0.0005", "min_chf": "5.00"}, "us": {"par_action_usd": "0.005", "min_usd": "1.00", "max_part": "0.01"},
         "change": {"taux": "0.00002", "min_usd": "2.00"}, "timbre": {"suisse": "0", "etranger": "0"}}
J = "Opération d'exemple pour le test de la comptabilité."
echecs = []


def attendu(quoi, obtenu, voulu):
    ok = str(obtenu) == str(voulu)
    print(("OK    " if ok else "ÉCHEC ") + f"{quoi} : {obtenu}" + ("" if ok else f" (attendu {voulu})"))
    if not ok:
        echecs.append(quoi)


def lancer(d, f, *args):
    try:
        compta.main(["--dossier", d, "--frais", f, *args])
    except SystemExit as e:
        return str(e)


d = tempfile.mkdtemp()
f = str(Path(d) / "frais.json"); Path(f).write_text(json.dumps(FRAIS))
ordre = lambda pf, sens, titre, nom, q, jour="2026-11-20": lancer(d, f, "ordre", "--portefeuille", pf, "--sens", sens, "--titre", titre,
                                                                 "--nom", nom, "--quantite", str(q), "--date-decision", jour, "--justification", J)
lancer(d, f, "init", "--capital", "10000", "--date", "2026-11-20")
ordre("agents", "achat", "CH0038863350", "Nestlé", 10)
ordre("agents", "achat", "AAPL", "Apple", 3)
ordre("agents", "achat", "IE00B53L3W79", "ETF Euro Stoxx 50", 2)
ordre("reference", "achat", "IE00B4L5Y983", "ETF MSCI World", 87)
lancer(d, f, "executer", str(RELEVE))
ordre("agents", "vente", "CH0038863350", "Nestlé", 5)
ordre("agents", "vente", "AAPL", "Apple", 4)                    # doit être rejeté : vente à découvert
ordre("agents", "achat", "MSFT", "Microsoft", 100)               # doit être rejeté : pas assez de liquidités
ordre("agents", "achat", "CH0012005267", "Novartis", 1, "2026-11-23")  # doit attendre : pas encore d'ouverture après le 23
lancer(d, f, "executer", str(RELEVE))
lancer(d, f, "etat", str(RELEVE))

journal = compta.lire_journal(d)
ex = {l["ordre"]: l for l in journal if l["type"] == "execution"}
rej = {l["ordre"]: l["raison"] for l in journal if l["type"] == "rejet"}
etat = json.loads((Path(d) / "etat.json").read_text())
print()
attendu("1. achat 10 Nestlé, total", ex["O-0001"]["total_chf"], "855.00")
attendu("2. achat 3 Apple, montant", ex["O-0002"]["montant_chf"], "888.40")
attendu("2. achat 3 Apple, total", ex["O-0002"]["total_chf"], "890.92")
attendu("3. achat 2 ETF Euro Stoxx, total", ex["O-0003"]["total_chf"], "442.10")
attendu("4. vente 5 Nestlé, net", ex["O-0005"]["net_chf"], "420.00")
attendu("5. référence 87 ETF MSCI World, total", ex["O-0004"]["total_chf"], "9972.80")
attendu("liquidités agents", etat["agents"]["liquidites_chf"], "8231.98")
attendu("liquidités référence", etat["reference"]["liquidites_chf"], "27.20")
attendu("valeur agents", etat["agents"]["valeur_chf"], "9950.13")
attendu("valeur référence", etat["reference"]["valeur_chf"], "9870.66")
attendu("performance agents %", etat["agents"]["performance_pct"], "-0.50")
attendu("performance référence %", etat["reference"]["performance_pct"], "-1.29")
attendu("vente à découvert rejetée", "découvert" in rej.get("O-0006", ""), True)
attendu("achat sans liquidités rejeté", "levier" in rej.get("O-0007", ""), True)
attendu("ordre du 23.11 laissé en attente", etat["ordres_en_attente"], 1)
attendu("justification trop courte refusée", "REFUS" in (lancer(d, f, "ordre", "--portefeuille", "agents", "--sens", "achat", "--titre", "AAPL",
        "--nom", "Apple", "--quantite", "1", "--date-decision", "2026-11-20", "--justification", "bof") or ""), True)
attendu("second « init » refusé", "REFUS" in (lancer(d, f, "init", "--capital", "10000", "--date", "2026-11-20") or ""), True)
# retouche du journal : doit être détectée
p = Path(d) / "journal.jsonl"
p.write_text(p.read_text().replace('"855.00"', '"755.00"'))
attendu("journal retouché détecté", "retouché" in (lancer(d, f, "verifier") or ""), True)
shutil.rmtree(d)
print(f"\n{'TOUT EST JUSTE' if not echecs else str(len(echecs)) + ' ÉCHEC(S)'}")
sys.exit(1 if echecs else 0)
