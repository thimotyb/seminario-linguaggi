from pathlib import Path
from copy import deepcopy

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

PPTX = Path("output/panoramica-linguaggi-scelte-architetturali-scheletro.pptx")
ASSETS = Path("assets/source-security")
AGID = "https://drive.google.com/file/d/1vK_ellHCkkFT6jE_KqAr3Kk4SaeWwz23/view"
MS_TOOL = "https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool"
MS_START = "https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-getting-started"
MS_DOWNLOAD = "https://aka.ms/threatmodelingtool"

NAVY = RGBColor(17, 36, 63); NAVY2 = RGBColor(25, 51, 82)
TEAL = RGBColor(40, 167, 158); CORAL = RGBColor(240, 102, 84)
SKY = RGBColor(83, 166, 214); WHITE = RGBColor(255, 255, 255)
PALE = RGBColor(232, 239, 245); MUTED = RGBColor(91, 107, 126)
GOLD = RGBColor(210, 160, 45); RED = RGBColor(201, 73, 64)


def box(slide, x, y, w, h, fill, line=None, radius=True):
    kind = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE if radius else MSO_AUTO_SHAPE_TYPE.RECTANGLE
    sh = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill; sh.line.color.rgb = line or fill
    return sh


def text(slide, value, x, y, w, h, size=15, color=NAVY, bold=False,
         align=PP_ALIGN.LEFT, font="Aptos", valign=MSO_ANCHOR.MIDDLE):
    sh = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = sh.text_frame; tf.clear(); tf.word_wrap = True; tf.vertical_anchor = valign
    tf.margin_left = tf.margin_right = Inches(.03); tf.margin_top = tf.margin_bottom = Inches(.02)
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = value; r.font.name = font; r.font.size = Pt(size)
    r.font.bold = bold; r.font.color.rgb = color
    return sh


def bullets(slide, items, x, y, w, h, size=14, color=NAVY):
    sh = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = sh.text_frame; tf.clear(); tf.word_wrap = True
    tf.margin_left = Inches(.06); tf.margin_right = Inches(.03)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = "•  " + item; p.space_after = Pt(8)
        for r in p.runs:
            r.font.name = "Aptos"; r.font.size = Pt(size); r.font.color.rgb = color
    return sh


def button(slide, caption, url, x, y, w, fill=TEAL):
    sh = box(slide, x, y, w, .43, fill); sh.click_action.hyperlink.address = url
    t = text(slide, caption, x+.08, y+.05, w-.16, .28, 9, WHITE, True, PP_ALIGN.CENTER)
    t.text_frame.paragraphs[0].runs[0].hyperlink.address = url


def picture_fit(slide, path, x, y, w, h, link=None):
    with Image.open(path) as im: ratio = im.width / im.height
    frame = w / h
    if ratio > frame:
        ph = w / ratio; px=x; py=y+(h-ph)/2; pw=w
    else:
        pw = h*ratio; px=x+(w-pw)/2; py=y; ph=h
    sh = slide.shapes.add_picture(str(path), Inches(px), Inches(py), width=Inches(pw), height=Inches(ph))
    if link: sh.click_action.hyperlink.address = link
    return sh


def base(prs, title, number, dark=False):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    notes_tree = slide.notes_slide.shapes._spTree
    template_notes = prs.slides[81].notes_slide
    for template_shape in template_notes.shapes:
        notes_tree.insert_element_before(deepcopy(template_shape._element), "p:extLst")
    bg = slide.background.fill; bg.solid(); bg.fore_color.rgb = NAVY if dark else RGBColor(247,249,251)
    box(slide,.55,.42,.12,.12,CORAL)
    text(slide,title,.8,.63,11.75,.72,27,WHITE if dark else NAVY,True)
    text(slide,"DECISIONI E QUALITÀ",.58,7.12,8.5,.22,9,SKY if dark else MUTED,True)
    text(slide,"15 min",10.92,7.08,1.35,.25,9,SKY if dark else MUTED,False,PP_ALIGN.RIGHT)
    n=text(slide,f"{number:02d}",12.38,7.04,.38,.28,10,CORAL,True,PP_ALIGN.RIGHT); n.name="SLIDE_NUMBER"
    return slide


def source(slide, value, dark=False):
    text(slide,value,.82,6.86,11.4,.18,8,SKY if dark else MUTED)


def notes(slide, purpose, sources, detail):
    tf=slide.notes_slide.notes_text_frame; tf.clear()
    tf.text=f"OBIETTIVO: {purpose}\nFONTI: {sources}\nNOTE: {detail}"


prs=Presentation(PPTX)
assert len(prs.slides)==87
assert next(s.text for s in prs.slides[81].shapes if getattr(s,"has_text_frame",False) and s.text.strip()) == "Sicurezza applicativa di base"
created=[]

# 83 — quadro AgID
s=base(prs,"Linee guida AgID: quattro prospettive sul software sicuro",83)
text(s,"Riferimento introduttivo del 21 novembre 2017 · applicazione alla Pubblica Amministrazione",.85,1.4,11.6,.34,12,CORAL,True,PP_ALIGN.CENTER)
cards=[
    ("SECURE SDLC","azioni di sicurezza in tutte le fasi",TEAL),
    ("SECURE CODING","prevenire e individuare vulnerabilità",SKY),
    ("HARDENING","proteggere software di base e contesto",GOLD),
    ("THREAT MODELING","minacce, mitigazioni, Secure/Privacy by Design",CORAL),
]
for i,(head,body,color) in enumerate(cards):
    x=.82+(i%2)*6.03; y=2.0+(i//2)*1.72
    box(s,x,y,5.68,1.4,WHITE,PALE)
    box(s,x,y,.13,1.4,color,color,False)
    text(s,head,x+.35,y+.2,2.25,.28,13,color,True)
    text(s,body,x+2.58,y+.18,2.72,.72,13,NAVY,False,PP_ALIGN.LEFT)
text(s,"OBIETTIVO",.9,5.58,1.25,.24,10,CORAL,True)
text(s,"Disponibilità · Integrità · Riservatezza delle informazioni della PA",2.08,5.5,9.65,.42,17,NAVY,True)
button(s,"APRI IL PDF AGID",AGID,4.75,6.05,3.8,CORAL)
source(s,"Fonte: AgID, Linee guida di sicurezza nello sviluppo delle applicazioni, pp. 4–7")
notes(s,"inquadrare i quattro allegati tecnici richiamati dall'introduzione AgID.",AGID,"Il documento è datato 2017: presentarlo come riferimento metodologico e verificare sempre eventuali aggiornamenti normativi applicabili.")
created.append(s)

# 84 — processo e responsabilità
s=base(prs,"Secure SDLC nella PA: requisiti, controlli e responsabilità",84,True)
stages=[("DESIGN","requisiti + threat model"),("CODING","standard + review"),("VERIFY","SAST · DAST · test"),("RELEASE","accettazione + hardening"),("OPERATE","monitoraggio + aggiornamento")]
for i,(head,body) in enumerate(stages):
    x=.43+i*2.57
    box(s,x,1.55,2.17,1.12,[CORAL,TEAL,SKY,GOLD,MUTED][i])
    text(s,head,x+.12,1.74,1.93,.25,12,WHITE,True,PP_ALIGN.CENTER)
    text(s,body,x+.12,2.09,1.93,.35,10,WHITE,False,PP_ALIGN.CENTER)
    if i<4:text(s,"→",x+2.18,1.93,.35,.28,16,WHITE,True,PP_ALIGN.CENTER)
box(s,.75,3.15,3.65,2.56,NAVY2); text(s,"GOVERNANCE PA",1.02,3.43,3.1,.28,13,CORAL,True,PP_ALIGN.CENTER)
bullets(s,["struttura tecnica che guida e monitora","infrastruttura operativa sicura","coordinamento funzionale"],1.02,3.93,3.08,1.35,12,WHITE)
box(s,4.85,3.15,3.65,2.56,NAVY2); text(s,"FORNITORE / TEAM",5.12,3.43,3.1,.28,13,TEAL,True,PP_ALIGN.CENTER)
bullets(s,["standard e best practice dichiarati","vulnerabilità corrette","revisioni di sicurezza continue"],5.12,3.93,3.08,1.35,12,WHITE)
box(s,8.95,3.15,3.65,2.56,NAVY2); text(s,"EVIDENZE",9.22,3.43,3.1,.28,13,SKY,True,PP_ALIGN.CENTER)
bullets(s,["controlli e risultati","criteri di accettazione","owner e tracciabilità"],9.22,3.93,3.08,1.35,12,WHITE)
source(s,"Fonte: AgID, pp. 7–9 · impatti organizzativi, strategia di applicazione e responsabilità",True)
notes(s,"tradurre le indicazioni AgID in gate ed evidenze lungo il ciclo di sviluppo.",AGID,"Collegare questa slide al caso Azure DevOps: requisiti, ticket, pipeline, test e dashboard diventano prove del controllo svolto.")
created.append(s)

# 85 — processo threat modeling
s=base(prs,"Threat modeling: trovare difetti di design prima del codice",85)
box(s,.72,1.43,5.2,4.87,WHITE,PALE)
picture_fit(s,ASSETS/"microsoft-sdl-threat-model-process.png",1.22,1.72,4.2,3.92,MS_START)
text(s,"Ciclo Microsoft SDL",1.15,5.71,4.35,.27,11,TEAL,True,PP_ALIGN.CENTER)
text(s,"IL MODELLO DIVENTA UN ARTEFATTO DI PROGETTO",6.35,1.56,5.65,.28,11,CORAL,True)
steps=[("1","Definire requisiti e obiettivi di sicurezza"),("2","Disegnare componenti, flussi e trust boundary"),("3","Identificare le minacce"),("4","Definire e assegnare le mitigazioni"),("5","Validare mitigazioni e rischio residuo")]
for i,(n,body) in enumerate(steps):
    y=2.04+i*.76
    box(s,6.4,y,.48,.48,[CORAL,TEAL,SKY,GOLD,NAVY2][i]); text(s,n,6.5,y+.1,.28,.24,12,WHITE,True,PP_ALIGN.CENTER)
    text(s,body,7.08,y-.01,4.78,.48,13,NAVY,True)
text(s,"AGID: fase preventiva per individuare requisiti di sicurezza e privacy",6.45,5.92,5.4,.38,11,MUTED,True,PP_ALIGN.CENTER)
button(s,"GUIDA MICROSOFT",MS_START,8.0,6.23,2.55,TEAL)
source(s,"Fonti: AgID pp. 4–5 · Microsoft Security Development Lifecycle")
notes(s,"spiegare il threat modeling come attività iterativa di design, non come penetration test tardivo.",f"{AGID} ; {MS_START}","Il processo Microsoft sintetizza: diagram, identify, mitigate, validate; la pagina SDL aggiunge esplicitamente la definizione dei requisiti di sicurezza.")
created.append(s)

# 86 — tool, DFD e STRIDE
s=base(prs,"Microsoft Threat Modeling Tool: dal DFD alle minacce STRIDE",86,True)
box(s,.62,1.38,8.18,4.96,WHITE,WHITE)
picture_fit(s,ASSETS/"microsoft-generated-threats.png",.76,1.54,7.9,4.64,MS_START)
text(s,"DFD + elenco delle minacce generate per elemento",1.25,5.95,6.9,.24,10,NAVY,True,PP_ALIGN.CENTER)
text(s,"STRIDE",9.17,1.48,2.85,.3,15,CORAL,True,PP_ALIGN.CENTER)
stride=[("S","Spoofing","autenticazione"),("T","Tampering","integrità"),("R","Repudiation","non ripudio"),("I","Information disclosure","riservatezza"),("D","Denial of service","disponibilità"),("E","Elevation of privilege","autorizzazione")]
for i,(letter,name,prop) in enumerate(stride):
    y=1.98+i*.63
    box(s,9.02,y,.43,.43,[CORAL,TEAL,SKY,GOLD,MUTED,NAVY2][i]); text(s,letter,9.12,y+.09,.23,.22,11,WHITE,True,PP_ALIGN.CENTER)
    text(s,name,9.61,y-.01,2.53,.23,10,WHITE,True)
    text(s,prop,9.61,y+.23,2.53,.2,8,SKY)
text(s,"Il tool guida il diagramma, applica STRIDE per elemento e gestisce mitigazioni e report.",9.0,5.86,3.25,.48,10,WHITE,True,PP_ALIGN.CENTER)
button(s,"PANORAMICA",MS_TOOL,8.93,6.36,1.45,TEAL)
button(s,"GUIDA",MS_START,10.5,6.36,1.1,SKY)
button(s,"DOWNLOAD",MS_DOWNLOAD,11.72,6.36,.95,CORAL)
source(s,"Screenshot e metodo: Microsoft Learn, Threat Modeling Tool",True)
notes(s,"mostrare come un DFD consenta di ragionare su entità esterne, processi, data store, flussi e confini di trust.",f"{MS_TOOL} ; {MS_START} ; {MS_DOWNLOAD}","Fare clic sullo screenshot o sui pulsanti. Il tool è pensato anche per non specialisti e genera categorie STRIDE e suggerimenti di mitigazione a partire dalla struttura del diagramma.")
created.append(s)

# Move the four new slides immediately after slide 82, preserving every existing slide object.
lst=prs.slides._sldIdLst
new_ids=list(lst[-4:])
for item in new_ids: lst.remove(item)
for offset,item in enumerate(new_ids): lst.insert(82+offset,item)

for i,slide in enumerate(prs.slides,1):
    for sh in slide.shapes:
        if sh.name=="SLIDE_NUMBER" and sh.has_text_frame:
            p=sh.text_frame.paragraphs[0]
            if p.runs: p.runs[0].text=f"{i:02d}"

prs.save(PPTX)
print(f"patched={PPTX} slides={len(prs.slides)} inserted=83-86")
