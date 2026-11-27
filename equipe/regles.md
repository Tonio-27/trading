# Règles communes à tous les rôles

Argent **fictif**. Aucun ordre réel, aucune connexion à un courtier.

## Règles fixes (jamais discutées)
- Pas d'effet de levier, pas de produits dérivés, pas de vente à découvert, pas de crypto.
- Achats permis : ETF et actions de **grandes entreprises** (dans un grand indice : SMI, S&P 100, Nasdaq 100). Or via ETF.
- Titres achetables : uniquement ceux que le programme sait relever — cotés à la bourse suisse (par ISIN) ou actions américaines (par code). L'Europe s'achète via des ETF cotés en Suisse.
- Nombres entiers de titres.

## Tout investi par défaut (D-66)
- L'argent qui ne sert à aucune idée est placé dans l'ETF de référence (`IE00B4L5Y983`). Les agents partent ainsi à égalité avec la référence : seules leurs idées font la différence.
- Une idée d'achat est financée par la vente d'une partie de cet ETF (le programme calcule lui-même combien de parts vendre).
- Garder plus de 5 % du portefeuille en liquidités est un **pari baissier** : il doit être écrit dans la décision du jour, appuyé par une prévision « marche » où le scénario défavorable est plus probable que le favorable, et accepté par le Gestionnaire de risques. Il vaut 5 jours de bourse, puis doit être renouvelé.

## Honnêteté
- Les agents ne calculent rien : valeur, frais, change et performance viennent de `outils/compta.py`.
- Aucun prix cité de mémoire. Un prix vient du relevé du jour (`<dossier>/prix/`), avec sa date.
- Le journal ne se modifie jamais. Une erreur se corrige par une nouvelle ligne, jamais en retouchant le passé.
- Les pertes et les erreurs sont écrites telles quelles.
- Une information importante (résultat d'entreprise, décision de banque centrale) doit être confirmée par 2 sources avant de fonder une décision. Chaque fait cité porte sa source et sa date.

## Esprit
- Objectif : battre l'ETF MSCI World d'au moins 2 points sur 6 mois, frais compris.
- « Ne rien faire » est la décision normale. Une opération doit justifier que le gain espéré dépasse nettement ses frais (compter CHF 5 à 7 par ordre, soit un aller-retour d'environ CHF 12).
- Horizon : semaines à mois. Pas d'achat-vente dans la journée.
- Écrire en français clair, sans jargon. Court.
