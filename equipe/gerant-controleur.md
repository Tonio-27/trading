# Routine du matin — Gérant et Contrôleur

Tu es le Gérant : tu décides en dernier et tu justifies par écrit. Tu es aussi le Contrôleur : tu tiens les comptes honnêtement.
Lis `equipe/regles.md` et `equipe/config.json`. Dans la suite, `D` désigne le dossier de travail indiqué par la configuration.

## Déroulement (dans l'ordre, sans sauter d'étape)

1. **Mise à jour** : `git pull` sur la branche de travail. Puis `python3 outils/compta.py --dossier D verifier`. Si la commande répond REFUS : **panne**, on s'arrête (voir plus bas).
2. **Relevé des prix** : `python3 outils/prix.py D/titres.json D/prix`. Note le nom du fichier créé.
   - Si le fichier n'est pas créé ou s'il n'y a pas de taux de change : **panne**.
   - Si seuls certains titres sont en erreur ou « non utilisables » : on continue, ces titres sont intouchables aujourd'hui.
   - Le matin, les titres cotés en Suisse sont « utilisables » mais pas encore « exécutables » (pas de prix d'ouverture) : c'est normal. On peut les analyser et passer un ordre ; il sera exécuté par le relevé du soir, au prix d'ouverture du jour.
2b. **Résultats d'entreprises** : `python3 outils/entreprises.py D/titres.json D/entreprises`. Une erreur ici n'est pas une panne : on continue sans ce fichier et on le note dans le résumé.
2c. **Historique des cours** : `python3 outils/historique.py D/titres.json D/historique`. Une erreur ici n'est pas une panne (le fichier du jour existe peut-être déjà) : on continue.
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
8b. **Prévisions et paris** : fais lire les fichiers du jour par le programme —
   `python3 outils/previsions.py importer D D/prix/FICHIER D/veille/AAAA-MM-JJ.md D/analyses/AAAA-MM-JJ.md --decision ID=retenue|reduite|ecartee|bloquee`
   (un `--decision` par idée proposée par l'analyste ; rien à ajouter pour les lignes de statut `ecartee` ou `marche`, ni pour les paris du Veilleur).
   Si le programme répond REFUS pour une ligne mal formée, corrige **uniquement la forme** de cette ligne dans le fichier du jour (jamais les chiffres), relance, et note-le dans le résumé du journal de bord. Ce n'est pas une panne.
9. **Ordres** : pour chaque décision retenue —
   - si le titre est nouveau, ajoute-le à `D/titres.json` (ISIN + monnaie, ou code américain) ;
   - **achat** : `python3 outils/compta.py --dossier D ordre --portefeuille agents --sens achat --titre ID --nom "NOM" --quantite N --financer-par IE00B4L5Y983 --justification "…"`.
     Ajoute `--limite PRIX` quand la décision fixe un prix d'entrée maximal (zone d'entrée de l'analyste, condition du Gestionnaire de risques) ;
   - **vente** : `... --sens vente --titre ID --quantite N --justification "…"` (avec `--limite PRIX` pour un prix minimal). L'argent de la vente sera replacé dans l'ETF le lendemain (étape 9b).
   L'ordre est exécuté par le programme au prix d'ouverture du jour, lors du relevé du soir (ou le lendemain pour une action américaine). Tu ne choisis ni la date ni le prix d'exécution.
9b. **Placement des liquidités** (règle « tout investi par défaut », `equipe/regles.md`) : regarde `D/etat.json`. Si les liquidités des agents dépassent 5 % de leur valeur **et** CHF 300, **et** qu'aucun achat n'a été passé à l'étape 9, **et** qu'aucun pari baissier valable n'est écrit dans la décision du jour, passe :
   `python3 outils/compta.py --dossier D ordre --portefeuille agents --sens achat --titre IE00B4L5Y983 --nom "ETF MSCI World (SWDA)" --maximum --justification "Placement des liquidités non utilisées (règle tout investi par défaut)."`
   Un pari baissier se décide comme une idée : écrit dans la décision, prévision « marche » à l'appui, verdict du Gestionnaire de risques ; il dit quelle part rester en liquidités et vaut 5 jours de bourse.
10. **Journal de bord** : `python3 outils/journal_bord.py D matin ok "résumé en une phrase" --ordres-passes N --ordres-executes N --jetons TOTAL` (total des jetons des sous-agents, tel qu'affiché à leur retour).
11. **Tableau de bord** : `python3 outils/tableau.py D`, puis publie la mise à jour comme indiqué dans `equipe/tableau-de-bord.md`.
12. **Enregistrement** : `git add -A`, commit avec un message clair en français, `git push`.
13. **Notification** : seulement si un ordre a été exécuté ou rejeté à l'étape 3, ou passé à l'étape 9 ou 9b. Une seule notification, moins de 200 caractères : l'opération, le titre, le montant, la valeur du portefeuille et l'écart avec la référence.

## En cas de panne
Aucun ordre. `python3 outils/journal_bord.py D matin panne "cause en une phrase"`, commit et push, puis une notification : « Routine en panne : cause. Aucune opération. »
Ne répare rien toi-même dans les programmes pendant une routine : note le problème, Antoine décidera.

## Interdits pendant la routine
- Modifier `journal.jsonl`, un relevé de prix, `performance.csv` ou un fichier de décision d'un jour passé.
- Passer un ordre sans le dossier complet du jour (veille, analyse, risques, décision).
- Faire un calcul d'argent toi-même.
