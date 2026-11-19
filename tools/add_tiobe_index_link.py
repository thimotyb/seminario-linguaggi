from datetime import datetime
from pathlib import Path
import shutil

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


PPTX = Path("output/panoramica-linguaggi-scelte-architetturali-scheletro.pptx")
BACKUPS = Path("output/backups")
TIOBE_URL = "https://www.tiobe.com/tiobe-index/"

BLUE = RGBColor(43, 98, 160)
WHITE = RGBColor(255, 255, 255)


def slide_has_url(slide, url):
    for shape in slide.shapes:
        try:
            if shape.click_action.hyperlink.address == url:
                return True
        except ValueError:
            pass
        if getattr(shape, "has_text_frame", False):
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    if run.hyperlink.address == url:
                        return True
    return False


def add_button(slide):
    x, y, width, height = 9.45, 6.58, 2.78, 0.4
    shape = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
        Inches(x), Inches(y), Inches(width), Inches(height),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = BLUE
    shape.line.color.rgb = BLUE
    shape.click_action.hyperlink.address = TIOBE_URL

    label = slide.shapes.add_textbox(
        Inches(x + 0.05), Inches(y + 0.035), Inches(width - 0.1), Inches(0.28)
    )
    frame = label.text_frame
    frame.clear()
    frame.word_wrap = False
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    frame.margin_left = frame.margin_right = Inches(0.02)
    frame.margin_top = frame.margin_bottom = Inches(0.01)
    paragraph = frame.paragraphs[0]
    paragraph.alignment = PP_ALIGN.CENTER
    run = paragraph.add_run()
    run.text = "TIOBE LANGUAGE INDEX"
    run.font.name = "Aptos"
    run.font.size = Pt(8)
    run.font.bold = True
    run.font.color.rgb = WHITE
    run.hyperlink.address = TIOBE_URL


def main():
    prs = Presentation(PPTX)
    assert len(prs.slides) == 97
    slide = prs.slides[16]
    assert any("griglia comune" in getattr(shape, "text", "").lower() for shape in slide.shapes)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    BACKUPS.mkdir(parents=True, exist_ok=True)
    backup = BACKUPS / f"panoramica-linguaggi-prima-link-tiobe-{stamp}.pptx"
    shutil.copy2(PPTX, backup)

    if not slide_has_url(slide, TIOBE_URL):
        add_button(slide)

    note = (
        "INDICATORE DI POPOLARITA: il TIOBE Programming Community index è aggiornato "
        "mensilmente e può fornire un segnale di popolarità/ecosistema; non misura la "
        f"qualità migliore del linguaggio né le righe di codice: {TIOBE_URL}"
    )
    notes = slide.notes_slide.notes_text_frame
    if note not in notes.text:
        notes.text += f"\n{note}"

    prs.save(PPTX)
    print(f"patched={PPTX} slide=17")
    print(f"backup={backup}")


if __name__ == "__main__":
    main()
