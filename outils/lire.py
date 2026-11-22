#!/usr/bin/env python3
"""Ouvre une page web autorisée et affiche son texte (sans menus ni scripts).
Usage : python3 outils/lire.py ADRESSE [nombre_max_de_caracteres]
Seuls les sites autorisés dans l'environnement « trading » répondent (voir equipe/sources.md).
Un site qui refuse la lecture n'est pas contourné : le programme l'annonce et s'arrête."""
import re, sys, urllib.request, urllib.error
from html.parser import HTMLParser

IGNORES = {"script", "style", "noscript", "svg", "nav", "footer", "header", "form", "aside", "iframe"}
BLOCS = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "tr", "article", "section", "time"}


class Texte(HTMLParser):
    def __init__(self):
        super().__init__()
        self.morceaux, self.profondeur = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in IGNORES:
            self.profondeur += 1
        elif tag in BLOCS:
            self.morceaux.append("\n")

    def handle_endtag(self, tag):
        if tag in IGNORES and self.profondeur:
            self.profondeur -= 1

    def handle_data(self, data):
        if not self.profondeur and data.strip():
            self.morceaux.append(data.strip() + " ")


def main():
    if len(sys.argv) < 2 or not sys.argv[1].startswith("https://"):
        sys.exit("Usage : lire.py https://… [nombre_max_de_caracteres]")
    limite = int(sys.argv[2]) if len(sys.argv) > 2 else 12000
    req = urllib.request.Request(sys.argv[1], headers={"User-Agent": "lecteur-actualites-perso/1.0", "Accept-Language": "fr,de,en"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            brut = r.read(3_000_000).decode(r.headers.get_content_charset() or "utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        sys.exit(f"LECTURE IMPOSSIBLE : le site répond {e.code}. Ne pas insister ; traiter l'information comme « extrait seulement ».")
    except Exception as e:
        sys.exit(f"LECTURE IMPOSSIBLE : {e}. Site non autorisé ou injoignable ; traiter l'information comme « extrait seulement ».")
    p = Texte()
    p.feed(brut)
    texte = re.sub(r"\n\s*\n+", "\n", re.sub(r"[ \t]+", " ", "".join(p.morceaux))).strip()
    print(texte[:limite])
    if len(texte) > limite:
        print(f"\n[… texte coupé à {limite} caractères sur {len(texte)}]")


if __name__ == "__main__":
    main()
