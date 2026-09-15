from pathlib import Path
from copy import deepcopy

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

PPTX = Path('output/panoramica-linguaggi-scelte-architetturali-scheletro.pptx')
IMAGE = Path('assets/source-gitflow/vincent-driessen-git-model.png')
ARTICLE = 'https://nvie.com/posts/a-successful-git-branching-model/'

NAVY = RGBColor(17, 36, 63)
TEAL = RGBColor(40, 167, 158)
CORAL = RGBColor(240, 102, 84)
SKY = RGBColor(83, 166, 214)
WHITE = RGBColor(255, 255, 255)
PALE = RGBColor(232, 239, 245)
MUTED = RGBColor(91, 107, 126)


def box(slide, x, y, w, h, fill, line=None):
    sh = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h),
    )
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = line or fill
    return sh


def text(slide, value, x, y, w, h, size=13, color=NAVY, bold=False,
         align=PP_ALIGN.LEFT):
    sh = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = sh.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(.04)
    tf.margin_top = tf.margin_bottom = Inches(.02)
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = value
    run.font.name = 'Aptos'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return sh


prs = Presentation(PPTX)
assert len(prs.slides) == 97
slide = prs.slides[69]
assert next(sh.text for sh in slide.shapes if getattr(sh, 'has_text_frame', False) and sh.text.strip()) == 'Git: il codice avanza per branch e controlli'

# Preserve title and standard footer objects; replace only the prior branching visual.
for sh in list(slide.shapes):
    if 1.35 <= sh.top / 914400 < 6.72:
        slide.shapes._spTree.remove(sh._element)

# Original portrait diagram, linked directly to the author's article.
frame = box(slide, 4.46, 1.31, 4.41, 5.34, WHITE, PALE)
picture = slide.shapes.add_picture(
    str(IMAGE), Inches(4.73), Inches(1.4), width=Inches(3.86), height=Inches(5.12)
)
picture.name = 'Git Flow — Vincent Driessen'
picture.click_action.hyperlink.address = ARTICLE

# Minimal reading key around the original figure.
text(slide, 'GIT FLOW', .82, 1.52, 3.05, .38, 17, CORAL, True, PP_ALIGN.CENTER)
left = box(slide, .78, 2.03, 3.18, 2.67, NAVY)
text(slide, 'BRANCH PRINCIPALI', 1.02, 2.28, 2.72, .26, 11, SKY, True, PP_ALIGN.CENTER)
text(slide, 'master\nproduzione e release', 1.08, 2.75, 2.6, .58, 13, WHITE, True, PP_ALIGN.CENTER)
text(slide, 'develop\nintegrazione della prossima release', 1.08, 3.64, 2.6, .7, 13, WHITE, True, PP_ALIGN.CENTER)
text(slide, 'feature/* · release/* · hotfix/*', .88, 5.04, 3.0, .5, 11, NAVY, True, PP_ALIGN.CENTER)

text(slide, 'QUANDO È ADATTO?', 9.3, 1.52, 3.0, .38, 14, TEAL, True, PP_ALIGN.CENTER)
box(slide, 9.18, 2.03, 3.28, 1.3, WHITE, PALE)
text(slide, 'Software versionato o più versioni supportate contemporaneamente.', 9.43, 2.25, 2.78, .78, 13, NAVY, True, PP_ALIGN.CENTER)
text(slide, 'NOTA 2020', 9.3, 3.76, 3.0, .3, 12, CORAL, True, PP_ALIGN.CENTER)
box(slide, 9.18, 4.13, 3.28, 1.18, NAVY)
text(slide, 'Per continuous delivery Driessen suggerisce un workflow più semplice, come GitHub Flow.', 9.42, 4.31, 2.8, .72, 11, WHITE, True, PP_ALIGN.CENTER)

button = box(slide, 9.55, 5.72, 2.54, .48, TEAL)
button.click_action.hyperlink.address = ARTICLE
label = text(slide, 'APRI L’ARTICOLO ORIGINALE', 9.68, 5.81, 2.28, .27, 9, WHITE, True, PP_ALIGN.CENTER)
label.text_frame.paragraphs[0].runs[0].hyperlink.address = ARTICLE

# Replace the old source line while preserving the deck footer and slide number.
for sh in list(slide.shapes):
    if getattr(sh, 'has_text_frame', False) and sh.text.startswith('Fonte: Guida S21'):
        slide.shapes._spTree.remove(sh._element)
source = text(slide, 'Figura: Vincent Driessen, “A successful Git branching model” · CC BY-SA', .82, 6.76, 10.8, .2, 8, MUTED)
source.text_frame.paragraphs[0].runs[0].hyperlink.address = ARTICLE

notes = slide.notes_slide.notes_text_frame
notes.clear()
notes.text = (
    'OBIETTIVO: spiegare il modello Git Flow attraverso la figura originale di Vincent Driessen.\n'
    f'FONTI: {ARTICLE}\n'
    'NOTE: la figura è pubblicata con licenza CC BY-SA. Evidenziare la nota retrospettiva del 2020: '
    'Git Flow resta adatto a software esplicitamente versionato o con più versioni supportate; per '
    'applicazioni in continuous delivery l’autore suggerisce un workflow più semplice, come GitHub Flow.'
)

prs.save(PPTX)
print('updated slide 70 with the original Vincent Driessen Git Flow diagram')
