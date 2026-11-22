#!/usr/bin/env python3
"""Audit de faisabilité : peut-on battre la référence de 2 points en 6 mois, et qu'est-ce que cela prouverait ?

Modèle simple et classique : l'écart entre le portefeuille et la référence sur une période suit une loi normale.
- « avance annuelle » : ce que le talent des agents rapporte en plus par an, avant frais (hypothèse).
- « écart de suivi » : de combien le portefeuille s'éloigne habituellement de la référence sur un an, en plus ou en
  moins (hypothèse : 4 % pour un portefeuille proche de l'indice, 8 % pour une dizaine d'actions, 12 % pour un
  portefeuille très concentré ou souvent en liquidités).
Les frais viennent de outils/frais.json. Ce sont des ordres de grandeur, pas des prévisions.
"""
import json
from pathlib import Path
from statistics import NormalDist

F = json.loads((Path(__file__).parent / "frais.json").read_text())
USD = 0.84           # ordre de grandeur du dollar en francs (relevé du 22.11.2026)
CAPITAL, OBJECTIF, DUREE = 10000, 2.0, 0.5   # CHF, points, années
N = NormalDist()


def frais_ordre(montant, marche):
    if marche == "suisse":
        return max(montant * float(F["six"]["taux"]), float(F["six"]["min_chf"]))
    return float(F["us"]["min_usd"]) * USD + max(montant * float(F["change"]["taux"]), float(F["change"]["min_usd"]) * USD)


print("1. CE QUE COÛTENT LES FRAIS (par ordre, puis sur 6 mois, moitié Suisse moitié États-Unis)")
for montant in (500, 1000, 2000):
    s, u = frais_ordre(montant, "suisse"), frais_ordre(montant, "us")
    print(f"   ordre de CHF {montant:>5} : Suisse CHF {s:.2f} ({s / montant * 100:.2f} %), États-Unis CHF {u:.2f} ({u / montant * 100:.2f} %)")
moyen = (frais_ordre(1500, "suisse") + frais_ordre(1500, "us")) / 2
couts = {}
for par_mois in (2, 4, 6):
    total = par_mois * 6 * moyen
    couts[par_mois] = total / CAPITAL * 100
    print(f"   {par_mois} ordres par mois : CHF {total:.0f} en 6 mois, soit {couts[par_mois]:.2f} point(s) de handicap")

print("\n2. CHANCE DE RÉUSSIR (+2 points nets en 6 mois) selon le talent et l'audace, avec 4 ordres par mois")
print("   avance annuelle due au talent →      0 %     2 %     5 %    10 %")
for suivi in (4, 8, 12):
    ligne = []
    for avance in (0, 2, 5, 10):
        moyenne = avance * DUREE - couts[4]
        ecart = suivi * DUREE ** 0.5
        ligne.append(f"{(1 - N.cdf((OBJECTIF - moyenne) / ecart)) * 100:5.0f} %")
    print(f"   écart de suivi {suivi:>2} % par an :        " + "  ".join(ligne))

print("\n3. RISQUE DE FINIR DERRIÈRE LA RÉFÉRENCE en 6 mois, sans aucun talent (avance 0 %)")
for suivi in (4, 8, 12):
    ecart = suivi * DUREE ** 0.5
    print(f"   écart de suivi {suivi:>2} % : {N.cdf((0 + couts[4]) / ecart) * 100:.0f} % de risque de finir derrière ; "
          f"1 chance sur 10 de finir à plus de {abs(N.inv_cdf(0.10) * ecart - couts[4]):.1f} points derrière")

print("\n4. COMBIEN DE TEMPS POUR DISTINGUER LE TALENT DE LA CHANCE (certitude de 95 %)")
for avance, suivi in ((2, 8), (5, 8), (10, 8), (5, 4)):
    print(f"   avance {avance:>2} % par an, écart de suivi {suivi} % : environ {(1.645 / (avance / suivi)) ** 2:.1f} an(s) de résultats")

print("\n5. TALENT NÉCESSAIRE pour avoir 2 chances sur 3 de réussir en 6 mois (4 ordres par mois)")
for suivi in (4, 8, 12):
    ecart = suivi * DUREE ** 0.5
    besoin = (OBJECTIF + couts[4] - N.inv_cdf(1 / 3) * ecart) / DUREE
    print(f"   écart de suivi {suivi:>2} % : il faudrait une avance d'environ {besoin:.0f} % par an avant frais")
