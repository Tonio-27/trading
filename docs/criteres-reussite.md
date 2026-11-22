# Critères de réussite et protocole de test

## 1. Essai d'une semaine (avant le départ du compteur)

| Critère | Mesure | Seuil |
|---|---|---|
| Fiabilité de la routine | Routines terminées sans erreur | 5 sur 5 |
| Fiabilité des prix | Écart entre les 2 sources pour chaque prix utilisé | Moins de 0,5 % ; sinon pas d'opération sur ce titre ce jour-là |
| Justesse de la comptabilité | Recalcul à la main de toutes les opérations de la semaine | Juste au centime |
| Coût | Quota de l'abonnement consommé par lancement | Mesuré et accepté par Antoine |

## 2. Objectif à 6 mois (frais et dividendes compris, tout en CHF)

| Résultat | Verdict |
|---|---|
| Au moins 2 points au-dessus de la référence (sans plafond) | Objectif atteint ; le passage en argent réel peut être étudié |
| Moins de 2 points au-dessus, ou en dessous | Pas d'arrêt : analyse des causes, correction de la méthode, nouvelle période de 6 mois |

- Entretien intermédiaire à 3 mois : avertissement si plus de 5 points de retard.
- Argent réel (D-13, D-35, D-56) : seulement si les quatre conditions sont réunies —
  1. 6 mois consécutifs à +2 points avec une méthode stable ;
  2. au moins 20 prévisions notées, avec une note moyenne meilleure que le hasard (note de Brier inférieure à 0.67) ;
  3. règles respectées : aucune retouche du journal, aucun ordre sans dossier complet ;
  4. chaque ordre réel validé par Antoine.
  Raison : à 6 mois, le résultat seul doit trop à la chance (voir `docs/audit-objectif.md`).

## 3. Protocole

- La référence est achetée fictivement le jour du départ, avec les mêmes frais, et n'est plus touchée.
- Exécution fictive au prix d'ouverture suivant la décision.
- Chaque prix est noté avec sa source et son heure.
- Rien n'est recalculé après coup ; une erreur se corrige par une nouvelle ligne datée.
- Rappel : un résultat trop parfait doit être vérifié, pas célébré. Un écart de plus de 10 points sur la référence déclenche un contrôle complet des prix et des calculs.
