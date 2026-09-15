# Seminario: linguaggi moderni e scelte architetturali

Materiali didattici per un seminario dedicato ai linguaggi di programmazione moderni, ai rispettivi ecosistemi e alle decisioni architetturali che guidano la realizzazione e il rilascio del software.

Il repository raccoglie una presentazione PowerPoint editabile, le fonti visuali utilizzate, gli script di generazione e modifica delle slide e una serie di dimostrazioni interattive utilizzabili durante le lezioni.

## Presentazione

L'artefatto principale è:

- [`output/panoramica-linguaggi-scelte-architetturali-scheletro.pptx`](output/panoramica-linguaggi-scelte-architetturali-scheletro.pptx)

Il deck contiene 97 slide in formato 16:9, organizzate in quattro aree:

1. linguaggi, paradigmi e runtime;
2. ecosistemi e casi d'uso;
3. architetture moderne e delivery;
4. decisioni, qualità e sicurezza.

La mappa dettagliata degli argomenti, delle fonti e degli interventi editoriali è disponibile in [`STRUTTURA-CORSO.md`](STRUTTURA-CORSO.md).

## Demo interattive

| Cartella | Ambiente | Contenuto |
|---|---|---|
| [`demo-mdn-playground/`](demo-mdn-playground/) | MDN Playground | Applicazione HTML, CSS e JavaScript costruita progressivamente |
| [`demo-dotnet-fiddle-azure/`](demo-dotnet-fiddle-azure/) | .NET Fiddle | Console C# che modella eventi Azure Event Grid |
| [`demo-expo-snack-android/`](demo-expo-snack-android/) | Expo Snack | Piccola applicazione Android in React Native |
| [`demo-mui-mcp/`](demo-mui-mcp/) | Browser locale e Codex | Dashboard React/MUI e dialogo guidato con MUI MCP |
| [`demo-stackblitz-comune/`](demo-stackblitz-comune/) | StackBlitz | Pagina comunale costruita con Design React Kit |
| [`demo-killercoda-microservices/`](demo-killercoda-microservices/) | Killercoda | Due microservizi Kubernetes, service discovery, scaling e recovery |

Ogni cartella contiene un README specifico con i passaggi da seguire e un copione adatto alla presentazione dal vivo.

## Avvio rapido delle demo locali

Sono richiesti Node.js e npm.

### Dashboard MUI MCP

```bash
cd demo-mui-mcp
npm install
./start-demo.sh
```

Aprire quindi `http://127.0.0.1:5175`.

La configurazione MCP di progetto è in [`.codex/config.toml`](.codex/config.toml). Il percorso del comando è locale al progetto e può essere adattato se il repository viene clonato in una posizione differente.

### Pagina comunale Design React Kit

```bash
cd demo-stackblitz-comune
npm install
npm run dev
```

La stessa cartella può essere importata in StackBlitz come progetto Vite/React.

## Struttura del repository

```text
assets/       immagini e schermate tratte dalle fonti didattiche
demo-*/       laboratori e tutorial interattivi
output/       presentazione corrente e backup delle revisioni
tools/        script per modifiche mirate al deck
create_deck.py
              generatore originale della presentazione
```

Le dipendenze installate, le cache, gli artefatti di test del browser e i file temporanei non sono versionati. Le build `dist/` già presenti sono invece conservate per permettere una consultazione immediata degli esempi.

## Aggiornare la presentazione

Per gli aggiornamenti ordinari è preferibile usare gli script mirati presenti in `tools/`, mantenendo un backup della presentazione prima di ogni modifica. `create_deck.py` serve a rigenerare l'intero deck e non è necessario per le correzioni puntuali.

Prima di pubblicare una revisione è opportuno verificare:

- collegamenti e note relatore;
- leggibilità e geometria delle slide interessate;
- apertura corretta del file PowerPoint;
- funzionamento delle demo richiamate dalle slide.

## Note

Il progetto ha finalità didattiche. Le applicazioni dimostrative non raccolgono dati reali e le integrazioni con servizi cloud sono simulate o eseguite in sandbox pubbliche.
