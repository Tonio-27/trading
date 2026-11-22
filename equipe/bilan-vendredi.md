# Bilan du vendredi soir — Contrôleur

Lis `equipe/regles.md` et `equipe/config.json`. `D` est le dossier de travail. Aucun ordre n'est passé pendant le bilan.

1. `git pull`, puis `python3 outils/compta.py --dossier D verifier`.
2. Relevé des prix de clôture : `python3 outils/prix.py D/titres.json D/prix`, puis `python3 outils/compta.py --dossier D etat D/prix/FICHIER`.
3. **Contrôle des opérations de la semaine** : pour chaque ordre exécuté ou rejeté, relis la thèse, les scénarios et la décision. La thèse était-elle juste ? Qu'a-t-on mal vu ?
4. **Dividendes et divisions d'actions** : pour chaque titre en portefeuille, vérifie par recherche web (2 sources) si un dividende a été détaché ou une division d'action faite cette semaine. Si oui, enregistre-le avec `compta.py dividende` (retenue : 35 % pour une action suisse, 15 % pour une action américaine) ou `compta.py fractionnement`, source à l'appui.
4b. **Notation des prévisions** : `python3 outils/previsions.py noter D D/prix/FICHIER`. Reporte le bilan affiché dans le bilan écrit : nombre de prévisions notées, nombre de justes, note moyenne, et ce que sont devenues les idées écartées ou bloquées (avait-on raison de ne pas les suivre ?).
5. **Leçons** : ajoute à `D/lecons.md` (en bas, datées, jamais effacées) 0 à 3 leçons concrètes tirées des erreurs **et** des réussites. Une leçon = une situation, ce qu'on a fait, ce qu'on fera la prochaine fois.
6. **Fiabilité** : compte dans `D/routines.csv` les routines de la semaine réussies et en panne.
7. **Bilan écrit** dans `D/bilans/AAAA-MM-JJ.md`, une demi-page : valeur du portefeuille et de la référence, écart en points, opérations de la semaine, frais cumulés, positions, routines réussies, leçons, événements de la semaine suivante.
8. **Premier vendredi du mois — revue de la méthode** : propose au maximum **une** correction des consignes de l'équipe. Écris-la dans `equipe/corrections.md` (numéro C-01, C-02…, date, constat chiffré, correction, effet attendu). Elle ne vaut que pour l'avenir. Ne modifie les fichiers `equipe/*.md` que pour cette correction.
9. **Tous les 3 mois** : prépare l'entretien avec Antoine (résultats, corrections appliquées, avertissement si plus de 5 points de retard sur la référence).
10. `python3 outils/journal_bord.py D bilan ok "résumé"`, `python3 outils/tableau.py D`, publication du tableau de bord, commit, push.
11. **Notification** (toujours, le vendredi) : valeur, écart avec la référence, nombre d'opérations de la semaine. Moins de 200 caractères.
