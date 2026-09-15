from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


PPTX = Path("output/panoramica-linguaggi-scelte-architetturali-scheletro.pptx")

NAVY = RGBColor(17, 36, 63)
NAVY_2 = RGBColor(25, 51, 82)
TEAL = RGBColor(40, 167, 158)
CORAL = RGBColor(240, 102, 84)
SKY = RGBColor(83, 166, 214)
WHITE = RGBColor(255, 255, 255)
PALE = RGBColor(232, 239, 245)
MUTED = RGBColor(91, 107, 126)


def clear_slide(slide):
    for shape in list(slide.shapes):
        slide.shapes._spTree.remove(shape._element)


def box(slide, x, y, w, h, fill, radius=True, line=None):
    kind = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE if radius else MSO_AUTO_SHAPE_TYPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line or fill
    return shape


def label(slide, value, x, y, w, h, size=16, color=NAVY, bold=False,
          align=PP_ALIGN.LEFT, font="Aptos", valign=MSO_ANCHOR.MIDDLE):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.vertical_anchor = valign
    frame.margin_left = frame.margin_right = Inches(0.03)
    frame.margin_top = frame.margin_bottom = Inches(0.02)
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    run = paragraph.add_run()
    run.text = value
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return shape


def rich_text(slide, lines, x, y, w, h, size=14, color=NAVY):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = Inches(0.04)
    frame.margin_top = frame.margin_bottom = Inches(0.03)
    for idx, (head, body) in enumerate(lines):
        p = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
        p.space_after = Pt(8)
        r = p.add_run(); r.text = head
        r.font.name = "Aptos"; r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = TEAL
        r = p.add_run(); r.text = body
        r.font.name = "Aptos"; r.font.size = Pt(size); r.font.color.rgb = color
    return shape


def button(slide, caption, url, x, y, w, fill=TEAL):
    shape = box(slide, x, y, w, .43, fill)
    shape.click_action.hyperlink.address = url
    text_shape = label(slide, caption, x+.08, y+.04, w-.16, .32, 10, WHITE, True, PP_ALIGN.CENTER)
    text_shape.text_frame.paragraphs[0].runs[0].hyperlink.address = url
    return shape


def common(slide, title, number, duration):
    box(slide, .55, .42, .12, .12, CORAL)
    label(slide, title, .8, .63, 11.8, .72, 27, NAVY, True)
    label(slide, "LINGUAGGI E PARADIGMI", .58, 7.08, 8.5, .24, 9, MUTED, True)
    label(slide, duration, 10.92, 7.04, 1.35, .28, 9, MUTED, False, PP_ALIGN.RIGHT)
    n = label(slide, f"{number:02d}", 12.38, 7.0, .38, .32, 10, CORAL, True, PP_ALIGN.RIGHT)
    n.name = "SLIDE_NUMBER"


def set_notes(slide, text):
    frame = slide.notes_slide.notes_text_frame
    frame.clear()
    frame.text = text


def build_oop(slide, number):
    clear_slide(slide)
    common(slide, "Object-oriented: oggetti che collaborano attraverso contratti", number, "18 min")

    box(slide, .78, 1.43, 11.8, .72, PALE, line=PALE)
    label(slide,
          "Definizione · Un programma è organizzato come oggetti che incapsulano dati e funzioni e interagiscono fra loro.",
          1.02, 1.56, 11.3, .42, 14, NAVY, True, PP_ALIGN.CENTER)

    label(slide, "DESIGN: PROGRAMMA CONTRO L’ASTRAZIONE", .82, 2.38, 6.35, .25, 11, CORAL, True)
    box(slide, 2.03, 2.77, 3.85, .78, NAVY_2)
    label(slide, "abstract Shape", 2.2, 2.9, 3.5, .25, 17, WHITE, True, PP_ALIGN.CENTER, "Aptos Mono")
    label(slide, "Area  ·  Perimeter", 2.2, 3.2, 3.5, .2, 11, SKY, False, PP_ALIGN.CENTER, "Aptos Mono")
    label(slide, "implementa ↓", 3.21, 3.61, 1.55, .25, 11, CORAL, True, PP_ALIGN.CENTER)

    for x, name, detail in [(1.02, "Rectangle", "w × h"), (3.18, "Square", "side²"), (5.34, "Circle", "πr²")]:
        box(slide, x, 4.03, 1.78, .96, WHITE, line=TEAL)
        label(slide, name, x+.1, 4.18, 1.58, .24, 13, NAVY, True, PP_ALIGN.CENTER)
        label(slide, detail, x+.1, 4.52, 1.58, .22, 12, TEAL, True, PP_ALIGN.CENTER, "Aptos Mono")

    box(slide, .9, 5.27, 6.22, .77, NAVY_2)
    label(slide, "foreach (Shape s in shapes)  →  s.Area", 1.08, 5.39, 5.86, .25, 14, WHITE, True, PP_ALIGN.CENTER, "Aptos Mono")
    label(slide, "dynamic binding: decide il tipo reale a runtime", 1.08, 5.7, 5.86, .2, 10, SKY, False, PP_ALIGN.CENTER)

    box(slide, 7.48, 2.38, 5.0, 3.66, WHITE, line=PALE)
    label(slide, "LE QUATTRO IDEE DA VEDERE NELL’ESEMPIO", 7.78, 2.63, 4.4, .34, 11, CORAL, True, PP_ALIGN.CENTER)
    rich_text(slide, [
        ("Astrazione · ", "Shape definisce il contratto comune."),
        ("Incapsulamento · ", "ogni oggetto conserva i propri dati."),
        ("Ereditarietà · ", "le forme concrete specializzano Shape."),
        ("Polimorfismo · ", "la stessa chiamata seleziona l’override corretto."),
    ], 7.78, 3.12, 4.35, 2.28, 13)
    button(slide, "TUTORIAL COMPLETO · MICROSOFT LEARN",
           "https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/tutorials/inheritance",
           7.92, 5.47, 4.05, CORAL)
    label(slide, "Fonti: Wikipedia · Microsoft Learn, Introduction to Inheritance", .84, 6.38, 11.45, .24, 9, MUTED)
    set_notes(slide,
        "OBIETTIVO: collegare la definizione OOP a un esempio completo di design.\n"
        "FLUSSO: Shape dichiara Area e Perimeter; Rectangle, Square e Circle forniscono implementazioni differenti; "
        "una collezione Shape[] le tratta in modo uniforme e il runtime richiama l'override del tipo concreto.\n"
        "FONTI: https://en.wikipedia.org/wiki/Object-oriented_programming ; "
        "https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/tutorials/inheritance")


def build_functional(slide, number):
    clear_slide(slide)
    common(slide, "Funzionale: descrivere trasformazioni componendo funzioni", number, "18 min")

    box(slide, .78, 1.43, 11.8, .72, PALE, line=PALE)
    label(slide,
          "Definizione · Il programma nasce applicando e componendo funzioni che trasformano valori, invece di aggiornare una sequenza di stati.",
          1.02, 1.53, 11.3, .49, 14, NAVY, True, PP_ALIGN.CENTER)

    label(slide, "ESEMPIO: UNA FUNZIONE DI TRASFORMAZIONE", .82, 2.38, 6.2, .25, 11, CORAL, True)
    box(slide, .8, 2.76, 7.08, 2.38, NAVY_2)
    code = "const numeri = [1, 4, 9, 16];\nconst raddoppia = x => x * 2;\n\nconst risultato = numeri.map(raddoppia);\n// [2, 8, 18, 32]"
    label(slide, code, 1.12, 3.05, 6.42, 1.75, 16, WHITE, False, PP_ALIGN.LEFT, "Aptos Mono", MSO_ANCHOR.TOP)

    for x, value, result in [(1.02,"1","2"),(2.58,"4","8"),(4.14,"9","18"),(5.7,"16","32")]:
        box(slide, x, 5.39, .64, .48, WHITE, line=TEAL)
        label(slide, value, x+.05, 5.49, .54, .24, 13, NAVY, True, PP_ALIGN.CENTER)
        label(slide, "→", x+.67, 5.48, .31, .25, 13, CORAL, True, PP_ALIGN.CENTER)
        box(slide, x+.99, 5.39, .64, .48, TEAL)
        label(slide, result, x+1.04, 5.49, .54, .24, 13, WHITE, True, PP_ALIGN.CENTER)

    box(slide, 8.18, 2.38, 4.3, 3.49, WHITE, line=PALE)
    label(slide, "COSA RENDE FUNZIONALE IL FLUSSO", 8.45, 2.65, 3.75, .34, 11, CORAL, True, PP_ALIGN.CENTER)
    rich_text(slide, [
        ("Funzione come valore · ", "raddoppia è passata a map."),
        ("Trasformazione · ", "ogni input produce un nuovo output."),
        ("Immutabilità · ", "numeri non viene modificato."),
        ("Composizione · ", "map, filter e reduce formano pipeline."),
    ], 8.47, 3.13, 3.72, 2.16, 12)
    button(slide, "ESEMPIO INTERATTIVO · MDN ARRAY.MAP",
           "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map",
           8.47, 5.42, 3.72, TEAL)
    label(slide, "Fonti: Wikipedia · MDN Web Docs, Array.prototype.map()", .84, 6.38, 11.45, .24, 9, MUTED)
    set_notes(slide,
        "OBIETTIVO: far vedere la programmazione funzionale come trasformazione di valori.\n"
        "FLUSSO: raddoppia è una funzione di prima classe passata a map; map la applica a ogni elemento e crea un nuovo array "
        "senza modificare quello iniziale. Collegare poi map, filter e reduce come pipeline componibile.\n"
        "FONTI: https://en.wikipedia.org/wiki/Functional_programming ; "
        "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map")


def delete_slide(prs, index):
    slide_id = prs.slides._sldIdLst[index]
    rel_id = slide_id.rId
    prs.part.drop_rel(rel_id)
    del prs.slides._sldIdLst[index]


prs = Presentation(PPTX)
assert len(prs.slides) == 88, "Il deck corrente non è quello atteso; patch interrotta."
def first_text(slide):
    return next(shape.text for shape in slide.shapes if getattr(shape, "has_text_frame", False) and shape.text.strip())

assert first_text(prs.slides[8]) == "Paradigma procedurale"
assert first_text(prs.slides[9]) == "Paradigma object-oriented"
assert first_text(prs.slides[10]) == "Paradigma funzionale"

delete_slide(prs, 8)
build_oop(prs.slides[8], 9)
build_functional(prs.slides[9], 10)

for idx, slide in enumerate(prs.slides, 1):
    for shape in slide.shapes:
        if shape.name == "SLIDE_NUMBER" and shape.has_text_frame:
            shape.text_frame.paragraphs[0].runs[0].text = f"{idx:02d}"

prs.save(PPTX)
print(f"patched={PPTX} slides={len(prs.slides)}")
