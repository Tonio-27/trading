# Mettre à jour le tableau de bord

Adresse : voir `tableau_de_bord` dans `equipe/config.json`. Page privée d'Antoine (type « Data » de Claude).
La page elle-même ne change pas d'un jour à l'autre : seul son fichier de données est remplacé. `D` est le dossier de travail.

1. `python3 outils/tableau.py D` → crée `D/tableau.json`.
2. Envoie ce fichier dans la page : outil `Artifact`, avec `url` = l'adresse, `file_path` = le chemin complet de `D/tableau.json`, `asset: true`. La réponse donne une adresse du type `/_blob/…`.
3. Lis la version des 4 sources : outil `ArtifactData`, `action: "list"`, `collection: "datasets"`.
4. Mets à jour les 4 sources en un seul envoi : `ArtifactData`, `action: "batch"`, avec pour chacun des documents `resume`, `performance`, `positions`, `operations` de la collection `datasets` une écriture `update` portant `if_version` (la version lue) et les données
   `{"source": {"url": "/_blob/…"}, "updated": {"at": "AAAA-MM-JJTHH:MM:SSZ", "by": "Routine des agents"}}`.
5. Supprime l'ancien fichier de données de la page (outil `Artifact`, `action: "delete"`, `url`, `path` = l'ancien identifiant, c'est-à-dire les 32 caractères après `/_blob/` dans l'ancienne adresse lue à l'étape 3).

Si une de ces étapes échoue, ce n'est **pas** une panne de la routine : note-le dans le résumé du journal de bord et continue. Les comptes font foi, pas la page.
La page (mise en forme, textes) est conservée dans `tableau-de-bord/index.html` ; elle ne se modifie que sur demande d'Antoine.
