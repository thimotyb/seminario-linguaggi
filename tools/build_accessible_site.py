#!/usr/bin/env python3
"""Genera il sito HTML accessibile (sito-accessibile/) a partire dal pptx del corso.

Il sito è statico, senza JavaScript, pensato per la navigazione con screen reader.
- Il testo delle slide viene estratto dal pptx in un ordine di lettura sensato.
- Ogni immagine ha testo alternativo, descrizione estesa e trascrizione del testo
  contenuto (file tools/accessible-site/images/<sha1[:10]>.md).
- Le slide che richiedono un intervento manuale (diagrammi, matrici) hanno un file
  tools/accessible-site/slides/NNN.md che sostituisce o integra il corpo generico.

Uso:  python3 tools/build_accessible_site.py [--check]
"""
import hashlib
import html
import re
import shutil
import sys
from pathlib import Path

from markdown_it import MarkdownIt
from pptx import Presentation

ROOT = Path(__file__).resolve().parent.parent
PPTX = ROOT / "output" / "panoramica-linguaggi-scelte-architetturali-scheletro.pptx"
DATA = ROOT / "tools" / "accessible-site"
OUT = ROOT / "sito-accessibile"
PX = 9525  # EMU per pixel a 1280 px di larghezza
CORAL = "F06654"
ARROWS = "↓→↑←"

COURSE_TITLE = "Panoramica sui linguaggi di programmazione moderni e scelte architetturali"

CHAPTERS = [
    # (file, titolo breve, slide iniziale, slide finale)
    ("apertura", "Apertura", 1, 4),
    ("giornata-1", "Giornata 1", 5, 15),
    ("giornata-2", "Giornata 2", 16, 48),
    ("giornata-3", "Giornata 3", 49, 79),
    ("giornata-4", "Giornata 4", 80, 96),
    ("chiusura", "Chiusura", 97, 97),
]

md = MarkdownIt("commonmark", {"html": False}).enable("table")


# ---------------------------------------------------------------- utilità testo
def esc(t):
    return html.escape(t, quote=True)


ACRONIMI = {"GC", "PSN", "API", "E2E", "CI", "CD", "JIT", "ADR", "JVM", "UAT", "SDLC", "PA", "CCC", "AWS", "ADO", "DTD", "IDE", "UI", "OCI", "SAST", "DAST", "K8S", "DFD", "STRIDE"}


def sentence_case(t):
    """Da MAIUSCOLO a frase (gli screen reader leggono male le parole tutte maiuscole)."""
    propri = {"AZURE": "Azure", "SEABORN": "Seaborn", "PANDAS": "Pandas", "JAVA": "Java", "COLAB": "Colab", "MICROSOFT": "Microsoft", "LEARN": "Learn", "MDN": "MDN", "REACT": "React", "STACKBLITZ": "StackBlitz", "VISUALVM": "VisualVM", "TERRAFORM": "Terraform"}
    words = []
    for w in t.split(" "):
        k = w.strip("·/:.,").upper()
        words.append(propri[k] if k in propri else w if k in ACRONIMI else w.lower())
    out = " ".join(words)
    return out[:1].upper() + out[1:]


def clean(t):
    t = t.replace("\x0b", "\n").replace(" ", " ")
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()


def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


# ------------------------------------------------------------ immagini (schede)
def parse_sections(path):
    sec, cur = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^# (\w+)\s*$", line)
        if m:
            cur = m.group(1)
            sec[cur] = []
        elif cur:
            sec[cur].append(line)
    return {k: "\n".join(v).strip("\n") for k, v in sec.items()}


def render_transcription(text):
    """Trascrizione: paragrafi, elenchi con '- ', blocchi di codice tra ``` ... ```."""
    out, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
        elif ln.startswith("```"):
            i += 1
            blk = []
            while i < len(lines) and not lines[i].startswith("```"):
                blk.append(lines[i])
                i += 1
            i += 1
            out.append(f"<pre><code>{esc(chr(10).join(blk))}</code></pre>")
        elif ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:])
                i += 1
            out.append("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul>")
        else:
            out.append(f"<p>{esc(ln)}</p>")
            i += 1
    return "\n".join(out)


class ImageStore:
    def __init__(self):
        self.seen = {}
        self.missing = []

    def register(self, pic):
        blob = pic.image.blob
        h = hashlib.sha1(blob).hexdigest()[:10]
        ext = pic.image.ext
        if h not in self.seen:
            card = DATA / "images" / f"{h}.md"
            if not card.exists():
                self.missing.append(h)
                data = {"alt": "Immagine senza descrizione", "descrizione": "", "testo": ""}
            else:
                data = parse_sections(card)
            (OUT / "immagini").mkdir(parents=True, exist_ok=True)
            fn = f"{h}.{ext}"
            (OUT / "immagini" / fn).write_bytes(blob)
            self.seen[h] = {"file": fn, **data}
        return h

    def figure(self, h, slide_no, idx):
        d = self.seen[h]
        fid = f"fig-{slide_no}-{idx}"
        parts = [f'<figure class="immagine" aria-labelledby="{fid}-t">']
        parts.append(f'<img src="immagini/{d["file"]}" alt="{esc(d["alt"])}" loading="lazy">')
        parts.append("<figcaption>")
        parts.append(f'<h3 id="{fid}-t">Immagine: {esc(d["alt"])}</h3>')
        if d.get("descrizione"):
            parts.append(f'<p><strong>Descrizione.</strong> {esc(d["descrizione"])}</p>')
        if d.get("testo", "").strip():
            parts.append(f'<h4>Testo contenuto nell’immagine</h4>')
            parts.append(render_transcription(d["testo"]))
        parts.append("</figcaption></figure>")
        return "\n".join(parts)


# ------------------------------------------------------------ estrazione slide
def shape_color(s):
    try:
        for para in s.text_frame.paragraphs:
            for r in para.runs:
                if r.font.color and r.font.color.type is not None:
                    return str(r.font.color.rgb)
                return None
    except Exception:
        pass
    return None


def shape_size(s):
    try:
        for para in s.text_frame.paragraphs:
            for r in para.runs:
                return r.font.size.pt if r.font.size else None
    except Exception:
        pass
    return None


def links_of(shape, part):
    """Collega ogni run con link e l'eventuale link dell'intera forma."""
    A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

    def url(el):
        rid = el.get(R + "id")
        if rid and rid in part.rels and part.rels[rid].is_external:
            return part.rels[rid].target_ref
        return None

    shape_link = None
    nv = shape._element.xpath(".//p:cNvPr")
    if nv:
        for h in nv[0].iter(A + "hlinkClick"):
            shape_link = url(h)
    return shape_link


def para_html(para, part, shape_link):
    """HTML di un paragrafo con i link dei run."""
    A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    out = []
    for r in para._p.iter(A + "r", A + "br"):
        if r.tag == A + "br":
            out.append("<br>")
            continue
        t = r.find(A + "t")
        text = esc((t.text or "") if t is not None else "")
        rpr = r.find(A + "rPr")
        u = None
        if rpr is not None:
            h = rpr.find(A + "hlinkClick")
            if h is not None:
                rid = h.get(R + "id")
                if rid and rid in part.rels and part.rels[rid].is_external:
                    u = part.rels[rid].target_ref
        u = u or shape_link
        out.append(f'<a href="{esc(u)}">{text}</a>' if u else text)
    return "".join(out)


class Item:
    def __init__(self, kind, x, y, w, h, **kw):
        self.kind, self.x, self.y, self.w, self.h = kind, x, y, w, h
        self.__dict__.update(kw)

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2


def slide_items(slide, store, slide_no):
    items, containers = [], []
    part = slide.part
    for s in slide.shapes:
        x, y, w, h = (round(v / PX) for v in (s.left, s.top, s.width, s.height))
        if s.shape_type == 13:
            hsh = store.register(s)
            items.append(Item("pic", x, y, w, h, hash=hsh))
        elif s.has_text_frame and s.text_frame.text.strip():
            items.append(
                Item(
                    "text", x, y, w, h,
                    shape=s, text=clean(s.text_frame.text),
                    color=shape_color(s), size=shape_size(s),
                    link=links_of(s, part),
                    has_link=bool(s._element.xpath(".//a:hlinkClick")),
                )
            )
        elif s.shape_type == 1 and w > 40 and h > 30:
            containers.append(Item("box", x, y, w, h, link=links_of(s, part)))
    return items, containers


def split_footer(items):
    foot, body = {}, []
    for it in items:
        if it.kind == "text" and it.y > 650:
            t = it.text
            if re.fullmatch(r"\d{1,3}", t):
                foot["num"] = t
            elif re.fullmatch(r"\d+ min", t):
                foot["min"] = t
            elif t == t.upper():
                foot["label"] = t
            else:
                foot["source"] = t
                foot["source_item"] = it
        else:
            body.append(it)
    return foot, body


def reading_order(items, containers, extra=()):
    """Ordina gli elementi: bande a tutta larghezza, poi colonne da sinistra a destra."""
    # associa ogni testo al più piccolo contenitore che lo racchiude
    for it in items:
        it.card = None
        best = None
        for c in containers:
            if c.x - 2 <= it.cx <= c.x + c.w + 2 and c.y - 2 <= it.cy <= c.y + c.h + 2:
                if c.w * c.h > it.w * it.h * 1.3 and (best is None or c.w * c.h < best.w * best.h):
                    best = c
        it.card = best
        if best is not None and getattr(best, "link", None) and it.link is None:
            it.link = best.link
    units = {}
    for it in items:
        key = id(it.card) if it.card else id(it)
        units.setdefault(key, {"box": it.card, "items": []})["items"].append(it)
    ulist = []
    for u in units.values():
        its = u["items"]
        if u["box"]:
            b = u["box"]
            u["x"], u["y"], u["w"], u["h"] = b.x, b.y, b.w, b.h
        else:
            it = its[0]
            u["x"], u["y"], u["w"], u["h"] = it.x, it.y, it.w, it.h
        its.sort(key=lambda i: (round(i.y / 14), i.x))
        ulist.append(u)
    ulist.extend(extra)
    ulist.sort(key=lambda u: (u["y"], u["x"]))
    full = lambda u: u["x"] < 120 and u["x"] + u["w"] > 1100
    result, group = [], []

    def flush():
        cols = []
        for u in sorted(group, key=lambda u: u["x"]):
            for c in cols:
                ov = min(u["x"] + u["w"], c["x"] + c["w"]) - max(u["x"], c["x"])
                if ov > 0.5 * min(u["w"], c["w"]):
                    c["us"].append(u)
                    break
            else:
                cols.append({"x": u["x"], "w": u["w"], "us": [u]})
        for c in cols:
            result.extend(sorted(c["us"], key=lambda u: (u["y"], u["x"])))
        group.clear()

    for u in ulist:
        if full(u):
            flush()
            result.append(u)
        else:
            group.append(u)
    flush()
    return result


def is_arrow(it):
    return it.kind == "text" and it.text.strip() and all(ch in ARROWS + " " for ch in it.text.strip())


def block_html(it, store, slide_no, counter):
    if it.kind == "pic":
        counter[0] += 1
        return store.figure(it.hash, slide_no, counter[0])
    if getattr(it, "caption", False) and not it.has_link and it.link is None:
        return f'<p class="didascalia"><strong>Didascalia.</strong> {esc(it.text)}</p>'
    t = it.text
    s = it.shape
    part = s.part
    raw = s.text_frame.text.replace("\x0b", "\n")
    if raw.count("\n") >= 2 and re.search(r"[=;{}()\[\]]", raw) and not raw.lstrip().startswith(("•", "-")) and "  " not in raw.split("\n")[0][:0]:
        return f"<pre><code>{esc(raw.strip())}</code></pre>"
    # etichetta (titoletto)
    if t == t.upper() and len(t) <= 60 and len(t.split("\n")) == 1 and it.link is None and not it.has_link and it.color in (CORAL, None) and any(c.isalpha() for c in t):
        return f"<h3>{esc(sentence_case(t))}</h3>"
    paras = [p for p in s.text_frame.paragraphs if p.text.strip()]
    bullets = [p for p in paras if p.text.lstrip().startswith(("•", "-", "–"))]
    if paras and len(bullets) == len(paras):
        li = []
        for p in paras:
            h = para_html(p, part, it.link)
            h = re.sub(r"^\s*[•\-–]\s*", "", h)
            li.append(f"<li>{h}</li>")
        return "<ul>" + "".join(li) + "</ul>"
    return "".join(f"<p>{para_html(p, part, it.link)}</p>" for p in paras)


def unit_html(u, store, slide_no, counter):
    its = u["items"]
    # righe: elementi sulla stessa riga vengono uniti (etichetta + descrizione)
    rows, last_y = [], None
    for it in its:
        if rows and last_y is not None and abs(it.y - last_y) <= 12 and it.kind == "text" and rows[-1][0].kind == "text" and not is_arrow(it) and "\n" not in it.text and "\n" not in rows[-1][0].text and not it.text.startswith("•") and len(it.text) < 60 and len(rows[-1][0].text) < 60:
            rows[-1].append(it)
        else:
            rows.append([it])
            last_y = it.y
    # sequenze separate da frecce
    out, chain = [], []

    def flush_chain():
        if not chain:
            return
        if len(chain) == 1:
            out.append(chain[0])
        else:
            out.append(
                '<p class="flusso">Sequenza, ogni passo porta al successivo:</p><ol class="flusso">'
                + "".join(f"<li>{c}</li>" for c in chain)
                + "</ol>"
            )
        chain.clear()

    def row_html(row):
        if len(row) == 1:
            return block_html(row[0], store, slide_no, counter)
        parts = [re.sub(r"</?p>", "", block_html(r, store, slide_no, counter)) for r in row]
        return "<p>" + " — ".join(parts) + "</p>"

    has_arrows = any(is_arrow(r[0]) or r[0].kind == "text" and r[0].text.rstrip().endswith(tuple(ARROWS)) for r in rows)
    for row in rows:
        it = row[0]
        if is_arrow(it):
            continue
        if has_arrows and it.kind == "text":
            h = row_html(row)
            h = re.sub(r"\s*[↓→↑←]\s*(</p>)", r"\1", h)
            chain.append(re.sub(r"^<p>|</p>$", "", h) if h.startswith("<p>") and h.count("<p>") == 1 else h)
        else:
            flush_chain()
            out.append(row_html(row))
    flush_chain()
    return "\n".join(out)


def title_of(body_items):
    cand = sorted([i for i in body_items if i.kind == "text" and i.y < 200], key=lambda i: i.y)
    if not cand:
        return None, None, body_items
    first = cand[0]
    kicker = None
    if first.text == first.text.upper() and len(cand) > 1 and cand[1].y - first.y < 90 and cand[1].text != cand[1].text.upper():
        kicker, first = first, cand[1]
    rest = [i for i in body_items if i is not first and i is not kicker]
    return first, kicker, rest


def slide_override(n):
    f = DATA / "slides" / f"{n:03d}.md"
    if not f.exists():
        return None
    return parse_sections(f)


md_counter = [0]


def md_to_html(text, store, slide_no):
    html_out = md.render(text)

    def pic(m):
        h = m.group(1)
        if h not in store.seen:
            raise SystemExit(f"slide {slide_no}: immagine {h} non trovata")
        md_counter[0] += 1
        return store.figure(h, slide_no, 100 + md_counter[0])

    html_out = re.sub(r"<p>\[\[img:([0-9a-f]{10})\]\]</p>", pic, html_out)
    return html_out


def mark_captions(items):
    pics = [i for i in items if i.kind == "pic"]
    for it in items:
        it.caption = False
        if it.kind == "text" and it.text == it.text.upper() and len(it.text) <= 90 and shape_color(it.shape) != CORAL:
            for p in pics:
                ov = min(it.x + it.w, p.x + p.w) - max(it.x, p.x)
                if ov > 0.5 * min(it.w, p.w) and -10 <= it.y - (p.y + p.h) <= 70 or (ov > 0.5 * min(it.w, p.w) and p.y <= it.y <= p.y + p.h and it.y + it.h >= p.y + p.h - 5):
                    it.caption = True


def build_slide(slide, n, store):
    items, containers = slide_items(slide, store, n)
    mark_captions(items)
    foot, body = split_footer(items)
    if "source_item" in foot:
        body_items_for_source = foot["source_item"]
    title_it, kicker, rest = title_of(body)
    title = title_it.text if title_it else f"Slide {n}"
    ov = slide_override(n)
    counter = [0]
    parts = []
    if ov and "sostituisci" in ov:
        parts.append(md_to_html(ov["sostituisci"], store, n))
    else:
        extra, regs = [], []
        for k in sorted(k for k in (ov or {}) if k.startswith("diagramma")):
            head, _, md_text = ov[k].partition("\n")
            x0, y0, x1, y1 = (int(v) for v in head.lstrip("@ ").split())
            regs.append((x0, y0, x1, y1))
            extra.append({"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0, "box": None, "items": [], "html": md_to_html(md_text, store, n)})
        if regs:
            c_in = lambda i: any(r[0] <= i.cx <= r[2] and r[1] <= i.cy <= r[3] for r in regs)
            rest = [i for i in rest if not c_in(i)]
            containers = [c for c in containers if not c_in(c)]
        ordered = reading_order(rest, containers, extra)
        for u in ordered:
            parts.append(u["html"] if "html" in u else unit_html(u, store, n, counter))
        if ov and "aggiungi" in ov:
            parts.append(md_to_html(ov["aggiungi"], store, n))
    return {
        "n": n,
        "title": title,
        "kicker": kicker.text if kicker else None,
        "minutes": foot.get("min"),
        "source": foot.get("source"),
        "body": "\n".join(p for p in parts if p),
    }


# --------------------------------------------------------------------- pagine
CSS = (DATA / "stile.css").read_text(encoding="utf-8") if (DATA / "stile.css").exists() else ""


def page(title, body, current=None, depth=0):
    nav = "".join(
        f'<li><a href="{f}.html"{" aria-current=\"page\"" if f == current else ""}>{esc(t)}</a></li>'
        for f, t, *_ in CHAPTERS
    )
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} – Seminario linguaggi</title>
<link rel="stylesheet" href="stile.css">
</head>
<body>
<a class="salta" href="#contenuto">Vai al contenuto</a>
<header>
<p class="sito"><a href="index.html">Seminario: linguaggi moderni e scelte architetturali</a></p>
<nav aria-label="Parti del corso"><ul>
<li><a href="index.html"{' aria-current="page"' if current == 'index' else ''}>Indice</a></li>{nav}
</ul></nav>
</header>
<main id="contenuto">
{body}
</main>
<footer>
<p>Versione accessibile della presentazione, per la lettura con screen reader. Il contenuto corrisponde alla presentazione PowerPoint; le immagini sono descritte a parole e il testo che contengono è trascritto.</p>
</footer>
</body>
</html>
"""


def slide_article(s):
    kick = f'<p class="kicker">{esc(s["kicker"])}</p>' if s["kicker"] else ""
    meta = []
    if s["minutes"]:
        meta.append(f"Durata prevista: {esc(s['minutes'].replace(' min', ' minuti'))}.")
    meta_html = f'<p class="meta">{" ".join(meta)}</p>' if meta else ""
    src = f'<p class="fonte"><strong>Fonte.</strong> {esc(s["source"])}</p>' if s["source"] else ""
    return f"""<article id="slide-{s['n']}" aria-labelledby="slide-{s['n']}-t">
<h2 id="slide-{s['n']}-t"><span class="num">Slide {s['n']}.</span> {esc(s['title'])}</h2>
{kick}{meta_html}
{s['body']}
{src}
</article>"""


def chapter_page(idx, slides_by_no, divider):
    f, name, a, b = CHAPTERS[idx]
    sl = [slides_by_no[n] for n in range(a, b + 1)]
    if name.startswith("Giornata"):
        d = sl[0]
        heading = f"{name}: {d['title']}"
        sl_content = sl[1:] if len(sl) > 1 else []
        intro = f'<p class="lead">{esc(d["body_text"])}</p>' if d.get("body_text") else ""
    else:
        heading = name if name != "Apertura" else "Apertura del corso"
        sl_content = sl
        intro = ""
    toc = "".join(
        f'<li><a href="#slide-{s["n"]}">Slide {s["n"]}: {esc(s["title"])}</a></li>' for s in sl_content
    )
    prev_l = f'<a href="{CHAPTERS[idx-1][0]}.html" rel="prev">← {esc(CHAPTERS[idx-1][1])}</a>' if idx > 0 else ""
    next_l = f'<a href="{CHAPTERS[idx+1][0]}.html" rel="next">{esc(CHAPTERS[idx+1][1])} →</a>' if idx < len(CHAPTERS) - 1 else ""
    body = f"""<h1>{esc(heading)}</h1>
{intro}
<nav aria-label="Slide di questa parte"><h2 class="toc-t">Slide di questa parte ({len(sl_content)})</h2><ol class="toc">{toc}</ol></nav>
{"".join(slide_article(s) for s in sl_content)}
<nav aria-label="Pagina precedente e successiva" class="pn"><p>{prev_l}</p><p>{next_l}</p></nav>"""
    return page(heading, body, current=f)


def index_page(slides_by_no):
    lis = []
    for f, name, a, b in CHAPTERS:
        titles = []
        for n in range(a, b + 1):
            s = slides_by_no[n]
            titles.append(f'<li><a href="{f}.html#slide-{n}">Slide {n}: {esc(s["title"])}</a></li>')
        label = name
        if name.startswith("Giornata"):
            label = f"{name}: {slides_by_no[a]['title']}"
            titles = titles[1:]
        lis.append(
            f'<section><h3><a href="{f}.html">{esc(label)}</a></h3>'
            f'<details><summary>Elenco delle slide ({len(titles)})</summary><ol class="toc">{"".join(titles)}</ol></details></section>'
        )
    body = f"""<h1>{esc(COURSE_TITLE)}</h1>
<p class="lead">Una guida comparativa per leggere proposte, architetture e trade-off tecnologici. Seminario organizzato per INPS.</p>
<h2>Come usare questo sito</h2>
<ul>
<li>Il sito riproduce, slide per slide, il contenuto della presentazione PowerPoint del corso, in forma di testo navigabile.</li>
<li>Il corso è diviso in quattro giornate più apertura e chiusura. Ogni parte è una pagina; ogni slide è un titolo di secondo livello (“Slide N. Titolo”), raggiungibile con i comandi di navigazione per titoli del lettore di schermo.</li>
<li>Le immagini hanno un testo alternativo breve, una descrizione estesa e, quando contengono testo, la trascrizione del testo (introdotta da un titolo “Testo contenuto nell’immagine”).</li>
<li>I diagrammi disegnati con forme e frecce sono descritti a parole, con le relazioni tra gli elementi.</li>
<li>Ogni pagina ha un collegamento “Vai al contenuto” all’inizio e i collegamenti alla pagina precedente e successiva alla fine.</li>
</ul>
<h2>Parti del corso</h2>
{"".join(lis)}"""
    return page(COURSE_TITLE, body, current="index")


def main():
    check = "--check" in sys.argv
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    store = ImageStore()
    prs = Presentation(str(PPTX))
    slides = {}
    for n, sl in enumerate(prs.slides, 1):
        slides[n] = build_slide(sl, n, store)
    # slide divisorie delle giornate: etichetta, titolo e sottotitolo si leggono dalla posizione
    for f, name, a, b in CHAPTERS:
        if name.startswith("Giornata"):
            txts = sorted(
                (s for s in prs.slides[a - 1].shapes if s.has_text_frame and clean(s.text_frame.text) and not clean(s.text_frame.text).isdigit()),
                key=lambda s: s.top,
            )
            slides[a]["title"] = clean(txts[1].text_frame.text)
            slides[a]["body_text"] = clean(txts[2].text_frame.text) if len(txts) > 2 else ""
    for i in range(len(CHAPTERS)):
        (OUT / f"{CHAPTERS[i][0]}.html").write_text(chapter_page(i, slides, None), encoding="utf-8")
    (OUT / "index.html").write_text(index_page(slides), encoding="utf-8")
    shutil.copy(DATA / "stile.css", OUT / "stile.css")
    print(f"Pagine: {len(CHAPTERS)+1}  Slide: {len(slides)}  Immagini: {len(store.seen)}")
    if store.missing:
        print("ATTENZIONE: immagini senza scheda:", store.missing)
        if check:
            sys.exit(1)


if __name__ == "__main__":
    main()
