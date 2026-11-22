# Audit de faisabilité de l'objectif (22.11.2026)

Question : l'outil peut-il atteindre l'objectif, battre l'ETF de référence d'au moins 2 points en 6 mois, frais compris ?
Chiffres produits par `python3 outils/audit_objectif.py` (modèle statistique simple, hypothèses écrites en tête du programme).
Ce sont des ordres de grandeur, pas des prévisions. Aucun essai sur le passé n'est possible honnêtement : les agents connaissent déjà l'histoire des marchés.

## Constats

1. **L'outil lui-même est apte.** Prix, comptabilité, règles et journal ont été relus et testés ; rien dans la mécanique n'empêche d'atteindre l'objectif.
2. **Les frais pèsent environ 1 point sur 6 mois** à 4 ordres par mois (0.45 point à 2 ordres, 1.35 point à 6). Pour finir à +2 points nets, il faut donc environ +3 points bruts. Un ordre de CHF 500 à la bourse suisse coûte 1 % à lui seul.
3. **L'objectif est atteignable, mais surtout par chance.** Sans aucun talent, les agents ont 15 à 37 % de chances de réussir, selon qu'ils s'éloignent peu ou beaucoup de la référence. Avec un bon talent (5 % d'avance par an, niveau de très bons professionnels), la chance de réussir n'est que d'environ 45 à 50 %.
4. **Un seul résultat à 6 mois ne prouve rien.** Il faudrait 2 à 7 ans de résultats pour distinguer un vrai talent de la chance. Un succès à 6 mois peut être un coup de chance, un échec peut frapper une bonne méthode.
5. **Plus les agents s'éloignent de la référence, plus le résultat est un tirage au sort.** Rester longtemps en liquidités ou concentrer sur 2 ou 3 titres augmente à la fois la chance de réussir et le risque de finir loin derrière (1 chance sur 10 de finir à plus de 8 à 12 points derrière).

## Recommandations (décisions d'Antoine)

- **R1 — Juger sur plus que le résultat.** Pour décider d'engager de l'argent réel : le résultat à 6 mois **et** la qualité des prévisions (au moins 20 prévisions notées, note moyenne meilleure que le hasard) **et** le respect des règles. La notation des prévisions donne une preuve bien plus rapide que la performance.
- **R2 — Discipline de frais.** Ordre minimal de CHF 1'500 et cible de 3 ordres par mois au plus, sauf urgence justifiée : handicap ramené à environ 0.6 point.
- **R3 — Cœur et satellites.** Placer par défaut une part du portefeuille (par exemple 60 %) dans l'ETF de référence et réserver le reste aux idées des agents. Le résultat reflète alors la qualité des idées, pas un pari sur la direction du marché ; le risque de finir loin derrière est divisé environ par deux. Contrepartie : moins de chances de gros écart, dans les deux sens.
