# Cadrage — Équipe d'agents de trading (argent fictif)

État : cadrage en cours (blocs 0 à 5 terminés, pas encore de GO).

## Bloc 0 — L'idée brute (22.11.2026)

- Projet personnel d'Antoine, sans lien avec Escaliers Mauron.
- Une équipe de 7 agents Claude Code gère un portefeuille fictif de CHF 10'000 :
  Veilleur, Agenda, Analyste, Gestionnaire de risques, Avocat du diable, Gérant, Contrôleur.
- But : battre sur 6 mois un ETF MSCI World acheté au départ et conservé.
- Motivation : comprendre comment ça fonctionne et, si possible, gagner de l'argent à côté du travail.
- Aucun outil existant aujourd'hui.
- Fonctionnement voulu : routine chaque jour de bourse vers 7 h 45 (Zurich), bilan le vendredi soir,
  prix relevés sur le web avec source et heure, exécution fictive au prix d'ouverture suivant,
  notification seulement en cas d'opération + bilan du vendredi, tableau de bord lisible sur téléphone.
- Fichiers tenus : portefeuille, journal des opérations (avec justification), agenda des événements,
  leçons apprises, performance contre la référence.

## Bloc 1 — Problème et objectif (22.11.2026)

- Critère de réussite : battre la référence sur 6 mois, frais compris. En dessous de l'ETF = échec.
- Suite envisagée : argent réel, CHF 5'000 pour commencer, horizon moyen-long terme (hors V1, décision séparée).
- Frais réels d'un courtier suisse simulés (courtage, timbre fédéral, change) ; dividendes comptés des deux côtés ; tout en CHF.
- Temps d'Antoine : 2 minutes par semaine. Autonomie complète des agents en mode fictif.
- Mises en garde données : 6 mois ne prouvent pas une méthode ; « gros gain » et « risque moyen » sont contradictoires ;
  le coût d'usage quotidien des agents peut dépasser le gain attendu sur CHF 5'000.

## Bloc 2 — Utilisateurs et niveau (22.11.2026)

- Utilisateur unique : Antoine, sur téléphone.
- Niveau N1 (perso), avec rigueur renforcée sur la comptabilité (journal non modifiable, prix sourcés).
- Pas de limite de baisse imposée : les agents gèrent librement (choix d'Antoine ; la recommandation était l'option B, alerte à −15 % et mise à l'abri partielle à −20 %).

## Bloc 3 — Périmètre (22.11.2026)

- V1, 3 fonctions indispensables : routine du matin qui décide et justifie par écrit ; comptabilité honnête
  (portefeuille, frais, journal, performance contre la référence) ; tableau de bord sur téléphone avec notification en cas d'opération.
- Peut attendre : séparation complète en 7 agents (après le prototype).
- Hors projet : ordres réels, connexion à un courtier, crypto, produits dérivés, conseil fiscal, actions de petites entreprises.
- Prototype jetable : routine lancée à la main pendant une semaine, sans automatisation ni tableau de bord.
- Le compteur des 6 mois démarre seulement après validation du prototype.

## Bloc 4 — Données et connexions (22.11.2026)

- Entrées : cours de bourse (source fixe gratuite + deuxième source de contrôle), nouvelles et agenda économique (recherche web).
- Sorties : portefeuille, journal des opérations, agenda, leçons apprises, performance contre la référence, tableau de bord, notifications.
- Aucune connexion à un logiciel de l'entreprise, aucune donnée personnelle ou sensible.
- Frais simulés selon les tarifs officiels d'Interactive Brokers (courtier envisagé pour la suite réelle, car il permet de connecter des programmes — à revérifier le moment venu).
- ETF de référence : MSCI World capitalisant coté à la bourse suisse, fonds exact à proposer et valider avant le GO.

## Bloc 5 — Usage concret (22.11.2026)

- Routine chaque jour de bourse vers 7 h 45 (Zurich), bilan le vendredi soir. Un seul utilisateur. Internet indispensable. Français uniquement.
- Antoine lit la notification d'opération et le bilan du vendredi ; 2 minutes par semaine.

## Journal des décisions

| N° | Décision | Date |
|---|---|---|
| D-01 | Projet personnel, hors Escaliers Mauron. | 22.11.2026 |
| D-02 | Argent fictif uniquement (paper trading), capital de départ CHF 10'000. | 22.11.2026 |
| D-03 | Référence : ETF MSCI World acheté au départ et conservé, comparaison sur 6 mois. | 22.11.2026 |
| D-04 | Univers : actions et ETF suisses, US et européens ; or via ETF. Pas de crypto. | 22.11.2026 |
| D-05 | Règles fixes : pas d'effet de levier, pas de produits dérivés, pas de vente à découvert. | 22.11.2026 |
| D-06 | Honnêteté : résultats notés tels quels, pertes comprises ; aucune opération recalculée après coup. | 22.11.2026 |
| D-07 | Réussite = portefeuille au-dessus de la référence après 6 mois, frais compris. Sinon échec. | 22.11.2026 |
| D-08 | Frais d'un courtier suisse simulés ; dividendes comptés des deux côtés ; tout mesuré en CHF. | 22.11.2026 |
| D-09 | Argent réel (CHF 5'000) envisagé après la phase fictive : hors V1, décision séparée. | 22.11.2026 |
| D-10 | Antoine y consacre 2 minutes par semaine ; les agents sont autonomes en mode fictif. | 22.11.2026 |
| D-11 | Pas de limite de baisse du portefeuille (option C). Risque accepté : une chute de 30 à 50 % est possible. | 22.11.2026 |
| D-12 | Niveau N1 (perso), avec rigueur renforcée sur la comptabilité. | 22.11.2026 |
| D-13 | Passage en argent réel seulement si : 6 mois complets en fictif, référence battue frais compris, et chaque ordre réel validé par Antoine avant exécution. | 22.11.2026 |
| D-14 | V1 = routine du matin + comptabilité honnête + tableau de bord sur téléphone avec notification. | 22.11.2026 |
| D-15 | Prototype avec 4 rôles regroupés (veille+agenda, analyste, risques+avocat du diable, gérant+contrôleur), puis 7 agents quand la routine tourne sans erreur. | 22.11.2026 |
| D-16 | Hors projet : ordres réels, connexion à un courtier, crypto, dérivés, conseil fiscal. | 22.11.2026 |
| D-17 | Achats permis : ETF et actions de grandes entreprises uniquement (précise D-04). | 22.11.2026 |
| D-18 | Prototype d'une semaine lancé à la main ; le compteur des 6 mois démarre après sa validation. | 22.11.2026 |
| D-19 | Prix relevés par programme à une source fixe, avec une deuxième source de contrôle ; la recherche web sert aux nouvelles seulement. | 22.11.2026 |
| D-20 | Frais fictifs calculés selon les tarifs officiels d'Interactive Brokers. | 22.11.2026 |
| D-21 | ETF de référence : MSCI World capitalisant coté en Suisse ; fonds exact proposé par Claude, validé par Antoine avant le GO. | 22.11.2026 |
| D-22 | Lancement automatique par tâche planifiée Claude (session cloud chaque jour de bourse à 7 h 45, bilan le vendredi soir). Consommation du quota à mesurer pendant l'essai. | 22.11.2026 |
| D-23 | Stockage en simples fichiers dans le dépôt GitHub « trading » ; l'historique Git sert de preuve qu'aucune opération n'est réécrite. | 22.11.2026 |
| D-24 | Tableau de bord : page privée Claude, mise à jour par la routine. | 22.11.2026 |
| D-25 | Notifications sur téléphone (application Claude) : à chaque opération et pour le bilan du vendredi. | 22.11.2026 |

## Points ouverts

- Fonds de référence exact (à valider avant le GO).
- Qui calcule la comptabilité (programme ou agents), critères de l'essai, conduite en cas de panne, budget.
