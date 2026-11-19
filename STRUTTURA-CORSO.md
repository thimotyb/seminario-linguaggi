# Struttura del corso e mappa delle fonti

## Artefatto principale

- `output/panoramica-linguaggi-scelte-architetturali-scheletro.pptx`
- 97 slide, formato 16:9, organizzate in quattro mezze giornate.
- Le note relatore di ogni slide contengono lo scopo didattico, una query suggerita per Google Drive e il lavoro editoriale ancora da svolgere.

## Articolazione

1. Linguaggi, paradigmi e runtime
   - evoluzione dei paradigmi;
   - compilazione, interpretazione e runtime;
   - tipizzazione, ecosistemi e trend.
2. Ecosistemi e casi d'uso
   - Java e .NET;
   - API REST;
   - Python;
   - JavaScript, React e SPA.
3. Architetture moderne e delivery
   - monolite e microservizi;
   - API management;
   - container e Kubernetes;
   - CI/CD e osservabilità.
4. Decisioni, qualità e casi
   - criteri e matrici di valutazione;
   - manutenibilità, testabilità e documentazione;
   - sicurezza applicativa;
   - valutazione di proposte e caso finale.

## Convenzioni editoriali

- Le slide chiare sono dedicate ai contenuti; quelle scure segnano sezioni e attività.
- I precedenti riquadri `VISUAL / ESEMPIO` sono stati sostituiti con diagrammi vettoriali editabili e coerenti con il contenuto di ciascuna slide.
- I contenuti recuperati da Drive devono essere registrati qui con: slide, file sorgente, pagina o sezione, tipo di riuso e adattamenti eseguiti.
- Non considerare una figura acquisita finché non è stata aperta e verificata visivamente.

## Laboratori dimostrativi

- `demo-mdn-playground/`: Runtime Explorer in HTML, CSS e JavaScript, organizzato in quattro step copiabili in MDN Playground, con versione finale locale.
- `demo-dotnet-fiddle-azure/`: console C# che modella ed elabora eventi di deployment con l'SDK Azure Event Grid, in tre step per .NET Fiddle.
- `demo-expo-snack-android/`: applicazione React Native Cloud Readiness Check, in tre step copiabili in Expo Snack e utilizzabili nell'anteprima Android.
- `demo-mui-mcp/`: dashboard React/Material UI avviabile in locale, server MUI MCP installato a livello di progetto e copione relatore-AI per una dimostrazione guidata.
- `demo-stackblitz-comune/`: pagina comunale dimostrativa per informazione e richiesta documenti, costruita con Design React Kit e pronta per un progetto Vite/React su StackBlitz.
- `demo-killercoda-microservices/`: laboratorio `kubectl` su Killercoda con due microservizi, service discovery, scaling, guasto controllato e ripristino.

## Registro fonti Drive

| Slide | Argomento | File Drive | Pagina/sezione | Elemento riusato | Stato |
|---:|---|---|---|---|---|
| 8-9 | Compilatore, interprete, runtime | Da cercare | | Figura | Da reperire |
| 9-10 | Paradigmi object-oriented e funzionale | Wikipedia; Microsoft Learn; MDN Web Docs | definizioni OOP/FP; tutorial Inheritance; `Array.prototype.map()` | Diagrammi editabili, codice e link ai tutorial | Integrato |
| 18-23 | Java, JVM, bytecode, GC, VisualVM e supporto LTS | `java-performance-course_v1.pdf`; Oracle Java SE Support Roadmap | pp. 7-13, 23-25, 74-85, 99, 111-113; roadmap delle release | Figure JVM/bytecode, memoria, G1, schermate VisualVM e link alla roadmap LTS | Integrato |
| 24-26 | .NET e confronto Java/.NET | Microsoft Learn, Introduzione a .NET e Common web application architectures; .NET Fiddle | componenti .NET; CLR/CIL; deployment Azure App Service; playground browser | Diagramma runtime editabile + figura architetturale Azure + link eseguibile | Integrato |
| 27 | REST API | Google Doc `ARCHITETTURE MICROSERVIZI CON DOCKER; SPRING BOOT; KAFKA` + `Microservices-Architectures_v3.pdf` | sezione API; p. 45 | Metodi, risorse, status code + figura | Integrato |
| 28-34 | Python, Pandas, visualizzazione, ML e AI generativa | Google Doc `Python Basic`; Google Slides `Practical Machine Learning`; gallery ufficiale Seaborn | sezioni Pandas/DataFrame; slide 29, 80, 158, 166; gallery 0.13.2 | Codice, notebook Colab, alberi e visualizzazioni | Integrato |
| 35-37 | JavaScript, Console e compatibilità browser | MDN JavaScript Guide; MDN Developer Tools; Can I Use | browser runtime, DOM/eventi, Console e support tables | Codice, screenshot e link live | Integrato |
| 38-46 | React, React Native, MUI e Design React Kit | React Quick Start; React Native; Expo Snack; MUI; Linee guida PA §6.3; Design React Kit | componenti, props/state, componenti mobili nativi, demo live, MUI MCP, Web Kit e laboratorio | Diagrammi, screenshot, codice e link StackBlitz/Snack | Integrato |
| 51 | Monolite e microservizi | `Microservices-Architectures_v3.pdf` | pp. 18, 30-31, 36, 38 | Testo comparativo + immagine Stonehenge | Integrato |
| 52 | Benefici e prerequisiti dei microservizi | `Microservices-Architectures_v3.pdf` | pp. 36, 38 | Benefici, condizioni e costi | Integrato |
| 53 | Confini dei servizi | `Microservices-Architectures_v3.pdf` | pp. 28-29, 33 | DDD, bounded context e livelli API | Integrato |
| 54 | Contratto API | Google Doc `ARCHITETTURE MICROSERVIZI CON DOCKER; SPRING BOOT; KAFKA` + `Microservices-Architectures_v3.pdf` | sezione API; p. 46 | Quattro ingredienti + figura request mapping | Integrato |
| 55 | API Gateway e policy | `Microservices-Architectures_v3.pdf` | pp. 64-65, 78 | Gateway, routing, policy e OAuth | Integrato |
| 56-59 | Container e Kubernetes | Google Doc `DOCKER-KUBERNETES 20240219`; Kubernetes Learning Environment; Killercoda | sezioni DOCKER, Orchestratore, Architettura interna/logica; playground online | Testo + diagrammi ridisegnati + link alla sandbox | Integrato |
| 60-65 | Cloud, PSN e Infrastructure as Code | Siti ufficiali AWS, Azure, Google Cloud, Oracle Cloud; DTD e PSN; HashiCorp; Google e Oracle Architecture Center | panoramiche provider; Polo Strategico Nazionale; Terraform Registry; blueprint e soluzioni | Confronto per scenario, cloud sovrano, flusso IaC, codice e link cliccabili | Integrato |
| 66-77 | DevOps, Git, CI/CD, testing e dashboard | `GUIDA OPERATIVA S21: AZURE DEVOPS`; progetto Azure DevOps `TitanoPortal` | §§2-11; Figure 1, 5, 8, 25-30, 31-43; work item aggiornati di recente | Team, ticket, board, PR, pipeline, flussi di test, cruscotti, release e link alla demo ADO | Integrato |
| 78 | Osservabilità | Da cercare | | Segnali operativi | Da reperire |
| 82-88 | Qualità, testabilità, documentazione e sicurezza | Da cercare | | Figure + checklist | Da reperire |
| 89-92 | Linee guida AgID e threat modeling | `lineeguidasicurezza-introduzione.pdf`; Microsoft Security Development Lifecycle | pp. 4-9; Threat Modeling Tool overview e getting started | Quattro assi AgID, Secure SDLC, processo, DFD, STRIDE e schermate del tool | Integrato |

## Fonte iniziale

- `04 - Panoramica sui Linguaggi di Programmazione Moderni e Scelte Architetturali_INPS.pdf`
- Il programma originale salta dal punto 3 al punto 5. Nel deck i casi e la valutazione delle alternative sono trattati come blocco decisionale, mantenendo separata la qualità del software.

## Fonti integrate

- Google Drive `Microservices-Architectures_v3.pdf`, file ID `1ayOkjDoMCIMr_sAUX1SV37SB0b1J40PL`.
- Google Doc `ARCHITETTURE MICROSERVIZI CON DOCKER; SPRING BOOT; KAFKA`, documento ID `1LcvVhX9P38E0f50wpURlyx2vs_9-CQsp0M0xfqRvw0w`.
- Google Doc `DOCKER-KUBERNETES 20240219`, documento ID `1D3QGSvZ1lK7-r_L5dWRH17BZWPgfJn0VzD_f3MMpGEQ`.
- Kubernetes Learning Environment e sandbox Killercoda: `https://kubernetes.io/docs/setup/learning-environment/` e `https://killercoda.com/kubernetes`.
- Documento Word Drive `GUIDA OPERATIVA S21: AZURE DEVOPS`, file ID `15uH8Rj1DAwjOc2ZmIZEimiqA7XthsLYM`.
- Progetto Azure DevOps `TitanoPortal`, vista dei work item aggiornati di recente: `https://thimoty.visualstudio.com/TitanoPortal/_workitems/recentlyupdated/`.
- PDF Drive `java-performance-course_v1.pdf`, file ID `1KOq4T9NVsarwD4DMNQzYzuYcTOc_ZdJ5`.
- Oracle Java SE Support Roadmap, riferimento aggiornato per release LTS e finestre di supporto: `https://www.oracle.com/java/technologies/java-se-support-roadmap.html`.
- TIOBE Programming Community Index, indicatore mensile di popolarità dei linguaggi da leggere come segnale di ecosistema e non come misura assoluta di qualità: `https://www.tiobe.com/tiobe-index/`.
- Google Slides `Practical Machine Learning`, presentazione ID `1_XzbegydeSEKW7hHcS27Fw9_Rjp9NZQHpviZ4icBS_s`.
- Google Doc `Python Basic`, documento ID `1ujryBtFvmoq9OapeV3vnDpvkuqjFAJzodAWzorFobQk`.
- Seaborn 0.13.2 Example Gallery: `https://seaborn.pydata.org/examples/index.html`.
- React Quick Start: `https://react.dev/learn`.
- React Native Introduction e Core Components: `https://reactnative.dev/docs/getting-started` e `https://reactnative.dev/docs/intro-react-native-components`.
- Demo React Native modificabile in Expo Snack: `https://snack.expo.dev/?description=Example+usage&hideQueryParams=true&name=Fetch+Example&platform=web`.
- Material UI overview, component demos e MCP: `https://mui.com/material-ui/`.
- Linee guida di design per i servizi web della PA, §6.3, e repository `italia/design-react-kit`.
- Template didattico ufficiale Design React Kit su StackBlitz: `https://stackblitz.com/edit/vitejs-vite-yy8bnk?file=src/App.tsx`.
- MDN JavaScript Guide, Developer Tools e Playground: `https://developer.mozilla.org/`.
- Can I Use, tabella di compatibilità CSS Grid: `https://caniuse.com/css-grid`.
- Wikipedia, definizioni di programmazione object-oriented e funzionale: `https://en.wikipedia.org/wiki/Object-oriented_programming` e `https://en.wikipedia.org/wiki/Functional_programming`.
- Microsoft Learn, tutorial completo `Shape` con classi concrete, area, perimetro e dispatch dinamico: `https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/tutorials/inheritance`.
- MDN Web Docs, esempio interattivo di trasformazione con `Array.prototype.map()`: `https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map`.
- Microsoft Learn, introduzione italiana a .NET e architetture ASP.NET Core su Azure: `https://learn.microsoft.com/it-it/dotnet/core/introduction` e `https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures`.
- .NET Fiddle, playground online per scrivere, compilare, eseguire e condividere rapidamente codice C#, F# e VB.NET: `https://dotnetfiddle.net/`.
- Google Drive `lineeguidasicurezza-introduzione.pdf`, file ID `1vK_ellHCkkFT6jE_KqAr3Kk4SaeWwz23` (AgID, 21 novembre 2017).
- Pubblicazione ufficiale AgID del 03/07/2024: `https://www.agid.gov.it/sites/agid/files/2024-07/Linee-guida_di_sicurezza_sviluppo-applicazioni.pdf`.
- Pagina ufficiale delle Linee Guida AgID: `https://www.agid.gov.it/it/linee-guida`.
- Allegato 4 AgID, modellazione delle minacce e mitigazioni Secure/Privacy by Design: `https://www.agid.gov.it/sites/default/files/repository_files/allegato_4_-_linee_guida_per_la_modellazione_delle_minacce-dlt.pdf`.
- Microsoft Security Development Lifecycle, Threat Modeling Tool e guida introduttiva: `https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling`, `https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool` e `https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-getting-started`.
- Cloud provider: `https://aws.amazon.com/`, `https://azure.microsoft.com/`, `https://cloud.google.com/` e `https://www.oracle.com/cloud/`.
- Polo Strategico Nazionale e pagina istituzionale DTD: `https://www.polostrategiconazionale.it/` e `https://innovazione.gov.it/dipartimento/focus/polo-strategico-nazionale/`.
- Terraform, provider Registry e confronto servizi: `https://developer.hashicorp.com/terraform/intro`, `https://registry.terraform.io/browse/providers` e `https://docs.cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison`.
- Google Cloud Architecture Center ed Enterprise foundations blueprint: `https://cloud.google.com/architecture` e `https://docs.cloud.google.com/architecture/blueprints/security-foundations`.
- Oracle Architecture Center ed esempi Terraform: `https://docs.oracle.com/en/solutions/` e `https://docs.oracle.com/en-us/iaas/Content/dev/terraform/examples-templates.htm`.
- Le figure estratte dal PDF sono conservate in `assets/source-microservices/`; le slide mantengono l'indicazione della pagina sorgente nelle note relatore.
- Le schermate estratte dalla guida S21 sono conservate in `assets/source-devops/`; le slide 46-57 ne mantengono provenienza e contesto nelle note relatore.
- Le figure Java e Python sono conservate in `assets/source-java/` e `assets/source-python/`; i notebook Colab sono collegati direttamente dai pulsanti nelle slide.
