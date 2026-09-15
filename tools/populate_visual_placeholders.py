from pathlib import Path
from math import cos, sin, pi

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

PPTX = Path("output/panoramica-linguaggi-scelte-architetturali-scheletro.pptx")
NAVY = RGBColor(17, 36, 63); NAVY2 = RGBColor(25, 51, 82)
TEAL = RGBColor(40, 167, 158); CORAL = RGBColor(240, 102, 84)
SKY = RGBColor(83, 166, 214); WHITE = RGBColor(255, 255, 255)
PALE = RGBColor(232, 239, 245); MUTED = RGBColor(91, 107, 126)
GOLD = RGBColor(210, 160, 45); RED = RGBColor(201, 73, 64); GREEN = RGBColor(67, 151, 105)
X, Y, W, H = 8.52, 1.94, 3.78, 4.18


def box(s, x, y, w, h, fill=PALE, line=None, radius=True):
    kind = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE if radius else MSO_AUTO_SHAPE_TYPE.RECTANGLE
    sh = s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = line or fill
    return sh


def txt(s, value, x, y, w, h, size=10, color=NAVY, bold=False, align=PP_ALIGN.CENTER, font="Aptos"):
    sh = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = sh.text_frame; tf.clear(); tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(.02); tf.margin_top = tf.margin_bottom = Inches(.01)
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = value; r.font.name = font; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color
    return sh


def arrow(s, x, y, horizontal=False, color=CORAL):
    txt(s, "→" if horizontal else "↓", x, y, .34, .25, 14, color, True)


def title(s, value):
    txt(s, value, X+.08, Y+.02, W-.16, .27, 10, CORAL, True)


def pills(s, items, start_y=2.45, colors=(NAVY2, TEAL, SKY, CORAL)):
    for i, item in enumerate(items):
        y = start_y + i*.72
        box(s, X+.27, y, W-.54, .5, colors[i % len(colors)])
        txt(s, item, X+.4, y+.07, W-.8, .3, 10, WHITE, True)
        if i < len(items)-1: arrow(s, X+W/2-.17, y+.49)


def timeline(s):
    title(s, "16 ORE · 4 TAPPE")
    items=[("1","PARADIGMI"),("2","ECOSISTEMI"),("3","DELIVERY"),("4","DECISIONI")]
    for i,(n,label) in enumerate(items):
        y=2.48+i*.78
        box(s,X+.2,y,.55,.55,[CORAL,TEAL,SKY,NAVY2][i])
        txt(s,n,X+.31,y+.12,.33,.26,13,WHITE,True)
        txt(s,label,X+.92,y+.08,2.35,.35,11,NAVY,True,PP_ALIGN.LEFT)
        if i<3: box(s,X+.45,y+.55,.06,.23,PALE,PALE,False)
    txt(s,"comprendere → confrontare → scegliere",X+.25,5.65,W-.5,.28,9,TEAL,True)


def language_stack(s):
    title(s,"TRE LIVELLI, TRE RESPONSABILITÀ")
    items=[("LINGUAGGIO","sintassi · semantica",CORAL),("RUNTIME","esegue · gestisce memoria",TEAL),("FRAMEWORK","struttura · librerie",NAVY2)]
    for i,(a,b,c) in enumerate(items):
        y=2.55+i*1.0; box(s,X+.25,y,W-.5,.72,c)
        txt(s,a,X+.42,y+.09,1.16,.24,11,WHITE,True)
        txt(s,b,X+1.55,y+.08,1.95,.38,9,WHITE,False,PP_ALIGN.LEFT)
        if i<2: arrow(s,X+W/2-.17,y+.73)
    txt(s,"Es.: C#  |  .NET  |  ASP.NET Core",X+.3,5.72,W-.6,.28,9,MUTED,True)


def execution_pipeline(s):
    title(s,"DAL TESTO AL PROCESSO")
    pills(s,["CODICE SORGENTE","COMPILER / INTERPRETE","RUNTIME + LIBRERIE","OS + INFRASTRUTTURA"],2.38)
    txt(s,"ogni livello introduce decisioni e vincoli",X+.28,5.68,W-.56,.3,9,MUTED,True)


def typing(s):
    title(s,"QUANDO ARRIVA IL FEEDBACK?")
    box(s,X+.18,2.48,1.58,2.75,PALE,TEAL); box(s,X+2.02,2.48,1.58,2.75,PALE,CORAL)
    txt(s,"STATICO",X+.35,2.68,1.25,.27,11,TEAL,True)
    txt(s,"codice\n↓\ncontrollo\n↓\nesecuzione",X+.39,3.13,1.16,1.55,11,NAVY,True)
    txt(s,"DINAMICO",X+2.18,2.68,1.25,.27,11,CORAL,True)
    txt(s,"codice\n↓\nesecuzione\n↓\ncontrollo",X+2.22,3.13,1.16,1.55,11,NAVY,True)
    txt(s,"trade-off: anticipo ↔ flessibilità",X+.25,5.63,W-.5,.3,9,MUTED,True)


def ecosystem(s):
    title(s,"LA SINTASSI È SOLO LA PUNTA")
    box(s,X+1.22,2.38,1.35,.55,CORAL)
    txt(s,"SINTASSI",X+1.34,2.5,1.11,.25,11,WHITE,True)
    widths=[2.0,2.55,3.15,3.55]; labels=["LIBRERIE","TOOLING + IDE","COMMUNITY + SKILL","SUPPORTO + GOVERNANCE"]
    for i,(w,l) in enumerate(zip(widths,labels)):
        y=3.15+i*.62; x=X+(W-w)/2; box(s,x,y,w,.43,[SKY,TEAL,NAVY2,MUTED][i])
        txt(s,l,x+.08,y+.07,w-.16,.26,9,WHITE,True)


def trends(s):
    title(s,"I TREND SI RAFFORZANO A VICENDA")
    cx,cy=X+W/2,3.95
    box(s,cx-.6,cy-.37,1.2,.74,CORAL); txt(s,"DELIVERY\nRAPIDO",cx-.5,cy-.26,1,.43,10,WHITE,True)
    nodes=[("API-FIRST",-pi/2), ("CLOUD",-pi/6),("CONTAINER",pi/6),("DEVOPS",pi/2),("AI",5*pi/6),("MICROSERVIZI",7*pi/6)]
    for i,(lab,a) in enumerate(nodes):
        x=cx+1.25*cos(a)-.58; y=cy+1.25*sin(a)-.28
        box(s,x,y,1.16,.55,TEAL if i%2 else NAVY2)
        txt(s,lab,x+.05,y+.07,1.06,.35,8,WHITE,True)


def comparison_grid(s):
    title(s,"STESSI CRITERI, TECNOLOGIE DIVERSE")
    cols=["JAVA",".NET","PY","JS"]
    rows=["runtime","ecosistema","fit","rischi"]
    ox,oy=X+.16,2.5; cw=.78; rh=.59
    for j,c in enumerate(cols):
        box(s,ox+.72+j*cw,oy,cw-.04,.43,NAVY2); txt(s,c,ox+.74+j*cw,oy+.07,cw-.08,.25,8,WHITE,True)
    for i,r in enumerate(rows):
        txt(s,r,ox,oy+.51+i*rh,.68,.3,8,MUTED,True,PP_ALIGN.RIGHT)
        for j in range(4):
            box(s,ox+.72+j*cw,oy+.49+i*rh,cw-.04,.45,[PALE,SKY,TEAL,CORAL][(i+j)%4],PALE)
            txt(s,"●",ox+.92+j*cw,oy+.57+i*rh,.3,.22,10,NAVY if (i+j)%4==0 else WHITE,True)
    txt(s,"pesi + evidenze → scelta motivata",X+.25,5.62,W-.5,.3,9,TEAL,True)


def dotnet_backend(s):
    title(s,"BACKEND .NET: FLUSSO TIPICO")
    boxes=[("CLIENT","web · mobile"),("ASP.NET CORE","API · auth"),("SERVIZI","business logic"),("DATI / CLOUD","SQL · Azure")]
    for i,(a,b) in enumerate(boxes):
        y=2.4+i*.79; box(s,X+.35,y,W-.7,.58,[NAVY2,TEAL,SKY,CORAL][i])
        txt(s,a,X+.5,y+.07,1.35,.25,10,WHITE,True)
        txt(s,b,X+1.75,y+.07,1.55,.3,9,WHITE,False,PP_ALIGN.LEFT)
        if i<3: arrow(s,X+W/2-.17,y+.58)
    txt(s,"DI · logging · config · observability",X+.27,5.68,W-.54,.28,9,MUTED,True)


def decision_chain(s):
    title(s,"UNA DECISIONE PROPAGA CONSEGUENZE")
    pills(s,["DRIVER + VINCOLI","DECISIONE","STRUTTURA","ATTRIBUTI DI QUALITÀ"],2.42,(CORAL,TEAL,NAVY2,SKY))
    txt(s,"misurare i trade-off, non nasconderli",X+.28,5.68,W-.56,.28,9,MUTED,True)


def observability(s):
    title(s,"TRE SEGNALI, UNA STORIA")
    cx,cy=X+W/2,3.55
    for lab,x,y,c in [("LOG",X+.35,2.55,NAVY2),("METRICHE",X+2.3,2.55,TEAL),("TRACE",X+1.33,4.25,CORAL)]:
        box(s,x,y,1.15,.75,c); txt(s,lab,x+.08,y+.2,.99,.28,10,WHITE,True)
    txt(s,"↘",X+1.55,3.18,.4,.35,18,SKY,True); txt(s,"↙",X+2.05,3.18,.4,.35,18,SKY,True)
    box(s,X+1.23,3.43,1.35,.61,PALE,TEAL); txt(s,"CONTESTO",X+1.33,3.59,1.15,.25,10,NAVY,True)
    txt(s,"alert → diagnosi → azione",X+.3,5.57,W-.6,.3,10,TEAL,True)


def funnel(s):
    title(s,"DALLA DOMANDA ALLA SHORTLIST")
    levels=[(3.25,"ESIGENZE",CORAL),(2.75,"VINCOLI",GOLD),(2.25,"CRITERI",TEAL),(1.7,"OPZIONI",NAVY2)]
    for i,(w,l,c) in enumerate(levels):
        x=X+(W-w)/2; y=2.48+i*.74; box(s,x,y,w,.52,c)
        txt(s,l,x+.08,y+.1,w-.16,.28,10,WHITE,True)
        if i<3: arrow(s,X+W/2-.17,y+.52)
    txt(s,"1 decisione + assunzioni esplicite",X+.25,5.65,W-.5,.28,9,MUTED,True)


def quality_wheel(s):
    title(s,"LA QUALITÀ È MULTIDIMENSIONALE")
    cx,cy=X+W/2,4.05
    box(s,cx-.55,cy-.38,1.1,.76,NAVY2); txt(s,"FIT\nFOR PURPOSE",cx-.46,cy-.27,.92,.45,9,WHITE,True)
    labs=["AFFIDABILITÀ","PRESTAZIONI","SICUREZZA","MANUTENIBILITÀ","INTEROPERABILITÀ","USABILITÀ"]
    for i,lab in enumerate(labs):
        a=-pi/2+i*2*pi/6; x=cx+1.33*cos(a)-.62; y=cy+1.33*sin(a)-.28
        box(s,x,y,1.24,.55,[TEAL,SKY,CORAL,GOLD,NAVY2,MUTED][i]); txt(s,lab,x+.04,y+.08,1.16,.34,7,WHITE,True)


def matrix(s):
    title(s,"ESEMPIO DI SCORE PESATO")
    cols=["PESO","A","B"]
    rows=[("Sicurezza","30%","5","4"),("Costo","20%","3","5"),("Skill","25%","4","3"),("Time","25%","4","2")]
    ox,oy=X+.2,2.48; widths=[1.45,.64,.64,.64]
    for j,c in enumerate(cols):
        x=ox+1.5+sum(widths[1:j+1]); box(s,x,oy,widths[j+1]-.04,.43,NAVY2); txt(s,c,x,y=oy+.07,w=widths[j+1]-.04,h=.25,size=8,color=WHITE,bold=True)
    for i,row in enumerate(rows):
        y=oy+.5+i*.55; txt(s,row[0],ox,y,1.38,.28,8,NAVY,True,PP_ALIGN.LEFT)
        for j,val in enumerate(row[1:]):
            x=ox+1.5+sum(widths[1:j+1]); box(s,x,y-.04,widths[j+1]-.04,.39,PALE if j==0 else (TEAL if int(val)>=4 else GOLD),PALE)
            txt(s,val,x,y+.03,widths[j+1]-.04,.22,8,NAVY if j==0 else WHITE,True)
    txt(s,"totale:  A 4,15   |   B 3,35",X+.32,5.35,W-.64,.36,11,TEAL,True)


def adr(s):
    title(s,"ADR-007 · DATABASE DEL SERVIZIO")
    box(s,X+.28,2.43,W-.56,3.13,WHITE,TEAL)
    entries=[("STATO","Accettata"),("CONTESTO","letture elevate, team SQL"),("DECISIONE","PostgreSQL gestito"),("ALTERNATIVE","SQL Server · NoSQL"),("CONSEGUENZE","skill + lock-in moderato")]
    for i,(a,b) in enumerate(entries):
        y=2.63+i*.54; txt(s,a,X+.46,y,.94,.25,8,CORAL,True,PP_ALIGN.LEFT); txt(s,b,X+1.42,y,2.43,.3,9,NAVY,False,PP_ALIGN.LEFT)
        if i<4: box(s,X+.45,y+.38,3.0,.012,PALE,PALE,False)
    txt(s,"data · owner · evidenze · link",X+.42,5.7,W-.84,.24,9,MUTED,True)


def maintainability(s):
    title(s,"COSTO DI UNA MODIFICA")
    box(s,X+.2,2.48,1.55,2.85,PALE,RED); box(s,X+2.03,2.48,1.55,2.85,PALE,GREEN)
    txt(s,"PRIMA",X+.38,2.69,1.18,.25,11,RED,True)
    txt(s,"duplicazione\n↓\n5 file\n↓\nregressioni",X+.39,3.1,1.16,1.55,11,NAVY,True)
    txt(s,"DOPO",X+2.2,2.69,1.18,.25,11,GREEN,True)
    txt(s,"responsabilità\n↓\n1 modulo\n↓\ntest rapido",X+2.22,3.1,1.16,1.55,11,NAVY,True)
    txt(s,"tempo di cambiamento ↓",X+.3,5.62,W-.6,.3,10,TEAL,True)


def test_pyramid(s):
    title(s,"PORTAFOGLIO DEI TEST")
    levels=[(1.35,"E2E · pochi",CORAL),(2.25,"INTEGRAZIONE",SKY),(3.25,"UNIT · molti",TEAL)]
    for i,(w,l,c) in enumerate(levels):
        x=X+(W-w)/2; y=2.5+i*.88; box(s,x,y,w,.67,c)
        txt(s,l,x+.06,y+.16,w-.12,.3,10,WHITE,True)
    txt(s,"veloci ↑                 fiducia ↑",X+.26,5.5,W-.52,.28,9,MUTED,True)
    txt(s,"feedback continuo nella pipeline",X+.26,5.79,W-.52,.25,9,TEAL,True)


def documentation_map(s):
    title(s,"DOCUMENTO GIUSTO, DESTINATARIO GIUSTO")
    center=(X+1.35,3.62)
    box(s,center[0]-.55,center[1]-.38,1.1,.76,NAVY2); txt(s,"SISTEMA",center[0]-.45,center[1]-.22,.9,.3,10,WHITE,True)
    data=[("API","DEV",X+.18,2.35,TEAL),("ADR","ARCH",X+2.37,2.35,CORAL),("RUNBOOK","OPS",X+.18,4.72,SKY),("GUIDA","UTENTE",X+2.37,4.72,GOLD)]
    for a,b,x,y,c in data:
        box(s,x,y,1.2,.73,c); txt(s,a,x+.08,y+.1,1.04,.24,10,WHITE,True); txt(s,b,x+.08,y+.4,1.04,.2,8,WHITE)
    txt(s,"↘",X+1.44,2.96,.34,.3,15,MUTED,True); txt(s,"↙",X+2.05,2.96,.34,.3,15,MUTED,True)
    txt(s,"↗",X+1.44,4.36,.34,.3,15,MUTED,True); txt(s,"↖",X+2.05,4.36,.34,.3,15,MUTED,True)


def security_cycle(s):
    title(s,"SECURITY BY DESIGN · OGNI FASE")
    labs=[("THREAT\nMODEL",CORAL),("DESIGN",GOLD),("CODE",TEAL),("TEST",SKY),("DEPLOY",NAVY2),("MONITOR",MUTED)]
    cx,cy=X+W/2,4.02
    for i,(lab,c) in enumerate(labs):
        a=-pi/2+i*2*pi/6; x=cx+1.28*cos(a)-.56; y=cy+1.28*sin(a)-.32
        box(s,x,y,1.12,.64,c); txt(s,lab,x+.05,y+.1,1.02,.4,8,WHITE,True)
    box(s,cx-.48,cy-.35,.96,.7,PALE,TEAL); txt(s,"RISCHIO\n↓",cx-.4,cy-.24,.8,.38,9,NAVY,True)


def traffic_light(s):
    title(s,"CHECKLIST SEMAFORO")
    items=[("VERDE","evidenze + metriche",GREEN),("GIALLO","assunzioni da validare",GOLD),("ROSSO","rischio senza owner",RED)]
    for i,(a,b,c) in enumerate(items):
        y=2.55+i*.95; box(s,X+.28,y,.63,.63,c); txt(s,"●",X+.42,y+.12,.35,.3,15,WHITE,True)
        txt(s,a,X+1.08,y+.02,.86,.25,10,c,True,PP_ALIGN.LEFT); txt(s,b,X+1.08,y+.3,2.24,.3,9,NAVY,False,PP_ALIGN.LEFT)
    txt(s,"se è rosso: fermarsi e chiedere evidenze",X+.3,5.55,W-.6,.42,9,MUTED,True)


def checklist(s):
    title(s,"6 DOMANDE PRIMA DI DIRE SÌ")
    labs=["Problema chiaro?","Owner definiti?","Qualità misurabile?","Sicurezza provata?","Esercizio sostenibile?","Uscita possibile?"]
    for i,lab in enumerate(labs):
        x=X+.2+(i%2)*1.84; y=2.48+(i//2)*1.0
        box(s,x,y,1.68,.76,PALE,TEAL)
        txt(s,"✓",x+.1,y+.18,.3,.3,14,TEAL,True); txt(s,lab,x+.42,y+.11,1.12,.45,9,NAVY,True,PP_ALIGN.LEFT)
    txt(s,"risposta + evidenza + responsabile",X+.27,5.64,W-.54,.3,9,CORAL,True)


def principles(s):
    title(s,"CINQUE PRINCIPI DA RIUSARE")
    labs=[("1","CONTESTO"),("2","TRADE-OFF"),("3","EVIDENZE"),("4","OPERABILITÀ"),("5","EVOLUZIONE")]
    for i,(n,lab) in enumerate(labs):
        y=2.4+i*.68; box(s,X+.28,y,.48,.48,[CORAL,TEAL,SKY,GOLD,NAVY2][i]); txt(s,n,X+.39,y+.1,.26,.24,11,WHITE,True)
        txt(s,lab,X+.92,y+.07,2.43,.3,10,NAVY,True,PP_ALIGN.LEFT)
    txt(s,"una buona scelta resta spiegabile nel tempo",X+.24,5.75,W-.48,.28,9,MUTED,True)


DRAWERS = {
    "Il percorso in quattro mezze giornate": timeline,
    "Che cos'è un linguaggio di programmazione?": language_stack,
    "Dal codice al sistema in esecuzione": execution_pipeline,
    "Tipi statici e dinamici": typing,
    "Ecosistema, tooling e comunità": ecosystem,
    "I trend che cambiano le scelte": trends,
    "Una griglia comune per il confronto": comparison_grid,
    ".NET nei sistemi applicativi": dotnet_backend,
    "Architettura: decisioni e trade-off": decision_chain,
    "Osservabilità e gestione operativa": observability,
    "Dalle esigenze ai criteri di scelta": funnel,
    "Attributi di qualità": quality_wheel,
    "Matrice di valutazione delle alternative": matrix,
    "Decision record: rendere la scelta leggibile": adr,
    "Codice manutenibile": maintainability,
    "Testabilità": test_pyramid,
    "Documentazione che accompagna il sistema": documentation_map,
    "Sicurezza applicativa di base": security_cycle,
    "Segnali di rischio in una proposta tecnica": traffic_light,
    "Checklist per il dialogo con i fornitori": checklist,
    "Messaggi da portare con sé": principles,
}


prs = Presentation(PPTX)
assert len(prs.slides) == 87
patched=[]
for idx, slide in enumerate(prs.slides, 1):
    text_shapes=[sh for sh in slide.shapes if getattr(sh,"has_text_frame",False) and sh.text.strip()]
    if not text_shapes: continue
    title_text=text_shapes[0].text.strip()
    placeholders=[sh for sh in text_shapes if "VISUAL / ESEMPIO" in sh.text.upper() or "DA REPERIRE SU DRIVE" in sh.text.upper()]
    example=[sh for sh in text_shapes if sh.left > Inches(8.3) and 2.4 < sh.top/Inches(1) < 4.4 and sh not in placeholders]
    if not placeholders: continue
    assert title_text in DRAWERS, f"Nessun visual definito per: {title_text}"
    for sh in placeholders + example:
        slide.shapes._spTree.remove(sh._element)
    DRAWERS[title_text](slide)
    notes=slide.notes_slide.notes_text_frame
    notes.text = notes.text.rstrip() + "\nVISUAL: diagramma vettoriale editabile inserito al posto del placeholder."
    patched.append(idx)

assert len(patched) == 21, patched
prs.save(PPTX)
print("patched visual slides:", ", ".join(map(str, patched)))
