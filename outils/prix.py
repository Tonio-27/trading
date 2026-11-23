#!/usr/bin/env python3
"""Relevé des prix : bourse suisse (SIX), actions américaines (Twelve Data contrôlé par Finnhub),
taux de change (BCE).

Liste des titres : {"isin", "monnaie"} pour un titre coté en Suisse, {"code_us"} pour une action américaine.
Les clés des deux services américains sont ajoutées par l'environnement cloud « trading » ; elles ne sont pas dans ce dépôt.

Usage : python3 outils/prix.py outils/titres-test.json [dossier_de_sortie]
Écrit un fichier daté, jamais modifié ensuite. Aucun calcul de portefeuille ici.
"""
import json, sys, time, urllib.request, urllib.parse, re
from datetime import datetime, timezone
from pathlib import Path

SIX = "https://www.six-group.com/fqs/ref.json"
BCE = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
CHAMPS = "ShortName,ISIN,ValorSymbol,ClosingPrice,PreviousClosingPrice,OpeningPrice,TradingBaseCurrency,LatestTradeDate"


AGE_MAX_JOURS = 5  # un cours plus vieux que cela n'est pas utilisable (titre peu échangé, source en panne)


def lire(url, essais=2):
    req = urllib.request.Request(url, headers={"User-Agent": "releve-prix-perso/1.0"})
    for n in range(essais):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8")
        except Exception:
            if n == essais - 1:
                raise
            time.sleep(5)


def controler(p, aujourd_hui):
    """Ajoute les alertes et le verdict « utilisable ». Ne corrige jamais un prix."""
    alertes = []
    age = (aujourd_hui - datetime.strptime(p["date_cours"], "%Y%m%d").date()).days
    if age > AGE_MAX_JOURS:
        alertes.append(f"cours vieux de {age} jours")
    if p.get("cloture_precedente") and abs(p["cloture"] / p["cloture_precedente"] - 1) > 0.15:
        alertes.append("variation de plus de 15 % sur un jour : à vérifier avant toute opération")
    if "controle" in p:
        c = p["controle"]
        if c["ecart_pct"] >= ECART_MAX * 100:
            alertes.append(f"écart de {c['ecart_pct']} % entre les 2 sources")
        if c["ecart_ouverture_pct"] is None or c["ecart_ouverture_pct"] >= ECART_MAX * 100:
            alertes.append("prix d'ouverture non confirmé par la 2e source")
        if c["date_cours"] != p["date_cours"]:
            alertes.append("les 2 sources ne donnent pas le même jour de cours")
    p["alertes"] = alertes
    p["utilisable"] = not alertes          # le cours de clôture est fiable : on peut valoriser, analyser, prévoir
    # Exécuter un ordre demande en plus le prix d'ouverture du jour. La bourse suisse ne l'affiche que du jour même
    # jusqu'au lendemain matin tôt : il est donc normal qu'il manque au relevé de 7 h 45 et soit présent le soir.
    p["executable"] = p["utilisable"] and bool(p.get("ouverture"))
    return p


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


ECART_MAX = 0.005  # 0,5 % : au-delà, le prix n'est pas confirmé


def prix_us(code):
    q = urllib.parse.urlencode({"symbol": code})
    a = json.loads(lire(f"https://api.twelvedata.com/quote?{q}"))
    if "close" not in a:
        raise ValueError(f"Twelve Data : {a.get('message', 'réponse inattendue')}")
    b = json.loads(lire(f"https://finnhub.io/api/v1/quote?{q}"))
    if not b.get("c"):
        raise ValueError("Finnhub : prix absent")
    p1, p2 = float(a["close"]), float(b["c"])
    d1 = a["datetime"][:10].replace("-", "")
    d2 = datetime.fromtimestamp(b["t"], timezone.utc).strftime("%Y%m%d")
    ecart = abs(p1 - p2) / p1
    r = {
        "code": code, "monnaie": a.get("currency", "USD"),
        "cloture": round(p1, 4), "cloture_precedente": float(a["previous_close"]),
        "ouverture": float(a["open"]), "date_cours": d1,
        "source": "Twelve Data", "controle": {"source": "Finnhub", "cloture": p2, "ouverture": b.get("o"), "date_cours": d2,
                                               "ecart_pct": round(ecart * 100, 3),
                                               "ecart_ouverture_pct": round(abs(float(a["open"]) - float(b["o"])) / float(a["open"]) * 100, 3) if b.get("o") else None},
    }
    r["cloture_precedente"] = round(r["cloture_precedente"], 4)
    r["ouverture"] = round(r["ouverture"], 4)
    return r


def taux_bce():
    x = lire(BCE)
    date = re.search(r"time='([^']+)'", x).group(1)
    t = {m.group(1): float(m.group(2)) for m in re.finditer(r"currency='(\w+)' rate='([^']+)'", x)}
    # Taux BCE : 1 EUR = t[X]. On veut la valeur en CHF d'une unité de chaque monnaie.
    for m in ("CHF", "USD"):
        if not t.get(m) or t[m] <= 0:
            raise ValueError(f"taux {m} absent")
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
    aujourd_hui = maintenant.date()
    if res["change_en_chf"]:
        age = (aujourd_hui - datetime.strptime(res["change_en_chf"]["date"], "%Y-%m-%d").date()).days
        if age > AGE_MAX_JOURS:
            res["erreurs"].append({"quoi": "taux de change", "erreur": f"taux vieux de {age} jours : écarté"})
            res["change_en_chf"] = None  # un taux périmé n'est jamais utilisé
    for t in titres:
        us = "code_us" in t
        cle = t.get("isin") or t.get("code_us")
        try:
            p = prix_us(t["code_us"]) if us else prix_six(t["isin"], t["monnaie"])
            res["titres"].append({"nom": t["nom"], "id": cle, **controler(p, aujourd_hui)})
        except Exception as e:
            res["erreurs"].append({"quoi": t["nom"], "titre": cle, "erreur": str(e)})
        time.sleep(8 if us else 0.5)  # compte gratuit Twelve Data : 8 demandes par minute
    sortie.mkdir(parents=True, exist_ok=True)
    f = sortie / f"{maintenant.strftime('%Y-%m-%d_%H%M')}.json"
    if f.exists():
        sys.exit(f"Refus : {f} existe déjà (un relevé n'est jamais réécrit).")
    f.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
    for x in res["titres"]:
        print(f"{x['nom']:28} {x['code']:6} {x['cloture']:>10} {x['monnaie']}  ouverture {x['ouverture']}  ({x['date_cours']})" + (f"  contrôle {x['controle']['cloture']} écart {x['controle']['ecart_pct']} %" if "controle" in x else "") + ("" if x["utilisable"] else "  NON UTILISABLE : " + " ; ".join(x["alertes"])) + ("" if x["executable"] or not x["utilisable"] else "  (pas encore d'ouverture)"))
    print("Change en CHF :", res["change_en_chf"])
    ok = sum(1 for x in res["titres"] if x["utilisable"])
    ex = sum(1 for x in res["titres"] if x["executable"])
    print(f"{len(res['titres'])} prix relevés dont {ok} utilisables et {ex} exécutables, {len(res['erreurs'])} erreur(s) -> {f}")
    for e in res["erreurs"]:
        print("ERREUR", e)
    sys.exit(1 if res["erreurs"] else 0)


if __name__ == "__main__":
    main()
