# Équipe d'agents de trading (argent fictif) — projet personnel d'Antoine

## But
Avec CHF 5'000 fictifs (CHF 10'000 pendant l'essai), battre d'au moins 2 points sur 6 mois un ETF MSCI World acheté et conservé, frais compris.

## Utilisateurs et niveau
Antoine seul, sur téléphone, 2 minutes par semaine · N1 (perso), rigueur renforcée sur la comptabilité.

## Périmètre V1
- Inclus : routine chaque jour de bourse à 7 h 45 (Zurich), bilan le vendredi soir, comptabilité par programme,
  tableau de bord sur téléphone, notification à chaque opération.
- Achats permis : ETF et actions de grandes entreprises suisses, US et européennes ; or via ETF.
- Hors projet : ordres réels, connexion à un courtier, crypto, dérivés, vente à découvert, effet de levier,
  conseil fiscal, petites entreprises.

## Choix techniques (décidés)
- D-15 : 4 rôles regroupés pour l'essai, puis 7 agents.
- D-19 : prix relevés par programme à une source fixe, contrôlés par une deuxième ; recherche web pour les nouvelles seulement.
- D-20 : frais fictifs aux tarifs officiels d'Interactive Brokers ; dividendes comptés ; tout en CHF (D-08).
- D-22 : lancement par tâche planifiée Claude.
- D-23 : données en simples fichiers dans ce dépôt GitHub.
- D-24 : tableau de bord en page privée Claude. D-25 : notifications sur téléphone.
- D-26 : les agents décident, un programme calcule.

## Données
Cours de bourse et nouvelles publics · aucune donnée personnelle ou sensible · aucun lien avec les outils d'Escaliers Mauron.

## Règles de travail
- Avancer par petites étapes selon docs/plan.md ; montrer le résultat à chaque étape.
- Pour toute nouvelle décision technique : options, puis recommandation, puis validation d'Antoine.
- Tester sur les vrais cas de docs/donnees-test/ avant de dire « c'est fait ».
- Jamais d'ordre réel, jamais de connexion à un courtier.
- Honnêteté : résultats notés tels quels, pertes comprises. Aucune opération, aucun prix, aucune ligne du journal
  n'est modifié ou recalculé après coup ; une erreur se corrige par une nouvelle ligne datée.
- Un prix non confirmé par les 2 sources (écart de 0,5 % ou plus) = pas d'opération sur ce titre ce jour-là.
- En cas de panne : aucune opération, panne notée au journal, notification à Antoine.
- Toute opération doit justifier que le gain espéré dépasse nettement ses frais ; « ne rien faire » est la décision normale.
- Une correction de méthode au maximum par mois, numérotée, datée, valable pour l'avenir seulement.
- Commit Git à chaque étape réussie, avec un message clair en français.
- Mettre à jour docs/cadrage.md (décisions) et docs/maintenance.md au fil de l'eau.
- Expliquer en français clair, sans jargon. Budget : zéro franc en plus de l'abonnement Claude.

## Critères de réussite
Essai : 5 routines sur 5 sans erreur, prix confirmés, comptabilité juste au centime, coût mesuré.
Ensuite : au moins +2 points contre la référence après 6 mois. Détail : docs/criteres-reussite.md.
