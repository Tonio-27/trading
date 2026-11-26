#!/usr/bin/env python3
"""Test de l'origine du résultat, calculé à la main.

Jour 1 → jour 2 : agents en liquidités (part 0), 10000 → 10000. Référence investie à 99 %, 10000 → 9800 (−2 %).
   L'ETF seul a fait −2 / 0.99 = −2.0202 %. Effet part investie = (0 − 0.99) × −2.0202 = +2.00. Effet titres = 0 − 0 = 0.
Jour 2 → jour 3 : agents investis à 50 %, 10000 → 10100 (+1 %). Référence investie à 100 %, 9800 → 9898 (+1 %).
   Effet part investie = (0.5 − 1) × 1 = −0.50. Effet titres = 1 − 0.5 × 1 = +0.50.
Total : part investie +1.50, titres +0.50. Écart réel = 10100/10000 − 9898/10000 = +2.02. Reste = +0.02.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import origine

lignes = [
    {"date_cours": "j1", "valeur_agents_chf": "10000", "valeur_reference_chf": "10000", "part_investie_agents": "0", "part_investie_reference": "0.99"},
    {"date_cours": "j2", "valeur_agents_chf": "10000", "valeur_reference_chf": "9800", "part_investie_agents": "0.5", "part_investie_reference": "1"},
    {"date_cours": "j3", "valeur_agents_chf": "10100", "valeur_reference_chf": "9898", "part_investie_agents": "0.5", "part_investie_reference": "1"},
]
obtenu = origine.decomposer(lignes)
voulu = (2.02, 1.5, 0.5, 0.02)
print(("OK    " if obtenu == voulu else "ÉCHEC ") + f"écart total, part investie, titres et frais, reste : {obtenu}" + ("" if obtenu == voulu else f" (attendu {voulu})"))
print("\nTOUT EST JUSTE" if obtenu == voulu else "\n1 ÉCHEC")
sys.exit(0 if obtenu == voulu else 1)
