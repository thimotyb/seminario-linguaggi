from pathlib import Path
from copy import deepcopy
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

PPTX=Path('output/panoramica-linguaggi-scelte-architetturali-scheletro.pptx')
NAVY=RGBColor(17,36,63); NAVY2=RGBColor(25,51,82); TEAL=RGBColor(40,167,158)
CORAL=RGBColor(240,102,84); SKY=RGBColor(83,166,214); GOLD=RGBColor(210,160,45)
WHITE=RGBColor(255,255,255); PALE=RGBColor(232,239,245); MUTED=RGBColor(91,107,126)
AWS='https://aws.amazon.com/'; AZURE='https://azure.microsoft.com/'; GCP='https://cloud.google.com/'; OCI='https://www.oracle.com/cloud/'
PSN='https://www.polostrategiconazionale.it/'; PSN_GOV='https://innovazione.gov.it/dipartimento/focus/polo-strategico-nazionale/'
TF='https://developer.hashicorp.com/terraform/intro'; REG='https://registry.terraform.io/browse/providers'
GA='https://cloud.google.com/architecture'; GBLUE='https://docs.cloud.google.com/architecture/blueprints/security-foundations'
OA='https://docs.oracle.com/en/solutions/'; OATF='https://docs.oracle.com/en-us/iaas/Content/dev/terraform/examples-templates.htm'
COMPARE='https://docs.cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison'

def box(s,x,y,w,h,fill,line=None,r=True):
 k=MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE if r else MSO_AUTO_SHAPE_TYPE.RECTANGLE
 q=s.shapes.add_shape(k,Inches(x),Inches(y),Inches(w),Inches(h)); q.fill.solid(); q.fill.fore_color.rgb=fill; q.line.color.rgb=line or fill; return q
def text(s,v,x,y,w,h,size=14,color=NAVY,bold=False,align=PP_ALIGN.LEFT):
 q=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); f=q.text_frame; f.clear(); f.word_wrap=True; f.vertical_anchor=MSO_ANCHOR.MIDDLE
 f.margin_left=f.margin_right=Inches(.04); f.margin_top=f.margin_bottom=Inches(.02); p=f.paragraphs[0]; p.alignment=align
 r=p.add_run(); r.text=v; r.font.name='Aptos'; r.font.size=Pt(size); r.font.bold=bold; r.font.color.rgb=color; return q
def button(s,label,url,x,y,w,fill=TEAL):
 q=box(s,x,y,w,.42,fill); q.click_action.hyperlink.address=url
 t=text(s,label,x+.05,y+.05,w-.1,.28,9,WHITE,True,PP_ALIGN.CENTER); t.text_frame.paragraphs[0].runs[0].hyperlink.address=url
def base(p,title,n,dark=False):
 s=p.slides.add_slide(p.slide_layouts[6]); nt=s.notes_slide.shapes._spTree
 for sh in p.slides[81].notes_slide.shapes: nt.insert_element_before(deepcopy(sh._element),'p:extLst')
 s.background.fill.solid(); s.background.fill.fore_color.rgb=NAVY if dark else RGBColor(247,249,251)
 box(s,.55,.42,.12,.12,CORAL); text(s,title,.8,.63,11.75,.72,27,WHITE if dark else NAVY,True)
 text(s,'CLOUD E INFRASTRUCTURE AS CODE',.58,7.12,8.5,.22,9,SKY if dark else MUTED,True)
 text(s,'20 min',10.92,7.08,1.35,.25,9,SKY if dark else MUTED,False,PP_ALIGN.RIGHT)
 q=text(s,f'{n:02d}',12.38,7.04,.38,.28,10,CORAL,True,PP_ALIGN.RIGHT); q.name='SLIDE_NUMBER'; return s
def notes(s,obj,sources,detail):
 f=s.notes_slide.notes_text_frame; f.clear(); f.text=f'OBIETTIVO: {obj}\nFONTI: {sources}\nNOTE: {detail}'
def source(s,v,dark=False): text(s,v,.82,6.82,11.5,.2,8,SKY if dark else MUTED)

p=Presentation(PPTX); assert len(p.slides)==91
assert next(x.text for x in p.slides[58].shapes if getattr(x,'has_text_frame',False) and x.text.strip())=='Kubernetes: dal cluster agli oggetti applicativi'

# 60
s=base(p,'Cloud: cosa cambia davvero rispetto al data center',60)
text(s,'RESPONSABILITÀ GESTITA DAL PROVIDER',.85,1.43,4.35,.25,11,CORAL,True)
layers=[('SaaS','applicazione pronta',CORAL),('PaaS','runtime + servizi gestiti',TEAL),('IaaS','compute · rete · storage',SKY),('On-prem','hardware → applicazione',NAVY2)]
for i,(h,b,c) in enumerate(layers):
 y=1.85+i*1.02; box(s,.9,y,4.18,.78,c); text(s,h,1.08,y+.12,1.05,.25,13,WHITE,True); text(s,b,2.08,y+.11,2.72,.3,12,WHITE)
text(s,'IL VALORE NON È “AVERE SERVER ALTROVE”',5.68,1.45,6.2,.25,11,TEAL,True)
items=[('ELASTICITÀ','capacità on demand'),('MANAGED SERVICES','meno componenti da operare'),('GLOBAL REACH','regioni, zone e rete'),('AUTOMAZIONE','API + IaC + policy')]
for i,(h,b) in enumerate(items):
 x=5.72+(i%2)*3.18; y=1.88+(i//2)*1.38; box(s,x,y,2.88,1.08,WHITE,PALE); text(s,h,x+.15,y+.14,2.58,.22,11,[CORAL,TEAL,SKY,GOLD][i],True,PP_ALIGN.CENTER); text(s,b,x+.15,y+.48,2.58,.3,11,NAVY,False,PP_ALIGN.CENTER)
box(s,5.72,4.72,6.06,1.02,NAVY); text(s,'Trade-off: più velocità e servizi, ma governance, costi e lock-in vanno progettati.',6.03,4.91,5.45,.5,13,WHITE,True,PP_ALIGN.CENTER)
source(s,'Sintesi didattica: modello di responsabilità condivisa e servizi cloud')
notes(s,'distinguere cloud da semplice hosting e introdurre il livello di servizio.','AWS, Microsoft Azure, Google Cloud, Oracle Cloud','Il confine di responsabilità varia per servizio: verificare sempre la matrice del provider.')

# 61
s=base(p,'Quattro cloud principali: stesso vocabolario, accenti diversi',61,True)
providers=[('AWS','ampiezza di servizi\necosistema cloud-native',AWS,CORAL),('MICROSOFT AZURE','identity, Microsoft stack\ne scenari hybrid',AZURE,SKY),('GOOGLE CLOUD','data/analytics, AI\ne Kubernetes',GCP,TEAL),('ORACLE CLOUD','Oracle Database, workload\nenterprise e multicloud',OCI,GOLD)]
for i,(h,b,u,c) in enumerate(providers):
 x=.72+(i%2)*6.05; y=1.5+(i//2)*2.15; q=box(s,x,y,5.65,1.72,NAVY2,c); q.click_action.hyperlink.address=u
 text(s,h,x+.25,y+.22,5.15,.32,16,c,True,PP_ALIGN.CENTER); t=text(s,b,x+.3,y+.7,5.05,.55,13,WHITE,False,PP_ALIGN.CENTER); t.text_frame.paragraphs[0].runs[0].hyperlink.address=u
 button(s,'SITO UFFICIALE',u,x+1.65,y+1.3,2.35,c)
text(s,'La scelta parte dal workload e dai vincoli, non dal logo.',2.0,6.03,9.3,.36,16,WHITE,True,PP_ALIGN.CENTER)
source(s,'Schede cliccabili: siti ufficiali AWS · Azure · Google Cloud · Oracle Cloud',True)
notes(s,'orientare gli studenti nei quattro ecosistemi con link diretti.',' ; '.join([AWS,AZURE,GCP,OCI]),'Gli accenti sono una sintesi didattica, non una graduatoria prestazionale.')

# 62 PSN
s=base(p,'Polo Strategico Nazionale: il cloud sovrano per la PA',62)
box(s,.8,1.46,4.18,4.65,NAVY); text(s,'PSN',1.2,1.86,3.38,.62,36,CORAL,True,PP_ALIGN.CENTER)
text(s,'Infrastruttura nazionale ad alta affidabilità per dati e servizi critici e strategici della PA.',1.2,2.72,3.38,1.02,16,WHITE,True,PP_ALIGN.CENTER)
text(s,'Non un quinto hyperscaler:\nun contesto di sovranità, sicurezza e continuità operativa.',1.18,4.18,3.42,.85,13,SKY,False,PP_ALIGN.CENTER)
button(s,'SITO PSN',PSN,1.35,5.4,1.45,CORAL); button(s,'PAGINA DTD',PSN_GOV,2.98,5.4,1.45,TEAL)
text(s,'COSA SIGNIFICA NELLA SCELTA ARCHITETTURALE',5.43,1.55,6.48,.28,11,CORAL,True)
rows=[('DATI E SERVIZI','classificazione e criticità'),('DEPLOYMENT','private cloud · hybrid cloud · CSP'),('SOVRANITÀ','territorio, controllo, chiavi e responsabilità'),('RESILIENZA','continuità operativa e tolleranza ai guasti')]
for i,(h,b) in enumerate(rows):
 y=2.0+i*.91; box(s,5.45,y,6.2,.68,WHITE,PALE); text(s,h,5.68,y+.12,1.55,.25,11,[CORAL,TEAL,SKY,GOLD][i],True); text(s,b,7.32,y+.1,4.05,.3,13,NAVY,True)
box(s,5.45,5.77,6.2,.48,PALE); text(s,'Domanda guida: quali vincoli pubblici cambiano region, servizio e modello operativo?',5.62,5.83,5.86,.28,11,NAVY,True,PP_ALIGN.CENTER)
source(s,'Fonti: Dipartimento per la trasformazione digitale · Polo Strategico Nazionale')
notes(s,'collocare PSN nel panorama cloud italiano e chiarire il concetto di cloud sovrano.',f'{PSN} ; {PSN_GOV}','PSN è presentato separatamente dagli hyperscaler: la pagina DTD descrive private/hybrid cloud e servizi che possono sfruttare tecnologie hyperscaler.')

# 63 matrix
s=base(p,'Confronto cloud: scegliere per scenario, non per slogan',63)
cols=[('CRITERIO',2.65),('AWS',2.05),('AZURE',2.05),('GOOGLE',2.05),('OCI',2.05)]; xs=[.55,3.2,5.25,7.3,9.35]
for (h,w),x,c in zip(cols,xs,[NAVY,CORAL,SKY,TEAL,GOLD]): box(s,x,1.43,w,.52,c); text(s,h,x,1.53,w,.25,10,WHITE,True,PP_ALIGN.CENTER)
matrix=[('Fit ricorrente','ecosistema ampio','Microsoft + hybrid','data · AI · K8s','Oracle workload'),('Differenziatore','maturità operativa','identity/enterprise','analytics/cloud-native','DB + multicloud'),('Verificare','complessità/costi','licenze e governance','skill e copertura','fit fuori stack Oracle'),('Prima domanda','servizi già usati?','Microsoft è centrale?','dati/AI dominano?','DB Oracle è centrale?')]
for r,row in enumerate(matrix):
 y=2.03+r*.88
 for c,(v,w) in enumerate(zip(row,[2.65,2.05,2.05,2.05,2.05])):
  box(s,xs[c],y,w,.7,WHITE,PALE,False); text(s,v,xs[c]+.08,y+.08,w-.16,.52,10,NAVY,c==0,PP_ALIGN.CENTER)
box(s,.72,5.75,11.1,.56,NAVY); text(s,'Decisione: skill disponibili · data gravity · compliance/region · servizi gestiti · TCO/egress · exit strategy',.92,5.86,10.7,.29,12,WHITE,True,PP_ALIGN.CENTER)
button(s,'MAPPA SERVIZI AWS / AZURE / GCP',COMPARE,4.55,6.39,4.25,TEAL)
source(s,'Sintesi didattica da documentazione ufficiale: validare sempre sul workload e con una prova di costo')
notes(s,'fornire una griglia comparativa utilizzabile senza proclamare un vincitore universale.',COMPARE,'La tabella è un’inferenza/sintesi editoriale. Il link Google aiuta a mappare servizi equivalenti fra AWS, Azure e GCP; OCI va verificato sul catalogo Oracle.')

# 64 IaC
s=base(p,'Infrastructure as Code: l’infrastruttura entra nel ciclo Git',64,True)
steps=[('CODICE','risorse + policy'),('PLAN','diff revisionabile'),('APPLY','API dei provider'),('STATE','drift + output')]
for i,(h,b) in enumerate(steps):
 x=.68+i*3.08; box(s,x,1.42,2.6,1.0,[CORAL,TEAL,SKY,GOLD][i]); text(s,h,x+.15,1.59,2.3,.25,13,WHITE,True,PP_ALIGN.CENTER); text(s,b,x+.15,1.94,2.3,.25,11,WHITE,False,PP_ALIGN.CENTER)
 if i<3:text(s,'→',x+2.62,1.75,.42,.28,17,WHITE,True,PP_ALIGN.CENTER)
box(s,.72,2.86,5.35,2.86,NAVY2); text(s,'main.tf',.98,3.08,1.3,.25,12,CORAL,True)
code='terraform {\n  required_providers {\n    google = { source = "hashicorp/google" }\n  }\n}\nresource "google_storage_bucket" "assets" {\n  name = "corso-assets"\n  location = "EU"\n}'
text(s,code,1.0,3.42,4.8,1.92,12,WHITE,False)
text(s,'PERCHÉ',6.48,2.93,2.25,.26,12,TEAL,True); text(s,'versioning · review · ripetibilità · ambienti coerenti',6.5,3.3,5.55,.58,14,WHITE,True)
text(s,'ATTENZIONE',6.48,4.14,2.25,.26,12,CORAL,True); text(s,'state remoto e lock · segreti fuori dal codice · versioni provider fissate · policy e test',6.5,4.48,5.55,.78,14,WHITE,True)
button(s,'TERRAFORM: INTRO',TF,7.1,5.61,2.15,TEAL); button(s,'REGISTRY PROVIDER',REG,9.47,5.61,2.15,CORAL)
source(s,'Fonte: HashiCorp Terraform documentation e Registry',True)
notes(s,'collegare IaC al flusso Git/PR/pipeline visto nella sezione DevOps.',f'{TF} ; {REG}','Spiegare che il plan è una previsione, lo state è sensibile e il drift richiede controllo; evitare credenziali nel repository.')

# 65 repositories
s=base(p,'Dai diagrammi al deployment: Architecture Center + Terraform',65)
box(s,.7,1.42,5.82,4.75,WHITE,PALE); text(s,'GOOGLE CLOUD',1.0,1.7,5.22,.32,16,TEAL,True,PP_ALIGN.CENTER)
text(s,'Cloud Architecture Center',1.03,2.25,5.16,.38,19,NAVY,True,PP_ALIGN.CENTER)
text(s,'reference architecture · design guidance\nWell-Architected · landing zone · blueprint',1.12,2.88,4.98,.8,14,NAVY,False,PP_ALIGN.CENTER)
box(s,1.2,3.99,4.82,1.0,NAVY); text(s,'Enterprise foundations blueprint\n+ repository Terraform deployable',1.38,4.17,4.46,.55,13,WHITE,True,PP_ALIGN.CENTER)
button(s,'ARCHITECTURE CENTER',GA,1.2,5.38,2.2,TEAL); button(s,'BLUEPRINT TERRAFORM',GBLUE,3.65,5.38,2.2,CORAL)
box(s,6.82,1.42,5.82,4.75,WHITE,PALE); text(s,'ORACLE CLOUD',7.12,1.7,5.22,.32,16,GOLD,True,PP_ALIGN.CENTER)
text(s,'Oracle Architecture Center',7.15,2.25,5.16,.38,19,NAVY,True,PP_ALIGN.CENTER)
text(s,'design pattern · reference architecture\nsolution playbook · deployment code',7.24,2.88,4.98,.8,14,NAVY,False,PP_ALIGN.CENTER)
box(s,7.32,3.99,4.82,1.0,NAVY); text(s,'Soluzioni con GitHub Terraform\ne “Deploy to Oracle Cloud”',7.5,4.17,4.46,.55,13,WHITE,True,PP_ALIGN.CENTER)
button(s,'ARCHITECTURE CENTER',OA,7.32,5.38,2.2,GOLD); button(s,'ESEMPI TERRAFORM',OATF,9.77,5.38,2.2,CORAL)
source(s,'Fonti ufficiali: Google Cloud Architecture Center · Oracle Architecture Center')
notes(s,'mostrare risorse che uniscono diagrammi, decisioni e codice infrastrutturale riusabile.',f'{GA} ; {GBLUE} ; {OA} ; {OATF}','Aprire un blueprint in aula e confrontare diagramma, moduli Terraform, prerequisiti e istruzioni di deploy.')

lst=p.slides._sldIdLst; ids=list(lst[-6:])
for q in ids: lst.remove(q)
for i,q in enumerate(ids): lst.insert(59+i,q)
for i,s in enumerate(p.slides,1):
 for sh in s.shapes:
  if sh.name=='SLIDE_NUMBER' and sh.has_text_frame and sh.text_frame.paragraphs[0].runs: sh.text_frame.paragraphs[0].runs[0].text=f'{i:02d}'
p.save(PPTX); print(f'patched {PPTX}: {len(p.slides)} slides, inserted 60-65')
