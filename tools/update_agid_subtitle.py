from pptx import Presentation

p = "output/panoramica-linguaggi-scelte-architetturali-scheletro.pptx"
prs = Presentation(p)
assert len(prs.slides) == 91
slide = prs.slides[82]

old = "Riferimento introduttivo del 21 novembre 2017 · applicazione alla Pubblica Amministrazione"
new = "Linee guida ufficiali per lo sviluppo sicuro delle applicazioni nella Pubblica Amministrazione"
matches = [shape for shape in slide.shapes
           if getattr(shape, "has_text_frame", False) and shape.text == old]
assert len(matches) == 1
shape = matches[0]
paragraph = shape.text_frame.paragraphs[0]
if paragraph.runs:
    paragraph.runs[0].text = new
else:
    shape.text = new

notes = slide.notes_slide.notes_text_frame
notes.text = notes.text.replace(
    "Il documento è datato 2017: presentarlo come riferimento metodologico e verificare sempre eventuali aggiornamenti normativi applicabili.",
    "Usare i collegamenti alla pagina ufficiale AgID, al documento pubblicato nel 2024 e all'Allegato 4 dedicato al threat modeling.",
)

prs.save(p)
print("updated AGID subtitle on slide 83")
