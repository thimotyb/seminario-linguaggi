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
PLAYGROUND_URL = "https://dotnetfiddle.net/"

TEAL = RGBColor(40, 167, 158)
CORAL = RGBColor(240, 102, 84)
SKY = RGBColor(83, 166, 214)
WHITE = RGBColor(255, 255, 255)


def add_button(slide, caption, url, x, width, fill):
    shape = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
        Inches(x), Inches(6.65), Inches(width), Inches(0.4),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = fill
    shape.click_action.hyperlink.address = url

    text = slide.shapes.add_textbox(
        Inches(x + 0.04), Inches(6.68), Inches(width - 0.08), Inches(0.3)
    )
    frame = text.text_frame
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


def main():
    prs = Presentation(PPTX)
    assert len(prs.slides) == 97
    slide = prs.slides[23]
    assert any(
        getattr(shape, "has_text_frame", False)
        and shape.text.strip() == ".NET: linguaggi, runtime e servizi cloud"
        for shape in slide.shapes
    )

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    BACKUPS.mkdir(parents=True, exist_ok=True)
    backup = BACKUPS / f"panoramica-linguaggi-prima-link-dotnet-playground-{stamp}.pptx"
    shutil.copy2(PPTX, backup)

    old_urls = {
        "https://learn.microsoft.com/it-it/dotnet/core/introduction",
        "https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures",
    }
    for shape in list(slide.shapes):
        urls = set()
        try:
            if shape.click_action.hyperlink.address:
                urls.add(shape.click_action.hyperlink.address)
        except ValueError:
            pass
        if getattr(shape, "has_text_frame", False):
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    if run.hyperlink.address:
                        urls.add(run.hyperlink.address)
        if urls & old_urls:
            slide.shapes._spTree.remove(shape._element)

    add_button(
        slide,
        "INTRODUZIONE .NET",
        "https://learn.microsoft.com/it-it/dotnet/core/introduction",
        6.86,
        1.66,
        TEAL,
    )
    add_button(slide, "PROVA .NET ONLINE", PLAYGROUND_URL, 8.65, 1.66, SKY)
    add_button(
        slide,
        "ARCHITETTURA AZURE",
        "https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures",
        10.44,
        1.78,
        CORAL,
    )

    notes = slide.notes_slide.notes_text_frame
    notes.text += (
        "\nPLAYGROUND: .NET Fiddle permette di scrivere, compilare ed eseguire rapidamente "
        "C#, F# e VB.NET nel browser, scegliendo anche versioni moderne di .NET: "
        f"{PLAYGROUND_URL}"
    )

    prs.save(PPTX)
    print(f"patched={PPTX}")
    print(f"backup={backup}")


if __name__ == "__main__":
    main()
