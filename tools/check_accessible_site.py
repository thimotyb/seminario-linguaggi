#!/usr/bin/env python3
"""Controlli statici sul sito accessibile: alt, id univoci, link interni, gerarchia dei titoli."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "sito-accessibile"
problems = []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hrefs, self.imgs, self.heads, self.empty_links = [], [], [], [], []
        self._a = None
        self._h = None
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "a":
            self._a = [a.get("href"), ""]
        if tag == "img":
            self.imgs.append(a)
        if tag in ("h1", "h2", "h3", "h4", "h5"):
            self._h = [int(tag[1]), ""]
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "a" and self._a:
            if not self._a[1].strip():
                self.empty_links.append(self._a[0])
            self.hrefs.append(self._a[0])
            self._a = None
        if tag in ("h1", "h2", "h3", "h4", "h5") and self._h:
            self.heads.append(tuple(self._h))
            self._h = None
        if tag == "title":
            self._in_title = False

    def handle_data(self, d):
        if self._a:
            self._a[1] += d
        if self._h:
            self._h[1] += d
        if self._in_title:
            self.title += d


pages = {f.name: f for f in SITE.glob("*.html")}
parsed = {}
for name, f in pages.items():
    p = P()
    p.feed(f.read_text(encoding="utf-8"))
    parsed[name] = p
for name, p in parsed.items():
    dup = {i for i in p.ids if p.ids.count(i) > 1}
    if dup:
        problems.append(f"{name}: id duplicati {sorted(dup)[:5]}")
    for im in p.imgs:
        if not im.get("alt", "").strip():
            problems.append(f"{name}: immagine senza alt {im.get('src')}")
        if not (SITE / im["src"]).exists():
            problems.append(f"{name}: file immagine mancante {im['src']}")
    if p.empty_links:
        problems.append(f"{name}: link senza testo {p.empty_links[:3]}")
    last = 0
    for lvl, txt in p.heads:
        if lvl > last + 1:
            problems.append(f"{name}: salto di livello h{last}→h{lvl} su «{txt.strip()[:40]}»")
        if not txt.strip():
            problems.append(f"{name}: titolo vuoto")
        last = lvl
    if sum(1 for l, _ in p.heads if l == 1) != 1:
        problems.append(f"{name}: deve avere un solo h1")
    for h in p.hrefs:
        if not h or h.startswith(("http://", "https://", "mailto:")):
            continue
        target, _, frag = h.partition("#")
        if target and target not in pages and not (SITE / target).exists():
            problems.append(f"{name}: link interno rotto {h}")
        elif frag:
            t = target or name
            if frag not in parsed[t].ids:
                problems.append(f"{name}: ancora mancante {h}")
n_img = sum(len(p.imgs) for p in parsed.values())
n_ext = sum(1 for p in parsed.values() for h in p.hrefs if h and h.startswith("http"))
print(f"Pagine: {len(pages)}  Immagini: {n_img}  Link esterni: {n_ext}")
if problems:
    print("PROBLEMI:")
    print("\n".join(problems))
    sys.exit(1)
print("OK: nessun problema rilevato")
