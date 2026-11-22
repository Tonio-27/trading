# Plan du projet

Règle : une étape à la fois. Chaque étape se termine par un test sur `docs/donnees-test/`, un commit et une démonstration à Antoine.

## Phase 1 — Prototype jetable (essai)

| N° | Étape | Objectif | Livrable | Critère « terminé » |
|---|---|---|---|---|
| 1 | Relevé des prix | Relever chaque jour le prix des titres à 2 sources gratuites | Programme de relevé ; choix des 2 sources validé par Antoine ; fonds de référence confirmé | Sur 10 titres réels (suisses, US, européens, or), les 2 sources concordent à moins de 0,5 % et la monnaie est correcte |
| 2 | Comptabilité | Calculer portefeuille, frais Interactive Brokers, change, dividendes, performance contre la référence | Programme de comptabilité ; fichiers portefeuille et journal | 5 opérations d'exemple recalculées à la main : juste au centime |
| 3 | Les 4 rôles | Écrire les consignes des 4 rôles regroupés et la routine du matin | Consignes des rôles ; routine lançable à la main | Une routine complète produit une décision justifiée par écrit, sans calcul fait par les agents |
| 4 | Essai d'une semaine | Lancer la routine à la main 5 jours de bourse | Journal de l'essai ; mesure du quota par lancement | Les 4 critères de l'essai sont remplis (voir `criteres-reussite.md`) ; Antoine valide |

## Phase 2 — V1 utile

| N° | Étape | Objectif | Livrable | Critère « terminé » |
|---|---|---|---|---|
| 5 | Automatisation | Tâche planifiée chaque jour de bourse à 7 h 45, bilan le vendredi soir | Tâches planifiées ; notifications sur téléphone | 3 lancements automatiques de suite réussis ; une panne simulée est notifiée |
| 6 | Tableau de bord | Page privée lisible sur téléphone : valeur, positions, opérations, courbe contre la référence | Page privée Claude mise à jour par la routine | Antoine lit l'essentiel en moins de 2 minutes sur son téléphone |
| 7 | Départ du compteur | Remise à zéro : CHF 10'000 fictifs, achat fictif de la référence, début des 6 mois | Portefeuille initial ; date de départ notée | Date de départ et prix de départ consignés dans le journal |

## Phase 3 — V2

| N° | Étape | Objectif | Critère « terminé » |
|---|---|---|---|
| 8 | Passage à 7 agents | Séparer les rôles : Veilleur, Agenda, Analyste, Risques, Avocat du diable, Gérant, Contrôleur | 5 routines de suite sans erreur ; quota toujours acceptable |
| 9 | Amélioration continue | Bilan du vendredi, revue mensuelle de la méthode, entretien à 3 mois | Première revue mensuelle faite et consignée |
| 10 | Bilan à 6 mois | Verdict contre l'objectif (+2 points) | Bilan daté dans `docs/bilans.md` ; décision d'Antoine sur la suite |

Hors plan : tout passage en argent réel est un nouveau projet, avec son propre cadrage.
