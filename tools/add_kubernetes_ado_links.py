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
KILLERCODA_URL = "https://killercoda.com/kubernetes"
ADO_URL = "https://thimoty.visualstudio.com/TitanoPortal/_workitems/recentlyupdated/"

TEAL = RGBColor(40, 167, 158)
AZURE = RGBColor(0, 120, 212)
WHITE = RGBColor(255, 255, 255)


def add_button(slide, caption, url, x, y, width, fill):
    shape = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
        Inches(x), Inches(y), Inches(width), Inches(0.38),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = fill
    shape.click_action.hyperlink.address = url

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
    run.text = caption
    run.font.name = "Aptos"
    run.font.size = Pt(8)
    run.font.bold = True
    run.font.color.rgb = WHITE
    run.hyperlink.address = url


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


def append_note(slide, text):
    notes = slide.notes_slide.notes_text_frame
    if text not in notes.text:
        notes.text += f"\n{text}"


def main():
    prs = Presentation(PPTX)
    assert len(prs.slides) == 97
    kubernetes = prs.slides[58]
    devops = prs.slides[65]
    assert any("Kubernetes: dal cluster" in getattr(shape, "text", "") for shape in kubernetes.shapes)
    assert any("Caso S21: DevOps" in getattr(shape, "text", "") for shape in devops.shapes)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    BACKUPS.mkdir(parents=True, exist_ok=True)
    backup = BACKUPS / f"panoramica-linguaggi-prima-link-kubernetes-ado-{stamp}.pptx"
    shutil.copy2(PPTX, backup)

    if not slide_has_url(kubernetes, KILLERCODA_URL):
        add_button(kubernetes, "SANDBOX KUBERNETES", KILLERCODA_URL, 9.67, 6.25, 2.55, TEAL)
    append_note(
        kubernetes,
        "SANDBOX: Killercoda offre scenari e un playground Kubernetes nel browser; è indicato anche dalla documentazione ufficiale Kubernetes: "
        + KILLERCODA_URL,
    )

    if not slide_has_url(devops, ADO_URL):
        add_button(devops, "APRI TITANOPORTAL IN ADO", ADO_URL, 9.47, 6.25, 2.75, AZURE)
    append_note(
        devops,
        "DEMO LIVE: progetto Azure DevOps TitanoPortal, work item aggiornati di recente: " + ADO_URL,
    )

    prs.save(PPTX)
    print(f"patched={PPTX} slides=59,66")
    print(f"backup={backup}")


if __name__ == "__main__":
    main()

