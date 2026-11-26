# Relevé du soir — Contrôleur (lundi à jeudi, vers 22 h 40)

But : exécuter les ordres décidés le matin au prix d'ouverture du jour, et noter la performance à la clôture.
Pourquoi le soir : la bourse suisse n'affiche le prix d'ouverture d'un jour que ce jour-là, jusqu'au lendemain matin tôt.
**Aucun agent, aucune analyse, aucun nouvel ordre.** `D` est le dossier de travail de `equipe/config.json`.

1. `git pull`, puis `python3 outils/compta.py --dossier D verifier`. REFUS = panne.
2. `python3 outils/prix.py D/titres.json D/prix`. Pas de fichier ou pas de taux de change = panne.
3. `python3 outils/compta.py --dossier D executer D/prix/FICHIER`, puis `... etat D/prix/FICHIER`.
3a. `python3 outils/origine.py noter D` : note la part investie du jour, pour l'analyse de l'origine du résultat.
3b. `python3 outils/previsions.py noter D D/prix/FICHIER` : note les prévisions et les paris arrivés à échéance (une erreur ici n'est pas une panne).
4. `python3 outils/journal_bord.py D soir ok "résumé en une phrase" --ordres-executes N`.
5. Tableau de bord : `equipe/tableau-de-bord.md`.
6. `git add -A`, commit, `git push`.
7. Notification seulement si un ordre a été exécuté ou rejeté : l'opération, le titre, le montant, la valeur du portefeuille et l'écart avec la référence. Moins de 200 caractères.

En cas de panne : `python3 outils/journal_bord.py D soir panne "cause"`, commit, push, notification.
Le vendredi, ce relevé est fait par le bilan (`equipe/bilan-vendredi.md`).
