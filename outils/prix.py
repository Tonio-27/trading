#!/usr/bin/env python3
"""Relevé des prix à la bourse suisse (SIX) et des taux de change (BCE).

Usage : python3 outils/prix.py outils/titres-test.json [dossier_de_sortie]
Écrit un fichier daté, jamais modifié ensuite. Aucun calcul de portefeuille ici.
"""
import json, sys, time, urllib.request, urllib.parse, re
from datetime import datetime, timezone
from pathlib import Path

SIX = "https://www.six-group.com/fqs/ref.json"
BCE = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
CHAMPS = "ShortName,ISIN,ValorSymbol,ClosingPrice,PreviousClosingPrice,OpeningPrice,TradingBaseCurrency,LatestTradeDate"


def lire(url):
    req = urllib.request.Request(url, headers={"User-Agent": "releve-prix-perso/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def prix_six(isin, monnaie):
    q = urllib.parse.urlencode({"select": CHAMPS, "where": f"ISIN={isin}", "pagesize": 20})
    d = json.loads(lire(f"{SIX}?{q}"))
    lignes = [dict(zip(d["colNames"], r)) for r in d.get("rowData", [])]
    lignes = [l for l in lignes if l["TradingBaseCurrency"] == monnaie]
    if not lignes:
        raise ValueError(f"aucune cotation en {monnaie}")
    l = max(lignes, key=lambda x: x["LatestTradeDate"] or 0)
    if not isinstance(l["ClosingPrice"], (int, float)) or l["ClosingPrice"] <= 0:
        raise ValueError("prix de clôture absent")
    return {
        "code": l["ValorSymbol"], "nom_six": l["ShortName"], "monnaie": monnaie,
        "cloture": l["ClosingPrice"], "cloture_precedente": l["PreviousClosingPrice"] or None,
        "ouverture": l["OpeningPrice"] or None, "date_cours": str(l["LatestTradeDate"]),
        "source": "SIX (différé 15 min)",
    }


def taux_bce():
    x = lire(BCE)
    date = re.search(r"time='([^']+)'", x).group(1)
    t = {m.group(1): float(m.group(2)) for m in re.finditer(r"currency='(\w+)' rate='([^']+)'", x)}
    # Taux BCE : 1 EUR = t[X]. On veut la valeur en CHF d'une unité de chaque monnaie.
    return {"date": date, "source": "BCE (taux de référence)",
            "CHF": 1.0, "EUR": round(t["CHF"], 6), "USD": round(t["CHF"] / t["USD"], 6)}


def main():
    titres = json.loads(Path(sys.argv[1]).read_text())
    sortie = Path(sys.argv[2] if len(sys.argv) > 2 else "donnees/prix")
    maintenant = datetime.now(timezone.utc)
    res = {"releve_utc": maintenant.strftime("%Y-%m-%dT%H:%M:%SZ"), "change_en_chf": None, "titres": [], "erreurs": []}
    try:
        res["change_en_chf"] = taux_bce()
    except Exception as e:
        res["erreurs"].append({"quoi": "taux de change", "erreur": str(e)})
    for t in titres:
        try:
            p = prix_six(t["isin"], t["monnaie"])
            # Contrôle de cohérence : un saut de plus de 15 % en un jour est signalé, pas corrigé.
            if p["cloture_precedente"] and abs(p["cloture"] / p["cloture_precedente"] - 1) > 0.15:
                p["alerte"] = "variation de plus de 15 % sur un jour : à vérifier avant toute opération"
            res["titres"].append({"nom": t["nom"], "isin": t["isin"], **p})
        except Exception as e:
            res["erreurs"].append({"quoi": t["nom"], "isin": t["isin"], "erreur": str(e)})
        time.sleep(0.5)
    sortie.mkdir(parents=True, exist_ok=True)
    f = sortie / f"{maintenant.strftime('%Y-%m-%d_%H%M')}.json"
    if f.exists():
        sys.exit(f"Refus : {f} existe déjà (un relevé n'est jamais réécrit).")
    f.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
    for x in res["titres"]:
        print(f"{x['nom']:28} {x['code']:6} {x['cloture']:>10} {x['monnaie']}  ouverture {x['ouverture']}  ({x['date_cours']})" + ("  ALERTE" if "alerte" in x else ""))
    print("Change en CHF :", res["change_en_chf"])
    print(f"{len(res['titres'])} prix relevés, {len(res['erreurs'])} erreur(s) -> {f}")
    for e in res["erreurs"]:
        print("ERREUR", e)
    sys.exit(1 if res["erreurs"] else 0)


if __name__ == "__main__":
    main()
