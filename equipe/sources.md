# Sources d'information

État au 22.11.2026. Les agents trouvent les nouvelles par la recherche web, puis **ouvrent** l'article ou la page officielle quand le site est lisible.

**Comment ouvrir une page** : `python3 outils/lire.py ADRESSE` (affiche le texte de la page). C'est le seul moyen qui fonctionne : l'outil de lecture web habituel des agents ne passe pas par le réseau autorisé. Si le programme répond « LECTURE IMPOSSIBLE », on n'insiste pas.

**Résultats et presse des actions américaines** : le fichier du jour dans `<dossier>/entreprises/` (créé par `outils/entreprises.py`) donne, pour chaque action américaine suivie, les 4 derniers résultats trimestriels (attendu, publié, surprise en %), la prochaine date de résultats et les titres de presse des 3 derniers jours. Les chiffres de résultats de ce fichier sont des **faits forts**. Les titres de presse sont des **faits faibles**.

## Sites que les agents peuvent ouvrir et lire (testés)
| Site | Sert à | Horizon |
|---|---|---|
| www.snb.ch | Décisions et calendrier de la BNS, discours | moyen et long |
| www.federalreserve.gov | Calendrier et communiqués de la Fed, projections | moyen et long |
| www.ecb.europa.eu | Calendrier et décisions de la BCE | moyen et long |
| www.bea.gov | Inflation PCE, croissance américaine, calendrier des publications | moyen |
| www.cash.ch | Bourse suisse au jour le jour, entreprises du SMI | court |
| www.swissinfo.ch | Économie et politique suisses | court et moyen |
| www.rts.ch | Économie suisse et internationale, en français | court |
| www.allnews.ch | Actualité financière suisse, analyses de gérants | court et moyen |
| www.six-group.com | Cours officiels de la bourse suisse | court |

## Sites qu'on ne peut pas ouvrir
- CNBC, BLS (emploi et inflation américains), FMI, OCDE, SEC : ces sites refusent les lecteurs automatiques. On ne contourne pas ce refus.
- AP, BBC, Guardian, Reuters : le service d'environnement cloud a refusé leur ajout (22.11.2026).
Leurs informations ne sont accessibles que par les extraits de la recherche web.

## Tout le reste
Seulement des extraits de recherche. Un fait connu par un extrait seul est marqué « extrait seulement ».

## Règle de confiance
- **Fait fort** : lu dans l'article ouvert ou sur une page officielle. Il peut fonder une décision.
- **Fait faible** : extrait seulement. Il ne peut pas, à lui seul, fonder un ordre ; il faut un deuxième appui, dont au moins un fait fort.
