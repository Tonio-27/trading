---
name: pilotage
description: Pilotage d'un projet logiciel Escaliers Mauron après le cadrage — points d'étape, recette, mise en service et vie de l'outil. À utiliser une fois le GO de CADRAGE.md donné.
---

# Canevas de pilotage — Projets Escaliers Mauron

> **Pour Claude Code.** Ce fichier prend le relais de `CADRAGE.md` une fois le GO donné. Il couvre 4 phases : **A. Développement → B. Recette → C. Mise en service → D. Vie de l'outil.**
> Les règles du §1 de `CADRAGE.md` restent valables : questions par blocs, résumé après chaque bloc, options et recommandation pour toute décision technique, français clair, challenge honnête.

---

## 0. Comment Antoine déclenche chaque phase

Antoine peut écrire l'un de ces mots-clés à tout moment :

| Antoine écrit | Tu lances |
|---|---|
| **« point d'étape »** | le bloc A2 |
| **« recette »** | la phase B |
| **« mise en service »** | la phase C |
| **« bilan »** | le bloc D1 |
| **« nouvelle demande »** | le bloc D2 |
| **« on en est où ? »** | un état du projet en 5 lignes (fait / en cours / à faire / blocages / prochaine décision) |

Tu proposes aussi **de toi-même** la phase suivante quand les conditions sont remplies.

**Intensité selon le niveau du projet** (défini au cadrage) :
- **N1** : A allégée, B réduite à un test par Antoine lui-même, C et D facultatives.
- **N2** : toutes les phases, en version courte.
- **N3 et N4** : toutes les phases, complètes. Une relecture externe (Tebicom ou autre professionnel) est recommandée avant C.

---

## Phase A — Développement

### A1. Règles pendant le développement
- Tu suis `docs/plan.md`, **une étape à la fois**.
- Avant chaque étape, tu annonces en 2 lignes ce que tu vas faire et le critère pour dire « terminé ».
- À la fin de chaque étape :
  - tu testes sur `docs/donnees-test/` ;
  - tu fais un commit Git ;
  - tu montres le résultat à Antoine.
- Tu mets à jour le journal des décisions (`docs/cadrage.md`) et `docs/maintenance.md` au fil de l'eau.
- **Alerte de dérive** : si une demande sort du périmètre V1, tu le signales immédiatement : « Ceci est hors périmètre V1 — on l'ajoute maintenant (impact : …) ou on le note pour la V2 ? »
- **Alerte de blocage** : si une étape prend plus du double du temps prévu, ou si tu tournes en rond sur un problème, tu t'arrêtes et tu présentes la situation avec 2 ou 3 options.

### A2. Point d'étape (à la fin de chaque étape du plan)
Commence par un résumé : ce qui est fait, ce qui a été testé, les résultats chiffrés.

Puis pose ces questions :
- Le résultat correspond-il à ce que tu imaginais ? Qu'est-ce qui te gêne, même un détail ?
- As-tu testé toi-même ? Sur quel cas réel ?
- Quelque chose a-t-il changé dans ton besoin depuis le cadrage ?
- Les priorités de la suite restent-elles les mêmes ?
- On continue avec l'étape suivante, on corrige d'abord, ou on revoit le plan ?

**Signaux d'alerte à vérifier toi-même :**
- un résultat trop parfait (à vérifier, pas à célébrer) ;
- une complexité qui grandit sans raison ;
- une dépendance nouvelle et coûteuse ;
- des données de production touchées.

### A3. Fin de développement de la V1
Avant de passer à la recette, vérifie et présente :
- [ ] Toutes les fonctions indispensables de la V1 sont faites.
- [ ] Tous les critères de `docs/criteres-reussite.md` ont été testés, avec les résultats.
- [ ] Le `README.md` et `docs/maintenance.md` sont à jour.
- [ ] Aucune donnée de test réelle et sensible n'est exposée.
- [ ] La liste des limites connues est écrite honnêtement.

Puis demande : **« Prêt pour la recette ? »**

---

## Phase B — Recette (test par les vrais utilisateurs)

### B1. Préparer la recette — questions à Antoine
- Qui va tester ? (Idéalement un vrai utilisateur, pas seulement Antoine.)
- Sur quels cas réels ? Choisis au moins un cas simple, un cas courant et un cas difficile ou inhabituel.
- Dans quelles conditions réelles : atelier, chantier, téléphone, PC du bureau ?
- Combien de temps dure la recette ?
- Qui note les problèmes, et où ?

### B2. Ce que tu produis
- **`docs/recette.md`** : la liste des scénarios à tester. Chaque scénario est écrit pas à pas, avec le résultat attendu, et peut être imprimé pour l'atelier.
- Une **fiche de retour simple**, avec une ligne par problème : ce que j'ai fait, ce que j'attendais, ce qui s'est passé, gravité (bloquant / gênant / détail).

### B3. Bilan de recette — questions à Antoine
- Qu'ont dit les testeurs ? Qu'est-ce qui les a bloqués, agacés ou surpris ?
- L'outil est-il plus rapide ou plus fiable que l'ancienne méthode ? De combien ?
- Pour chaque problème remonté : est-ce bloquant pour la mise en service ? À corriger plus tard ? À ignorer ?

**Décision finale à demander : « Mise en service : OUI / OUI après corrections / NON, on revoit. »**

---

## Phase C — Mise en service

### C1. Préparer — questions à Antoine
- Quelle date de démarrage ? (Évite les périodes chargées et les veilles de vacances.)
- L'ancienne méthode reste-t-elle disponible en parallèle ? Combien de temps ?
- Faut-il reprendre des données existantes (Excel, ERP…) ?
- Qui forme l'équipe, et comment : démonstration de 15 minutes, fiche imprimée, vidéo ?
- Qui est la personne de référence en cas de question ou de panne ?
- Faut-il prévenir Tebicom : installation, hébergement, sauvegarde ?

### C2. Ce que tu produis
- **`docs/mise-en-service.md`** : la check-list du jour J (installation, vérifications, test final, sauvegarde avant et après).
- **`docs/guide-utilisateur.md`** : un mode d'emploi d'**une page maximum**, en langage simple, imprimable pour l'atelier.
- **Plan de retour arrière** : comment revenir à l'ancienne méthode en moins d'une heure si ça tourne mal.

### C3. Check-list jour J
- [ ] Sauvegarde complète faite avant.
- [ ] Installation faite et vérifiée sur chaque poste ou appareil.
- [ ] Un test réel réussi en conditions de production.
- [ ] Les utilisateurs formés et le guide distribué.
- [ ] La personne de référence connue de tous.
- [ ] La sauvegarde automatique vérifiée (Tebicom / NAS).
- [ ] Une version figée dans Git, étiquetée `v1.0`.

### C4. Suivi des premiers jours
À J+2 et à J+7, pose ces questions :
- L'équipe l'utilise-t-elle vraiment, ou revient-elle à l'ancienne méthode ? Pourquoi ?
- Y a-t-il eu des pannes, des erreurs, des contournements ?
- Que faut-il corriger en urgence ?

---

## Phase D — Vie de l'outil

### D1. Bilan (à 1 mois, puis tous les 6 mois)
- L'outil atteint-il les objectifs fixés au cadrage ? Compare chiffres contre chiffres.
- Combien de temps gagne-t-on, combien d'erreurs évite-t-on, quel est le gain réel ?
- Qui l'utilise, et qui ne l'utilise pas ? Pourquoi ?
- Quelles sont les 3 améliorations les plus demandées ?
- L'outil a-t-il changé de public, par exemple d'Antoine seul vers toute l'équipe ? → **Si oui, reclasser le niveau (N1 à N4) et appliquer les nouvelles exigences.**
- Faut-il le garder, l'améliorer, ou l'arrêter ?

Le résultat est consigné dans **`docs/bilans.md`**, daté.

### D2. Nouvelle demande d'évolution
Pour toute nouvelle idée, pose ces questions :
- Quel problème résout-elle ? Qui l'a demandée ?
- Quel gain, et pour qui ?
- Est-ce urgent, important, ou simplement agréable ?
- Est-ce une petite correction ou un gros changement ?

Ensuite, classe la demande :
- **Correction** → tu la fais directement : version `v1.0.1`.
- **Petite évolution** → tu l'ajoutes à la version suivante : `v1.1`.
- **Gros changement** → tu relances un mini-cadrage avec `CADRAGE.md`, blocs 1, 3, 4 et 7 : `v2.0`.

Toutes les demandes sont tenues dans **`docs/evolutions.md`**, avec leur statut : à faire / en cours / fait / refusé.

### D3. Règles de maintenance
- Chaque modification est testée sur `docs/donnees-test/` avant d'être déployée.
- Chaque version est notée dans **`CHANGELOG.md`** : date, version, ce qui change, en français simple.
- `docs/maintenance.md` est toujours à jour : une autre personne doit pouvoir reprendre l'outil sans Antoine.
- Au moins une fois par an, tu vérifies :
  - les dépendances et mises à jour de sécurité ;
  - que la sauvegarde se restaure vraiment (test réel) ;
  - les accès : qui a encore besoin de quoi.

---

## Récapitulatif des fichiers du projet

| Fichier | Créé en | Contenu |
|---|---|---|
| `CLAUDE.md`, `docs/cadrage.md`, `docs/plan.md`, `docs/criteres-reussite.md`, `docs/risques.md`, `README.md` | Cadrage | Base du projet |
| `docs/maintenance.md` | Cadrage, tenu à jour ensuite | Fiche de passation |
| `docs/recette.md` | Phase B | Scénarios de test et retours |
| `docs/mise-en-service.md`, `docs/guide-utilisateur.md` | Phase C | Jour J et mode d'emploi |
| `docs/bilans.md`, `docs/evolutions.md`, `CHANGELOG.md` | Phase D | Vie de l'outil |
