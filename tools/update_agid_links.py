from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

PPTX = "output/panoramica-linguaggi-scelte-architetturali-scheletro.pptx"
AGID_2024 = "https://www.agid.gov.it/sites/agid/files/2024-07/Linee-guida_di_sicurezza_sviluppo-applicazioni.pdf"
AGID_ALLEGATO_4 = "https://www.agid.gov.it/sites/default/files/repository_files/allegato_4_-_linee_guida_per_la_modellazione_delle_minacce-dlt.pdf"
AGID_LINEE_GUIDA = "https://www.agid.gov.it/it/linee-guida"
CORAL = RGBColor(240, 102, 84)
TEAL = RGBColor(40, 167, 158)
WHITE = RGBColor(255, 255, 255)


def add_button(slide, caption, url, x, y, w, fill):
    shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
                                   Inches(x), Inches(y), Inches(w), Inches(.43))
    shape.fill.solid(); shape.fill.fore_color.rgb = fill; shape.line.color.rgb = fill
    shape.click_action.hyperlink.address = url
    text = slide.shapes.add_textbox(Inches(x+.08), Inches(y+.05), Inches(w-.16), Inches(.28))
    frame = text.text_frame; frame.clear(); frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    paragraph = frame.paragraphs[0]; paragraph.alignment = PP_ALIGN.CENTER
    run = paragraph.add_run(); run.text = caption; run.font.name = "Aptos"; run.font.size = Pt(9)
    run.font.bold = True; run.font.color.rgb = WHITE; run.hyperlink.address = url


prs = Presentation(PPTX)
assert len(prs.slides) == 91
slide = prs.slides[82]
assert next(s.text for s in slide.shapes if getattr(s, "has_text_frame", False) and s.text.strip()).startswith("Linee guida AgID")

old_text = next(s for s in slide.shapes if getattr(s, "has_text_frame", False) and s.text == "APRI IL PDF AGID")
old_url_shapes = []
for shape in slide.shapes:
    try:
        address = shape.click_action.hyperlink.address
    except Exception:
        address = None
    if address and "drive.google.com/file/d/1vK_ellHCkkFT6jE_KqAr3Kk4SaeWwz23" in address:
        old_url_shapes.append(shape)
assert len(old_url_shapes) == 1
old_button = old_url_shapes[0]
slide.shapes._spTree.remove(old_text._element)
slide.shapes._spTree.remove(old_button._element)

add_button(slide, "PAGINA LINEE GUIDA", AGID_LINEE_GUIDA, 2.15, 6.05, 2.72, TEAL)
add_button(slide, "DOCUMENTO AGID · 2024", AGID_2024, 5.08, 6.05, 2.82, CORAL)
add_button(slide, "ALLEGATO 4 · THREAT MODELING", AGID_ALLEGATO_4, 8.1, 6.05, 3.12, TEAL)

source = next(s for s in slide.shapes if getattr(s, "has_text_frame", False) and s.text.startswith("Fonte: AgID"))
source.text = "Fonti ufficiali AgID: pubblicazione 03/07/2024 · Allegato 4 Secure/Privacy by Design"

notes = slide.notes_slide.notes_text_frame
notes.text = notes.text.replace(
    "https://drive.google.com/file/d/1vK_ellHCkkFT6jE_KqAr3Kk4SaeWwz23/view",
    AGID_LINEE_GUIDA + " ; " + AGID_2024 + " ; " + AGID_ALLEGATO_4,
)

prs.save(PPTX)
print("updated AGID links on slide 83")
