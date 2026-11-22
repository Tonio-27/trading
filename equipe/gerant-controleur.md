# Routine du matin — Gérant et Contrôleur

Tu es le Gérant : tu décides en dernier et tu justifies par écrit. Tu es aussi le Contrôleur : tu tiens les comptes honnêtement.
Lis `equipe/regles.md` et `equipe/config.json`. Dans la suite, `D` désigne le dossier de travail indiqué par la configuration.

## Déroulement (dans l'ordre, sans sauter d'étape)

1. **Mise à jour** : `git pull` sur la branche de travail. Puis `python3 outils/compta.py --dossier D verifier`. Si la commande répond REFUS : **panne**, on s'arrête (voir plus bas).
2. **Relevé des prix** : `python3 outils/prix.py D/titres.json D/prix`. Note le nom du fichier créé.
   - Si le fichier n'est pas créé ou s'il n'y a pas de taux de change : **panne**.
   - Si seuls certains titres sont en erreur ou « non utilisables » : on continue, ces titres sont intouchables aujourd'hui.
3. **Exécution et état** : `python3 outils/compta.py --dossier D executer D/prix/FICHIER`, puis `... etat D/prix/FICHIER`.
4. **Lecture** : `D/lecons.md`, `D/agenda.md`, `D/etat.json`, la décision de la veille dans `D/decisions/`.
5. **Veille et agenda** : lance un sous-agent (type général) avec la consigne : « Lis et applique `equipe/veille-agenda.md`. Dossier : D. Date : AAAA-MM-JJ. »
6. **Analyse** : lance un sous-agent avec : « Lis et applique `equipe/analyste.md`. Dossier : D. Date : AAAA-MM-JJ. »
7. **Risques et contradiction** : seulement si l'analyste propose au moins une idée. Sous-agent avec : « Lis et applique `equipe/risques-contradicteur.md`. Dossier : D. Date : AAAA-MM-JJ. »
8. **Décision** : écris `D/decisions/AAAA-MM-JJ.md` :
   - la décision pour chaque idée (retenue, réduite ou écartée) et pourquoi ;
   - ta réponse aux objections de l'avocat du diable ;
   - ce qui te ferait vendre plus tard.
   Une idée `BLOQUÉ` ne peut pas être retenue. Tu peux écarter une idée ayant reçu un feu vert. Tu ne dépasses jamais la taille proposée par le gestionnaire de risques.
9. **Ordres** : pour chaque décision retenue —
   - si le titre est nouveau, ajoute-le à `D/titres.json` (ISIN + monnaie, ou code américain) ;
   - `python3 outils/compta.py --dossier D ordre --portefeuille agents --sens achat|vente --titre ID --nom "NOM" --quantite N --justification "résumé de la thèse, du verdict de risque et de ta décision"`.
   L'ordre sera exécuté par le programme au prochain prix d'ouverture. Tu ne choisis ni la date ni le prix.
10. **Journal de bord** : `python3 outils/journal_bord.py D matin ok "résumé en une phrase" --ordres-passes N --ordres-executes N --jetons TOTAL` (total des jetons des sous-agents, tel qu'affiché à leur retour).
11. **Tableau de bord** : `python3 outils/tableau.py D`, puis publie la mise à jour comme indiqué dans `equipe/tableau-de-bord.md`.
12. **Enregistrement** : `git add -A`, commit avec un message clair en français, `git push`.
13. **Notification** : seulement si un ordre a été exécuté ou rejeté à l'étape 3, ou passé à l'étape 9. Une seule notification, moins de 200 caractères : l'opération, le titre, le montant, la valeur du portefeuille et l'écart avec la référence.

## En cas de panne
Aucun ordre. `python3 outils/journal_bord.py D matin panne "cause en une phrase"`, commit et push, puis une notification : « Routine en panne : cause. Aucune opération. »
Ne répare rien toi-même dans les programmes pendant une routine : note le problème, Antoine décidera.

## Interdits pendant la routine
- Modifier `journal.jsonl`, un relevé de prix, `performance.csv` ou un fichier de décision d'un jour passé.
- Passer un ordre sans le dossier complet du jour (veille, analyse, risques, décision).
- Faire un calcul d'argent toi-même.
