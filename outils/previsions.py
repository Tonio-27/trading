#!/usr/bin/env python3
"""Notation des prévisions des agents : on note chaque scénario contre ce qui s'est réellement passé.

Chaque idée examinée (retenue ou non) est enregistrée avec ses 3 probabilités et ses 2 seuils. À l'échéance,
le programme regarde la variation réelle du cours et calcule une note. Fichiers en ajout seul.

  ajouter DOSSIER RELEVE --titre ID --nom NOM --horizon-jours N --seuil-haut X --seuil-bas Y
          --p-favorable A --p-neutre B --p-defavorable C --decision retenue|reduite|ecartee|bloquee [--note TEXTE]
      Favorable = variation ≥ seuil haut ; défavorable = variation ≤ seuil bas ; neutre = entre les deux.
      Le prix de départ est la clôture du relevé : l'agent ne le saisit pas.
  importer DOSSIER RELEVE FICHIER.md [FICHIER.md …] [--decision ID=retenue|reduite|ecartee|bloquee …]
      Lit dans les fichiers des agents les lignes « PRÉVISION : » et « PARI : » et les enregistre (voir plus bas).
  noter DOSSIER RELEVE     note les prévisions et les paris arrivés à échéance et affiche le bilan

Lignes lues par « importer » (une par ligne, format strict) :
  PRÉVISION : ID ; NOM ; horizon N jours ; favorable si ≥ +X % ; défavorable si ≤ −Y % ; probabilités A / B / C ; statut idee|ecartee|marche
      statut « idee » : idée proposée par l'analyste — le Gérant doit donner sa décision avec --decision ID=…
      statut « ecartee » : titre examiné puis écarté par l'analyste lui-même ; statut « marche » : prévision sur la référence.
  PARI : ID ; NOM ; hausse|baisse
      Pari du Veilleur sur la prochaine séance, noté contre la clôture suivante. Sur un ETF large (marché), « hausse » veut dire
      que le cours monte. Sur tout autre titre, « hausse » veut dire qu'il fait mieux que l'ETF de référence, « baisse » moins bien.

Note de Brier : somme des carrés des écarts entre les probabilités annoncées et ce qui est arrivé.
0 = prévision parfaite ; 0.67 = prévision au hasard (un tiers partout) ; 2 = certitude totale et fausse.
"""
import argparse, fcntl, json, re, sys
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import compta

SCENARIOS = ("favorable", "neutre", "defavorable")
# Paris « de marché » : jugés dans l'absolu. Tout autre titre est jugé par rapport à l'ETF de référence.
ETF_MARCHE = {"IE00B4L5Y983", "IE00B5BMR087", "IE00B53L3W79"}
REFERENCE = "IE00B4L5Y983"


def fiable(p):
    """Le cours de clôture est fiable (les relevés d'avant le 23.11.2026 comptaient l'ouverture absente comme une alerte)."""
    return bool(p) and (p["utilisable"] or p.get("alertes") == ["prix d'ouverture absent"])


def lire(f):
    return [json.loads(l) for l in f.read_text().splitlines() if l.strip()] if f.exists() else []


def ajouter_ligne(f, ligne):
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(f.parent / ".verrou", "w") as v:
        fcntl.flock(v, fcntl.LOCK_EX)
        with open(f, "a") as h:
            h.write(json.dumps(ligne, ensure_ascii=False) + "\n")


def jour(aaaammjj):
    return datetime.strptime(aaaammjj, "%Y%m%d").date()


DECISIONS = ("retenue", "reduite", "ecartee", "bloquee", "non_proposee", "marche")
NB = r"([+\-−]?\s*\d+(?:[.,]\d+)?)"
RE_PREV = re.compile(r"^\W*PR[ÉE]VISION\s*:\s*([^;]+);([^;]+);\s*horizon\s+(\d+)\s+jours?\s*;\s*favorable si\s*[≥>]=?\s*" + NB +
                     r"\s*%\s*;\s*d[ée]favorable si\s*[≤<]=?\s*" + NB + r"\s*%\s*;\s*probabilit[ée]s\s+(\d+)\s*/\s*(\d+)\s*/\s*(\d+)\s*;\s*statut\s+(idee|ecartee|marche)\W*$", re.I)
RE_PARI = re.compile(r"^\W*PARI\s*:\s*([^;]+);([^;]+);\s*(hausse|baisse)\W*$", re.I)
nombre = lambda t: float(t.replace(" ", "").replace("−", "-").replace(",", "."))


def enregistrer_prevision(dossier, releve, prix, titre, nom, horizon, haut, bas, probas, decision, note=""):
    """Rend True si la prévision est enregistrée, False si elle existait déjà. Lève Refus si elle est invalide."""
    p = prix.get(titre)
    if not fiable(p):
        raise compta.Refus(f"{titre} : titre absent du relevé ou prix non utilisable")
    if any(x < 0 for x in probas) or sum(probas) != 100:
        raise compta.Refus(f"{titre} : les trois probabilités doivent être positives et faire 100 au total")
    if not bas < 0 < haut or not 5 <= horizon <= 365:
        raise compta.Refus(f"{titre} : seuil bas négatif, seuil haut positif, horizon de 5 à 365 jours")
    f = Path(dossier) / "previsions.jsonl"
    deja = lire(f)
    if any((l["titre"], l["date_cours"], l["horizon_jours"]) == (titre, p["date_cours"], horizon) for l in deja):
        return False
    echeance = jour(p["date_cours"]) + timedelta(days=horizon)
    ajouter_ligne(f, {"id": f"P-{len(deja) + 1:04d}", "titre": titre, "nom": nom, "date_cours": p["date_cours"],
                      "prix_depart": p["cloture"], "monnaie": p["monnaie"], "horizon_jours": horizon,
                      "echeance": echeance.strftime("%Y%m%d"), "seuil_haut_pct": haut, "seuil_bas_pct": bas,
                      "p_favorable": probas[0], "p_neutre": probas[1], "p_defavorable": probas[2],
                      "decision": decision, "note": note, "releve": releve["_nom"],
                      "enregistre_utc": compta.maintenant().strftime("%Y-%m-%dT%H:%M:%SZ")})
    return True


def cmd_importer(a):
    releve, prix = compta.charger_releve(a.releve, [])
    decisions = dict(x.split("=", 1) for x in a.decision)
    previsions, paris, erreurs = [], [], []
    for fichier in a.fichiers:
        for n, ligne in enumerate(Path(fichier).read_text().splitlines(), 1):
            brut = ligne.strip().strip("`*").strip()
            if re.match(r"^\W*PR[ÉE]VISION\s*:", brut, re.I):
                m = RE_PREV.match(brut)
                if not m:
                    erreurs.append(f"{fichier}:{n} : ligne PRÉVISION mal formée")
                    continue
                titre, statut = m.group(1).strip(), m.group(9).lower()
                decision = {"ecartee": "non_proposee", "marche": "marche"}.get(statut) or decisions.get(titre)
                if decision not in DECISIONS:
                    erreurs.append(f"{fichier}:{n} : idée {titre} sans décision du Gérant (ajouter --decision {titre}=…)")
                    continue
                previsions.append((titre, m.group(2).strip(), int(m.group(3)), nombre(m.group(4)), nombre(m.group(5)),
                                   [int(m.group(6)), int(m.group(7)), int(m.group(8))], decision))
            elif re.match(r"^\W*PARI\s*:", brut, re.I):
                m = RE_PARI.match(brut)
                if not m:
                    erreurs.append(f"{fichier}:{n} : ligne PARI mal formée")
                    continue
                paris.append((m.group(1).strip(), m.group(2).strip(), m.group(3).lower()))
    for pr in previsions:
        try:
            if not fiable(prix.get(pr[0])) or sum(pr[5]) != 100 or not pr[4] < 0 < pr[3] or not 5 <= pr[2] <= 365:
                raise compta.Refus("valeurs invalides ou prix non utilisable")
        except compta.Refus as e:
            erreurs.append(f"prévision {pr[0]} : {e}")
    if erreurs:   # tout ou rien : on ne garde pas un import à moitié fait
        raise compta.Refus("import refusé, rien n'est enregistré :\n  " + "\n  ".join(erreurs))
    np_ = sum(enregistrer_prevision(a.dossier, releve, prix, *pr) for pr in previsions)
    f = Path(a.dossier) / "paris.jsonl"
    deja, npa = lire(f), 0
    for titre, nom, sens in paris:
        p = prix.get(titre)
        if not fiable(p) or any((l["titre"], l["date_cours"]) == (titre, p["date_cours"]) for l in deja + lire(f)):
            continue
        ref = prix.get(REFERENCE)
        relatif = titre not in ETF_MARCHE and fiable(ref) and ref["date_cours"] == p["date_cours"]
        ajouter_ligne(f, {"id": f"V-{len(lire(f)) + 1:04d}", "titre": titre, "nom": nom, "sens": sens,
                          "type": "relatif" if relatif else "marche",
                          "date_cours": p["date_cours"], "prix_depart": p["cloture"],
                          **({"reference_depart": ref["cloture"]} if relatif else {}), "releve": releve["_nom"]})
        npa += 1
    print(f"Import : {np_} prévision(s) nouvelle(s) sur {len(previsions)} lue(s), {npa} pari(s) nouveau(x) sur {len(paris)} lu(s).")


def noter_paris(d, releve, prix):
    notes = {l["id"] for l in lire(d / "paris-notes.jsonl")}
    for pa in lire(d / "paris.jsonl"):
        p = prix.get(pa["titre"])
        if pa["id"] in notes or not fiable(p) or p["date_cours"] <= pa["date_cours"]:
            continue
        var = lambda fin, debut: (Decimal(str(fin)) / Decimal(str(debut)) * 100 - 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        variation = var(p["cloture"], pa["prix_depart"])
        extra = {}
        if pa.get("type") == "relatif":
            ref = prix.get(REFERENCE)
            if not fiable(ref) or ref["date_cours"] != p["date_cours"]:
                continue   # on attend un relevé où le titre et la référence ont un cours du même jour
            ecart = variation - var(ref["cloture"], pa["reference_depart"])
            extra = {"variation_reference_pct": str(var(ref["cloture"], pa["reference_depart"])), "variation_relative_pct": str(ecart)}
            juste = ecart > 0 if pa["sens"] == "hausse" else ecart < 0
        else:
            juste = variation > 0 if pa["sens"] == "hausse" else variation < 0
        ajouter_ligne(d / "paris-notes.jsonl", {"id": pa["id"], "titre": pa["titre"], "nom": pa["nom"], "sens": pa["sens"],
                      "type": pa.get("type", "absolu"), "date_cours_fin": p["date_cours"], "variation_pct": str(variation), **extra,
                      "juste": juste, "releve": releve["_nom"]})
    tous = lire(d / "paris-notes.jsonl")
    for t, nom in (("relatif", "sur des titres, par rapport au marché"), ("marche", "sur le marché (ETF larges)"), ("absolu", "anciens, dans l'absolu (avant le 28.11.2026)")):
        g = [n for n in tous if n.get("type", "absolu") == t]
        if g:
            print(f"Paris du Veilleur {nom} : {sum(n['juste'] for n in g)} juste(s) sur {len(g)} (le hasard donnerait environ la moitié).")


def cmd_ajouter(a):
    releve, prix = compta.charger_releve(a.releve, [])
    p = prix.get(a.titre)
    if not fiable(p):
        raise compta.Refus("titre absent du relevé ou prix non utilisable")
    probas = [a.p_favorable, a.p_neutre, a.p_defavorable]
    if any(x < 0 for x in probas) or sum(probas) != 100:
        raise compta.Refus("les trois probabilités doivent être positives et faire 100 au total")
    if not a.seuil_bas < 0 < a.seuil_haut or not 5 <= a.horizon_jours <= 365:
        raise compta.Refus("seuil bas négatif, seuil haut positif, horizon de 5 à 365 jours")
    f = Path(a.dossier) / "previsions.jsonl"
    deja = lire(f)
    if any((l["titre"], l["date_cours"], l["horizon_jours"]) == (a.titre, p["date_cours"], a.horizon_jours) for l in deja):
        raise compta.Refus("une prévision existe déjà pour ce titre, cette date de cours et cet horizon")
    echeance = jour(p["date_cours"]) + timedelta(days=a.horizon_jours)
    ajouter_ligne(f, {"id": f"P-{len(deja) + 1:04d}", "titre": a.titre, "nom": a.nom, "date_cours": p["date_cours"],
                      "prix_depart": p["cloture"], "monnaie": p["monnaie"], "horizon_jours": a.horizon_jours,
                      "echeance": echeance.strftime("%Y%m%d"), "seuil_haut_pct": a.seuil_haut, "seuil_bas_pct": a.seuil_bas,
                      "p_favorable": a.p_favorable, "p_neutre": a.p_neutre, "p_defavorable": a.p_defavorable,
                      "decision": a.decision, "note": a.note, "releve": releve["_nom"],
                      "enregistre_utc": compta.maintenant().strftime("%Y-%m-%dT%H:%M:%SZ")})
    print(f"Prévision enregistrée : {a.nom}, départ {p['cloture']} {p['monnaie']}, échéance le {echeance.isoformat()}.")


def cmd_noter(a):
    releve, prix = compta.charger_releve(a.releve, [])
    d = Path(a.dossier)
    notees = {l["id"] for l in lire(d / "previsions-notes.jsonl")}
    for pr in lire(d / "previsions.jsonl"):
        p = prix.get(pr["titre"])
        if pr["id"] in notees or not fiable(p) or p["date_cours"] < pr["echeance"]:
            continue
        variation = (Decimal(str(p["cloture"])) / Decimal(str(pr["prix_depart"])) * 100 - 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        arrive = "favorable" if variation >= Decimal(str(pr["seuil_haut_pct"])) else "defavorable" if variation <= Decimal(str(pr["seuil_bas_pct"])) else "neutre"
        brier = sum((Decimal(pr[f"p_{s}"]) / 100 - (1 if s == arrive else 0)) ** 2 for s in SCENARIOS)
        plus_probable = max(SCENARIOS, key=lambda s: pr[f"p_{s}"])
        ajouter_ligne(d / "previsions-notes.jsonl", {"id": pr["id"], "titre": pr["titre"], "nom": pr["nom"], "decision": pr["decision"],
                      "date_cours_fin": p["date_cours"], "prix_fin": p["cloture"], "variation_pct": str(variation), "arrive": arrive,
                      "plus_probable_annonce": plus_probable, "juste": plus_probable == arrive,
                      "brier": str(brier.quantize(Decimal("0.0001"))), "releve": releve["_nom"]})
        print(f"{pr['id']} {pr['nom']} : {variation} % → scénario {arrive} ; annoncé le plus probable : {plus_probable} ; note {brier.quantize(Decimal('0.0001'))}")
    noter_paris(d, releve, prix)
    notes = lire(d / "previsions-notes.jsonl")
    en_cours = len(lire(d / "previsions.jsonl")) - len(notes)
    if not notes:
        print(f"Aucune prévision arrivée à échéance pour l'instant ({en_cours} en cours).")
        return
    moyenne = sum(Decimal(n["brier"]) for n in notes) / len(notes)
    print(f"Bilan : {len(notes)} prévision(s) notée(s), {sum(n['juste'] for n in notes)} juste(s), note moyenne {moyenne.quantize(Decimal('0.01'))} "
          f"(0 = parfait, 0.67 = hasard) ; {en_cours} en cours.")
    noms = {"retenue": "idées retenues", "reduite": "idées réduites", "ecartee": "idées écartées par le Gérant", "bloquee": "idées bloquées",
            "non_proposee": "titres écartés par l'analyste", "marche": "prévisions sur la référence"}
    for dec, nom in noms.items():
        g = [n for n in notes if n["decision"] == dec]
        if g:
            m = sum(Decimal(n["variation_pct"]) for n in g) / len(g)
            b = sum(Decimal(n["brier"]) for n in g) / len(g)
            print(f"  {nom} : {len(g)}, {sum(n['juste'] for n in g)} juste(s), note {b.quantize(Decimal('0.01'))}, variation moyenne ensuite {m.quantize(Decimal('0.01'))} %")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Notation des prévisions")
    sp = ap.add_subparsers(dest="commande", required=True)
    p = sp.add_parser("ajouter"); p.add_argument("dossier"); p.add_argument("releve")
    p.add_argument("--titre", required=True); p.add_argument("--nom", required=True)
    p.add_argument("--horizon-jours", type=int, required=True)
    p.add_argument("--seuil-haut", type=float, required=True); p.add_argument("--seuil-bas", type=float, required=True)
    for s in SCENARIOS:
        p.add_argument(f"--p-{s}", type=int, required=True)
    p.add_argument("--decision", choices=DECISIONS, required=True)
    p.add_argument("--note", default="")
    p = sp.add_parser("importer"); p.add_argument("dossier"); p.add_argument("releve"); p.add_argument("fichiers", nargs="+")
    p.add_argument("--decision", action="append", default=[])
    p = sp.add_parser("noter"); p.add_argument("dossier"); p.add_argument("releve")
    a = ap.parse_args(argv)
    try:
        {"ajouter": cmd_ajouter, "importer": cmd_importer, "noter": cmd_noter}[a.commande](a)
    except compta.Refus as e:
        sys.exit(f"REFUS : {e}")
    except (ValueError, KeyError, FileNotFoundError) as e:
        sys.exit(f"REFUS : donnée invalide ou manquante ({type(e).__name__} : {e})")


if __name__ == "__main__":
    main()
