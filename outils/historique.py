#!/usr/bin/env python3
"""Fiche chiffrée par titre : où en est le cours par rapport à son passé (5 ans).
Usage : python3 outils/historique.py DOSSIER/titres.json DOSSIER/historique
Sources : bourse suisse (SIX) pour les titres cotés en Suisse, Twelve Data pour les actions américaines.
Écrit AAAA-MM-JJ.json (pour les programmes) et AAAA-MM-JJ.md (tableau pour les agents). Fichiers datés, jamais réécrits.
Limites : variations de cours hors dividendes ; ce sont des faits sur le passé, pas des prévisions."""
import json, sys, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import pstdev

ANNEES = 5
PERIODES = [("1 sem.", 7), ("1 mois", 30), ("3 mois", 91), ("1 an", 365), ("3 ans", 1096), ("5 ans", 1826)]


def lire(url):
    req = urllib.request.Request(url, headers={"User-Agent": "releve-prix-perso/1.0"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))


def cours_six(isin, monnaie, debut):
    q = urllib.parse.urlencode({"select": "ISIN,ClosingPrice", "where": f"ValorId={isin}{monnaie}4", "columns": "Date,Close",
                                "fromdate": debut.strftime("%Y%m%d"), "netting": 1440})
    d = lire(f"https://www.six-group.com/fqs/charts.json?{q}")["valors"][0]["data"]
    return [(datetime.strptime(str(j), "%Y%m%d").date(), float(c)) for j, c in zip(d["Date"], d["Close"]) if c]


def cours_us(code):
    d = lire("https://api.twelvedata.com/time_series?" + urllib.parse.urlencode({"symbol": code, "interval": "1day", "outputsize": 252 * ANNEES + 40}))
    if "values" not in d:
        raise ValueError(d.get("message", "réponse inattendue"))
    return sorted((datetime.strptime(v["datetime"], "%Y-%m-%d").date(), float(v["close"])) for v in d["values"])


def fiche(cours):
    """`cours` : liste (date, clôture) triée par date. Rend les chiffres de la fiche."""
    pct = lambda a, b: round((a / b - 1) * 100, 1)
    jour, dernier = cours[-1]
    f = {"date_cours": jour.isoformat(), "cours": dernier, "jours_de_bourse": len(cours), "variations_pct": {}}
    for nom, n in PERIODES:
        avant = [c for d, c in cours if d <= jour - timedelta(days=n)]
        # la période n'est donnée que si l'historique remonte assez loin
        f["variations_pct"][nom] = pct(dernier, avant[-1]) if avant and cours[0][0] <= jour - timedelta(days=n) else None
    an = [c for d, c in cours if d > jour - timedelta(days=365)]
    f["plus_haut_1_an"], f["plus_bas_1_an"] = max(an), min(an)
    f["ecart_au_plus_haut_1_an_pct"] = pct(dernier, max(an))
    f["ecart_au_plus_bas_1_an_pct"] = pct(dernier, min(an))
    f["ecart_au_plus_haut_5_ans_pct"] = pct(dernier, max(c for _, c in cours))
    var = [(an[i] / an[i - 1] - 1) * 100 for i in range(1, len(an))]
    f["variation_quotidienne_habituelle_pct"] = round(pstdev(var), 2) if len(var) > 20 else None
    sommet, pire = cours[0][1], 0.0
    for _, c in cours:
        sommet = max(sommet, c)
        pire = min(pire, (c / sommet - 1) * 100)
    f["plus_forte_baisse_5_ans_pct"] = round(pire, 1)
    return f


def main():
    titres = json.loads(Path(sys.argv[1]).read_text())
    sortie = Path(sys.argv[2])
    m = datetime.now(timezone.utc)
    debut = m.date() - timedelta(days=366 * ANNEES + 10)
    res = {"releve_utc": m.strftime("%Y-%m-%dT%H:%M:%SZ"), "annees": ANNEES, "titres": [], "erreurs": []}
    for t in titres:
        us = "code_us" in t
        cle = t.get("isin") or t.get("code_us")
        try:
            cours = cours_us(t["code_us"]) if us else cours_six(t["isin"], t["monnaie"], debut)
            if len(cours) < 30:
                raise ValueError("historique trop court")
            res["titres"].append({"nom": t["nom"], "id": cle, "source": "Twelve Data" if us else "SIX", **fiche(cours)})
        except Exception as e:
            res["erreurs"].append({"titre": cle, "erreur": str(e)})
        time.sleep(8 if us else 0.5)
    sortie.mkdir(parents=True, exist_ok=True)
    base = sortie / m.strftime("%Y-%m-%d")
    if base.with_suffix(".json").exists():
        sys.exit(f"Refus : la fiche du {m.strftime('%Y-%m-%d')} existe déjà.")
    base.with_suffix(".json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    v = lambda x: "—" if x is None else f"{x:+.1f}"
    lignes = [f"# Historique des cours au {m.strftime('%d.%m.%Y')} ({ANNEES} ans)", "",
              "Variations en %, hors dividendes. Faits sur le passé, pas des prévisions.", "",
              "| Titre | Cours | " + " | ".join(n for n, _ in PERIODES) + " | Écart au plus haut d'un an | Écart au plus bas d'un an | Écart au plus haut de 5 ans | Variation d'un jour habituelle | Plus forte baisse en 5 ans |",
              "|---|---|" + "---|" * (len(PERIODES) + 5)]
    for t in res["titres"]:
        lignes.append(f"| {t['nom']} | {t['cours']} | " + " | ".join(v(t["variations_pct"][n]) for n, _ in PERIODES) +
                      f" | {v(t['ecart_au_plus_haut_1_an_pct'])} | {v(t['ecart_au_plus_bas_1_an_pct'])} | {v(t['ecart_au_plus_haut_5_ans_pct'])} | "
                      f"± {t['variation_quotidienne_habituelle_pct']} | {v(t['plus_forte_baisse_5_ans_pct'])} |")
    for e in res["erreurs"]:
        lignes.append(f"\nHistorique indisponible pour {e['titre']} : {e['erreur']}")
    base.with_suffix(".md").write_text("\n".join(lignes) + "\n")
    print("\n".join(lignes[4:]))
    print(f"\n{len(res['titres'])} fiche(s), {len(res['erreurs'])} erreur(s) -> {base}.md")


if __name__ == "__main__":
    main()
