# Fiche de maintenance

État au 22.11.2026 : cadrage validé, aucun programme encore écrit. Cette fiche se complète à chaque étape.

## Où sont les choses
- Code, données et documents : dépôt GitHub `trading`.
- Règles des agents : `CLAUDE.md` et `.claude/`.
- Décisions : `docs/cadrage.md`. Plan : `docs/plan.md`.

## Lancer, arrêter
- Lancement automatique : tâches planifiées du compte Claude d'Antoine (à créer à l'étape 5).
- Pour tout arrêter : désactiver les tâches planifiées dans le compte Claude. Aucun argent réel n'est en jeu.

## Sauvegarde
- Tout est dans GitHub ; chaque modification est datée et conservée.

## En cas de panne
- La routine ne passe aucune opération, note la panne au journal et prévient Antoine.
- Rien à faire en urgence : elle reprend le jour de bourse suivant. Deux pannes de suite : ouvrir une session Claude Code sur le dépôt et demander « on en est où ? ».

## Si Antoine est absent
- La routine tourne seule. Si elle casse, elle s'arrête sans dégât ; le compteur des 6 mois note les jours manqués.

## Environnement cloud
- Les sessions et tâches planifiées doivent tourner dans l'environnement « trading » (réglages Claude Code) : c'est lui qui autorise les sources de cours.

## Sources de prix
- Titres suisses et ETF : bourse suisse SIX (`www.six-group.com`, cours différés de 15 minutes), lus par `outils/prix.py`.
- Taux de change : Banque centrale européenne (`www.ecb.europa.eu`), un taux officiel par jour.
- Actions américaines : Twelve Data et Finnhub (à brancher dès que les clés sont enregistrées).
- Lancer un relevé : `python3 outils/prix.py outils/titres-test.json`. Chaque relevé crée un fichier daté, jamais réécrit.
- Si SIX change son service : le programme signale l'erreur, aucune opération n'est passée, Antoine est prévenu. Il faudra alors choisir une autre source.

## À compléter
- Tarifs Interactive Brokers appliqués et date du relevé (étape 2).
- Adresse du tableau de bord (étape 6).
