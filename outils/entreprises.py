#!/usr/bin/env python3
"""Résultats et actualités des actions américaines suivies (source : Finnhub, compte gratuit).
Usage : python3 outils/entreprises.py DOSSIER/titres.json DOSSIER/entreprises
Pour chaque titre : les 4 derniers résultats trimestriels (attendu, publié, surprise en %), la prochaine date de
résultats dans les 45 jours, et les titres de presse des 3 derniers jours. Fichier daté, jamais réécrit.
Les titres cotés en Suisse ne sont pas couverts : pour eux, voir cash.ch et allnews.ch."""
import json, sys, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path


def appel(chemin, **params):
    url = f"https://finnhub.io/api/v1/{chemin}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "releve-prix-perso/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read().decode("utf-8"))
    time.sleep(1.1)  # compte gratuit : 60 demandes par minute
    return d


def main():
    titres = [t for t in json.loads(Path(sys.argv[1]).read_text()) if "code_us" in t]
    sortie = Path(sys.argv[2])
    m = datetime.now(timezone.utc)
    jour = lambda d: d.strftime("%Y-%m-%d")
    res = {"releve_utc": m.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "Finnhub", "entreprises": [], "erreurs": []}
    for t in titres:
        c = t["code_us"]
        try:
            resultats = [{"trimestre_clos_le": r.get("period"), "benefice_par_action_attendu": r.get("estimate"),
                          "benefice_par_action_publie": r.get("actual"), "surprise_pct": r.get("surprisePercent")}
                         for r in appel("stock/earnings", symbol=c)[:4]]
            cal = appel("calendar/earnings", symbol=c, **{"from": jour(m), "to": jour(m + timedelta(days=45))}).get("earningsCalendar", [])
            presse = appel("company-news", symbol=c, **{"from": jour(m - timedelta(days=3)), "to": jour(m)})
            res["entreprises"].append({
                "nom": t["nom"], "code": c, "derniers_resultats": resultats,
                "prochains_resultats": sorted(x["date"] for x in cal if x.get("date"))[:1] or None,
                "presse_3_jours": [{"date": datetime.fromtimestamp(n["datetime"], timezone.utc).strftime("%Y-%m-%d %H:%M"),
                                    "source": n.get("source"), "titre": n.get("headline"), "resume": (n.get("summary") or "")[:300]}
                                   for n in presse[:8]]})
        except Exception as e:
            res["erreurs"].append({"titre": c, "erreur": str(e)})
    sortie.mkdir(parents=True, exist_ok=True)
    f = sortie / f"{m.strftime('%Y-%m-%d_%H%M')}.json"
    if f.exists():
        sys.exit(f"Refus : {f} existe déjà.")
    f.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    for e in res["entreprises"]:
        d = e["derniers_resultats"][0] if e["derniers_resultats"] else {}
        print(f"{e['nom']:20} dernier trimestre : surprise {d.get('surprise_pct')} %  prochains résultats : {e['prochains_resultats']}  presse : {len(e['presse_3_jours'])} titre(s)")
    print(f"{len(res['entreprises'])} entreprise(s), {len(res['erreurs'])} erreur(s) -> {f}")


if __name__ == "__main__":
    main()
