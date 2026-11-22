#!/usr/bin/env python3
"""Notation des prévisions des agents : on note chaque scénario contre ce qui s'est réellement passé.

Chaque idée examinée (retenue ou non) est enregistrée avec ses 3 probabilités et ses 2 seuils. À l'échéance,
le programme regarde la variation réelle du cours et calcule une note. Fichiers en ajout seul.

  ajouter DOSSIER RELEVE --titre ID --nom NOM --horizon-jours N --seuil-haut X --seuil-bas Y
          --p-favorable A --p-neutre B --p-defavorable C --decision retenue|reduite|ecartee|bloquee [--note TEXTE]
      Favorable = variation ≥ seuil haut ; défavorable = variation ≤ seuil bas ; neutre = entre les deux.
      Le prix de départ est la clôture du relevé : l'agent ne le saisit pas.
  noter DOSSIER RELEVE     note les prévisions arrivées à échéance et affiche le bilan

Note de Brier : somme des carrés des écarts entre les probabilités annoncées et ce qui est arrivé.
0 = prévision parfaite ; 0.67 = prévision au hasard (un tiers partout) ; 2 = certitude totale et fausse.
"""
import argparse, fcntl, json, sys
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import compta

SCENARIOS = ("favorable", "neutre", "defavorable")


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


def cmd_ajouter(a):
    releve, prix = compta.charger_releve(a.releve, [])
    p = prix.get(a.titre)
    if not p or not p["utilisable"]:
        raise compta.Refus("titre absent du relevé ou prix non utilisable")
    probas = [a.p_favorable, a.p_neutre, a.p_defavorable]
    if any(x < 0 for x in probas) or sum(probas) != 100:
        raise compta.Refus("les trois probabilités doivent être positives et faire 100 au total")
    if not a.seuil_bas < 0 < a.seuil_haut or not 5 <= a.horizon_jours <= 365:
        raise compta.Refus("seuil bas négatif, seuil haut positif, horizon de 5 à 365 jours")
    f = Path(a.dossier) / "previsions.jsonl"
    deja = lire(f)
    if any((l["titre"], l["date_cours"]) == (a.titre, p["date_cours"]) for l in deja):
        raise compta.Refus("une prévision existe déjà pour ce titre à cette date de cours")
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
        if pr["id"] in notees or not p or not p["utilisable"] or p["date_cours"] < pr["echeance"]:
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
    notes = lire(d / "previsions-notes.jsonl")
    en_cours = len(lire(d / "previsions.jsonl")) - len(notes)
    if not notes:
        print(f"Aucune prévision arrivée à échéance pour l'instant ({en_cours} en cours).")
        return
    moyenne = sum(Decimal(n["brier"]) for n in notes) / len(notes)
    print(f"Bilan : {len(notes)} prévision(s) notée(s), {sum(n['juste'] for n in notes)} juste(s), note moyenne {moyenne.quantize(Decimal('0.01'))} "
          f"(0 = parfait, 0.67 = hasard) ; {en_cours} en cours.")
    for dec in ("retenue", "reduite", "ecartee", "bloquee"):
        g = [n for n in notes if n["decision"] == dec]
        if g:
            m = sum(Decimal(n["variation_pct"]) for n in g) / len(g)
            print(f"  idées {dec}s : {len(g)}, variation moyenne ensuite {m.quantize(Decimal('0.01'))} %")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Notation des prévisions")
    sp = ap.add_subparsers(dest="commande", required=True)
    p = sp.add_parser("ajouter"); p.add_argument("dossier"); p.add_argument("releve")
    p.add_argument("--titre", required=True); p.add_argument("--nom", required=True)
    p.add_argument("--horizon-jours", type=int, required=True)
    p.add_argument("--seuil-haut", type=float, required=True); p.add_argument("--seuil-bas", type=float, required=True)
    for s in SCENARIOS:
        p.add_argument(f"--p-{s}", type=int, required=True)
    p.add_argument("--decision", choices=("retenue", "reduite", "ecartee", "bloquee"), required=True)
    p.add_argument("--note", default="")
    p = sp.add_parser("noter"); p.add_argument("dossier"); p.add_argument("releve")
    a = ap.parse_args(argv)
    try:
        (cmd_ajouter if a.commande == "ajouter" else cmd_noter)(a)
    except compta.Refus as e:
        sys.exit(f"REFUS : {e}")
    except (ValueError, KeyError, FileNotFoundError) as e:
        sys.exit(f"REFUS : donnée invalide ou manquante ({type(e).__name__} : {e})")


if __name__ == "__main__":
    main()
