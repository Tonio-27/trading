#!/usr/bin/env python3
"""Comptabilité du portefeuille fictif. Les agents décident ; ce programme calcule.

Le journal (journal.jsonl) est la seule vérité : on y ajoute des lignes, on n'en modifie jamais.
Positions, liquidités et performance sont recalculées en relisant le journal.
Protections : empreinte en chaîne sur chaque ligne ; comparaison avec toutes les versions déjà
enregistrées dans Git ; dates fixées par le programme ; relevés de prix récents uniquement.
La vraie garantie reste l'historique Git poussé sur GitHub, que personne ne peut réécrire discrètement.

Commandes :
  init --capital 10000
  ordre --portefeuille agents|reference --sens achat|vente --titre ID --nom NOM --quantite N --justification TEXTE
  executer RELEVE.json     exécute les ordres en attente au prix d'ouverture du relevé
  etat RELEVE.json         valorise les deux portefeuilles et ajoute une ligne à la performance
  dividende RELEVE.json --portefeuille P --titre ID --par-action X --retenue-pct Y --date-detachement J --source S
  fractionnement --titre ID --rapport N --date J --source S   (division d'action : N nouvelles pour 1 ancienne)
  verifier                 contrôle que le journal n'a pas été retouché
Options communes : --dossier (défaut : donnees), --frais (défaut : outils/frais.json)
"""
import argparse, fcntl, hashlib, json, subprocess, sys
from datetime import datetime, date, timedelta, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from zoneinfo import ZoneInfo

PORTEFEUILLES = ("agents", "reference")
EXPIRATION_JOURS = 5      # un ordre sans prix d'ouverture utilisable dans ce délai est rejeté
AGE_MAX_RELEVE_H = 36     # un relevé plus ancien ne sert ni à exécuter ni à valoriser
RENDEMENT_MAX = Decimal("0.10")  # un dividende de plus de 10 % du cours est refusé (erreur de saisie probable)
HEURE_LIMITE = (8, 55)    # un ordre enregistré plus tard (heure de Zurich) compte pour le lendemain :
                          # il ne peut ainsi jamais être exécuté à un prix d'ouverture déjà connu
ZURICH = ZoneInfo("Europe/Zurich")


def maintenant():
    """Seule horloge du programme (les tests automatiques la remplacent ; la ligne de commande ne le peut pas)."""
    return datetime.now(timezone.utc)


def date_decision_auto():
    m = maintenant().astimezone(ZURICH)
    return (m.date() + timedelta(days=0 if (m.hour, m.minute) < HEURE_LIMITE else 1)).isoformat()


def D(x):
    return Decimal(str(x))


def centime(x):
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def jour(texte):
    """Valide une date AAAA-MM-JJ et la rend au format AAAAMMJJ des relevés."""
    return date.fromisoformat(texte).strftime("%Y%m%d")


class Refus(Exception):
    pass


# ---------- journal ----------

def lire_journal(dossier):
    f = Path(dossier) / "journal.jsonl"
    if not f.exists():
        return []
    try:
        return [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
    except json.JSONDecodeError:
        raise Refus("journal illisible (ligne abîmée) : ne rien modifier, prévenir Antoine")


def empreinte(precedente, ligne):
    corps = json.dumps({k: v for k, v in ligne.items() if k != "empreinte"}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256((precedente + corps).encode()).hexdigest()[:16]


def ajouter(dossier, ligne):
    Path(dossier).mkdir(parents=True, exist_ok=True)
    with open(Path(dossier) / ".verrou", "w") as verrou:   # une seule écriture à la fois
        fcntl.flock(verrou, fcntl.LOCK_EX)
        journal = lire_journal(dossier)
        ligne = {"n": len(journal) + 1, "enregistre_utc": maintenant().strftime("%Y-%m-%dT%H:%M:%SZ"), **ligne}
        ligne["empreinte"] = empreinte(journal[-1]["empreinte"] if journal else "", ligne)
        with open(Path(dossier) / "journal.jsonl", "a") as f:
            f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return ligne


def controle_git(f):
    """Chaque version de `f` déjà enregistrée dans Git doit se retrouver telle quelle au début du fichier.
    Rend True si Git protège le fichier, False s'il ne le connaît pas encore."""
    def git(*a):
        return subprocess.run(["git", *a], cwd=f.parent, capture_output=True, text=True)
    versions = git("log", "--format=%H", "-400", "--", f.name).stdout.split()
    amont = git("rev-parse", "--verify", "-q", "@{u}").stdout.strip()
    if amont:
        versions.append(amont)
    actuel, vu = (f.read_text() if f.exists() else None), False
    for v in versions:
        r = git("show", f"{v}:./{f.name}")
        if r.returncode != 0:
            continue
        vu = True
        if actuel is None or not actuel.startswith(r.stdout):
            raise Refus(f"{f.name} : une partie déjà enregistrée dans Git a été modifiée ou supprimée")
    return vu


def verifier(dossier):
    """Rend (nombre de lignes, protégé par Git ?). Lève Refus à la moindre retouche."""
    prec, n = "", 0
    for n, l in enumerate(lire_journal(dossier), 1):
        if l.get("n") != n or l.get("empreinte") != empreinte(prec, l):
            raise Refus(f"journal retouché ou abîmé à la ligne {n}")
        prec = l["empreinte"]
    protege = controle_git(Path(dossier) / "journal.jsonl")
    controle_git(Path(dossier) / "performance.csv")
    return n, protege


# ---------- calculs ----------

def frais_ordre(marche, quantite, prix, monnaie, taux, taux_usd, F):
    """Montant et frais d'un ordre, en CHF. Tous les paramètres viennent du fichier de frais."""
    montant_dev = D(quantite) * D(prix)
    montant = centime(montant_dev * taux)
    if marche == "six":
        commission = centime(max(montant * D(F["six"]["taux"]), D(F["six"]["min_chf"])))
    else:
        c = max(D(quantite) * D(F["us"]["par_action_usd"]), D(F["us"]["min_usd"]))
        commission = centime(min(c, montant_dev * D(F["us"]["max_part"])) * taux)
    change = D(0)
    if monnaie != "CHF":
        change = centime(max(montant * D(F["change"]["taux"]), D(F["change"]["min_usd"]) * taux_usd))
    timbre = centime(montant * D(F["timbre"]["suisse" if monnaie == "CHF" and marche == "six" else "etranger"]))
    return montant, commission, change, timbre


def situation(journal):
    """Rejoue le journal : liquidités, positions et lots de chaque portefeuille, ordres en attente."""
    s = {p: {"liquidites": D(0), "lots": {}, "noms": {}, "frais": D(0)} for p in PORTEFEUILLES}
    ordres, clos = {}, set()
    for l in journal:
        t = l["type"]
        if t == "depot":
            s[l["portefeuille"]]["liquidites"] += D(l["montant_chf"])
        elif t == "ordre":
            ordres[l["id"]] = l
        elif t == "rejet":
            clos.add(l["ordre"])
        elif t == "execution":
            clos.add(l["ordre"])
            o = ordres[l["ordre"]]
            pf, signe = s[o["portefeuille"]], (1 if o["sens"] == "achat" else -1)
            pf["lots"].setdefault(o["titre"], []).append([l["date_cours"], signe * l.get("quantite", o["quantite"])])
            pf["noms"][o["titre"]] = o["nom"]
            pf["liquidites"] += D(l["net_chf"]) if signe == -1 else -D(l["total_chf"])
            pf["frais"] += D(l["commission_chf"]) + D(l["frais_change_chf"]) + D(l["timbre_chf"])
        elif t == "dividende":
            s[l["portefeuille"]]["liquidites"] += D(l["net_chf"])
        elif t == "fractionnement":
            for pf in s.values():   # seuls les titres acquis avant la date de division sont multipliés
                for lot in pf["lots"].get(l["titre"], []):
                    if lot[0] < jour(l["date"]):
                        lot[1] *= l["rapport"]
    for pf in s.values():
        pf["positions"] = {t: {"nom": pf["noms"][t], "quantite": sum(q for _, q in lots)}
                           for t, lots in pf["lots"].items() if sum(q for _, q in lots) != 0}
    return s, [o for i, o in ordres.items() if i not in clos]


def quantite_au(pf, titre, avant):
    """Quantité détenue juste avant le jour `avant` (AAAAMMJJ)."""
    return sum(q for d, q in pf["lots"].get(titre, []) if d < avant)


def charger_releve(chemin, journal):
    brut = Path(chemin).read_bytes()
    r = json.loads(brut)
    if not r.get("change_en_chf"):
        raise Refus("relevé sans taux de change utilisable : aucune opération possible")
    age = maintenant() - datetime.strptime(r["releve_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    if not timedelta(0) <= age <= timedelta(hours=AGE_MAX_RELEVE_H):
        raise Refus(f"relevé trop ancien ou daté du futur ({r['releve_utc']}) : faire un nouveau relevé")
    dernier = max((l["releve_utc"] for l in journal if "releve_utc" in l), default="")
    if r["releve_utc"] < dernier:
        raise Refus("ce relevé est plus ancien que le dernier relevé déjà utilisé")
    r["_sha256"] = hashlib.sha256(brut).hexdigest()[:16]
    r["_nom"] = Path(chemin).name
    return r, {t["id"]: t for t in r["titres"]}


def taux_de(releve, monnaie):
    t = releve["change_en_chf"].get(monnaie)
    if not t:
        raise Refus(f"monnaie {monnaie} absente des taux de change du relevé")
    return D(t)


def trace(releve):
    return {"releve": releve["_nom"], "releve_utc": releve["releve_utc"], "releve_sha256": releve["_sha256"]}


# ---------- commandes ----------

def cmd_init(a, F):
    f = Path(a.dossier) / "journal.jsonl"
    _, protege = verifier(a.dossier)
    if f.exists() or protege:
        raise Refus("un journal existe déjà (ou a existé dans Git) : on ne repart jamais de zéro")
    if D(a.capital) <= 0:
        raise Refus("le capital doit être positif")
    for p in PORTEFEUILLES:
        ajouter(a.dossier, {"type": "depot", "portefeuille": p, "montant_chf": str(centime(D(a.capital)))})
    print(f"Départ : CHF {a.capital} fictifs dans chaque portefeuille ({', '.join(PORTEFEUILLES)}).")


def cmd_ordre(a, F):
    verifier(a.dossier)
    journal = lire_journal(a.dossier)
    if not journal:
        raise Refus("journal vide : lancer d'abord « init »")
    if a.maximum and (a.portefeuille, a.sens) != ("reference", "achat"):
        raise Refus("--maximum est réservé à l'achat de la référence")
    if a.quantite <= 0 and not a.maximum:
        raise Refus("la quantité doit être un nombre entier positif")
    if len(a.justification.strip()) < 20:
        raise Refus("justification trop courte : chaque ordre doit être justifié par écrit")
    n = sum(1 for l in journal if l["type"] == "ordre") + 1
    l = ajouter(a.dossier, {"type": "ordre", "id": f"O-{n:04d}", "portefeuille": a.portefeuille, "sens": a.sens,
                            "titre": a.titre, "nom": a.nom, "quantite": 0 if a.maximum else a.quantite,
                            **({"maximum": True} if a.maximum else {}), "date_decision": date_decision_auto(), "justification": a.justification.strip()})
    print(f"Ordre {l['id']} enregistré : {a.sens} {'le maximum possible' if a.maximum else a.quantite} × {a.nom}, décision datée du {l['date_decision']}, "
          f"exécution au premier prix d'ouverture à partir de ce jour.")


def cmd_executer(a, F):
    verifier(a.dossier)
    releve, prix = charger_releve(a.releve, lire_journal(a.dossier))
    _, attente = situation(lire_journal(a.dossier))
    jour_releve = datetime.strptime(releve["releve_utc"][:10], "%Y-%m-%d").date()
    for o in sorted(attente, key=lambda o: (o["sens"] != "vente", o["id"])):  # les ventes d'abord
        s, _ = situation(lire_journal(a.dossier))
        pf, p = s[o["portefeuille"]], prix.get(o["titre"])
        decision = date.fromisoformat(o["date_decision"])
        limite = decision + timedelta(days=EXPIRATION_JOURS)

        def rejet(raison):
            ajouter(a.dossier, {"type": "rejet", "ordre": o["id"], "raison": raison, **trace(releve)})
            print(f"{o['id']} REJETÉ : {raison}")

        enregistre = datetime.strptime(o["enregistre_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).astimezone(ZURICH).date()
        if decision < enregistre:
            rejet("date de décision antérieure à l'enregistrement de l'ordre")
            continue
        if not p or not p["utilisable"] or p["date_cours"] < decision.strftime("%Y%m%d"):
            if jour_releve > limite:
                rejet(f"aucun prix d'ouverture utilisable dans les {EXPIRATION_JOURS} jours après la décision")
            else:
                print(f"{o['id']} en attente : pas encore de prix d'ouverture utilisable à partir du {o['date_decision']}")
            continue
        if p["date_cours"] > limite.strftime("%Y%m%d"):
            rejet(f"premier prix d'ouverture disponible plus de {EXPIRATION_JOURS} jours après la décision")
            continue
        taux = taux_de(releve, p["monnaie"])
        marche = "six" if p["source"].startswith("SIX") else "us"
        calcul = lambda q: frais_ordre(marche, q, p["ouverture"], p["monnaie"], taux, taux_de(releve, "USD"), F)
        if o.get("maximum"):   # achat de la référence : le plus grand nombre entier de parts que les liquidités permettent
            q = int(pf["liquidites"] / (D(p["ouverture"]) * taux))
            while q > 0 and sum(calcul(q)) > pf["liquidites"]:
                q -= 1
            if q == 0:
                rejet("liquidités insuffisantes pour une seule part")
                continue
            o = {**o, "quantite": q}
        montant, commission, change, timbre = calcul(o["quantite"])
        frais = commission + change + timbre
        if o["sens"] == "vente":
            if pf["positions"].get(o["titre"], {"quantite": 0})["quantite"] < o["quantite"]:
                rejet("vente à découvert interdite : quantité détenue insuffisante")
                continue
            if montant - frais <= 0:
                rejet("vente qui ne couvre pas ses frais")
                continue
            montants = {"net_chf": str(montant - frais)}
        else:
            if montant + frais > pf["liquidites"]:
                rejet(f"liquidités insuffisantes (CHF {pf['liquidites']} disponibles, CHF {montant + frais} nécessaires) : pas d'effet de levier")
                continue
            montants = {"total_chf": str(montant + frais)}
        ajouter(a.dossier, {"type": "execution", "ordre": o["id"], "quantite": o["quantite"], "date_cours": p["date_cours"],
                            "prix": p["ouverture"], "monnaie": p["monnaie"], "taux_chf": str(taux),
                            "date_taux": releve["change_en_chf"]["date"], "montant_chf": str(montant),
                            "commission_chf": str(commission), "frais_change_chf": str(change),
                            "timbre_chf": str(timbre), **montants, "source_prix": p["source"], **trace(releve)})
        print(f"{o['id']} EXÉCUTÉ : {o['sens']} {o['quantite']} × {o['nom']} à {p['ouverture']} {p['monnaie']}, "
              f"montant CHF {montant}, frais CHF {frais}")


def cmd_dividende(a, F):
    verifier(a.dossier)
    journal = lire_journal(a.dossier)
    releve, prix = charger_releve(a.releve, journal)
    s, _ = situation(journal)
    detachement, p = jour(a.date_detachement), prix.get(a.titre)
    if date.fromisoformat(a.date_detachement) > maintenant().astimezone(ZURICH).date():
        raise Refus("date de détachement dans le futur")
    quantite = quantite_au(s[a.portefeuille], a.titre, detachement)
    if quantite <= 0 or not p:
        raise Refus("titre non détenu la veille du détachement, ou absent du relevé")
    if any(l["type"] == "dividende" and (l["portefeuille"], l["titre"], l["date_detachement"]) == (a.portefeuille, a.titre, a.date_detachement) for l in journal):
        raise Refus("ce dividende est déjà enregistré")
    if not 0 <= D(a.retenue_pct) <= 100 or D(a.par_action) <= 0 or len(a.source.strip()) < 8:
        raise Refus("dividende : montant positif, retenue de 0 à 100 et source obligatoires")
    if D(a.par_action) > D(p["cloture"]) * RENDEMENT_MAX:
        raise Refus("dividende de plus de 10 % du cours : montant invraisemblable, à vérifier")
    taux = taux_de(releve, p["monnaie"])
    brut = centime(D(quantite) * D(a.par_action) * taux)
    net = centime(brut * (1 - D(a.retenue_pct) / 100))
    ajouter(a.dossier, {"type": "dividende", "portefeuille": a.portefeuille, "titre": a.titre,
                        "nom": s[a.portefeuille]["noms"][a.titre], "quantite": quantite, "par_action": a.par_action,
                        "monnaie": p["monnaie"], "taux_chf": str(taux), "retenue_pct": a.retenue_pct, "brut_chf": str(brut),
                        "net_chf": str(net), "date_detachement": a.date_detachement, "source": a.source.strip(), **trace(releve)})
    print(f"Dividende {a.titre} sur {quantite} titres : brut CHF {brut}, net CHF {net} ajouté aux liquidités.")


def cmd_fractionnement(a, F):
    verifier(a.dossier)
    journal = lire_journal(a.dossier)
    jour(a.date)
    if date.fromisoformat(a.date) > maintenant().astimezone(ZURICH).date():
        raise Refus("date de division dans le futur")
    if a.rapport < 2 or len(a.source.strip()) < 8:
        raise Refus("fractionnement : rapport entier d'au moins 2 et source obligatoires")
    if any(l["type"] == "fractionnement" and (l["titre"], l["date"]) == (a.titre, a.date) for l in journal):
        raise Refus("cette division d'action est déjà enregistrée")
    ajouter(a.dossier, {"type": "fractionnement", "titre": a.titre, "rapport": a.rapport, "date": a.date, "source": a.source.strip()})
    print(f"Division notée : {a.rapport} nouvelles actions {a.titre} pour 1 ancienne, pour les titres acquis avant le {a.date}.")


def cmd_etat(a, F):
    verifier(a.dossier)
    journal = lire_journal(a.dossier)
    releve, prix = charger_releve(a.releve, journal)
    s, attente = situation(journal)
    depart = {p: sum(D(l["montant_chf"]) for l in journal if l["type"] == "depot" and l["portefeuille"] == p) for p in PORTEFEUILLES}
    if not all(depart.values()):
        raise Refus("journal vide : lancer d'abord « init »")
    dc = max((t["date_cours"] for t in releve["titres"]), default=None)
    if not dc:
        raise Refus("relevé sans aucun prix")
    jour_cours = f"{dc[:4]}-{dc[4:6]}-{dc[6:]}"
    etat = {"date_cours": jour_cours, "releve": releve["_nom"], "releve_utc": releve["releve_utc"], "ordres_en_attente": len(attente)}
    for nom, pf in s.items():
        lignes, total = [], pf["liquidites"]
        for titre, pos in sorted(pf["positions"].items()):
            p = prix.get(titre)
            if not p:
                raise Refus(f"{pos['nom']} est en portefeuille mais absent du relevé : valorisation impossible")
            v = centime(D(pos["quantite"]) * D(p["cloture"]) * taux_de(releve, p["monnaie"]))
            total += v
            lignes.append({"titre": titre, "nom": pos["nom"], "quantite": pos["quantite"], "cloture": p["cloture"],
                           "monnaie": p["monnaie"], "date_cours": p["date_cours"], "valeur_chf": str(v),
                           "prix_douteux": not p["utilisable"]})
        etat[nom] = {"valeur_chf": str(total), "liquidites_chf": str(pf["liquidites"]), "frais_cumules_chf": str(pf["frais"]),
                     "performance_pct": str((total / depart[nom] * 100 - 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                     "positions": lignes}
    etat["ecart_points"] = str(D(etat["agents"]["performance_pct"]) - D(etat["reference"]["performance_pct"]))
    dossier = Path(a.dossier)
    (dossier / "etat.json").write_text(json.dumps(etat, ensure_ascii=False, indent=2) + "\n")
    # Une ligne par jour de cours (et non par jour de relevé) : la première écrite fait foi.
    perf = dossier / "performance.csv"
    deja = perf.read_text().splitlines() if perf.exists() else ["date_cours,valeur_agents_chf,valeur_reference_chf,ecart_points"]
    if any(l.startswith(jour_cours + ",") for l in deja):
        print(f"Performance des cours du {jour_cours} déjà notée : ligne non réécrite.")
    else:
        with open(perf, "w") as h:
            h.write("\n".join(deja + [f"{jour_cours},{etat['agents']['valeur_chf']},{etat['reference']['valeur_chf']},{etat['ecart_points']}"]) + "\n")
    for nom in PORTEFEUILLES:
        e = etat[nom]
        print(f"{nom:10} valeur CHF {e['valeur_chf']:>10}  ({e['performance_pct']} %)  liquidités CHF {e['liquidites_chf']}  frais cumulés CHF {e['frais_cumules_chf']}")
    print(f"Écart agents − référence : {etat['ecart_points']} point(s), cours du {jour_cours}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Comptabilité du portefeuille fictif")
    ap.add_argument("--dossier", default="donnees")
    ap.add_argument("--frais", default="outils/frais.json")
    sp = ap.add_subparsers(dest="commande", required=True)
    p = sp.add_parser("init"); p.add_argument("--capital", required=True)
    p = sp.add_parser("ordre")
    p.add_argument("--portefeuille", choices=PORTEFEUILLES, required=True)
    p.add_argument("--sens", choices=("achat", "vente"), required=True)
    p.add_argument("--titre", required=True); p.add_argument("--nom", required=True)
    p.add_argument("--quantite", type=int, default=0); p.add_argument("--justification", required=True)
    p.add_argument("--maximum", action="store_true")
    p = sp.add_parser("dividende"); p.add_argument("releve")
    p.add_argument("--portefeuille", choices=PORTEFEUILLES, required=True); p.add_argument("--titre", required=True)
    p.add_argument("--par-action", required=True); p.add_argument("--retenue-pct", required=True)
    p.add_argument("--date-detachement", required=True); p.add_argument("--source", required=True)
    p = sp.add_parser("fractionnement"); p.add_argument("--titre", required=True); p.add_argument("--rapport", type=int, required=True)
    p.add_argument("--date", required=True); p.add_argument("--source", required=True)
    for c in ("executer", "etat"):
        p = sp.add_parser(c); p.add_argument("releve")
    sp.add_parser("verifier")
    a = ap.parse_args(argv)
    try:
        F = json.loads(Path(a.frais).read_text())
        if a.commande == "verifier":
            n, protege = verifier(a.dossier)
            print(f"Journal intact : {n} ligne(s) contrôlée(s). " + ("Protégé par l'historique Git." if protege else
                  "ATTENTION : pas encore enregistré dans Git, donc non protégé contre une réécriture."))
        else:
            {"init": cmd_init, "ordre": cmd_ordre, "executer": cmd_executer, "etat": cmd_etat,
             "dividende": cmd_dividende, "fractionnement": cmd_fractionnement}[a.commande](a, F)
    except Refus as e:
        sys.exit(f"REFUS : {e}")
    except (InvalidOperation, ValueError, KeyError, FileNotFoundError) as e:
        sys.exit(f"REFUS : donnée invalide ou manquante ({type(e).__name__} : {e})")


if __name__ == "__main__":
    main()
