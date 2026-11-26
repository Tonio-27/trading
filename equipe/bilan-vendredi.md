# Bilan du vendredi soir — Contrôleur

Lis `equipe/regles.md` et `equipe/config.json`. `D` est le dossier de travail. Aucun ordre n'est passé pendant le bilan.

1. `git pull`, puis `python3 outils/compta.py --dossier D verifier`.
2. Relevé des prix de clôture : `python3 outils/prix.py D/titres.json D/prix`, puis `python3 outils/compta.py --dossier D executer D/prix/FICHIER` (exécution des ordres du matin au prix d'ouverture du jour), puis `... etat D/prix/FICHIER`.
3. **Contrôle des opérations de la semaine** : pour chaque ordre exécuté ou rejeté, relis la thèse, les scénarios et la décision. La thèse était-elle juste ? Qu'a-t-on mal vu ?
4. **Dividendes et divisions d'actions** : pour chaque titre en portefeuille, vérifie par recherche web (2 sources) si un dividende a été détaché ou une division d'action faite cette semaine. Si oui, enregistre-le avec `compta.py dividende` (retenue : 35 % pour une action suisse, 15 % pour une action américaine) ou `compta.py fractionnement`, source à l'appui.
4b. **Notation des prévisions** : `python3 outils/previsions.py noter D D/prix/FICHIER`. Reporte le bilan affiché dans le bilan écrit : nombre de prévisions notées, nombre de justes, note moyenne ; les prévisions sur la référence (l'équipe a-t-elle eu raison d'être investie ou en liquidités ?) ; ce que sont devenus les titres écartés par l'analyste et les idées écartées ou bloquées (avait-on raison de ne pas les suivre ?) ; les paris du Veilleur (combien de justes, à comparer à la moitié).
5. **Notes par rôle** : dans le bilan écrit, une ligne par rôle pour la semaine — Veilleur (faits démentis ou dates corrigées ensuite), Analyste (prévisions notées, justes ou non), Contradicteur (objections confirmées ou démenties par les faits ; que sont devenues les idées bloquées ou réduites), Gérant (idées écartées contre idées retenues : lesquelles ont le mieux fait).
5b. **Leçons** dans `D/lecons.md` (on ajoute en bas, on n'efface jamais) :
   - 0 à 3 leçons nouvelles tirées des erreurs **et** des réussites. Format : date, situation, ce qu'on a fait, ce qu'on fera la prochaine fois, **cas à l'appui** (dates des décisions concernées).
   - Relis les leçons existantes : pour chacune touchée par les faits de la semaine, ajoute une ligne datée « confirmée par … » ou « contredite par … ». Une leçon contredite 2 fois est marquée « retirée » (elle reste écrite, mais ne s'applique plus).
   - Une leçon appuyée par un seul cas est marquée « à confirmer » : elle informe, elle n'interdit rien. Un seul résultat peut être de la chance.
5c. **L'outil** : note dans `docs/evolutions.md` (statut « à faire ») toute amélioration utile constatée pendant la semaine : panne, prix non utilisable, source illisible, consigne ambiguë. Tu ne modifies aucun programme toi-même : Antoine décide.
6. **Fiabilité** : compte dans `D/routines.csv` les routines de la semaine réussies et en panne.
7. **Bilan écrit** dans `D/bilans/AAAA-MM-JJ.md`, une demi-page : valeur du portefeuille et de la référence, écart en points, opérations de la semaine, frais cumulés, positions, routines réussies, leçons, événements de la semaine suivante.
8. **Premier vendredi du mois — audit et revue de la méthode** :
   - lance un sous-agent avec la consigne « Lis et applique `equipe/auditeur.md`. Dossier : D. Mois : AAAA-MM. » ;
   - à partir de son audit, retiens au maximum **une** correction des consignes de l'équipe. Écris-la dans `equipe/corrections.md` (numéro C-01, C-02…, date, constat chiffré, correction, effet attendu, comment on jugera dans un mois). Elle ne vaut que pour l'avenir. Ne modifie les fichiers `equipe/*.md` que pour cette correction ;
   - juge la correction du mois précédent : a-t-elle eu l'effet attendu ? Si non, propose de la retirer.
9. **Tous les 3 mois** : prépare l'entretien avec Antoine (résultats, corrections appliquées, avertissement si plus de 5 points de retard sur la référence).
10. `python3 outils/journal_bord.py D bilan ok "résumé"`, `python3 outils/tableau.py D`, publication du tableau de bord, commit, push.
11. **Notification** (toujours, le vendredi) : valeur, écart avec la référence, nombre d'opérations de la semaine. Moins de 200 caractères.
