from pptx import Presentation
from pptx.util import Inches

p = "output/panoramica-linguaggi-scelte-architetturali-scheletro.pptx"
prs = Presentation(p)
assert len(prs.slides) == 91
for number in range(83, 87):
    slide = prs.slides[number - 1]
    matches = [shape for shape in slide.shapes
               if getattr(shape, "has_text_frame", False)
               and shape.text.startswith(("Fonte:", "Fonti:", "Screenshot"))]
    assert len(matches) == 1, (number, len(matches))
    matches[0].top = Inches(6.86)
    matches[0].height = Inches(.18)
prs.save(p)
print("adjusted source labels on slides 83-86")
