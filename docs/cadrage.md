# Cadrage — Équipe d'agents de trading (argent fictif)

État : cadrage validé — GO donné par Antoine le 22.11.2026. Suite : `docs/plan.md`, piloté avec `/pilotage`.

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

## Blocs 7 à 9 — Qualité, pannes, budget (22.11.2026)

- Tous les calculs (valeur, frais, change, performance) sont faits par un programme ; les agents décident, ils ne calculent pas.
- Essai validé si : 5 routines sur 5 sans erreur ; chaque prix confirmé par les 2 sources à moins de 0,5 % d'écart
  (sinon pas d'opération sur ce titre ce jour-là) ; comptabilité recalculée à la main et juste au centime ; coût d'un lancement mesuré et accepté.
- En cas de panne : aucune opération, portefeuille inchangé, panne notée au journal, notification à Antoine, reprise le jour de bourse suivant.
- Sécurité : aucun accès à de l'argent réel, aucune donnée sensible. Si Antoine est absent, la routine tourne seule ; si elle casse, elle s'arrête sans dégât.
- Budget : zéro franc en plus de l'abonnement Claude. Si le quota ne suffit pas, on réduit la fréquence.

## Synthèse (présentée le 22.11.2026)

1. Problème et objectif : Antoine veut savoir si une équipe d'agents peut gérer un portefeuille mieux qu'un simple ETF, avant d'y mettre CHF 5'000 réels.
   Objectif : avec CHF 10'000 fictifs, battre sur 6 mois un ETF MSCI World acheté et conservé, frais compris.
2. Niveau : N1 (perso), rigueur renforcée sur la comptabilité.
3. Périmètre V1 : routine du matin, comptabilité par programme, tableau de bord et notifications. Hors projet : ordres réels, courtier, crypto, dérivés, conseil fiscal, petites entreprises.
4. Choix techniques : tâche planifiée Claude, fichiers dans GitHub, programme de calcul, 2 sources de prix, page privée Claude, notification sur téléphone, frais Interactive Brokers.
5. Critères de réussite : les 4 critères de l'essai ; puis portefeuille au-dessus de la référence après 6 mois, frais compris.
6. Risques : prix faux ou source gratuite qui casse ; résultat dû à la chance sur 6 mois (et aucune limite de baisse) ; quota de l'abonnement insuffisant pour une routine par jour.
7. Étapes : documents du projet ; programme de comptabilité et relevé des prix ; 4 rôles et essai d'une semaine à la main ; automatisation et notifications ; tableau de bord ; départ du compteur ; passage à 7 agents.

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
| D-26 | Tous les calculs sont faits par un programme ; les agents décident, ils ne calculent pas. | 22.11.2026 |
| D-27 | Essai validé sur 4 critères chiffrés (5/5 routines, écart de prix < 0,5 % entre 2 sources, comptabilité juste au centime, coût mesuré et accepté). | 22.11.2026 |
| D-28 | En cas de panne : aucune opération, panne notée au journal, notification à Antoine. | 22.11.2026 |
| D-29 | Budget : zéro franc en plus de l'abonnement Claude ; sources gratuites uniquement. | 22.11.2026 |
| D-30 | Rythme : analyse chaque jour de bourse, ordres rares (« ne rien faire » est la décision normale) ; toute opération doit justifier que le gain espéré dépasse nettement ses frais. Pas d'achats-ventes en cours de journée. | 22.11.2026 |
| D-31 | Pas de limite de taille par action (choix d'Antoine ; la recommandation était 10 % maximum par action). Risque accepté : une seule action peut faire perdre beaucoup en un jour. | 22.11.2026 |
| D-32 | Objectif : au moins 2 points au-dessus de la référence sur 6 mois, frais compris, sans plafond (précise D-07). | 22.11.2026 |
| D-33 | Objectif manqué = pas d'arrêt du projet : analyse des causes, correction de la méthode, nouvelle période de 6 mois (remplace « échec » de D-07). | 22.11.2026 |
| D-34 | Amélioration continue : leçons relues chaque matin ; bilan du Contrôleur chaque vendredi ; une correction de méthode au maximum par mois, numérotée et datée, valable pour l'avenir seulement ; entretien avec Antoine tous les 3 mois (avertissement si plus de 5 points de retard). | 22.11.2026 |
| D-35 | Argent réel conditionné à 6 mois consécutifs à +2 points avec une méthode stable (complète D-13). | 22.11.2026 |
| D-36 | GO d'Antoine pour générer les documents du projet. Référence proposée : iShares Core MSCI World UCITS ETF (capitalisant), ISIN IE00B4L5Y983, à confirmer à l'étape 1. | 22.11.2026 |
| D-37 | Environnement cloud personnel « trading » créé pour ce dépôt : il autorise uniquement les sources de cours et de change. Les tâches planifiées devront tourner dans cet environnement. | 22.11.2026 |
| D-38 | Sources de cours (adapte D-19 et D-17) : actions suisses et tous les ETF par la bourse suisse (SIX, source officielle, contrôle de cohérence par le programme) ; actions américaines par 2 comptes gratuits, Twelve Data et Finnhub, qui se contrôlent l'un l'autre ; taux de change de la BCE. Yahoo et Stooq écartés (accès refusé depuis le cloud). | 22.11.2026 |
| D-39 | Pas d'actions européennes seules pour l'instant : l'Europe est achetée via des ETF cotés en Suisse. À réexaminer en V2. | 22.11.2026 |
| D-40 | Fonds de référence confirmé : iShares Core MSCI World, code SWDA à la bourse suisse, coté en USD, converti en CHF au taux BCE. | 22.11.2026 |
| D-41 | Programmes écrits en Python, sans dépendance à installer. | 22.11.2026 |
| D-42 | Clés Twelve Data et Finnhub enregistrées comme secrets de l'environnement « trading » (jamais dans le dépôt). Étape 1 testée : 15 titres relevés, 0 erreur, 5 actions américaines confirmées par 2 sources. | 22.11.2026 |
| D-43 | Frais simulés : tarif « Fixed » d'Interactive Brokers — bourse suisse 0,05 % (minimum CHF 5) ; actions US USD 0.005 par action (minimum USD 1, maximum 1 %) ; change 0,002 % (minimum USD 2) à chaque opération en monnaie étrangère ; pas de timbre fédéral chez un courtier étranger. Hypothèse prudente, réglable dans `outils/frais.json`. À valider par Antoine. | 22.11.2026 |
| D-44 | Règles de comptabilité : nombres entiers de titres ; liquidités tenues en CHF ; ordre exécuté au premier prix d'ouverture utilisable après la décision, rejeté après 5 jours sans prix ; ventes traitées avant les achats ; journal en ajout seul, protégé par une empreinte en chaîne. | 22.11.2026 |
| D-45 | Contrôle des étapes 1 et 2 par un relecteur indépendant : 12 défauts corrigés (date des ordres fixée par le programme, relevés récents uniquement, dividendes et divisions d'actions datés et non répétables, écritures verrouillées, comparaison du journal avec tout l'historique Git, prix d'ouverture confirmé par la 2e source, taux de change périmé écarté, performance notée par jour de cours). | 22.11.2026 |
| D-46 | Sur délégation d'Antoine (« passer à toutes les autres étapes ») : l'essai est conduit par deux tâches planifiées Claude dans la session de développement — routine du lundi au vendredi à 7 h 45, bilan le vendredi à 22 h 40 (après la clôture américaine). Adapte D-18 (essai « à la main ») et D-22. À confirmer par Antoine. | 22.11.2026 |
| D-47 | Les données de l'essai vivent dans `essai/`. Au départ du compteur, un dossier neuf `donnees/` est ouvert ; l'essai n'est jamais mélangé au résultat des 6 mois. | 22.11.2026 |
| D-48 | La référence est achetée en une fois, au plus grand nombre entier de parts que CHF 10'000 permettent (calculé par le programme à l'exécution). | 22.11.2026 |
| D-49 | Tableau de bord : page privée Claude de type « Data », https://claude.ai/artifact/V4wDXGeLNUN91P56uWSiVy, dont le fichier de données est remplacé à chaque routine. | 22.11.2026 |
| D-50 | Répétition générale du 22.11.2026 réussie : veille, analyse, contradiction, décision écrite (idée Nestlé écartée, gain espéré trop faible face aux frais), sans aucun calcul fait par les agents. | 22.11.2026 |
| D-51 | Sources d'information : l'environnement « trading » autorise la BNS, la Fed, la BEA, cash.ch, swissinfo, la RTS et allnews (en plus de la BCE et de SIX), que les agents peuvent ouvrir et lire. Règle de confiance : un ordre doit reposer sur au moins un fait lu dans l'article ou sur une page officielle. | 22.11.2026 |
| D-52 | Trois horizons : veille quotidienne (jours), agenda vérifié sur pages officielles (semaines), dossier de fond mis à jour le lundi (3 à 12 mois). L'analyste doit appuyer chaque idée sur au moins deux horizons. | 22.11.2026 |
| D-53 | Lecture des pages web par le programme `outils/lire.py`, seul moyen qui passe par le réseau autorisé (l'outil de lecture web habituel des agents ne le fait pas). | 22.11.2026 |
| D-54 | Résultats d'entreprises (option A) : `outils/entreprises.py` relève chaque matin, pour les actions américaines suivies, les résultats trimestriels avec leur surprise, la prochaine date de résultats et la presse des 3 derniers jours (Finnhub, compte gratuit). Le Veilleur écrit une fiche à chaque publication. | 22.11.2026 |
| D-55 | Notation des prévisions (option B) : chaque idée examinée, retenue ou non, est enregistrée avec ses probabilités ; `outils/previsions.py` la note à l'échéance contre le cours réel (note de Brier). Bilan chaque vendredi. | 22.11.2026 |
| D-56 | Suite de l'audit de faisabilité : R1 retenue — la décision d'engager de l'argent réel se juge aussi sur la qualité des prévisions (au moins 20 notées, meilleures que le hasard) et le respect des règles. R2 (discipline de frais) et R3 (cœur et satellites) non retenues à ce stade. | 22.11.2026 |
| D-57 | Apprentissage renforcé (précise D-34) : notes par rôle chaque vendredi ; leçons avec cas à l'appui, confirmées, contredites ou retirées ; améliorations de l'outil proposées à Antoine dans `docs/evolutions.md` ; audit mensuel par un agent indépendant avant l'unique correction de méthode, et jugement de la correction précédente. | 22.11.2026 |
| D-58 | Le compteur des 6 mois démarrera avec CHF 5'000 fictifs, le montant réel envisagé (modifie D-02). Raison : les frais ont un minimum fixe et pèsent deux fois plus lourd sur CHF 5'000 que sur CHF 10'000 ; le test doit être fidèle à la situation réelle. L'essai en cours reste à CHF 10'000 : il ne sert qu'à vérifier la mécanique. | 22.11.2026 |
| D-59 | Portefeuille « deux poches » affiché au tableau de bord : moitié ETF de référence, moitié agents (50/50, sans rééquilibrage), calculé à partir des deux autres sans aucun ordre. Il montre ce que donnerait un placement réel réparti ; l'objectif des agents se juge toujours sur leur courbe seule. | 22.11.2026 |
| D-60 | Défaut révélé par la première routine automatique (23.11.2026) : à 7 h 45, la bourse suisse n'affiche plus le prix d'ouverture de la veille. Correction choisie par Antoine (option A) : un relevé du soir sans agents, du lundi au jeudi vers 22 h 40 (le vendredi, c'est le bilan), exécute les ordres du matin au prix d'ouverture du jour. Les programmes distinguent désormais « prix utilisable » (cours fiable) et « prix exécutable » (ouverture présente). | 23.11.2026 |
| D-61 | Apprentissage accéléré, décidé après 3 jours d'essai (2 prévisions seulement en 4 jours) : A — une prévision à 7 jours pour chaque titre examiné, même écarté par l'analyste, en plus de la prévision à l'horizon de la thèse ; B — chaque jour une prévision à 7 jours sur l'ETF de référence, qui mesure le pari d'être investi ou en liquidités ; C — les paris de hausse ou de baisse du Veilleur sont notés contre la clôture suivante. Un programme lit ces lignes dans les fichiers des agents (`previsions.py importer`) et les note chaque soir. D (fiche chiffrée par titre) non retenue pour le moment. | 26.11.2026 |
| D-62 | Fiche d'historique par titre (option D) : chaque matin, `outils/historique.py` calcule sur 5 ans de cours quotidiens (bourse suisse, Twelve Data) les variations sur 1 semaine à 5 ans, l'écart aux plus hauts et plus bas, la variation d'un jour habituelle et la plus forte baisse. L'analyste et le contradicteur doivent s'en servir. Durée de 5 ans recommandée par Claude, réglable. Limite : variations hors dividendes. | 26.11.2026 |
| D-63 | Analyse de l'origine du résultat : `outils/origine.py` note chaque soir la part investie des deux portefeuilles et sépare l'écart en « effet de la part investie » et « choix des titres et frais ». Reprise dans le bilan du vendredi. | 26.11.2026 |

## Points ouverts


- Résultats des entreprises suisses : pas de source chiffrée automatique ; ils passent par les articles de cash.ch et allnews.ch. Le site de la SEC refuse les lecteurs automatiques sans adresse de contact : non utilisé.
- Sources : CNBC, BLS (emploi et inflation américains), FMI et OCDE refusent les lecteurs automatiques ; l'ajout d'AP, BBC, Guardian et Reuters a été refusé par le service d'environnement ; la presse financière internationale (Reuters, Bloomberg, Financial Times) est payante ou fermée. Ces informations restent connues par extraits seulement.
- Coût mesuré à la répétition : environ 360'000 jetons pour les 3 sous-agents d'une routine. À suivre pendant l'essai (colonne `jetons_sous_agents` de `essai/routines.csv`) et à juger par Antoine.
- La routine tourne dans la session de développement : à confirmer ou à déplacer vers une session dédiée au départ du compteur.
- Tarifs Interactive Brokers relevés par extraits de pages officielles : à revérifier avant tout passage en argent réel.
- Limites connues des prix : bon de jouissance Roche (ROG) introuvable ; titres suisses et ETF à une seule source ; Twelve Data et Finnhub peut-être issus du même fournisseur.
- Protection du journal : l'empreinte en chaîne détecte une retouche accidentelle ; la vraie garantie contre une réécriture est l'historique poussé sur GitHub.
