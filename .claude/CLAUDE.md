# Règles globales — Antoine Mauron (Escaliers Mauron)

## Démarrage de session
Au premier message de chaque session, vérifie l'état du dossier ouvert, puis réagis selon le cas :

**Cas 1 — Nouveau projet** (pas de `CLAUDE.md` dans le dossier, ni de `docs/cadrage.md`)
Avant toute autre chose, affiche ce rappel :

> 📋 **Nouveau projet détecté — les étapes :**
> 1. `/cadrage` → répondre aux questions bloc par bloc (prépare de vrais exemples de données)
> 2. Relire la synthèse d'une page → dire **GO** seulement si elle convient
> 3. `/pilotage` → développement étape par étape
> 4. Piloter avec : « point d'étape », « recette », « mise en service », « bilan », « on en est où ? »
>
> **On lance le cadrage maintenant ?**

Ne code rien tant que le cadrage n'est pas fait et validé par un GO.

**Cas 2 — Cadrage commencé mais sans GO** (`docs/cadrage.md` existe, mais pas de `docs/plan.md`)
Rappelle où en est le cadrage et propose de le reprendre.

**Cas 3 — Projet en cours** (`docs/plan.md` existe)
Donne l'état du projet en 5 lignes : fait / en cours / à faire / blocages / prochaine décision. Puis propose l'étape suivante selon `/pilotage`.

## Règles permanentes
- Toujours en français clair, sans jargon. Réponses courtes et structurées.
- Pour toute décision technique : 2 ou 3 options, ma recommandation, puis la décision d'Antoine.
- Jamais d'écriture dans CID ERP ni dans des données de production sans accord explicite.
