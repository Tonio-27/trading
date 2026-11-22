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
- Actions américaines : Twelve Data (`api.twelvedata.com`), contrôlé par Finnhub (`finnhub.io`). Les deux clés sont des secrets de l'environnement « trading » ; pour les changer : réglages de l'environnement, secrets réseau. Compte gratuit Twelve Data : 8 demandes par minute, 800 par jour.
- Lancer un relevé : `python3 outils/prix.py outils/titres-test.json`. Chaque relevé crée un fichier daté, jamais réécrit.
- Si SIX change son service : le programme signale l'erreur, aucune opération n'est passée, Antoine est prévenu. Il faudra alors choisir une autre source.

## Comptabilité
- `outils/compta.py` : commandes `init`, `ordre`, `executer`, `etat`, `verifier`. Les données vivent dans `donnees/` (journal, état, performance).
- Le journal `donnees/journal.jsonl` ne se modifie jamais à la main : `python3 outils/compta.py verifier` détecte toute retouche.
- Frais : `outils/frais.json` (tarifs Interactive Brokers relevés le 22.11.2026). Un changement de tarif ne vaut que pour les opérations futures.
- Tests : `python3 outils/test_compta.py` doit afficher « TOUT EST JUSTE » avant toute mise en service d'une modification.

## À compléter
- Adresse du tableau de bord (étape 6).
