#!/usr/bin/env python3
"""Journal de bord des routines : une ligne par lancement, jamais réécrite.
Usage : journal_bord.py DOSSIER matin|soir|bilan|repetition ok|panne "résumé" [--ordres-passes N] [--ordres-executes N] [--jetons N]"""
import argparse, csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ap = argparse.ArgumentParser()
ap.add_argument("dossier"); ap.add_argument("type", choices=("matin", "soir", "bilan", "repetition")); ap.add_argument("statut", choices=("ok", "panne"))
ap.add_argument("resume"); ap.add_argument("--ordres-passes", type=int, default=0); ap.add_argument("--ordres-executes", type=int, default=0)
ap.add_argument("--jetons", type=int, default=0)
a = ap.parse_args()
f = Path(a.dossier) / "routines.csv"
nouveau = not f.exists()
with open(f, "a", newline="") as h:
    w = csv.writer(h)
    if nouveau:
        w.writerow(["date_heure_zurich", "type", "statut", "ordres_passes", "ordres_executes", "jetons_sous_agents", "resume"])
    w.writerow([datetime.now(ZoneInfo("Europe/Zurich")).strftime("%Y-%m-%d %H:%M"), a.type, a.statut, a.ordres_passes, a.ordres_executes, a.jetons, a.resume])
print(f"Journal de bord : {a.type} {a.statut} noté dans {f}")
