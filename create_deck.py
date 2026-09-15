from pathlib import Path
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt
from PIL import Image


OUT = Path("output")
OUT.mkdir(exist_ok=True)
PPTX_PATH = OUT / "panoramica-linguaggi-scelte-architetturali-scheletro.pptx"

W, H = Inches(13.333), Inches(7.5)
NAVY = RGBColor(16, 28, 48)
NAVY_2 = RGBColor(27, 43, 70)
CREAM = RGBColor(247, 244, 237)
WHITE = RGBColor(255, 255, 255)
CORAL = RGBColor(240, 102, 84)
TEAL = RGBColor(40, 167, 158)
SKY = RGBColor(93, 174, 219)
INK = RGBColor(28, 39, 55)
MUTED = RGBColor(103, 114, 128)
PALE = RGBColor(231, 235, 236)

prs = Presentation()
prs.slide_width = W
prs.slide_height = H


def rect(slide, x, y, w, h, fill, radius=False, line=None):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    shp.line.color.rgb = line or fill
    return shp


def text(slide, value, x, y, w, h, size=24, color=INK, bold=False,
         font="Aptos", align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame; tf.clear(); tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.03)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]; p.text = value; p.alignment = align
    p.font.name = font; p.font.size = Pt(size); p.font.bold = bold; p.font.color.rgb = color
    return box


def add_rich_lines(slide, lines, x, y, w, h, size=21, color=INK):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame; tf.clear(); tf.word_wrap = True
    tf.margin_left = Inches(.08); tf.margin_right = Inches(.04)
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line; p.font.name = "Aptos"; p.font.size = Pt(size); p.font.color.rgb = color
        p.space_after = Pt(11); p.level = 0
        p.text = "•  " + p.text
    return box


def link_button(slide, label, url, x, y, w, dark=False):
    fill = NAVY_2 if dark else WHITE
    box = rect(slide, x, y, w, .48, fill, True, TEAL)
    t = text(slide, label, x+.12, y+.13, w-.24, .2, 10, TEAL, True, align=PP_ALIGN.CENTER)
    t.text_frame.paragraphs[0].runs[0].hyperlink.address = url
    return box


def footer(slide, section, number, duration=None, dark=False):
    col = RGBColor(191, 200, 211) if dark else MUTED
    text(slide, section.upper(), .58, 7.12, 8.5, .22, 8.5, col, True)
    if duration:
        text(slide, duration, 10.92, 7.08, 1.35, .25, 9, col, False, align=PP_ALIGN.RIGHT)
    nbox = text(slide, f"{number:02d}", 12.38, 7.04, .38, .28, 10, CORAL, True, align=PP_ALIGN.RIGHT)
    nbox.name = "SLIDE_NUMBER"


def notes(slide, purpose, drive_query, content=""):
    msg = f"SCOPO DIDATTICO\n{purpose}\n\nRICERCA SU DRIVE\n{drive_query}"
    if content:
        msg += f"\n\nDA SVILUPPARE\n{content}"
    slide.notes_slide.notes_text_frame.text = msg


def base(light=True):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill; bg.solid(); bg.fore_color.rgb = CREAM if light else NAVY
    rect(slide, .55, .42, .12, .12, CORAL, True)
    return slide


def title_slide(title, subtitle, eyebrow="PERCORSO FORMATIVO • 16 ORE"):
    s = base(False)
    rect(s, 9.7, 0, 3.633, 7.5, NAVY_2)
    rect(s, 9.7, 0, .13, 7.5, TEAL)
    text(s, eyebrow, .78, .7, 8.2, .35, 12, TEAL, True)
    text(s, title, .78, 1.32, 8.15, 2.5, 31, WHITE, True)
    text(s, subtitle, .8, 4.1, 7.9, 1.0, 17, RGBColor(207,216,229))
    text(s, "INPS", 10.22, 1.1, 2.4, .7, 28, WHITE, True)
    text(s, "LINGUAGGI\nARCHITETTURE\nDECISIONI", 10.22, 2.2, 2.4, 2.0, 15, SKY, True)
    text(s, "Scheletro editoriale\nContenuti e figure da appunti Drive", 10.22, 5.7, 2.45, .8, 11, RGBColor(191,200,211))
    notes(s, "Aprire il corso e chiarire che l'obiettivo è leggere e valutare scelte tecnologiche, non imparare a programmare.", "Nessuna: copertina istituzionale. Cercare eventualmente logo o immagine già usata nelle lezioni INPS.")
    return s


def section_slide(kicker, title, subtitle, number):
    s = base(False)
    text(s, kicker, .8, .78, 3.2, .35, 12, TEAL, True)
    text(s, title, .8, 1.53, 8.6, 1.65, 34, WHITE, True)
    text(s, subtitle, .82, 3.52, 7.8, 1.0, 17, RGBColor(207,216,229))
    text(s, f"{number:02d}", 10.42, 1.02, 2.0, 1.2, 62, CORAL, True, align=PP_ALIGN.RIGHT)
    rect(s, 9.82, 2.55, 2.65, .12, TEAL)
    notes(s, f"Introdurre il blocco {number}: {title} e collegarlo agli obiettivi del corso.", f"Materiali introduttivi {title}; cercare una figura panoramica già usata nelle lezioni.")
    return s


def content_slide(title_, section, number, bullets, duration="10 min", purpose=None, query=None, prompt=None):
    s = base(True)
    text(s, title_, .8, .7, 11.75, .72, 27, NAVY, True)
    rect(s, .8, 1.55, 1.25, .06, CORAL)
    add_rich_lines(s, bullets, .84, 1.92, 7.1, 4.6, 19)
    rect(s, 8.35, 1.75, 4.12, 4.65, WHITE, True, PALE)
    text(s, "VISUAL / ESEMPIO", 8.72, 2.12, 3.25, .3, 11, TEAL, True)
    text(s, prompt or "Inserire una figura, uno schema o un esempio tratto dagli appunti.", 8.72, 2.72, 3.22, 1.45, 18, NAVY, True)
    text(s, "DA REPERIRE SU DRIVE", 8.72, 5.48, 3.05, .28, 9, CORAL, True)
    footer(s, section, number, duration)
    notes(s, purpose or f"Presentare {title_.lower()} con taglio comparativo e non operativo.", query or title_, "Sostituire il riquadro visual con materiale verificato; ridurre il testo a un messaggio principale e 2-4 evidenze.")
    return s


def comparison_slide(title_, section, number, left_title, right_title, left, right, duration="12 min", query=None):
    s = base(True)
    text(s, title_, .8, .7, 11.7, .65, 27, NAVY, True)
    for x, ttl, items, color in [(0.8, left_title, left, TEAL), (6.8, right_title, right, CORAL)]:
        rect(s, x, 1.65, 5.7, 4.8, WHITE, True, PALE)
        rect(s, x, 1.65, 5.7, .14, color)
        text(s, ttl, x+.38, 2.05, 4.85, .55, 21, NAVY, True)
        add_rich_lines(s, items, x+.38, 2.83, 4.85, 2.9, 17)
    footer(s, section, number, duration)
    notes(s, f"Confrontare {left_title} e {right_title} usando dimensioni omogenee.", query or f"{left_title} {right_title} confronto", "Integrare esempi e figure precedenti; evitare classifiche assolute e rendere esplicito il contesto.")
    return s


def activity_slide(title_, section, number, scenario, questions, duration="20 min", query=""):
    s = base(False)
    text(s, "CONFRONTO GUIDATO", .82, .7, 4, .35, 11, TEAL, True)
    text(s, title_, .82, 1.25, 11.4, .8, 29, WHITE, True)
    rect(s, .82, 2.35, 4.4, 3.9, NAVY_2, True)
    text(s, "SCENARIO", 1.15, 2.74, 3.7, .3, 10, CORAL, True)
    text(s, scenario, 1.15, 3.28, 3.65, 2.2, 18, WHITE, True)
    rect(s, 5.58, 2.35, 6.7, 3.9, WHITE, True, WHITE)
    text(s, "DOMANDE", 5.98, 2.74, 5.8, .3, 10, TEAL, True)
    add_rich_lines(s, questions, 5.98, 3.22, 5.72, 2.4, 17, INK)
    footer(s, section, number, duration, True)
    notes(s, "Attivare il gruppo e far emergere criteri decisionali, rischi e informazioni mancanti.", query or title_, "Sostituire lo scenario con un caso già usato nelle lezioni o con un caso INPS anonimizzato.")
    return s


def picture_fit(slide, path, x, y, w, h):
    """Fit an image without distortion, centered in the requested frame."""
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    pw, ph = iw * scale, ih * scale
    return slide.shapes.add_picture(str(path), Inches(x + (w-pw)/2), Inches(y + (h-ph)/2), Inches(pw), Inches(ph))


def source_label(slide, label, dark=False):
    color = RGBColor(177, 188, 202) if dark else MUTED
    text(slide, label, .82, 6.76, 10.8, .2, 7.5, color)


def microservices_comparison(number):
    s = base(True)
    text(s, "Monolite e microservizi: cambia l'unità di cambiamento", .8, .7, 11.7, .65, 27, NAVY, True)
    rect(s,.78,1.55,8.15,5.02,WHITE,True,PALE)
    picture_fit(s, Path("assets/source-api/image1.png"), 1.0, 1.78, 7.72, 4.6)
    text(s,"COME LEGGERLA",9.28,1.72,2.55,.28,10,CORAL,True)
    text(s,"Nel monolite si replica e si rilascia l'intera applicazione.",9.28,2.22,2.8,1.0,17,NAVY,True)
    text(s,"Nei microservizi ogni servizio può scalare e cambiare in modo indipendente.",9.28,3.55,2.8,1.05,17,NAVY,True)
    rect(s,9.28,5.05,2.75,.08,TEAL)
    text(s,"Il prezzo è una rete di componenti da governare.",9.28,5.38,2.8,.75,15,MUTED,True)
    source_label(s, "Figura originale: appunti “ARCHITETTURE MICROSERVIZI…”, sezione MONOLITI E MICROSERVIZI")
    footer(s, "architetture", number, "18 min")
    notes(s, "Confrontare le due forme senza presentare i microservizi come evoluzione obbligatoria. La metafora di Stonehenge distingue unità grande, unità intermedia e singolo elemento.", "Microservices-Architectures_v3.pdf: pagine 18, 30-31, 36 e 38.", "Evidenziare che robustezza, velocità di cambiamento e complessità dipendono da contesto, design e capacità operative.")
    return s


def microservices_conditions(number):
    s = base(False)
    text(s, "I benefici dei microservizi non arrivano da soli", .82, .7, 11.4, .7, 28, WHITE, True)
    cards=[("SERVICE DISCOVERY","repliche e failover","assets/source-api-pdf/p047-2.jpg"),("RESILIENZA","circuit breaker","assets/source-api-pdf/p063-1.jpg"),("OSSERVABILITÀ","topologia e tracing","assets/source-api-pdf/p076-1.jpg")]
    for i,(ttl,sub,img) in enumerate(cards):
        x=.82+i*4.1
        rect(s,x,1.62,3.7,3.55,WHITE,True,WHITE)
        picture_fit(s,Path(img),x+.18,1.88,3.34,1.8)
        text(s,ttl,x+.22,3.88,3.25,.28,10,CORAL if i==1 else TEAL,True,align=PP_ALIGN.CENTER)
        text(s,sub,x+.22,4.35,3.25,.35,16,NAVY,True,align=PP_ALIGN.CENTER)
    text(s,"Deploy autonomi, scala selettiva e partial degradation richiedono automazione, pattern di resilienza e diagnosi distribuita.",1.12,5.55,11.05,.62,18,WHITE,True,align=PP_ALIGN.CENTER)
    source_label(s, "Figure originali: Microservices-Architectures_v3.pdf, pp. 47, 63 e 76", True)
    footer(s, "architetture", number, "15 min", True)
    notes(s, "Mettere in relazione ciascun beneficio promesso con le condizioni necessarie per ottenerlo.", "Microservices-Architectures_v3.pdf: pagine 36 e 38.", "Richiamare i rischi esplicitati nella fonte: complessità operativa, sicurezza, logging/monitoring distribuiti, tracing, latenza di rete e pattern di resilienza.")
    return s


def service_boundaries(number):
    s = base(True)
    text(s, "Il confine giusto parte dal dominio", .8, .7, 11.7, .65, 27, NAVY, True)
    picture_fit(s,Path("assets/source-api/image14.png"),.85,1.55,5.9,4.75)
    labels=[("BUSINESS", "Capacità e processi", TEAL), ("DATI", "Ownership e modello", SKY), ("SERVIZIO", "Responsabilità coesa", CORAL), ("API", "Contratto esplicito", NAVY_2)]
    for i,(k,v,c) in enumerate(labels):
        x=7.05+(i%2)*2.72; y=1.76+(i//2)*1.65
        rect(s,x,y,2.42,1.35,WHITE,True,PALE); rect(s,x,y,2.42,.12,c)
        text(s,k,x+.18,y+.28,2.0,.22,9,c,True); text(s,v,x+.18,y+.67,2.0,.45,15,NAVY,True)
    rect(s,7.05,5.14,5.15,1.0,NAVY,True)
    text(s,"Il confine segue il dominio: non coincide automaticamente con server, team o livelli tecnici.",7.36,5.35,4.52,.52,16,WHITE,True,align=PP_ALIGN.CENTER)
    source_label(s, "Figura originale: appunti “ARCHITETTURE MICROSERVIZI…”, schema ArchiMate/DDD")
    footer(s, "architetture", number, "15 min")
    notes(s, "Spiegare che la scomposizione nasce dalle capacità di business e dall'ownership dei dati, non dalla semplice divisione frontend/backend/database.", "Microservices-Architectures_v3.pdf: pagine 28-29 e 33.", "Collegare DDD, bounded context e livelli Experience/Process/System API senza approfondire l'implementazione.")
    return s


def container_lifecycle(number):
    s = base(True)
    text(s, "Container: immagine, istanza, runtime", .8, .7, 11.7, .65, 27, NAVY, True)
    picture_fit(s,Path("assets/source-platform/p080-1.jpg"),.78,1.5,7.25,4.95)
    text(s,"QUATTRO LIVELLI",8.45,1.72,3.3,.28,10,CORAL,True)
    add_rich_lines(s,["Dockerfile: istruzioni", "Immagine: layer versionati", "Registry: distribuzione", "Container: processo isolato"],8.42,2.25,3.55,2.5,16)
    rect(s,8.48,5.15,3.48,.9,NAVY,True)
    text(s,"Il runtime gestisce il ciclo di vita; i dati durevoli richiedono volumi.",8.75,5.32,2.94,.5,14,WHITE,True,align=PP_ALIGN.CENTER)
    source_label(s, "Figura originale: Microservices-Architectures_v3.pdf, p. 80; testo: appunti Docker/Kubernetes")
    footer(s, "architetture", number, "15 min")
    notes(s, "Distinguere con precisione immagine, container e runtime. Correggere l'ambiguità degli appunti sulla persistenza: le modifiche nel writable layer non sostituiscono uno storage durevole.", "DOCKER-KUBERNETES 20240219: sezione DOCKER, indici 2620-3460.", "Usare il flusso visuale come riferimento durante la spiegazione.")
    return s


def orchestrator_slide(number):
    s = base(False)
    text(s, "Perché serve un orchestratore", .82, .7, 11.4, .7, 29, WHITE, True)
    picture_fit(s,Path("assets/source-api-pdf/p047-1.jpg"),.78,1.55,3.65,2.1)
    picture_fit(s,Path("assets/source-api-pdf/p047-2.jpg"),4.75,1.55,3.65,2.1)
    picture_fit(s,Path("assets/source-api-pdf/p047-3.jpg"),8.72,1.55,3.65,2.1)
    text(s,"1. Trova istanze sane",1.05,3.85,3.15,.32,14,WHITE,True,align=PP_ALIGN.CENTER)
    text(s,"2. Aggiorna la mappa",5.02,3.85,3.15,.32,14,WHITE,True,align=PP_ALIGN.CENTER)
    text(s,"3. Esclude i guasti",8.99,3.85,3.15,.32,14,WHITE,True,align=PP_ALIGN.CENTER)
    rect(s,.95,4.65,11.45,1.13,NAVY_2,True)
    text(s,"Scheduling • self-healing • scaling • networking • rollout",1.25,4.92,10.85,.35,19,TEAL,True,align=PP_ALIGN.CENTER)
    text(s,"Kubernetes osserva lo stato reale e lo riconcilia con quello desiderato.",1.25,5.38,10.85,.28,14,RGBColor(207,216,229),False,align=PP_ALIGN.CENTER)
    source_label(s, "Sequenza originale: Microservices-Architectures_v3.pdf, p. 47; concetti: appunti Docker/Kubernetes", True)
    footer(s, "architetture", number, "15 min", True)
    notes(s, "Presentare Kubernetes come sistema di riconciliazione, non come semplice esecutore di comandi.", "DOCKER-KUBERNETES 20240219: indici 3851-4445.", "Riprendere le metafore degli appunti: timoniere per il self-healing e parcheggiatore per lo scheduling.")
    return s


def kubernetes_overview(number):
    s = base(True)
    text(s, "Kubernetes: dal cluster agli oggetti applicativi", .8, .7, 11.7, .65, 27, NAVY, True)
    picture_fit(s,Path("assets/source-api/image12.png"),.75,1.45,8.65,5.15)
    text(s,"DUE PIANI",9.67,1.7,2.4,.25,10,CORAL,True)
    text(s,"Control plane",9.67,2.12,2.55,.35,18,NAVY,True)
    text(s,"API server, scheduler, controller, etcd",9.67,2.58,2.55,.72,14,MUTED)
    rect(s,9.67,3.55,2.55,.07,TEAL)
    text(s,"Worker plane",9.67,3.92,2.55,.35,18,NAVY,True)
    text(s,"kubelet, runtime, rete e Pod applicativi",9.67,4.38,2.55,.72,14,MUTED)
    rect(s,9.67,5.38,2.55,.75,NAVY,True)
    text(s,"Manifest → stato desiderato",9.87,5.56,2.15,.35,13,WHITE,True,align=PP_ALIGN.CENTER)
    source_label(s, "Figura originale: appunti “ARCHITETTURE MICROSERVIZI…”, architettura Kubernetes")
    footer(s, "architetture", number, "20 min")
    notes(s, "Dare una mappa mentale a due livelli: componenti del cluster e oggetti dichiarati dall'applicazione.", "DOCKER-KUBERNETES 20240219: architettura interna 4502-5344; architettura logica 5347-6638.", "Richiamare namespace/RBAC, NetworkPolicy e registry come temi di governance, senza entrare nei comandi kubectl.")
    return s


def vm_container_visual(number):
    s=base(True)
    text(s,"VM e container: due livelli di isolamento",.8,.7,11.7,.65,27,NAVY,True)
    # Native layer stacks make the comparison readable; source photo anchors the container metaphor.
    for x,title_,layers,color in [(.82,"MACCHINA VIRTUALE",["Applicazione","Guest OS","Hypervisor","Hardware"],TEAL),(5.02,"CONTAINER",["Applicazione + dipendenze","Container runtime","Host OS / kernel","Hardware"],CORAL)]:
        text(s,title_,x,1.56,3.7,.28,10,color,True,align=PP_ALIGN.CENTER)
        for i,lab in enumerate(layers):
            y=2.03+i*.78; rect(s,x,y,3.7,.59,WHITE if i<2 else PALE,True,color if i==0 else PALE)
            text(s,lab,x+.18,y+.12,3.34,.28,14,NAVY,True,align=PP_ALIGN.CENTER)
    picture_fit(s,Path("assets/source-platform/p082-2.jpg"),9.08,1.54,3.28,3.72)
    rect(s,9.08,5.43,3.28,.78,NAVY,True)
    text(s,"Spesso i container girano dentro VM: i due modelli si combinano.",9.33,5.57,2.78,.48,13,WHITE,True,align=PP_ALIGN.CENTER)
    source_label(s,"Figura originale: Microservices-Architectures_v3.pdf, p. 82; confronto dagli appunti Docker/Kubernetes")
    footer(s,"architetture",number,"12 min")
    notes(s,"Mostrare dove avviene l'isolamento: hardware per la VM, processi e risorse sul kernel host per il container.","Microservices-Architectures_v3.pdf, pp. 80 e 82; Google Doc DOCKER-KUBERNETES, sezione DOCKER.","Sottolineare che VM e container non sono sostituti assoluti e spesso vengono combinati.")
    return s


def rest_api_visual(number):
    s=base(True)
    text(s,"REST: risorse, metodi e risposte HTTP",.8,.7,11.7,.65,27,NAVY,True)
    picture_fit(s,Path("assets/source-api-pdf/p045-1.jpg"),.88,1.65,2.9,2.25)
    text(s,"/cittadini/472",4.18,1.74,4.9,.52,24,NAVY,True)
    text(s,"una risorsa identificata da URI",4.2,2.36,4.4,.35,14,MUTED)
    methods=[("GET","legge",TEAL),("POST","crea",SKY),("PUT/PATCH","aggiorna",CORAL),("DELETE","elimina",NAVY_2)]
    for i,(m,v,c) in enumerate(methods):
        x=4.18+(i%2)*2.45; y=3.02+(i//2)*1.05
        rect(s,x,y,2.18,.78,WHITE,True,c); text(s,m,x+.14,y+.12,.85,.25,11,c,True); text(s,v,x+1.0,y+.12,1.02,.28,14,NAVY,True)
    rect(s,9.38,1.65,2.9,3.83,NAVY,True)
    text(s,"RISPOSTA",9.72,1.98,2.2,.28,10,TEAL,True)
    text(s,"200",9.72,2.5,1.0,.48,24,WHITE,True); text(s,"OK",10.62,2.62,1.2,.28,13,RGBColor(207,216,229))
    text(s,"404",9.72,3.28,1.0,.48,24,WHITE,True); text(s,"non trovata",10.62,3.4,1.35,.28,13,RGBColor(207,216,229))
    text(s,"429",9.72,4.06,1.0,.48,24,WHITE,True); text(s,"troppi accessi",10.62,4.18,1.4,.35,13,RGBColor(207,216,229))
    text(s,"503",9.72,4.84,1.0,.48,24,WHITE,True); text(s,"non disponibile",10.62,4.96,1.45,.35,13,RGBColor(207,216,229))
    text(s,"REST trasferisce rappresentazioni dello stato tramite il protocollo HTTP.",1.42,5.82,10.45,.42,17,NAVY,True,align=PP_ALIGN.CENTER)
    source_label(s,"Fonte: appunti “ARCHITETTURE MICROSERVIZI…”, sezione API; figura dal PDF, p. 45")
    footer(s,"ecosistemi",number,"15 min")
    notes(s,"Legare il metodo HTTP all'intento sulla risorsa e mostrare che anche lo status code appartiene al contratto.","ARCHITETTURE MICROSERVIZI CON DOCKER; SPRING BOOT; KAFKA, sezione API, paragrafi 266-295; Microservices-Architectures_v3.pdf p.45.","Evitare l'equazione semplicistica REST=CRUD: è una prima mappa per il pubblico non operativo.")
    return s


def java_execution_slide(number):
    s=base(False)
    text(s,"Come funziona Java: dal sorgente al codice macchina",.82,.7,11.4,.7,28,WHITE,True)
    stages=[("SORGENTE",".java",CORAL),("COMPILATORE","javac",TEAL),("BYTECODE",".class",SKY),("JVM","load · verify · execute",TEAL),("MACCHINA","codice nativo",CORAL)]
    for i,(title,sub,color) in enumerate(stages):
        x=.55+i*2.55
        rect(s,x,1.65,2.05,1.08,NAVY_2,True)
        text(s,title,x+.12,1.88,1.81,.24,12,color,True,align=PP_ALIGN.CENTER)
        text(s,sub,x+.12,2.23,1.81,.22,10,WHITE,False,align=PP_ALIGN.CENTER)
        if i<4:text(s,"→",x+2.08,2.02,.42,.3,17,color,True,align=PP_ALIGN.CENTER)
    rect(s,.72,3.2,11.86,2.77,WHITE,True,WHITE)
    picture_fit(s,Path("assets/source-java/page-007.png"),.9,3.38,11.5,2.42)
    text(s,"La portabilità nasce dal bytecode; le prestazioni dal runtime che lo interpreta e lo compila JIT.",1.05,6.15,11.2,.34,14,TEAL,True,align=PP_ALIGN.CENTER)
    source_label(s,"Java Performance Course v1, p. 7",True)
    footer(s,"Ecosistemi · Java",number,"15 min",True)
    notes(s,"Separare chiaramente linguaggio, compilatore, formato .class e runtime. La JVM non esegue direttamente il sorgente Java.","java-performance-course_v1.pdf, pp. 7-9.","javac produce bytecode portabile. La JVM carica e verifica le classi, interpreta inizialmente le istruzioni e può tradurre i metodi più usati in codice macchina tramite JIT.")
    return s


def bytecode_slide(number):
    s=base(True)
    text(s,"Bytecode: il contratto portabile della piattaforma Java",.8,.7,11.7,.65,27,NAVY,True)
    rect(s,.7,1.42,7.58,5.08,WHITE,True,PALE)
    picture_fit(s,Path("assets/source-java/page-023.png"),.9,1.62,7.2,4.67)
    text(s,"TRE IDEE",8.75,1.62,2.7,.25,10,CORAL,True)
    add_rich_lines(s,["È un linguaggio intermedio, non codice macchina", "Ogni opcode occupa un byte", "javap permette di disassemblare i file .class", "Il JIT ottimizza a runtime i metodi più usati"],8.65,2.08,3.55,3.45,14)
    rect(s,8.72,5.65,3.3,.62,NAVY,True)
    text(s,"Write once → JVM compatibile → run",8.96,5.82,2.82,.24,11,WHITE,True,align=PP_ALIGN.CENTER)
    source_label(s,"Java Performance Course v1, pp. 8, 19 e 23")
    footer(s,"Ecosistemi · Java",number,"15 min")
    notes(s,"Usare il frammento javap per rendere concreto il passaggio dal costrutto Java alle istruzioni della macchina a stack.","java-performance-course_v1.pdf, pp. 8, 19, 23-25.","Il bytecode conserva una rappresentazione semplice e verificabile. Costrutti di alto livello come i cicli diventano salti; il runtime usa operand stack per i calcoli.")
    return s


def jvm_runtime_slide(number):
    s=base(False)
    text(s,"Dentro la JVM: caricare, verificare, eseguire, ottimizzare",.82,.7,11.4,.7,28,WHITE,True)
    phases=[("1","CLASS LOADING","Trova classi e dipendenze"),("2","LINKING","Verifica · prepara · risolve"),("3","INTERPRETER","Esegue subito il bytecode"),("4","JIT","Compila i metodi caldi")]
    for i,(n,title,body) in enumerate(phases):
        x=.65+i*3.1
        rect(s,x,1.55,2.78,1.35,NAVY_2,True)
        text(s,n,x+.18,1.76,.35,.34,18,CORAL,True)
        text(s,title,x+.62,1.75,1.95,.25,12,TEAL,True)
        text(s,body,x+.2,2.22,2.38,.36,12,WHITE,False,align=PP_ALIGN.CENTER)
        if i<3:text(s,"→",x+2.8,2.03,.28,.3,16,CORAL,True,align=PP_ALIGN.CENTER)
    rect(s,.74,3.32,5.72,2.72,WHITE,True,WHITE); picture_fit(s,Path("assets/source-java/page-008.png"),.9,3.5,5.4,2.35)
    rect(s,6.83,3.32,5.75,2.72,WHITE,True,WHITE); picture_fit(s,Path("assets/source-java/page-025.png"),7.0,3.5,5.4,2.35)
    text(s,"BYTECODE VERIFICATO",1.05,6.15,5.1,.22,10,TEAL,True,align=PP_ALIGN.CENTER)
    text(s,"STACK PER THREAD · OPERAND STACK PER METODO",7.02,6.15,5.35,.22,10,CORAL,True,align=PP_ALIGN.CENTER)
    source_label(s,"Java Performance Course v1, pp. 8-13 e 25",True)
    footer(s,"Ecosistemi · Java",number,"18 min",True)
    notes(s,"Mostrare che JVM significa più di macchina virtuale: include caricamento dinamico, verifica, memoria, interprete e compilatore JIT.","java-performance-course_v1.pdf, pp. 8-13, 25 e 88.","La verifica anticipa controlli di sicurezza e consistenza. Ogni thread possiede un call stack; ogni metodo usa un operand stack. I metodi partono interpretati e diventano candidati alla compilazione JIT.")
    return s


def java_gc_slide(number):
    s=base(True)
    text(s,"Garbage Collector: recuperare memoria senza gestione manuale",.8,.7,11.7,.65,27,NAVY,True)
    rect(s,.7,1.42,5.7,4.92,WHITE,True,PALE); picture_fit(s,Path("assets/source-java/page-075.png"),.88,1.62,5.34,4.5)
    rect(s,6.68,1.42,5.92,4.92,WHITE,True,PALE); picture_fit(s,Path("assets/source-java/page-077.png"),6.86,1.62,5.56,4.5)
    text(s,"STACK: variabili locali e riferimenti",.95,6.1,5.18,.24,10,TEAL,True,align=PP_ALIGN.CENTER)
    text(s,"HEAP: Eden → Survivor → Old generation",6.94,6.1,5.22,.24,10,CORAL,True,align=PP_ALIGN.CENTER)
    source_label(s,"Java Performance Course v1, pp. 74-78")
    footer(s,"Ecosistemi · Java",number,"18 min")
    notes(s,"Partire dalla distinzione stack/heap, poi spiegare raggiungibilità e ipotesi generazionale.","java-performance-course_v1.pdf, pp. 74-78.","Il GC parte dalle radici vive, marca gli oggetti raggiungibili e recupera gli altri. La maggioranza degli oggetti muore giovane: Eden e Survivor permettono collezioni frequenti e brevi; gli oggetti longevi vengono promossi.")
    return s


def g1_slide(number):
    s=base(False)
    text(s,"G1: regioni, generazioni e pause controllabili",.82,.7,11.4,.7,28,WHITE,True)
    rect(s,.72,1.42,7.45,5.0,WHITE,True,WHITE); picture_fit(s,Path("assets/source-java/page-083.png"),.9,1.62,7.08,4.58)
    text(s,"COME LEGGERLO",8.65,1.65,2.9,.25,10,CORAL,True)
    add_rich_lines(s,["Heap diviso in regioni di pari dimensione", "Generazioni non necessariamente contigue", "Young collection in Stop-the-World", "Old collection per quanto possibile concorrente", "Obiettivo: maggiore prevedibilità delle pause"],8.56,2.08,3.65,3.72,14,WHITE)
    source_label(s,"Java Performance Course v1, pp. 80-85",True)
    footer(s,"Ecosistemi · Java",number,"15 min",True)
    notes(s,"Collegare il GC alle qualità operative: throughput, latenza e prevedibilità delle pause sono trade-off.","java-performance-course_v1.pdf, pp. 80-85.","G1 è il collector predefinito da Java 9. Regionalizza lo heap e può scegliere gruppi di regioni da raccogliere, evitando che ogni ciclo sulla old generation debba essere necessariamente all-or-nothing.")
    return s


def visualvm_slide(number):
    s=base(True)
    text(s,"VisualVM: osservare la JVM mentre l'applicazione vive",.8,.7,11.7,.65,27,NAVY,True)
    panels=[("MEMORIA E GC","page-079.png"),("THREAD E STATO","page-099.png"),("LOCK E PROFILER","page-112.png")]
    for i,(cap,img) in enumerate(panels):
        x=.55+i*4.18
        rect(s,x,1.48,3.86,4.82,WHITE,True,PALE)
        picture_fit(s,Path("assets/source-java")/img,x+.14,1.66,3.58,4.15)
        text(s,cap,x+.18,5.93,3.5,.22,10,[TEAL,CORAL,SKY][i],True,align=PP_ALIGN.CENTER)
    text(s,"Correlare timeline, heap, GC, thread e metodi: il profiler formula ipotesi, non sostituisce le misure.",.9,6.47,11.5,.3,13,NAVY,True,align=PP_ALIGN.CENTER)
    source_label(s,"Java Performance Course v1, pp. 79, 99 e 111-113")
    footer(s,"Ecosistemi · Java",number,"20 min")
    notes(s,"Usare le tre schermate per mostrare una diagnosi progressiva: prima il comportamento globale, poi i thread e infine lock o metodi costosi.","java-performance-course_v1.pdf, pp. 79, 99, 111-113.","VisualVM consente monitoraggio di heap e GC, thread dump e timeline, sampling/profiling e analisi dei lock. Chiedere sempre quale sintomo e quale intervallo temporale si sta osservando.")
    return s


def python_overview_slide(number):
    s=base(False)
    text(s,"Python: dal dato al modello, fino all'AI generativa",.82,.7,11.4,.7,28,WHITE,True)
    stages=[("DATI","Pandas",TEAL),("ESPLORAZIONE","Seaborn",SKY),("MODELLO","scikit-learn",CORAL),("GEN AI","modelli + API",TEAL)]
    for i,(title,sub,color) in enumerate(stages):
        x=.72+i*3.05
        rect(s,x,1.58,2.68,1.15,NAVY_2,True)
        text(s,title,x+.15,1.83,2.38,.25,14,color,True,align=PP_ALIGN.CENTER)
        text(s,sub,x+.15,2.22,2.38,.22,11,WHITE,False,align=PP_ALIGN.CENTER)
        if i<3:text(s,"→",x+2.7,2.02,.32,.3,16,color,True,align=PP_ALIGN.CENTER)
    rect(s,.72,3.22,11.86,2.55,WHITE,True,WHITE)
    text(s,"Python è il collante",1.05,3.58,3.25,.38,22,NAVY,True)
    add_rich_lines(s,["notebook per esplorare", "librerie per manipolare dati", "API semplici per addestrare e usare modelli", "ecosistema per orchestrare servizi AI"],4.45,3.55,7.3,1.75,15,NAVY)
    link_button(s,"APRIRE IL NOTEBOOK INTRODUTTIVO","https://colab.research.google.com/github/thimotyb/real-world-machine-learning/blob/python3/learning-python3.ipynb",4.7,5.08,4.95,True)
    footer(s,"Ecosistemi · Python",number,"12 min",True)
    notes(s,"Presentare Python come ecosistema trasversale, non soltanto come sintassi: accompagna l'intero ciclo dal dato all'applicazione AI.","Google Doc Python Basic; Practical Machine Learning, agenda.","Il pulsante apre direttamente il notebook Colab introduttivo indicato negli appunti.")
    return s


def pandas_dataframe_slide(number):
    s=base(True)
    text(s,"Pandas DataFrame: una tabella con indici, tipi e operazioni",.8,.7,11.7,.65,27,NAVY,True)
    code="""import pandas as pd\n\ndf = pd.DataFrame({\n    \"team\": [\"A\", \"A\", \"B\"],\n    \"score\": [72, 91, 84]\n})\n\nhigh = df.loc[df[\"score\"] >= 80]\nsummary = df.groupby(\"team\")[\"score\"].mean()"""
    rect(s,.72,1.5,5.5,4.9,NAVY_2,True)
    text(s,code,1.02,1.83,4.92,3.85,15,WHITE,False,font="Aptos Mono")
    text(s,"DataFrame = colonne (Series) allineate sullo stesso indice",1.0,5.8,4.95,.34,12,TEAL,True,align=PP_ALIGN.CENTER)
    add_rich_lines(s,["df['colonna'] seleziona una Series", ".loc usa etichette e condizioni", ".iloc usa posizioni", "groupby aggrega per gruppi", "read_csv / read_excel / read_sql importano dati"],6.7,1.72,5.3,3.7,16)
    link_button(s,"COLAB · INTRODUZIONE AI DATAFRAME","https://colab.research.google.com/github/thimotyb/real-world-machine-learning/blob/python3/pandas-dataframe.ipynb",6.82,5.35,4.75)
    link_button(s,"COLAB · IMPORTARE I DATI","https://colab.research.google.com/github/thimotyb/real-world-machine-learning/blob/python3/Importing_data_with_pandas.ipynb",6.82,5.92,4.75)
    footer(s,"Ecosistemi · Python",number,"18 min")
    notes(s,"Costruire il modello mentale: una Series ha indice e dtype; un DataFrame è una collezione di Series allineate. Collegare selezione, filtro e raggruppamento all'equivalente SQL.","Google Doc Python Basic, sezione Pandas e Dataframes.","I due pulsanti aprono i notebook Colab su DataFrame e importazione dati presenti negli appunti.")
    return s


def pandas_workflow_slide(number):
    s=base(False)
    text(s,"Il flusso Pandas: caricare, capire, trasformare, riassumere",.82,.7,11.4,.7,28,WHITE,True)
    stages=[("1","LOAD","read_csv / read_sql"),("2","INSPECT","head · info · describe"),("3","FILTER","loc · condizioni"),("4","TRANSFORM","assign · merge"),("5","GROUP","groupby · agg")]
    for i,(n,title,body) in enumerate(stages):
        x=.46+i*2.56
        rect(s,x,1.58,2.2,1.28,NAVY_2,True)
        text(s,n,x+.12,1.78,.35,.3,16,CORAL,True)
        text(s,title,x+.52,1.8,1.5,.22,12,TEAL,True)
        text(s,body,x+.12,2.25,1.96,.25,10,WHITE,False,align=PP_ALIGN.CENTER)
        if i<4:text(s,"→",x+2.2,2.05,.32,.3,16,CORAL,True,align=PP_ALIGN.CENTER)
    rect(s,.72,3.35,11.86,2.35,WHITE,True,WHITE)
    text(s,"Domanda",1.05,3.7,1.5,.3,12,CORAL,True)
    text(s,"Qual è la distribuzione del punteggio per team?",1.05,4.12,4.2,.42,18,NAVY,True)
    text(s,"Risposta riproducibile",6.02,3.7,2.5,.3,12,TEAL,True)
    text(s,"df.groupby('team').score.agg(['count','mean','std'])",6.02,4.15,5.55,.5,16,NAVY_2,False,font="Aptos Mono")
    link_button(s,"COLAB · FILTRARE E ORDINARE","https://colab.research.google.com/github/thimotyb/pandas_exercises/blob/master/02_Filtering_%26_Sorting/Chipotle/Exercises_with_solutions.ipynb",2.0,5.1,4.25,True)
    link_button(s,"COLAB · GROUPING","https://colab.research.google.com/github/thimotyb/pandas_exercises/blob/master/03_Grouping/Alcohol_Consumption/Exercise_with_solutions.ipynb",6.95,5.1,4.25,True)
    footer(s,"Ecosistemi · Python",number,"18 min",True)
    notes(s,"Leggere il flusso come una pipeline trasformativa. Ogni passaggio produce un DataFrame o una Series ispezionabile e ripetibile.","Google Doc Python Basic, Pandas/Dataframes e notebook collegati.","I pulsanti conducono direttamente agli esercizi Colab di filtering/sorting e grouping.")
    return s


def seaborn_gallery_slide(number):
    s=base(True)
    text(s,"Visualizzare con Seaborn: scegliere il grafico per la domanda",.8,.7,11.7,.65,27,NAVY,True)
    items=[("RELAZIONI","pairplot", "seaborn-pairplot.png"),("DISTRIBUZIONI","violinplot", "seaborn-violinplot.png"),("MATRICI","heatmap", "seaborn-heatmap.png")]
    for i,(title,fn,img) in enumerate(items):
        x=.48+i*4.22
        rect(s,x,1.48,3.95,4.95,WHITE,True,PALE)
        picture_fit(s,Path("assets/source-python")/img,x+.15,1.68,3.65,3.75)
        text(s,title,x+.18,5.55,3.58,.2,10,[TEAL,CORAL,SKY][i],True,align=PP_ALIGN.CENTER)
        text(s,f"sns.{fn}(data=df, …)",x+.18,5.9,3.58,.26,12,NAVY_2,False,font="Aptos Mono",align=PP_ALIGN.CENTER)
    source_label(s,"Seaborn 0.13.2 official example gallery")
    footer(s,"Ecosistemi · Python",number,"18 min")
    notes(s,"Associare la forma grafica alla domanda: relazioni tra variabili, distribuzioni per gruppi, intensità in una matrice.","Seaborn official gallery: pairplot, grouped violinplots, annotated heatmaps.","Gallery: https://seaborn.pydata.org/examples/index.html. Notebook visualizzazione: https://colab.research.google.com/github/thimotyb/pandas_exercises/blob/master/07_Visualization/Chipotle/Exercise_with_Solutions.ipynb")
    return s


def python_ml_slide(number):
    s=base(False)
    text(s,"Machine Learning in Python: dai feature al risultato",.82,.7,11.4,.7,28,WHITE,True)
    rect(s,.7,1.43,5.85,4.95,WHITE,True,WHITE); picture_fit(s,Path("assets/source-python/ml-slide-029.png"),.88,1.62,5.5,4.58)
    rect(s,6.83,1.43,5.78,4.95,WHITE,True,WHITE); picture_fit(s,Path("assets/source-python/ml-slide-080.png"),7.0,1.62,5.44,4.58)
    text(s,"PREPARAZIONE: categorie → feature numeriche",1.02,6.12,5.2,.22,10,TEAL,True,align=PP_ALIGN.CENTER)
    text(s,"MODELLO: regole apprese → albero interpretabile",7.05,6.12,5.32,.22,10,CORAL,True,align=PP_ALIGN.CENTER)
    source_label(s,"Practical Machine Learning, slide 29 e 80",True)
    footer(s,"Ecosistemi · Python",number,"20 min",True)
    notes(s,"Evidenziare che addestrare un modello richiede prima una rappresentazione numerica coerente. L'albero mostra il risultato come sequenza di decisioni sui feature.","Google Slides Practical Machine Learning, slide 29 e 80.","Il codice converte categorie in colonne binarie; l'albero suddivide ricorsivamente i dati per produrre una previsione.")
    return s


def python_tree_lab_slide(number):
    s=base(True)
    text(s,"Dal notebook all'albero: addestrare e leggere il modello",.8,.7,11.7,.65,27,NAVY,True)
    rect(s,.7,1.42,6.0,4.95,WHITE,True,PALE); picture_fit(s,Path("assets/source-python/ml-slide-166.png"),.9,1.62,5.62,4.58)
    rect(s,6.98,1.42,5.62,4.95,WHITE,True,PALE); picture_fit(s,Path("assets/source-python/ml-slide-158.png"),7.16,1.62,5.26,4.58)
    text(s,"PYTHON: fit del classificatore",1.05,6.12,5.3,.22,10,TEAL,True,align=PP_ALIGN.CENTER)
    text(s,"RISULTATO: split, soglie e foglie",7.25,6.12,4.95,.22,10,CORAL,True,align=PP_ALIGN.CENTER)
    source_label(s,"Practical Machine Learning, slide 158 e 166")
    footer(s,"Ecosistemi · Python",number,"20 min")
    notes(s,"Mostrare insieme codice e output: il valore didattico è collegare i parametri dell'algoritmo alla struttura dell'albero prodotto.","Google Slides Practical Machine Learning, slide 158 e 166.","Discutere feature, soglia di split, profondità, foglie, rischio di overfitting e necessità di valutazione su dati non usati nel training.")
    return s


def python_genai_slide(number):
    s=base(False)
    text(s,"AI generativa con Python: un'applicazione attorno al modello",.82,.7,11.4,.7,28,WHITE,True)
    code="""context = retrieve(question)\nprompt = build_prompt(context, question)\nanswer = model.generate(prompt)\nreturn validate(answer, context)"""
    rect(s,.72,1.5,5.25,3.2,NAVY_2,True)
    text(s,code,1.05,1.92,4.6,2.2,17,WHITE,False,font="Aptos Mono")
    stages=[("DOMANDA",CORAL),("RETRIEVAL",TEAL),("PROMPT",SKY),("MODELLO",TEAL),("VALIDAZIONE",CORAL)]
    for i,(label,color) in enumerate(stages):
        x=6.32+(i%2)*3.0; y=1.48+(i//2)*1.23
        rect(s,x,y,2.62,.7,NAVY_2,True)
        text(s,label,x+.15,y+.23,2.32,.22,11,color,True,align=PP_ALIGN.CENTER)
        if i<4:text(s,"↓" if i%2 else "→",x+2.66 if i%2==0 else x+1.05,y+.22 if i%2==0 else y+.76,.28,.3,15,color,True,align=PP_ALIGN.CENTER)
    rect(s,.72,5.15,11.86,.94,WHITE,True,WHITE)
    text(s,"Python orchestra librerie, dati, chiamate API e controlli. Il modello è un componente, non l'intera soluzione.",1.03,5.46,11.2,.34,15,NAVY,True,align=PP_ALIGN.CENTER)
    link_button(s,"COLAB · TECNICHE PANDAS AVANZATE","https://colab.research.google.com/github/thimotyb/real-world-machine-learning/blob/python3/pandas_advanced_techniques.ipynb",4.25,6.3,4.85,True)
    footer(s,"Ecosistemi · Python",number,"15 min",True)
    notes(s,"Usare l'AI generativa come estensione del flusso dati: preparazione del contesto, invocazione del modello e validazione dell'output.","Estensione didattica coerente con Python Basic e con il workflow ML della presentazione Practical Machine Learning.","Distinguere training del modello, spesso esterno, dall'integrazione applicativa in Python. Introdurre retrieval, prompt, modello e guardrail senza attribuire affidabilità automatica alla risposta generata.")
    return s


def javascript_browser_slide(number):
    s=base(False)
    text(s,"JavaScript nel browser: comportamento sopra HTML e CSS",.82,.7,11.4,.7,28,WHITE,True)
    layers=[("HTML","struttura",CORAL),("CSS","presentazione",SKY),("JAVASCRIPT","comportamento",TEAL)]
    for i,(name,role,color) in enumerate(layers):
        x=.72+i*3.0
        rect(s,x,1.55,2.55,1.02,NAVY_2,True)
        text(s,name,x+.16,1.8,2.23,.25,14,color,True,align=PP_ALIGN.CENTER)
        text(s,role,x+.16,2.18,2.23,.2,11,WHITE,False,align=PP_ALIGN.CENTER)
        if i<2:text(s,"+",x+2.58,1.93,.34,.3,17,color,True,align=PP_ALIGN.CENTER)
    rect(s,9.77,1.55,2.75,1.02,WHITE,True,WHITE)
    text(s,"PAGINA INTERATTIVA",9.95,1.9,2.39,.3,12,NAVY,True,align=PP_ALIGN.CENTER)
    code="""const button = document.querySelector('button');\n\nbutton.addEventListener('click', () => {\n  document.querySelector('h1').textContent = 'Ciao!';\n});"""
    rect(s,.72,3.05,7.18,2.9,WHITE,True,WHITE); text(s,code,1.05,3.47,6.52,1.95,17,NAVY_2,False,font="Aptos Mono")
    add_rich_lines(s,["il browser è l'ambiente di esecuzione", "DOM e Web API collegano codice e pagina", "eventi attivano funzioni", "JavaScript moderno usa compilazione JIT"],8.35,3.12,3.75,2.25,14,WHITE)
    link_button(s,"PROVA NEL PLAYGROUND MDN","https://developer.mozilla.org/en-US/play",8.48,5.48,3.45,True)
    source_label(s,"MDN: What is JavaScript? e JavaScript Guide",True)
    footer(s,"Ecosistemi · JavaScript",number,"15 min",True)
    notes(s,"Spiegare il ruolo di JavaScript nel browser distinguendolo da HTML e CSS. Collegare eventi, DOM e aggiornamento dell'interfaccia.","MDN What is JavaScript?: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/What_is_JavaScript","Il browser riceve il sorgente e lo esegue nel contesto della scheda; i motori moderni applicano compilazione JIT. Il pulsante apre il Playground MDN.")
    return s


def javascript_console_slide(number):
    s=base(True)
    text(s,"La Console JavaScript: provare, osservare, diagnosticare",.8,.7,11.7,.65,27,NAVY,True)
    rect(s,.7,1.42,8.02,5.0,WHITE,True,PALE)
    picture_fit(s,Path("assets/source-javascript/mdn-browser-console.png"),.9,1.63,7.62,4.58)
    text(s,"PROVA ORA",9.05,1.65,2.65,.24,10,CORAL,True)
    code="""> const nums = [2, 4, 6]\nundefined\n> nums.map(n => n * 2)\n[4, 8, 12]\n> console.table(nums)"""
    rect(s,8.95,2.08,3.18,2.42,NAVY_2,True); text(s,code,9.2,2.38,2.7,1.82,14,WHITE,False,font="Aptos Mono")
    text(s,"F12 oppure Ctrl+Shift+I",9.1,4.88,2.9,.28,13,TEAL,True,align=PP_ALIGN.CENTER)
    link_button(s,"GUIDA MDN ALLA CONSOLE","https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Tools_and_setup/What_are_browser_developer_tools#the_javascript_console",9.0,5.48,3.08)
    source_label(s,"Screenshot originale MDN: browser Developer Tools, Console")
    footer(s,"Ecosistemi · JavaScript",number,"15 min")
    notes(s,"Far aprire la Console e provare una dichiarazione, map e console.table. Evidenziare che la console esegue codice nel contesto della pagina corrente.","MDN browser developer tools, sezione JavaScript console.","La console mostra valori restituiti ed errori; console.log, console.error e console.table aiutano a osservare il programma. Le modifiche fatte qui non persistono nel sorgente.")
    return s


def caniuse_slide(number):
    s=base(False)
    text(s,"Can I Use: decidere se una funzionalità Web è utilizzabile",.82,.7,11.4,.7,28,WHITE,True)
    rect(s,.7,1.42,8.35,5.0,WHITE,True,WHITE)
    picture_fit(s,Path("assets/source-javascript/caniuse-css-grid.png"),.88,1.62,7.98,4.58)
    text(s,"COME SI LEGGE",9.42,1.63,2.45,.24,10,CORAL,True)
    items=[("VERDE","supportata",TEAL),("GIALLO","parziale",RGBColor(205,160,45)),("ROSSO","non supportata",CORAL),("GRIGIO","dato ignoto",MUTED)]
    for i,(name,meaning,color) in enumerate(items):
        y=2.08+i*.72; rect(s,9.38,y,.34,.34,color,True); text(s,name,9.9,y-.01,.82,.22,10,color,True); text(s,meaning,10.78,y-.01,1.22,.24,11,WHITE)
    text(s,"Controlla versioni, note, supporto parziale e quota d'uso del pubblico reale.",9.4,5.03,2.63,.62,13,WHITE,True,align=PP_ALIGN.CENTER)
    link_button(s,"APRI CANIUSE.COM","https://caniuse.com/",9.42,5.83,2.58,True)
    source_label(s,"Screenshot aggiornato: caniuse.com/css-grid",True)
    footer(s,"Ecosistemi · JavaScript",number,"12 min",True)
    notes(s,"Usare CSS Grid come esempio per mostrare che compatibilità non è un sì/no globale: varia per browser, versione e dettaglio della specifica.","Can I Use: https://caniuse.com/","Verde indica supporto, rosso assenza, giallo supporto parziale e grigio stato ignoto. La percentuale globale va confrontata con analytics e browser support policy del progetto.")
    return s


def react_quickstart_slide(number):
    s=base(False)
    text(s,"React Quick Start: l'interfaccia come composizione",.82,.7,11.4,.7,28,WHITE,True)
    concepts=[("COMPONENTI","funzioni che restituiscono UI",CORAL),("JSX","markup dentro JavaScript",TEAL),("DATI","props dal padre",SKY),("STATO","memoria locale con useState",TEAL),("EVENTI","azioni che aggiornano lo stato",CORAL)]
    for i,(title,body,color) in enumerate(concepts):
        x=.48+i*2.56
        rect(s,x,1.55,2.23,1.45,NAVY_2,True)
        text(s,title,x+.14,1.8,1.95,.25,12,color,True,align=PP_ALIGN.CENTER)
        text(s,body,x+.17,2.23,1.89,.48,11,WHITE,False,align=PP_ALIGN.CENTER)
        if i<4:text(s,"→",x+2.25,2.12,.28,.3,15,color,True,align=PP_ALIGN.CENTER)
    code="""function ServiceCard({ title }) {\n  const [count, setCount] = useState(0);\n\n  return (\n    <button onClick={() => setCount(count + 1)}>\n      {title}: {count}\n    </button>\n  );\n}"""
    rect(s,.72,3.43,7.02,2.82,WHITE,True,WHITE); text(s,code,1.02,3.72,6.42,2.24,15,NAVY_2,False,font="Aptos Mono")
    text(s,"RENDER",8.25,3.72,3.3,.26,11,CORAL,True,align=PP_ALIGN.CENTER)
    rect(s,8.38,4.16,3.06,.74,TEAL,True); text(s,"Servizio: 0",8.62,4.39,2.58,.24,15,WHITE,True,align=PP_ALIGN.CENTER)
    text(s,"click → setState → nuovo render",8.2,5.3,3.42,.3,13,SKY,True,align=PP_ALIGN.CENTER)
    source_label(s,"React documentation, Quick Start",True)
    footer(s,"Ecosistemi · React",number,"18 min",True)
    notes(s,"Usare un solo esempio per collegare i concetti quotidiani del Quick Start: componente, JSX, props, stato ed evento.","React Quick Start: https://react.dev/learn","React presenta nel Quick Start creazione e nesting dei componenti, markup e stili, visualizzazione dei dati, liste e condizioni, eventi, aggiornamento dello schermo e condivisione dei dati.")
    return s


def react_dataflow_slide(number):
    s=base(True)
    text(s,"Props, state e render: il flusso dei dati in React",.8,.7,11.7,.65,27,NAVY,True)
    rect(s,.72,1.55,3.05,1.0,WHITE,True,PALE); text(s,"PARENT",1.02,1.78,2.45,.23,12,TEAL,True,align=PP_ALIGN.CENTER); text(s,"possiede i dati condivisi",1.02,2.13,2.45,.2,11,NAVY,False,align=PP_ALIGN.CENTER)
    text(s,"props ↓",1.92,2.73,.72,.3,14,CORAL,True,align=PP_ALIGN.CENTER)
    rect(s,.72,3.16,3.05,1.0,WHITE,True,PALE); text(s,"CHILD",1.02,3.39,2.45,.23,12,TEAL,True,align=PP_ALIGN.CENTER); text(s,"renderizza e genera eventi",1.02,3.74,2.45,.2,11,NAVY,False,align=PP_ALIGN.CENTER)
    text(s,"evento ↑",1.87,4.34,.82,.3,14,CORAL,True,align=PP_ALIGN.CENTER)
    rect(s,4.25,1.48,8.28,4.92,NAVY_2,True)
    code="""function App() {\n  const [filter, setFilter] = useState('Tutti');\n  const visible = services.filter(s =>\n    filter === 'Tutti' || s.area === filter\n  );\n\n  return <ServiceList items={visible}\n    onSelect={setFilter} />;\n}"""
    text(s,code,4.65,1.93,7.48,3.75,17,WHITE,False,font="Aptos Mono")
    text(s,"Lo stato non modifica il DOM direttamente: descrive la UI desiderata.",4.68,5.72,7.38,.34,13,SKY,True,align=PP_ALIGN.CENTER)
    source_label(s,"React Quick Start: responding to events, updating the screen, sharing data")
    footer(s,"Ecosistemi · React",number,"15 min")
    notes(s,"Spiegare il flusso unidirezionale: i dati scendono attraverso le props; gli eventi risalgono tramite callback; lo stato guida un nuovo render.","React Quick Start: https://react.dev/learn","Evitare il modello mentale del DOM manipolato a mano. React ricalcola la descrizione dell'interfaccia quando cambia lo stato.")
    return s


def react_native_overview_slide(number):
    s=base(False)
    text(s,"Inciso · React Native: React incontra le UI mobili native",.82,.7,11.4,.7,28,WHITE,True)
    stages=[("COMPONENTE REACT","JSX + props + state",CORAL),("REACT NATIVE","renderer e runtime nativo",TEAL),("UI NATIVA","Android · iOS",SKY)]
    for i,(title,body,color) in enumerate(stages):
        x=.72+i*4.15
        rect(s,x,1.5,3.55,1.18,NAVY_2,True)
        text(s,title,x+.2,1.78,3.15,.25,12,color,True,align=PP_ALIGN.CENTER)
        text(s,body,x+.2,2.17,3.15,.25,13,WHITE,False,align=PP_ALIGN.CENTER)
        if i<2:text(s,"→",x+3.6,1.89,.48,.34,18,CORAL,True,align=PP_ALIGN.CENTER)
    mappings=[("<View>","UIView / ViewGroup","contenitore"),("<Text>","UITextView / TextView","testo"),("<Image>","UIImageView / ImageView","immagine")]
    for i,(component,native,role) in enumerate(mappings):
        x=.72+i*4.15
        rect(s,x,3.15,3.55,2.12,WHITE,True,WHITE)
        text(s,component,x+.22,3.48,3.1,.32,19,NAVY_2,True,font="Aptos Mono",align=PP_ALIGN.CENTER)
        text(s,"↓",x+1.48,3.95,.6,.3,17,CORAL,True,align=PP_ALIGN.CENTER)
        text(s,native,x+.2,4.35,3.15,.34,13,TEAL,True,align=PP_ALIGN.CENTER)
        text(s,role,x+.2,4.84,3.15,.24,11,MUTED,False,align=PP_ALIGN.CENTER)
    text(s,"Il modello mentale resta React; l'output non è HTML: sono building block dell'interfaccia della piattaforma.",1.05,5.72,11.2,.5,14,WHITE,True,align=PP_ALIGN.CENTER)
    link_button(s,"CORE COMPONENTS","https://reactnative.dev/docs/intro-react-native-components",4.77,6.32,3.8,True)
    source_label(s,"React Native official documentation: Core Components",True)
    footer(s,"Ecosistemi · React Native",number,"12 min",True)
    notes(s,"Presentare React Native come estensione del modello a componenti di React verso applicazioni Android e iOS. Sottolineare che non genera una pagina Web: i componenti fondamentali sono tradotti nei corrispondenti controlli nativi.","React Native Introduction: https://reactnative.dev/; Core Components: https://reactnative.dev/docs/intro-react-native-components","React Native usa React e JavaScript per descrivere l'interfaccia, ma esegue il rendering con codice nativo. View, Text e Image corrispondono ai building block delle piattaforme mobili.")
    return s


def react_native_snack_slide(number):
    s=base(True)
    text(s,"Expo Snack: una app React Native modificabile nel browser",.8,.7,11.7,.65,27,NAVY,True)
    rect(s,.66,1.42,8.55,4.92,WHITE,True,PALE)
    picture_fit(s,Path("output/playwright/react-native-expo-snack.png"),.78,1.56,8.3,4.64)
    text(s,"PROVA IN 3 PASSI",9.48,1.62,2.55,.24,11,CORAL,True,align=PP_ALIGN.CENTER)
    steps=[("1","modifica App.js"),("2","scegli Android o iOS"),("3","osserva l'anteprima")]
    for i,(n,label) in enumerate(steps):
        y=2.12+i*.92
        rect(s,9.42,y,.48,.48,TEAL,True)
        text(s,n,9.53,y+.11,.26,.22,13,WHITE,True,align=PP_ALIGN.CENTER)
        text(s,label,10.08,y+.08,2.15,.35,13,NAVY,True)
    text(s,"Stesso progetto, feedback immediato su più piattaforme.",9.47,4.98,2.7,.62,12,NAVY,True,align=PP_ALIGN.CENTER)
    link_button(s,"APRI EXPO SNACK","https://snack.expo.dev/?description=Example+usage&hideQueryParams=true&name=Fetch+Example&platform=web",9.4,5.72,2.82)
    source_label(s,"Screenshot: Expo Snack, esempio ufficiale modificabile")
    footer(s,"Ecosistemi · React Native",number,"18 min")
    notes(s,"Aprire Snack dal pulsante e cambiare il testo dentro <Text>. Se disponibile, passare dalla preview Web ad Android o iOS; il QR permette anche la prova sul dispositivo con Expo Go.","React Native Getting Started: https://reactnative.dev/docs/getting-started; Expo Snack: https://snack.expo.dev/","La documentazione React Native incorpora Snack Player modificabili. Snack permette di sperimentare nel browser e offre target Web, Android e iOS senza predisporre subito una toolchain locale.")
    return s


def mui_components_slide(number):
    s=base(False)
    text(s,"Material UI: componenti pronti, tema coerente, API React",.82,.7,11.4,.7,28,WHITE,True)
    variants=[("Text",WHITE,NAVY_2),("Contained",TEAL,WHITE),("Outlined",NAVY_2,TEAL)]
    for i,(label,fill,col) in enumerate(variants):
        x=.85+i*2.18
        rect(s,x,1.63,1.82,.68,fill,True,TEAL)
        text(s,label,x+.12,1.85,1.58,.22,12,col,True,align=PP_ALIGN.CENTER)
    code="""import Button from '@mui/material/Button';\n\n<Button variant=\"contained\"\n        color=\"primary\"\n        onClick={submit}>\n  Invia richiesta\n</Button>"""
    rect(s,.72,2.72,6.45,3.42,WHITE,True,WHITE); text(s,code,1.05,3.08,5.78,2.65,16,NAVY_2,False,font="Aptos Mono")
    add_rich_lines(s,["componenti accessibili come base", "varianti e proprietà dichiarative", "tema centralizzato", "composizione con layout, form e feedback", "template React pronti"],7.62,1.65,4.55,3.72,15,WHITE)
    link_button(s,"ESEMPI MUI · BUTTON","https://mui.com/material-ui/react-button/",8.0,5.45,3.75,True)
    source_label(s,"Material UI documentation: overview and Button demos",True)
    footer(s,"Ecosistemi · React",number,"18 min",True)
    notes(s,"Mostrare che una component library riduce il lavoro ripetitivo, ma richiede una strategia di tema, accessibilità e composizione.","MUI overview: https://mui.com/material-ui/getting-started/; Button: https://mui.com/material-ui/react-button/","MUI offre componenti React che implementano Material Design. I Button hanno varianti text, contained e outlined; gli handler React restano normali proprietà onClick.")
    return s


def mui_mcp_slide(number):
    s=base(True)
    text(s,"MUI MCP: documentazione del componente dentro il flusso AI",.8,.7,11.7,.65,27,NAVY,True)
    stages=[("IDE / AGENTE",CORAL),("MUI MCP",TEAL),("DOCS UFFICIALI",SKY),("CODICE + PROPS",TEAL)]
    for i,(label,color) in enumerate(stages):
        x=.65+i*3.08
        rect(s,x,1.62,2.62,.82,WHITE,True,PALE); text(s,label,x+.18,1.9,2.26,.23,12,color,True,align=PP_ALIGN.CENTER)
        if i<3:text(s,"→",x+2.64,1.9,.34,.3,16,CORAL,True,align=PP_ALIGN.CENTER)
    rect(s,.72,2.95,11.86,2.25,NAVY_2,True)
    text(s,"npx -y @mui/mcp@latest",1.12,3.48,5.3,.5,23,WHITE,False,font="Aptos Mono",align=PP_ALIGN.CENTER)
    text(s,"preferred_theme · component_filter",6.78,3.5,4.9,.45,17,TEAL,True,font="Aptos Mono",align=PP_ALIGN.CENTER)
    rect(s,.72,5.55,11.86,.72,WHITE,True,PALE)
    text(s,"Obiettivo: generare esempi aderenti alle API correnti, riducendo props inventate o pattern obsoleti.",1.02,5.78,11.2,.28,13,NAVY,True,align=PP_ALIGN.CENTER)
    source_label(s,"MUI official MCP documentation")
    footer(s,"Ecosistemi · React",number,"12 min")
    notes(s,"Presentare MCP come accesso strutturato alla documentazione MUI per strumenti AI, non come parte necessaria del runtime React.","MUI MCP: https://mui.com/material-ui/getting-started/mcp/","La configurazione ufficiale usa npx con @mui/mcp@latest. Alcuni client supportano preferred_theme e component_filter per restringere il contesto.")
    return s


def design_italia_slide(number):
    s=base(False)
    text(s,"Design Italia: dal sistema di design al componente React",.82,.7,11.4,.7,28,WHITE,True)
    layers=[("LINEE GUIDA","principi e requisiti",CORAL),("UI KIT ITALIA","progettazione e prototipi",SKY),("BOOTSTRAP ITALIA","stili e componenti web",TEAL),("DESIGN REACT KIT","componenti React",CORAL)]
    for i,(title,body,color) in enumerate(layers):
        y=1.45+i*1.2
        rect(s,1.0,y,11.25,.82,NAVY_2,True)
        text(s,title,1.28,y+.22,3.05,.24,13,color,True)
        text(s,body,4.52,y+.22,6.92,.28,14,WHITE,False)
        if i<3:text(s,"↓",6.22,y+.83,.55,.28,16,color,True,align=PP_ALIGN.CENTER)
    text(s,"Il kit rende riusabili le decisioni del design system, ma non sostituisce ricerca, contenuti e test di accessibilità.",1.1,6.37,11.05,.38,13,TEAL,True,align=PP_ALIGN.CENTER)
    source_label(s,"Linee guida di design PA, §6.3; repository ufficiali Italia",True)
    footer(s,"Ecosistemi · React",number,"18 min",True)
    notes(s,"Presentare il React Kit come ultimo livello di una filiera: principi, asset di progettazione, implementazione CSS/JS e componenti React.","Linee guida PA §6.3; https://github.com/italia/design-react-kit","Le linee guida descrivono Web Kit distribuiti come pacchetti npm. Design React Kit implementa Bootstrap Italia e gli stili del Design UI Kit per applicazioni ad alta interattività.")
    return s


def design_react_code_slide(number):
    s=base(True)
    text(s,"Design React Kit: un componente conforme resta codice React",.8,.7,11.7,.65,27,NAVY,True)
    code="""import { Alert, Button } from 'design-react-kit';\nimport 'bootstrap-italia/dist/css/bootstrap-italia.min.css';\n\nfunction App() {\n  const [sent, setSent] = useState(false);\n  return <>\n    <Button color=\"primary\" onClick={() => setSent(true)}>\n      Avvia richiesta\n    </Button>\n    {sent && <Alert color=\"success\">Richiesta avviata</Alert>}\n  </>;\n}"""
    rect(s,.68,1.45,7.05,5.02,NAVY_2,True); text(s,code,.98,1.78,6.42,4.35,13,WHITE,False,font="Aptos Mono")
    rect(s,8.0,1.45,4.58,5.02,WHITE,True,PALE)
    text(s,"COSA FORNISCE IL KIT",8.35,1.83,3.88,.28,12,CORAL,True,align=PP_ALIGN.CENTER)
    add_rich_lines(s,["componenti React tipizzati", "stili di Bootstrap Italia", "font istituzionali configurabili", "Storybook con esempi", "pacchetto npm riusabile"],8.25,2.38,4.05,3.2,14)
    link_button(s,"APRI IL TEMPLATE STACKBLITZ","https://stackblitz.com/edit/vitejs-vite-yy8bnk?file=src/App.tsx",8.38,5.67,3.82)
    source_label(s,"Design React Kit README e template StackBlitz ufficiale")
    footer(s,"Ecosistemi · React",number,"20 min")
    notes(s,"Collegare il codice al risultato visivo. Evidenziare import del CSS Bootstrap Italia, gestione dello stato e composizione dei componenti.","Design React Kit: https://github.com/italia/design-react-kit","Il kit richiede bootstrap-italia e i font separatamente. Il repository suggerisce Vite e fornisce un template StackBlitz ufficiale.")
    return s


def react_live_lab_slide(number):
    s=base(False)
    text(s,"Laboratorio live: modifica React direttamente nel browser",.82,.7,11.4,.7,28,WHITE,True)
    rect(s,.72,1.45,11.86,1.0,WHITE,True,WHITE)
    text(s,"STACKBLITZ",1.08,1.77,2.15,.28,15,CORAL,True)
    text(s,"Modifica src/App.tsx → anteprima immediata → condividi il risultato",3.25,1.77,8.75,.3,17,NAVY,True)
    tasks=[("1","Sostituisci Alert con un messaggio diverso"),("2","Aggiungi un Button primario con onClick"),("3","Introduci useState per mostrare/nascondere l'Alert"),("4","Prova color, outline, size e stato disabled")]
    for i,(n,task) in enumerate(tasks):
        x=.72+(i%2)*6.02; y=2.83+(i//2)*1.25
        rect(s,x,y,5.72,.92,NAVY_2,True)
        text(s,n,x+.2,y+.25,.35,.28,16,CORAL,True)
        text(s,task,x+.72,y+.22,4.65,.42,13,WHITE,True)
    link_button(s,"APRI IL LABORATORIO UFFICIALE IN STACKBLITZ","https://stackblitz.com/edit/vitejs-vite-yy8bnk?file=src/App.tsx",3.67,5.64,6.0,True)
    source_label(s,"Template StackBlitz ufficiale di Design React Kit",True)
    footer(s,"Ecosistemi · React",number,"25 min",True)
    notes(s,"Aprire il template StackBlitz ufficiale e assegnare una modifica per coppia. Tutto avviene nel browser, senza installazione locale.","StackBlitz ufficiale: https://stackblitz.com/edit/vitejs-vite-yy8bnk?file=src/App.tsx","Sequenza consigliata: modificare l'Alert, aggiungere un Button, introdurre useState, quindi sperimentare le proprietà visuali e disabled.")
    return s


def api_contract_visual(number):
    s=base(True)
    text(s,"Il contratto API: quattro ingredienti",.8,.7,11.7,.65,27,NAVY,True)
    picture_fit(s,Path("assets/source-api-pdf/p046-1.jpg"),.75,1.45,7.2,5.05)
    ingredients=[("1","SERVIZI","cosa è disponibile"),("2","INPUT","cosa inviare"),("3","OUTPUT","cosa ritorna"),("4","SCHEMI","forma e tipi dei dati")]
    for i,(n,k,v) in enumerate(ingredients):
        y=1.55+i*1.17; rect(s,8.32,y,3.9,.93,WHITE,True,PALE)
        text(s,n,8.52,y+.22,.38,.3,14,CORAL,True); text(s,k,9.0,y+.16,1.15,.25,10,TEAL,True); text(s,v,9.0,y+.48,2.85,.28,13,NAVY,True)
    text(s,"Una specifica formale consente documentazione, validazione, mocking e generazione di strumenti.",8.38,6.02,3.78,.52,13,MUTED,True,align=PP_ALIGN.CENTER)
    source_label(s,"Figura originale: Microservices-Architectures_v3.pdf, p. 46; testo dagli appunti API")
    footer(s,"architetture",number,"15 min")
    notes(s,"Spiegare che un'API non è soltanto un endpoint: è un contratto analizzabile dagli strumenti.","ARCHITETTURE MICROSERVIZI…, paragrafi 266-295; Microservices-Architectures_v3.pdf p.46.","Citare OpenAPI/RAML per REST, IDL per gRPC e AsyncAPI per pub/sub come esempi, senza entrare nella sintassi.")
    return s


def api_gateway_visual(number):
    s=base(False)
    text(s,"API Gateway: un punto di ingresso, molte policy",.82,.7,11.4,.7,28,WHITE,True)
    rect(s,.72,1.46,7.45,4.95,WHITE,True,WHITE); picture_fit(s,Path("assets/source-api-pdf/p064-1.jpg"),.92,1.68,7.05,4.48)
    text(s,"POLICY TRASVERSALI",8.55,1.58,3.25,.28,10,CORAL,True)
    items=["Routing e versioni","Autenticazione","Rate limiting e quote","Caching e CORS","Logging e metriche"]
    for i,it in enumerate(items):
        y=2.13+i*.72; rect(s,8.55,y,3.2,.52,NAVY_2,True); text(s,it,8.78,y+.1,2.74,.27,14,WHITE,True)
    picture_fit(s,Path("assets/source-api-pdf/p078-1.jpg"),8.68,5.72,2.9,.75)
    source_label(s,"Figure originali: Microservices-Architectures_v3.pdf, pp. 64 e 78",True)
    footer(s,"architetture",number,"18 min",True)
    notes(s,"Mostrare il gateway come punto di enforcement e non come luogo dove accumulare logica di business.","Microservices-Architectures_v3.pdf pp.64-65 e 78; appunti, Service Gateway / Policy Proxy.","Collegare client diversi, routing verso microservizi e OAuth/JWT. Evidenziare il rischio di single point of failure e di nuovo monolite nel gateway.")
    return s


def devops_flow_slide(number):
    s=base(False)
    text(s,"Caso S21: DevOps è una catena di tracciabilità",.82,.7,11.45,.7,29,WHITE,True)
    stages=[("BISOGNO","Epic / Feature"),("LAVORO","Story / Task"),("CODICE","Git / PR"),("VERIFICA","CI / test"),("RILASCIO","artifact / deploy"),("MISURA","dashboard")]
    for i,(a,b) in enumerate(stages):
        x=.65+i*2.08
        rect(s,x,2.05,1.73,2.0,NAVY_2,True)
        text(s,str(i+1).zfill(2),x+.18,2.28,.38,.25,10,CORAL,True)
        text(s,a,x+.16,2.85,1.41,.28,12,TEAL,True,align=PP_ALIGN.CENTER)
        text(s,b,x+.16,3.34,1.41,.36,13,WHITE,True,align=PP_ALIGN.CENTER)
        if i<5: text(s,"→",x+1.75,2.9,.31,.3,15,SKY,True,align=PP_ALIGN.CENTER)
    rect(s,1.18,4.75,10.95,1.05,WHITE,True,WHITE)
    text(s,"Ogni passaggio produce evidenze collegate: requisito → ticket → commit → pull request → build → test → release.",1.55,5.02,10.2,.5,18,NAVY,True,align=PP_ALIGN.CENTER)
    source_label(s,"Fonte: GUIDA OPERATIVA S21: AZURE DEVOPS, sezioni 1-11",True)
    footer(s,"DevOps e CI/CD",number,"12 min",True)
    notes(s,"Introdurre il caso S21 come sistema di lavoro end-to-end, non come semplice uso di Azure DevOps.","GUIDA OPERATIVA S21: AZURE DEVOPS, intero documento.","La parola chiave è tracciabilità: ogni artefatto deve poter essere ricondotto al bisogno e alle verifiche.")
    return s


def devops_team_slide(number):
    s=base(True)
    text(s,"Il team DevOps S21: responsabilità lungo il flusso",.8,.7,11.7,.65,27,NAVY,True)
    rect(s,.72,1.42,9.0,5.18,WHITE,True,PALE)
    picture_fit(s,Path("assets/source-devops/image23.png"),.9,1.62,8.64,4.82)
    text(s,"LETTURA",10.05,1.65,2.0,.25,10,CORAL,True)
    add_rich_lines(s,["Analista funzionale: bisogno e criteri", "Architect/lead: disegno e coordinamento", "Developer: implementazione e review", "Tester/QA: evidenze e difetti", "Operations: rilascio ed esercizio"],10.0,2.12,2.35,3.35,13)
    text(s,"Il lavoro attraversa ruoli diversi; la piattaforma conserva i collegamenti.",10.05,5.73,2.18,.55,13,NAVY,True,align=PP_ALIGN.CENTER)
    source_label(s,"Figura 1 originale: struttura organizzativa S21 per l'adozione DevOps")
    footer(s,"DevOps e CI/CD",number,"15 min")
    notes(s,"Mostrare la composizione reale e distinguere il Team Azure DevOps, che rappresenta un'iniziativa, dal team fisico.","Guida S21, §1.1 e Figura 1.","Evidenziare i passaggi di responsabilità e lo swarming tra sviluppatori.")
    return s


def workitem_hierarchy_slide(number):
    s=base(True)
    text(s,"Dal requisito al ticket: una gerarchia verificabile",.8,.7,11.7,.65,27,NAVY,True)
    levels=[("INIZIATIVA","contenitore"),("EPIC","obiettivo"),("FEATURE","caso d'uso"),("USER STORY","valore utente"),("TASK / BUG","lavoro tecnico")]
    for i,(a,b) in enumerate(levels):
        x=.74+i*2.5; y=1.58+i*.18
        rect(s,x,y,2.13,1.28,WHITE,True,[TEAL,SKY,NAVY_2,CORAL,TEAL][i])
        text(s,a,x+.15,y+.27,1.83,.25,10,[TEAL,SKY,NAVY_2,CORAL,TEAL][i],True,align=PP_ALIGN.CENTER)
        text(s,b,x+.15,y+.71,1.83,.3,13,NAVY,True,align=PP_ALIGN.CENTER)
        if i<4: text(s,"→",x+2.14,y+.5,.34,.28,15,MUTED,True,align=PP_ALIGN.CENTER)
    rect(s,.82,3.45,11.66,2.55,NAVY,True)
    text(s,"BRD → dominio → Use Case → Feature → User Story → Sequence Diagram → Task",1.17,3.85,10.95,.42,20,WHITE,True,align=PP_ALIGN.CENTER)
    text(s,"DoR prima di iniziare: titolo, bisogno, criteri di accettazione, stima e dipendenze.",1.45,4.64,10.4,.34,16,TEAL,True,align=PP_ALIGN.CENTER)
    text(s,"DoD per chiudere: criteri soddisfatti, task chiusi, codice revisionato e validazione completata.",1.45,5.21,10.4,.34,15,RGBColor(207,216,229),False,align=PP_ALIGN.CENTER)
    source_label(s,"Fonte: Guida S21, §§2, 4 e 8")
    footer(s,"DevOps e CI/CD",number,"15 min")
    notes(s,"Spiegare come nasce il ticket e perché la gerarchia evita il salto diretto dal requisito al task.","Guida S21, §2 Gerarchia Work Item; §4 DoR/DoD; §8 Analisi e tracciamento.","Usare il flusso inferiore come catena di derivazione, non come metodologia universale.")
    return s


def story_board_slide(number):
    s=base(False)
    text(s,"Ticket e board: dal chiarimento al lavoro quotidiano",.82,.7,11.4,.7,28,WHITE,True)
    rect(s,.72,1.45,6.15,4.9,WHITE,True,WHITE); picture_fit(s,Path("assets/source-devops/image27.png"),.88,1.62,5.82,4.55)
    rect(s,7.13,1.45,5.48,4.9,WHITE,True,WHITE); picture_fit(s,Path("assets/source-devops/image33.png"),7.3,1.62,5.14,4.55)
    text(s,"USER STORY / TASK CON CCC",1.12,6.12,5.35,.24,10,TEAL,True,align=PP_ALIGN.CENTER)
    text(s,"SPRINT BOARD E STATO DEL FLUSSO",7.48,6.12,4.82,.24,10,CORAL,True,align=PP_ALIGN.CENTER)
    source_label(s,"Figure originali S21: User Story con Card-Conversation-Confirmation e Sprint Board",True)
    footer(s,"DevOps e CI/CD",number,"18 min",True)
    notes(s,"Mostrare la creazione operativa del ticket: Card sintetica, Conversation tra ruoli e Confirmation tramite acceptance criteria; poi la sua visibilità sulla board.","Guida S21, §4.2 Figura 5 e §7.1 Figura 8.","Far notare collegamenti a parent, commit e pull request presenti nel work item.")
    return s


def git_flow_slide(number):
    s=base(True)
    text(s,"Git: il codice avanza per branch e controlli",.8,.7,11.7,.65,27,NAVY,True)
    branches=[("master","produzione",CORAL),("staging","pre-produzione",NAVY_2),("acceptance","UAT",SKY),("develop","integrazione",TEAL)]
    for i,(name,env,c) in enumerate(branches):
        y=1.65+i*1.05
        text(s,name,1.0,y,1.45,.3,14,c,True,align=PP_ALIGN.RIGHT)
        rect(s,2.72,y+.1,7.9,.10,c)
        for j in range(4): rect(s,3.3+j*1.9,y-.04,.34,.34,c,True)
        text(s,env,10.85,y,1.25,.3,11,MUTED,True)
    rect(s,4.2,5.65,4.8,.74,NAVY,True)
    text(s,"feature/* → Pull Request → develop",4.5,5.84,4.2,.3,16,WHITE,True,align=PP_ALIGN.CENTER)
    text(s,"Flusso unidirezionale: develop → acceptance → staging → master",2.0,6.52,9.3,.28,14,NAVY,True,align=PP_ALIGN.CENTER)
    source_label(s,"Fonte: Guida S21, §3 Strategia di Branching e Merging")
    footer(s,"DevOps e CI/CD",number,"15 min")
    notes(s,"Presentare Git come meccanismo di collaborazione e controllo, non soltanto come archivio del codice.","Guida S21, §3.1.","Regole S21: niente commit diretti sui branch long-lived; feature, bugfix e hotfix sono short-lived; cancellare il branch dopo il merge.")
    return s


def pull_request_slide(number):
    s=base(True)
    text(s,"Pull Request: il punto di controllo prima del merge",.8,.7,11.7,.65,27,NAVY,True)
    rect(s,.78,1.52,7.5,4.95,WHITE,True,PALE); picture_fit(s,Path("assets/source-devops/image27.png"),.98,1.72,7.1,4.55)
    checks=[("1","Work item collegato"),("2","Reviewer nominato"),("3","Build CI superata"),("4","Discussione risolta"),("5","Merge nel branch target")]
    for i,(n,v) in enumerate(checks):
        y=1.63+i*.9; rect(s,8.62,y,3.55,.66,WHITE,True,PALE)
        text(s,n,8.84,y+.15,.35,.25,12,CORAL,True); text(s,v,9.28,y+.13,2.55,.3,14,NAVY,True)
    source_label(s,"Schermata S21: collegamenti Development del work item; regole PR dalla Guida §5.2")
    footer(s,"DevOps e CI/CD",number,"15 min")
    notes(s,"Usare la zona Development della schermata per mostrare il collegamento tra ticket, commit, branch e pull request.","Guida S21, §5.2; Figura 5 come schermata di contesto.","La PR combina revisione umana, policy automatiche e tracciabilità. Il merge è una decisione verificata.")
    return s


def pipeline_slide(number):
    s=base(False)
    text(s,"Pipeline CI/CD: dal commit a un artefatto distribuibile",.82,.7,11.4,.7,28,WHITE,True)
    stages=["COMMIT","BUILD","TEST","PACKAGE","PUBLISH","DEPLOY"]
    for i,a in enumerate(stages):
        x=.65+i*2.08; rect(s,x,1.58,1.72,.65,NAVY_2,True); text(s,a,x+.12,1.77,1.48,.24,11,WHITE,True,align=PP_ALIGN.CENTER)
        if i<5:text(s,"→",x+1.75,1.77,.29,.24,13,TEAL,True,align=PP_ALIGN.CENTER)
    rect(s,.72,2.58,5.9,3.55,WHITE,True,WHITE); picture_fit(s,Path("assets/source-devops/image2.png"),.9,2.76,5.55,3.18)
    rect(s,6.9,2.58,5.7,3.55,WHITE,True,WHITE); picture_fit(s,Path("assets/source-devops/image13.png"),7.08,2.76,5.34,3.18)
    text(s,"ESECUZIONE E LOG",1.1,6.18,5.15,.24,10,TEAL,True,align=PP_ALIGN.CENTER)
    text(s,"ARTIFACT VERSIONATI",7.28,6.18,4.95,.24,10,CORAL,True,align=PP_ALIGN.CENTER)
    source_label(s,"Figure S21: monitoraggio pipeline e artifact pubblicati",True)
    footer(s,"DevOps e CI/CD",number,"18 min",True)
    notes(s,"Descrivere la pipeline come sequenza automatica e ripetibile che produce evidenze e un artefatto versionato.","Guida S21, §11 e Figure 41-42.","Collegare Maven/.NET, feed Azure Artifacts, permessi del build service e separazione tra build e deploy.")
    return s


def testing_pipeline_slide(number):
    s=base(True)
    text(s,"Il flusso di testing S21: tre livelli, un solo feedback loop",.8,.7,11.7,.65,27,NAVY,True)
    lanes=[
        ("1  UNIT TEST / TEST DEL DEVELOPER", "TASK · locale", "Verifica il comportamento del codice prima della Pull Request.", TEAL),
        ("2  TEST AUTOMATICI IN CI", "PR · build", "La pipeline esegue i controlli: un esito negativo blocca il merge.", CORAL),
        ("3  TEST DI INTEGRAZIONE E VALIDAZIONE", "develop → UAT → staging", "Integrazione tecnica, accettazione stakeholder e verifica finale pre-produzione.", SKY),
    ]
    for i,(title,where,body,color) in enumerate(lanes):
        y=1.5+i*1.48
        rect(s,.72,y,11.86,1.15,WHITE,True,PALE)
        rect(s,.72,y,.16,1.15,color)
        text(s,title,1.08,y+.17,4.25,.28,14,NAVY,True)
        text(s,where,1.08,y+.55,3.9,.23,10,color,True)
        text(s,body,5.25,y+.24,6.75,.52,14,INK)
        if i<2: text(s,"↓",6.38,y+1.15,.55,.3,17,color,True,align=PP_ALIGN.CENTER)
    rect(s,.72,6.04,11.86,.52,NAVY,True)
    text(s,"FAIL → niente avanzamento: correggere il Task o aprire un Bug collegato → rieseguire il test",1.05,6.18,11.2,.22,12,WHITE,True,align=PP_ALIGN.CENTER)
    source_label(s,"Guida S21: workflow Task/Story, ambienti dev-develop, UAT-acceptance e staging")
    footer(s,"DevOps e CI/CD",number,"18 min")
    notes(s,"Spiegare il testing come una progressione di feedback: il developer verifica il Task, la CI applica il gate automatico sulla PR, gli ambienti condivisi verificano integrazione e accettazione.","Guida S21, §§3.1, 5.2, 6.3 e 9.2; tabelle Ambienti, Definition of Done e workflow.","Nel documento i test a livello Task sono chiamati test del developer: qui sono presentati didatticamente come unit test. develop ospita l'integration testing; acceptance la UAT; staging l'integrazione finale del release candidate.")
    return s


def testing_evidence_slide(number):
    s=base(False)
    text(s,"Dal requisito al difetto: ogni test lascia un'evidenza",.82,.7,11.4,.7,28,WHITE,True)
    items=[("1. TEST PLAN","image1.png"),("2. TEST CASE","image16.png"),("3. TEST RUN","image17.png"),("4. BUG + FIX","image35.png")]
    for i,(cap,img) in enumerate(items):
        x=.58+i*3.17
        rect(s,x,1.52,2.9,3.92,WHITE,True,WHITE)
        picture_fit(s,Path("assets/source-devops")/img,x+.12,1.68,2.66,3.34)
        text(s,cap,x+.13,5.14,2.64,.2,10,CORAL if i in (0,3) else TEAL,True,align=PP_ALIGN.CENTER)
        if i<3: text(s,"→",x+2.91,3.16,.25,.3,16,TEAL,True,align=PP_ALIGN.CENTER)
    rect(s,.72,5.76,11.86,.64,NAVY_2,True)
    text(s,"Test fallito → Bug collegato al Test Case → Task di correzione → nuova esecuzione → chiusura",1.03,5.96,11.22,.24,12,WHITE,True,align=PP_ALIGN.CENTER)
    source_label(s,"Schermate originali S21: creazione ed esecuzione dei test in Azure DevOps",True)
    footer(s,"DevOps e CI/CD",number,"18 min",True)
    notes(s,"Seguire da sinistra a destra la catena di evidenze. Il valore non è la singola schermata, ma la tracciabilità tra requisito, esecuzione, difetto e correzione.","Guida S21, §9.2, Figure 25-30.","Un Test Plan organizza le verifiche; il Test Case descrive passi ed esito atteso; il Test Run registra l'esecuzione; dal fallimento nasce un Bug collegato, risolto tramite un Task e poi ritestato.")
    return s


def dashboard_operations_slide(number):
    s=base(False)
    text(s,"Dashboard operative: vedere flusso e capacità",.82,.7,11.4,.7,28,WHITE,True)
    rect(s,.72,1.42,6.0,4.95,WHITE,True,WHITE); picture_fit(s,Path("assets/source-devops/image19.png"),.9,1.62,5.65,4.58)
    rect(s,6.98,1.42,5.62,4.95,WHITE,True,WHITE); picture_fit(s,Path("assets/source-devops/image20.png"),7.16,1.62,5.26,4.58)
    text(s,"TEAM: carico, burndown, blocchi",1.05,6.13,5.36,.24,10,TEAL,True,align=PP_ALIGN.CENTER)
    text(s,"MANAGEMENT: velocity, CFD, cycle time",7.3,6.13,4.95,.24,10,CORAL,True,align=PP_ALIGN.CENTER)
    source_label(s,"Figure S21: Cruscotto tattico e cruscotto strategico",True)
    footer(s,"DevOps e CI/CD",number,"15 min",True)
    notes(s,"Distinguere la dashboard per il daily da quella per la governance. Una metrica serve a una decisione, non a valutare persone.","Guida S21, §§10.1-10.2 e Figure 31-33.","Leggere burndown, blocked items, velocity, cumulative flow e cycle time nel loro contesto.")
    return s


def dashboard_quality_slide(number):
    s=base(True)
    text(s,"Dashboard qualità: difetti, tempi ed esiti dei test",.8,.7,11.7,.65,27,NAVY,True)
    rect(s,.7,1.42,6.0,4.95,WHITE,True,PALE); picture_fit(s,Path("assets/source-devops/image6.png"),.9,1.62,5.62,4.58)
    rect(s,6.96,1.42,5.65,4.95,WHITE,True,PALE); picture_fit(s,Path("assets/source-devops/image37.png"),7.16,1.62,5.27,4.58)
    text(s,"BUG ATTIVI, SEVERITÀ, LEAD TIME",1.02,6.13,5.35,.24,10,TEAL,True,align=PP_ALIGN.CENTER)
    text(s,"SCOPE CREEP ED ESCAPED DEFECT",7.27,6.13,4.98,.24,10,CORAL,True,align=PP_ALIGN.CENTER)
    source_label(s,"Figure 34-36 originali: Dashboard Quality Management S21")
    footer(s,"DevOps e CI/CD",number,"18 min")
    notes(s,"Usare la dashboard per spiegare come si misura la qualità nel tempo e lungo il flusso.","Guida S21, §10.3 e Figure 34-36.","Indicatori: active bugs per severity, lead time dei bug, risultati test, scope creep ed escaped defect. Evitare interpretazioni isolate dal volume e dalla severità.")
    return s


def release_case_slide(number):
    s=base(False)
    text(s,"Caso S21: dall'approvazione della release al deploy",.82,.7,11.4,.7,28,WHITE,True)
    imgs=[("1. APPROVAZIONE","image4.png"),("2. TRIGGER","image15.png"),("3. PIPELINE","image2.png"),("4. ARTIFACT","image13.png")]
    for i,(cap,img) in enumerate(imgs):
        x=.72+(i%2)*6.0; y=1.45+(i//2)*2.48
        rect(s,x,y,5.72,2.17,WHITE,True,WHITE); picture_fit(s,Path("assets/source-devops")/img,x+.13,y+.13,5.46,1.74)
        text(s,cap,x+.2,y+1.89,5.3,.2,9,CORAL if i in (0,3) else TEAL,True,align=PP_ALIGN.CENTER)
    source_label(s,"Sequenza originale S21, Figure 37, 39, 41 e 42",True)
    footer(s,"DevOps e CI/CD",number,"20 min",True)
    notes(s,"Chiudere il caso seguendo l'evidenza: work item approvato, trigger/webhook, esecuzione pipeline, artifact versionato e deploy.","Guida S21, §11.4, Figure 37-43.","Chiedere al gruppo quali controlli devono essere automatici e quali richiedono approvazione umana.")
    return s


slides = []
slides.append(title_slide("Panoramica sui linguaggi di programmazione moderni e scelte architetturali", "Una guida comparativa per leggere proposte, architetture e trade-off tecnologici"))

slides.append(content_slide("Perché siamo qui", "apertura", 2,
    ["Orientarsi tra linguaggi, framework e piattaforme", "Collegare le tecnologie ai contesti applicativi", "Valutare proposte tecniche con criteri espliciti", "Dialogare con sviluppatori e fornitori con un lessico condiviso"],
    "8 min", query="obiettivi corso linguaggi architetture governance", prompt="Mappa: tecnologia → contesto → decisione"))
slides.append(content_slide("Il percorso in quattro mezze giornate", "apertura", 3,
    ["1. Linguaggi e paradigmi", "2. Ecosistemi: Java, .NET, Python, JavaScript e React", "3. Architetture cloud-native e delivery", "4. Scelte, qualità, sicurezza e casi"],
    "7 min", query="agenda corso linguaggi moderni", prompt="Timeline delle 16 ore"))
slides.append(content_slide("La lente con cui confronteremo le tecnologie", "apertura", 4,
    ["Problema e vincoli", "Ecosistema e competenze", "Qualità operative", "Costi e sostenibilità", "Rischi e reversibilità della scelta"],
    "12 min", query="criteri scelta tecnologia matrice trade off", prompt="Radar o matrice di decisione"))
slides.append(activity_slide("Mappa iniziale delle percezioni", "apertura", 5,
    "Un fornitore propone un nuovo stack. Prima di valutarlo, quali domande fate?",
    ["Qual è il problema che risolve?", "Quali vincoli abbiamo?", "Quali evidenze chiediamo?", "Quali rischi vanno resi visibili?"], "15 min", "domande valutazione proposta tecnica fornitore"))

slides.append(section_slide("GIORNATA 1", "Linguaggi, paradigmi e runtime", "Costruire un vocabolario comune prima di confrontare gli stack.", 1))
slides.append(content_slide("Che cos'è un linguaggio di programmazione?", "linguaggi e paradigmi", 7,
    ["Una notazione con regole sintattiche e semantiche", "Un modello per esprimere dati, controllo e comportamento", "Un elemento di un ecosistema più ampio"],
    query="introduzione linguaggi programmazione sintassi semantica ecosistema", prompt="Schema: linguaggio ≠ runtime ≠ framework"))
slides.append(content_slide("Dal codice al sistema in esecuzione", "linguaggi e paradigmi", 8,
    ["Codice sorgente", "Compilatore o interprete", "Runtime e librerie", "Sistema operativo e infrastruttura"],
    query="compilatore interprete runtime diagramma", prompt="Pipeline sorgente → runtime → infrastruttura"))
slides.append(comparison_slide("Compilato e interpretato: una distinzione utile ma non assoluta", "linguaggi e paradigmi", 9,
    "Compilazione", "Interpretazione / VM",
    ["Traduzione prima dell'esecuzione", "Controlli anticipati", "Artefatto distribuibile"],
    ["Runtime intermedio", "Portabilità e dinamismo", "JIT e approcci ibridi"], query="compilati interpretati JIT bytecode figura"))
slides.append(content_slide("Paradigma procedurale", "linguaggi e paradigmi", 10,
    ["Sequenze di operazioni", "Stato modificato nel tempo", "Procedure e funzioni come unità di scomposizione"],
    query="paradigma procedurale esempio diagramma", prompt="Piccolo esempio: flusso procedurale"))
slides.append(content_slide("Paradigma object-oriented", "linguaggi e paradigmi", 11,
    ["Oggetti con stato e comportamento", "Incapsulamento e responsabilità", "Composizione, ereditarietà e polimorfismo"],
    query="object oriented incapsulamento polimorfismo figura", prompt="Diagramma di oggetti e responsabilità"))
slides.append(content_slide("Paradigma funzionale", "linguaggi e paradigmi", 12,
    ["Funzioni come valori", "Immutabilità e trasformazioni", "Riduzione degli effetti collaterali"],
    query="programmazione funzionale immutabilità pure functions figura", prompt="Input → trasformazioni → output"))
slides.append(comparison_slide("Multiparadigma: il caso reale", "linguaggi e paradigmi", 13,
    "Etichetta del linguaggio", "Uso nel progetto",
    ["Orientamento prevalente", "Costrutti disponibili", "Storia dell'ecosistema"],
    ["Stile scelto dal team", "Vincoli del framework", "Coesistenza di paradigmi"], query="linguaggi multiparadigma Java Python JavaScript"))
slides.append(content_slide("Tipi statici e dinamici", "linguaggi e paradigmi", 14,
    ["Quando avvengono i controlli", "Cosa può inferire lo strumento", "Impatto su feedback, refactoring e interoperabilità"],
    query="static dynamic typing confronto", prompt="Stessa operazione, feedback in momenti diversi"))
slides.append(content_slide("Ecosistema, tooling e comunità", "linguaggi e paradigmi", 15,
    ["Librerie e framework", "IDE, build, test e osservabilità", "Competenze disponibili", "Ciclo di vita e governance"],
    query="ecosistema linguaggio package manager IDE framework", prompt="Iceberg: sintassi sopra, ecosistema sotto"))
slides.append(content_slide("I trend che cambiano le scelte", "linguaggi e paradigmi", 16,
    ["API-first", "Cloud-native", "Microservizi", "Containerizzazione", "Automazione della delivery"],
    query="api first cloud native microservices container trend", prompt="Mappa dei trend e delle relazioni"))
slides.append(activity_slide("Leggere oltre l'etichetta", "linguaggi e paradigmi", 17,
    "Tre proposte si dichiarano rispettivamente “moderna”, “cloud-native” e “enterprise-grade”.",
    ["Quali fatti verifichiamo?", "Quali qualità ci interessano?", "Quali parole sono solo etichette?"], "20 min", "buzzword cloud native enterprise grade valutazione"))
slides.append(section_slide("GIORNATA 2", "Ecosistemi e casi d'uso", "Java, .NET, Python, JavaScript e React letti con la stessa griglia.", 2))
slides.append(content_slide("Una griglia comune per il confronto", "ecosistemi", 20,
    ["Modello di esecuzione", "Punti di forza dell'ecosistema", "Contesti tipici", "Qualità operative", "Rischi e competenze"], query="matrice confronto linguaggi programmazione", prompt="Tabella comparativa progressiva"))
slides.append(java_execution_slide(21))
slides.append(bytecode_slide(22))
slides.append(jvm_runtime_slide(23))
slides.append(java_gc_slide(24))
slides.append(g1_slide(25))
slides.append(visualvm_slide(26))
slides.append(content_slide(".NET: runtime e piattaforma", "ecosistemi", 23,
    ["C# e Common Language Runtime", "Librerie e strumenti integrati", "Portabilità moderna", "Ecosistema Microsoft e open source"], query="dotnet CLR C sharp architecture", prompt="C# → IL → CLR"))
slides.append(content_slide(".NET nei sistemi applicativi", "ecosistemi", 24,
    ["Web API e servizi", "Applicazioni enterprise", "Integrazione con ambienti Microsoft", "Deployment multipiattaforma"], query="ASP.NET Web API enterprise architecture", prompt="Architettura backend .NET annotata"))
slides.append(comparison_slide("Java e .NET", "ecosistemi", 25, "Java / JVM", ".NET / CLR",
    ["Ecosistema JVM", "Framework e standard enterprise", "Ampia base installata"],
    ["Toolchain integrata", "Ecosistema Microsoft", "Runtime multipiattaforma"], "15 min", "Java vs .NET architettura confronto enterprise"))
slides.append(rest_api_visual(26))
slides.append(python_overview_slide(31))
slides.append(pandas_dataframe_slide(32))
slides.append(pandas_workflow_slide(33))
slides.append(seaborn_gallery_slide(34))
slides.append(python_ml_slide(35))
slides.append(python_tree_lab_slide(36))
slides.append(python_genai_slide(37))
slides.append(javascript_browser_slide(37))
slides.append(javascript_console_slide(38))
slides.append(caniuse_slide(39))
slides.append(react_quickstart_slide(39))
slides.append(react_dataflow_slide(40))
slides.append(react_native_overview_slide(41))
slides.append(react_native_snack_slide(42))
slides.append(mui_components_slide(41))
slides.append(mui_mcp_slide(42))
slides.append(design_italia_slide(43))
slides.append(design_react_code_slide(44))
slides.append(react_live_lab_slide(45))
slides.append(comparison_slide("Backend e frontend: responsabilità diverse", "ecosistemi", 32,
    "Frontend", "Backend",
    ["Interazione e presentazione", "Stato dell'interfaccia", "Accessibilità e UX"],
    ["Regole e dati", "Sicurezza e integrazione", "Affidabilità e scalabilità"], query="frontend backend responsibilities diagram"))
slides.append(activity_slide("Scegliere uno stack per un servizio", "ecosistemi", 33,
    "Un nuovo servizio deve offrire un portale, integrare sistemi esistenti e produrre analisi periodiche.",
    ["Quali componenti distinguiamo?", "Quale tecnologia per ciascun ruolo?", "Quali competenze e vincoli contano?", "Cosa chiediamo al fornitore?"], "30 min", "case study Java .NET Python React architecture"))
slides.append(section_slide("GIORNATA 3", "Architetture moderne e delivery", "Dalla forma dell'applicazione al modo in cui viene rilasciata e gestita.", 3))
slides.append(content_slide("Architettura: decisioni e trade-off", "architetture", 36,
    ["Struttura dei componenti", "Relazioni e contratti", "Qualità da privilegiare", "Vincoli e decisioni difficili da cambiare"], query="software architecture tradeoffs diagram", prompt="Decisioni → struttura → qualità"))
slides.append(microservices_comparison(37))
slides.append(microservices_conditions(38))
slides.append(service_boundaries(39))
slides.append(api_contract_visual(40))
slides.append(api_gateway_visual(41))
slides.append(container_lifecycle(42))
slides.append(vm_container_visual(43))
slides.append(orchestrator_slide(44))
slides.append(kubernetes_overview(45))
slides.append(devops_flow_slide(46))
slides.append(devops_team_slide(47))
slides.append(workitem_hierarchy_slide(48))
slides.append(story_board_slide(49))
slides.append(git_flow_slide(50))
slides.append(pull_request_slide(51))
slides.append(pipeline_slide(52))
slides.append(testing_pipeline_slide(53))
slides.append(testing_evidence_slide(54))
slides.append(dashboard_operations_slide(55))
slides.append(dashboard_quality_slide(56))
slides.append(release_case_slide(57))
slides.append(content_slide("Osservabilità e gestione operativa", "architetture", 47,
    ["Log, metriche e trace", "Health check e alert", "Obiettivi di servizio", "Capacità di diagnosi"], query="observability logs metrics traces diagram", prompt="Tre segnali + contesto operativo"))
slides.append(activity_slide("Modernizzare: dove sta davvero il valore?", "architetture", 48,
    "Un'applicazione stabile viene proposta per la migrazione a microservizi su Kubernetes.",
    ["Quale problema stiamo risolvendo?", "Quali benefici sono misurabili?", "Quali nuove complessità introduciamo?", "Quale percorso incrementale è possibile?"], "30 min", "modernization monolith microservices Kubernetes case study"))
slides.append(section_slide("GIORNATA 4", "Decisioni, qualità e casi", "Trasformare la panoramica tecnica in capacità di valutazione.", 4))
slides.append(content_slide("Dalle esigenze ai criteri di scelta", "decisioni e qualità", 51,
    ["Driver di business", "Vincoli tecnici e normativi", "Attributi di qualità", "Competenze e modello operativo", "Evidenze e assunzioni"], query="technology decision criteria quality attributes", prompt="Funnel: esigenze → criteri → opzioni"))
slides.append(content_slide("Attributi di qualità", "decisioni e qualità", 52,
    ["Affidabilità", "Prestazioni e scalabilità", "Sicurezza", "Manutenibilità", "Interoperabilità", "Usabilità e accessibilità"], query="software quality attributes ISO 25010 diagram", prompt="Quality attribute wheel"))
slides.append(content_slide("Matrice di valutazione delle alternative", "decisioni e qualità", 53,
    ["Criteri espliciti e pesati", "Scala di valutazione condivisa", "Evidenze a supporto", "Sensibilità rispetto ai pesi", "Decisione documentata"], query="weighted decision matrix technology selection", prompt="Tabella opzioni × criteri"))
slides.append(content_slide("Decision record: rendere la scelta leggibile", "decisioni e qualità", 54,
    ["Contesto", "Decisione", "Alternative considerate", "Conseguenze", "Data, stato e responsabili"], query="architecture decision record ADR example", prompt="Scheda ADR in una pagina"))
slides.append(content_slide("Codice manutenibile", "decisioni e qualità", 55,
    ["Leggibilità e semplicità", "Responsabilità chiare", "Riduzione della duplicazione", "Standard condivisi e revisione"], query="clean code maintainability teaching figure", prompt="Prima / dopo: costo del cambiamento"))
slides.append(content_slide("Testabilità", "decisioni e qualità", 56,
    ["Comportamenti verificabili", "Dipendenze controllabili", "Test a più livelli", "Automazione e feedback rapido"], query="testing pyramid unit integration end to end", prompt="Piramide o portafoglio dei test"))
slides.append(content_slide("Documentazione che accompagna il sistema", "decisioni e qualità", 57,
    ["Contratti API", "Decisioni architetturali", "Modelli e diagrammi", "Runbook e conoscenza operativa", "Aggiornamento come parte del lavoro"], query="software documentation architecture API runbook", prompt="Mappa dei documenti per destinatario"))
slides.append(content_slide("Sicurezza applicativa di base", "decisioni e qualità", 58,
    ["Identità e controllo degli accessi", "Validazione degli input", "Protezione dei dati e dei segreti", "Dipendenze e supply chain", "Logging e gestione degli incidenti"], query="application security basics OWASP diagram", prompt="Security by design lungo il ciclo"))
slides.append(content_slide("Segnali di rischio in una proposta tecnica", "decisioni e qualità", 59,
    ["Benefici senza metriche", "Dipendenze e lock-in non esplicitati", "Complessità operativa sottovalutata", "Migrazione all-or-nothing", "Responsabilità e competenze non definite"], query="technology proposal red flags vendor lock in", prompt="Checklist semaforo"))
slides.append(activity_slide("Caso finale: valutare una proposta", "decisioni e qualità", 60,
    "Un fornitore propone React, microservizi Java e Python, container e Kubernetes per un nuovo servizio istituzionale.",
    ["Quali parti della proposta sono motivate?", "Quali dati e diagrammi chiediamo?", "Quali alternative confrontiamo?", "Quali rischi, responsabilità e criteri di accettazione?"], "45 min", "case study architettura React Java Python Kubernetes proposta"))
slides.append(content_slide("Checklist per il dialogo con i fornitori", "decisioni e qualità", 61,
    ["Problema, utenti e vincoli", "Architettura e responsabilità", "Qualità misurabili", "Sicurezza e conformità", "Delivery, esercizio e supporto", "Evoluzione, costi e uscita"], query="vendor technical due diligence checklist software", prompt="Checklist riutilizzabile"))
slides.append(content_slide("Messaggi da portare con sé", "chiusura", 62,
    ["Non esiste una tecnologia migliore in assoluto", "Il contesto rende una scelta adeguata o fragile", "Architettura e organizzazione si influenzano", "Qualità, sicurezza e operabilità vanno progettate", "Una buona decisione rende visibili trade-off ed evidenze"],
    "12 min", query="nessuna", prompt="Cinque principi finali"))

end = base(False)
text(end, "Domande e confronto", .8, 1.25, 8.4, .8, 35, WHITE, True)
text(end, "Quale decisione tecnologica vorreste riuscire a leggere meglio da domani?", .82, 2.7, 7.8, 1.2, 20, RGBColor(207,216,229))
rect(end, 9.72, 0, .13, 7.5, TEAL)
end_no = text(end, "89", 11.1, 5.95, 1.2, .7, 35, CORAL, True, align=PP_ALIGN.RIGHT)
end_no.name = "SLIDE_NUMBER"
notes(end, "Chiudere con una domanda applicativa e raccogliere i temi per eventuali approfondimenti.", "Nessuna.")
slides.append(end)

prs.core_properties.title = "Panoramica sui linguaggi di programmazione moderni e scelte architetturali"
prs.core_properties.subject = "Scheletro PowerPoint del percorso formativo di 16 ore"
prs.core_properties.author = "Thimoty - materiale didattico"
prs.core_properties.keywords = "linguaggi, architetture, Java, .NET, Python, React, Kubernetes"
for idx, slide in enumerate(prs.slides, 1):
    for shape in slide.shapes:
        if shape.name == "SLIDE_NUMBER" and shape.has_text_frame:
            paragraph = shape.text_frame.paragraphs[0]
            if paragraph.runs:
                paragraph.runs[0].text = f"{idx:02d}"
prs.save(PPTX_PATH)
print(PPTX_PATH)
print(f"slides={len(prs.slides)}")
