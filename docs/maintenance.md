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

## À compléter
- Sources de prix retenues et que faire si l'une change (étape 1).
- Tarifs Interactive Brokers appliqués et date du relevé (étape 2).
- Adresse du tableau de bord (étape 6).
