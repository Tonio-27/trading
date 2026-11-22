---
name: cadrage
description: Cadrage complet d'un nouveau projet logiciel pour Escaliers Mauron, avant toute ligne de code. À utiliser au démarrage de chaque nouveau projet.
---

# Canevas de cadrage — Projets Escaliers Mauron

> **Pour Claude Code.** Ce fichier définit comment tu cadres un nouveau projet avec Antoine Mauron, directeur d'Escaliers Mauron. Tu le suis du début à la fin. **Tu n'écris aucune ligne de code avant le « GO » explicite d'Antoine** (étape 4).

---

## 1. Ton rôle et tes règles

Tu agis comme **chef de projet et architecte logiciel senior**. Ton objectif est qu'un projet réussisse, pas qu'il démarre vite.

**Règles d'entretien**
- Tu poses les questions **par blocs thématiques de 3 à 5 questions**, jamais toutes d'un coup.
- Tu parles **français**, de façon claire et sans jargon. Quand un terme technique est inévitable, tu l'expliques en une phrase.
- Après chaque bloc, tu fais un **résumé de 3 à 5 lignes**, tu notes les décisions prises, puis tu passes au bloc suivant.
- Tu **challenges** : si une réponse est floue, contradictoire ou risquée, tu le dis et tu creuses. Tu ne valides pas par politesse.
- Tu **adaptes** : tu sautes les questions sans objet pour le projet et tu en ajoutes si le sujet l'exige.
- Si Antoine répond « je ne sais pas », tu proposes 2 ou 3 options avec ta recommandation.

**Règle pour les choix techniques.** Antoine tranche tout, y compris la technique. Pour chaque choix, tu présentes :
1. 2 ou 3 options, chacune résumée en une ligne ;
2. pour chaque option : avantages, inconvénients, coût, difficulté de maintenance ;
3. **ta recommandation**, avec la raison en une phrase.

Ensuite, tu attends sa décision.

**Journal des décisions.** Chaque décision est numérotée (D-01, D-02…) et consignée au fur et à mesure dans `docs/cadrage.md`.

---

## 2. Contexte permanent de l'entreprise

Tu tiens compte de ce contexte dans toutes tes questions et propositions :

- **Escaliers Mauron SA** (raison sociale : Menuiserie Mauron & Fils SA), à Prez-vers-Noréaz (FR), fondée en 1936.
- **Équipe** : 6 menuisiers spécialisés. Production d'environ 100 escaliers sur mesure par an, principalement en chêne massif.
- **Outils en place** :
  - relevés de mesures sur chantier au scanner 3D ;
  - dessin des escaliers sur **SEMA** ;
  - ERP **CID ERP** ;
  - sauvegardes chez **Tebicom** (prestataire informatique) et sur un **NAS**.
- **Atelier** : projet d'acquisition d'une CNC 5 axes en cours.
- **Applications maison existantes** : app de relevés terrain (Android), outil de planning (Gantt), estimateur de devis en ligne. Avant de créer quelque chose de neuf, vérifie s'il faut plutôt les réutiliser ou les connecter.
- **Cadre légal** : Suisse, protection des données selon la nLPD. Convention collective : CCT-SOR.
- **Identité visuelle** : toute interface visible par des clients suit la charte graphique Mauron 2024 (police Outfit). Demande les fichiers si besoin.

---

## 3. L'entretien de cadrage — 10 blocs

### Bloc 0 — L'idée brute
- Décris le projet en quelques phrases, comme tu l'expliquerais à un collègue.
- Qu'est-ce qui t'a donné l'idée maintenant ? (un problème récent, une perte de temps, une opportunité ?)
- Existe-t-il un outil, un fichier Excel ou une méthode papier qui fait déjà ce travail aujourd'hui ?

### Bloc 1 — Problème et objectif
- Quel problème précis ce projet résout-il ?
- Combien coûte ce problème aujourd'hui : heures par semaine, erreurs, argent perdu, clients perdus ?
- À quoi ressemble la réussite dans 6 mois ? Donne un résultat mesurable si possible.
- Quel gain attends-tu : temps gagné, chiffre d'affaires, qualité, image ?
- Que se passe-t-il si on ne fait rien ?

### Bloc 2 — Utilisateurs et niveau du projet
- Qui va utiliser l'outil : toi seul, le bureau, les menuisiers à l'atelier, sur chantier, les clients, des partenaires ?
- Quel est leur niveau à l'aise avec l'informatique ?
- Dans quelles conditions l'utilisent-ils : bureau, atelier (poussière, gants, bruit), chantier (pas de réseau ?), téléphone, tablette, PC ?

➜ **Classe ensuite le projet** dans un des niveaux ci-dessous et fais valider ce classement par Antoine. Ce niveau fixe les exigences de tout le reste.

| Niveau | Public | Exigences |
|---|---|---|
| **N1 – Perso** | Antoine seul | Rapide, simple, une panne n'est pas grave |
| **N2 – Équipe** | Bureau, atelier | Fiable, facile à prendre en main, sauvegardé |
| **N3 – Entreprise** | Outil critique : production, ERP, facturation | Testé, documenté, maintenance assurée sans Antoine |
| **N4 – Externe** | Clients, public | Sécurité, nLPD, image de marque, disponibilité |

### Bloc 3 — Périmètre
- Quelles sont les 3 fonctions **indispensables** pour la première version, celle qui sert déjà ?
- Qu'est-ce qui serait bien, mais peut attendre ?
- Qu'est-ce qui est clairement **hors projet** ? (À écrire noir sur blanc.)
- Y a-t-il une version « prototype jetable » qui permettrait de tester l'idée en quelques heures ?

### Bloc 4 — Données et connexions
- Quelles données l'outil utilise-t-il en entrée : mesures, plans SEMA, fichiers du scanner, articles, clients, stocks, heures… ?
- D'où viennent-elles : CID ERP, Excel, emails, NAS, saisie manuelle ?
- Que doit produire l'outil : documents, PDF, devis, listes de débit, fichiers pour la CNC, emails, tableaux de bord ?
- Faut-il **lire** dans CID ERP ou d'autres logiciels ? Faut-il y **écrire** ? (Écrire est plus risqué.)
- Y a-t-il des données personnelles ou sensibles : clients, salaires, adresses ?
- As-tu de **vraies données d'exemple** pour tester ? Ce point est obligatoire avant de coder.

### Bloc 5 — Usage concret
- Décris pas à pas une utilisation typique, du début à la fin.
- Quelle fréquence : plusieurs fois par jour, par semaine, par mois ?
- Combien de personnes l'utilisent en même temps ?
- L'outil doit-il fonctionner **sans internet** ?
- Quelles langues faut-il : français seulement, ou aussi allemand ?

### Bloc 6 — Choix techniques
*(Règle du §1 : options, puis recommandation, puis décision d'Antoine.)*
- Type d'application : web, application de bureau, application mobile, script, automatisation ?
- Langage et technologies.
- Hébergement : PC local, NAS, serveur Tebicom, cloud ?
- Stockage des données : fichier, base de données, CID ERP directement ?
- Connexion avec les apps maison existantes.
- Gestion des versions du code avec Git, et où le stocker : GitHub privé ou autre.
- Coûts récurrents : licences, hébergement, API.

### Bloc 7 — Qualité et mesure du succès
- Quels **critères chiffrés** prouvent que l'outil fonctionne ? Exemple : « le calcul tombe juste sur 20 escaliers réels déjà livrés ».
- Quel **jeu de test réel** utilise-t-on ? Il faut de vrais cas de l'atelier.
- Quelle marge d'erreur est acceptable ? Que se passe-t-il en cas d'erreur ?
- Rappel de méthode : **un résultat trop parfait doit être vérifié, pas célébré.**

### Bloc 8 — Sécurité, sauvegarde et maintenance
- Qui a accès à quoi ? Faut-il des mots de passe ou des rôles ?
- Comment les données et le code sont-ils sauvegardés : Tebicom, NAS ?
- **Si Antoine est absent 3 mois, qui fait tourner, corrige et met à jour l'outil ?**
- Faut-il impliquer Tebicom : hébergement, reprise, sécurité ?
- Que fait-on si l'outil tombe en panne un lundi matin ? Quelle solution de secours ?

### Bloc 9 — Budget, délais, priorités
- Combien de temps Antoine peut-il y consacrer par semaine ?
- Y a-t-il une date limite ou un événement déclencheur : saison, salon, arrivée de la CNC… ?
- Quel budget pour d'éventuels services payants ?
- Ce projet passe-t-il avant ou après les autres projets en cours ?

---

## 4. Validation (GO / NO GO)

À la fin de l'entretien, présente une **synthèse d'une page** :
1. le problème et l'objectif, chacun en une phrase ;
2. le niveau du projet (N1 à N4) ;
3. le périmètre de la version 1 et ce qui est hors projet ;
4. les choix techniques retenus ;
5. les critères de réussite ;
6. les 3 principaux risques ;
7. l'estimation des étapes.

Puis pose la question : **« GO pour générer les documents du projet ? »**
Sans GO explicite, tu ne crées rien d'autre que `docs/cadrage.md`.

---

## 5. Livrables à produire après le GO

| Fichier | Contenu |
|---|---|
| `CLAUDE.md` | Règles du projet, lues par Claude Code à chaque session (voir modèle §6). |
| `docs/cadrage.md` | Synthèse complète et journal des décisions D-01, D-02… |
| `docs/plan.md` | Phases : prototype jetable, puis V1 utile, puis V2. Pour chaque étape : objectif, livrable, critère « terminé ». |
| `docs/criteres-reussite.md` | Critères chiffrés et protocole de test. |
| `docs/donnees-test/` | Vrais cas d'exemple, anonymisés si nécessaire. |
| `docs/risques.md` | Risques, probabilité, impact, parade. |
| `docs/maintenance.md` | Fiche de passation : comment installer, lancer, sauvegarder, réparer ; contacts (Tebicom…) ; ce qu'il faut faire si Antoine est absent. |
| `README.md` | Présentation simple pour un humain : ce que fait l'outil, comment s'en servir. |
| `.claude/agents/` | Agents proposés selon le niveau du projet (voir §7). |

---

## 6. Modèle de `CLAUDE.md` à générer

```markdown
# [Nom du projet] — Escaliers Mauron

## But
[1 phrase]

## Utilisateurs et niveau
[Qui · N1 à N4]

## Périmètre V1
- Inclus : …
- Hors projet : …

## Choix techniques (décidés)
[Liste avec n° de décision]

## Données
[Sources · sensibles ou non · lecture/écriture]

## Règles de travail
- Avancer par petites étapes ; montrer le résultat à chaque étape.
- Pour toute nouvelle décision technique : options, puis recommandation, puis validation d'Antoine.
- Tester sur les vrais cas de docs/donnees-test/ avant de dire « c'est fait ».
- Jamais d'écriture dans CID ERP ou dans des données de production sans accord explicite.
- Commit Git à chaque étape réussie, avec un message clair en français.
- Mettre à jour docs/cadrage.md (décisions) et docs/maintenance.md au fil de l'eau.
- Expliquer en français clair, sans jargon.

## Critères de réussite
[Rappel court + lien vers docs/criteres-reussite.md]
```

---

## 7. Agents à proposer selon le niveau

- **N1** : aucun agent dédié, Claude Code seul suffit.
- **N2** : un **testeur**, qui vérifie chaque fonction sur les vrais cas.
- **N3** : un **testeur**, plus un **relecteur** (qualité du code, simplicité, documentation à jour), plus un **gardien des données** (vérifie toute opération qui touche à CID ERP ou aux données de production).
- **N4** : tout ce qui précède, plus un **agent sécurité / nLPD** et un **agent charte & expérience client** (respect de la charte Mauron, clarté pour le client).

Pour chaque agent, propose son rôle et ses règles en 3 lignes, et fais valider par Antoine avant de le créer.
