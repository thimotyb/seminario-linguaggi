from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


PPTX = Path("output/panoramica-linguaggi-scelte-architetturali-scheletro.pptx")
AZURE_FIGURE = Path("assets/source-dotnet/dotnet-azure-app-service.png")

NAVY = RGBColor(17, 36, 63)
NAVY_2 = RGBColor(25, 51, 82)
TEAL = RGBColor(40, 167, 158)
CORAL = RGBColor(240, 102, 84)
SKY = RGBColor(83, 166, 214)
WHITE = RGBColor(255, 255, 255)
PALE = RGBColor(232, 239, 245)
MUTED = RGBColor(91, 107, 126)


def clear(slide):
    for shape in list(slide.shapes):
        slide.shapes._spTree.remove(shape._element)


def box(slide, x, y, w, h, fill, line=None):
    shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
                                   Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid(); shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line or fill
    return shape


def text(slide, value, x, y, w, h, size=15, color=NAVY, bold=False,
         align=PP_ALIGN.LEFT, font="Aptos", valign=MSO_ANCHOR.MIDDLE):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = shape.text_frame; frame.clear(); frame.word_wrap = True
    frame.vertical_anchor = valign
    frame.margin_left = frame.margin_right = Inches(.03)
    frame.margin_top = frame.margin_bottom = Inches(.02)
    p = frame.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = value; r.font.name = font; r.font.size = Pt(size)
    r.font.bold = bold; r.font.color.rgb = color
    return shape


def button(slide, caption, url, x, y, w, fill):
    shape = box(slide, x, y, w, .4, fill)
    shape.click_action.hyperlink.address = url
    t = text(slide, caption, x+.07, y+.03, w-.14, .3, 9, WHITE, True, PP_ALIGN.CENTER)
    t.text_frame.paragraphs[0].runs[0].hyperlink.address = url


def fit_picture(slide, path, x, y, w, h):
    from PIL import Image
    with Image.open(path) as image:
        ratio = image.width / image.height
    frame_ratio = w / h
    if ratio > frame_ratio:
        ph = w / ratio; py = y + (h - ph) / 2
        return slide.shapes.add_picture(str(path), Inches(x), Inches(py), width=Inches(w), height=Inches(ph))
    pw = h * ratio; px = x + (w - pw) / 2
    return slide.shapes.add_picture(str(path), Inches(px), Inches(y), width=Inches(pw), height=Inches(h))


prs = Presentation(PPTX)
assert len(prs.slides) == 87
slide = prs.slides[23]
old_title = next(s.text for s in slide.shapes if getattr(s, "has_text_frame", False) and s.text.strip())
assert old_title == ".NET: runtime e piattaforma"
clear(slide)

box(slide, .55, .42, .12, .12, CORAL)
text(slide, ".NET: linguaggi, runtime e servizi cloud", .8, .63, 11.8, .72, 27, NAVY, True)
box(slide, .78, 1.42, 11.8, .66, PALE, PALE)
text(slide, ".NET è una piattaforma gratuita, open source e multipiattaforma: runtime, librerie, compilatori, SDK e stack applicativi.",
     1.02, 1.52, 11.3, .43, 13, NAVY, True, PP_ALIGN.CENTER)

text(slide, "DAL SORGENTE ALL’ESECUZIONE", .82, 2.29, 5.9, .24, 11, CORAL, True)
layers = [
    ("C#  ·  F#  ·  Visual Basic", NAVY_2, WHITE),
    ("Compiler  →  CIL + metadata (assembly)", TEAL, WHITE),
    ("CoreCLR / CLR", NAVY_2, WHITE),
    ("JIT  ·  GC  ·  type system  ·  threading", SKY, WHITE),
    ("Windows  ·  Linux  ·  macOS  |  x64 · Arm64", WHITE, NAVY),
]
for i, (caption, fill, color) in enumerate(layers):
    y = 2.65 + i * .66
    box(slide, .82, y, 5.55, .48, fill, TEAL if fill == WHITE else fill)
    text(slide, caption, .99, y+.07, 5.2, .3, 11 if i != 2 else 14, color, True, PP_ALIGN.CENTER,
         "Aptos Mono" if i in (1, 2, 3) else "Aptos")
    if i < len(layers)-1:
        text(slide, "↓", 3.3, y+.47, .55, .2, 10, CORAL, True, PP_ALIGN.CENTER)

text(slide, "COMPONENTI CHE COMPLETANO LA PIATTAFORMA", .82, 6.12, 5.9, .22, 10, CORAL, True)
for i, caption in enumerate(["LIBRERIE", "SDK + CLI", "NuGet", "ASP.NET Core"]):
    x = .82 + i * 1.43
    box(slide, x, 6.4, 1.26, .4, PALE, PALE)
    text(slide, caption, x+.04, 6.47, 1.18, .24, 9, NAVY, True, PP_ALIGN.CENTER)

text(slide, "DALLA PIATTAFORMA AL DEPLOYMENT AZURE", 6.85, 2.29, 5.15, .24, 11, CORAL, True)
box(slide, 6.78, 2.62, 5.63, 3.73, WHITE, PALE)
fit_picture(slide, AZURE_FIGURE, 6.98, 2.78, 5.23, 3.38)
text(slide, "App Service esegue l’app .NET e aggiunge scaling, slot, identità e servizi dati gestiti.",
     6.93, 6.31, 5.34, .3, 10, NAVY, True, PP_ALIGN.CENTER)

button(slide, "INTRODUZIONE A .NET", "https://learn.microsoft.com/it-it/dotnet/core/introduction",
       7.0, 6.65, 2.42, TEAL)
button(slide, "ARCHITETTURA SU AZURE", "https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures",
       9.65, 6.65, 2.55, CORAL)

text(slide, "LINGUAGGI E PARADIGMI", .58, 7.12, 8.5, .22, 9, MUTED, True)
text(slide, "18 min", 10.92, 7.08, 1.35, .25, 9, MUTED, False, PP_ALIGN.RIGHT)
n = text(slide, "24", 12.38, 7.04, .38, .28, 10, CORAL, True, PP_ALIGN.RIGHT); n.name = "SLIDE_NUMBER"

notes = slide.notes_slide.notes_text_frame
notes.clear()
notes.text = (
    "OBIETTIVO: distinguere .NET moderno dalla sola associazione storica a Windows e mostrare il passaggio dal codice al cloud.\n"
    "LETTURA: i compilatori producono CIL e metadati negli assembly; CoreCLR/CLR offre JIT, garbage collection, type system e threading; "
    "librerie, SDK, NuGet e stack come ASP.NET Core completano la piattaforma. Azure App Service è una possibile destinazione gestita, non una parte del runtime.\n"
    "FONTI: https://learn.microsoft.com/it-it/dotnet/core/introduction ; "
    "https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-netod/61429371-4f97-4576-8043-d7c28f61587b ; "
    "https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures"
)

prs.save(PPTX)
print(f"patched={PPTX} slide=24")
