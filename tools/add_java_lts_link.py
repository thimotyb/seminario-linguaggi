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
ROADMAP_URL = "https://www.oracle.com/java/technologies/java-se-support-roadmap.html"

ORACLE_RED = RGBColor(196, 38, 29)
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
    x, y, width, height = 9.55, 6.59, 2.67, 0.4
    shape = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
        Inches(x), Inches(y), Inches(width), Inches(height),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = ORACLE_RED
    shape.line.color.rgb = ORACLE_RED
    shape.click_action.hyperlink.address = ROADMAP_URL

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
    run.text = "ROADMAP SUPPORTO LTS"
    run.font.name = "Aptos"
    run.font.size = Pt(8)
    run.font.bold = True
    run.font.color.rgb = WHITE
    run.hyperlink.address = ROADMAP_URL


def main():
    prs = Presentation(PPTX)
    assert len(prs.slides) == 97
    slide = prs.slides[17]
    assert any(
        "Come funziona Java" in getattr(shape, "text", "") for shape in slide.shapes
    )

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    BACKUPS.mkdir(parents=True, exist_ok=True)
    backup = BACKUPS / f"panoramica-linguaggi-prima-link-java-lts-{stamp}.pptx"
    shutil.copy2(PPTX, backup)

    if not slide_has_url(slide, ROADMAP_URL):
        # Accorcia il riquadro della fonte per lasciare libero il pulsante nel footer.
        for shape in slide.shapes:
            if getattr(shape, "has_text_frame", False) and shape.text.startswith(
                "Java Performance Course"
            ):
                shape.width = Inches(8.45)
        add_button(slide)

    note = (
        "SUPPORTO LTS: usare la Oracle Java SE Support Roadmap come fonte aggiornata "
        "per distinguere release LTS e non-LTS e verificare le rispettive finestre di "
        f"supporto: {ROADMAP_URL}"
    )
    notes = slide.notes_slide.notes_text_frame
    if note not in notes.text:
        notes.text += f"\n{note}"

    prs.save(PPTX)
    print(f"patched={PPTX} slide=18")
    print(f"backup={backup}")


if __name__ == "__main__":
    main()
