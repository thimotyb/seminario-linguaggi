# Copione: costruire un'interfaccia con AI + MUI MCP

Obiettivo: simulare una conversazione credibile in cui l'AI consulta la documentazione ufficiale MUI tramite MCP e costruisce progressivamente una dashboard React. Durata: 15–20 minuti.

## Prima del seminario

Da `/home/thimoty/git/seminario-linguaggi`:

```bash
codex mcp list
codex mcp get mui-mcp
cd demo-mui-mcp
npm run build
```

La configurazione MCP è project-scoped. Dopo una nuova installazione o una modifica a `.codex/config.toml`, chiudere e riaprire Codex in questa cartella.

Per avviare la versione finale già pronta:

```bash
cd /home/thimoty/git/seminario-linguaggi/demo-mui-mcp
./start-demo.sh
```

Aprire nel browser locale: <http://127.0.0.1:5175>

## Apertura — spiegare che cosa succede

Da dire:

> L'AI non conosce necessariamente l'ultima API di ogni libreria. MUI MCP le permette di interrogare documentazione ed esempi ufficiali. Il server MCP fornisce conoscenza e strumenti; Vite continua a eseguire normalmente l'applicazione React.

La demo usa lo strumento MCP `fetchDocs`. L'ulteriore strumento `generateReactCode` richiede una chiave `MUI_RECIPES_API_KEY` e non è necessario per questo copione.

Nel client Codex mostrare `/mcp`, oppure nel terminale mostrare:

```bash
codex mcp list
```

## Dialogo 1 — chiedere prima le fonti

**Relatore:**

```text
Usa MUI MCP. Prima di modificare il codice, consulta la documentazione ufficiale per AppBar, Card, Chip, LinearProgress, Dialog, Snackbar e responsive styling con sx. Riassumi in cinque righe i pattern che userai e indicami quali fonti MCP hai consultato.
```

**Risposta AI attesa:**

- dichiara di avere interrogato MUI MCP;
- identifica i componenti appropriati;
- spiega `sx` e breakpoint responsive;
- non modifica ancora il progetto.

Messaggio didattico:

> Separiamo ricerca e implementazione. Possiamo verificare che la proposta derivi dalle API correnti e non da memoria generica.

## Dialogo 2 — creare lo scheletro

**Relatore:**

```text
Ora crea in questa cartella una dashboard React con Material UI. Deve avere AppBar, selettore ambiente, titolo, quattro metriche e una lista di servizi. Usa soltanto componenti e proprietà verificati tramite MUI MCP. Mantieni i dati locali e non aggiungere un backend.
```

**Risposta AI attesa:**

- crea o aggiorna `src/App.jsx`;
- usa componenti MUI al posto di ricostruirli con HTML grezzo;
- mantiene una struttura responsive;
- suggerisce `npm run dev`.

Nel browser mostrare il primo risultato e ridurre la finestra per verificare il layout.

## Dialogo 3 — aggiungere interazione

**Relatore:**

```text
Rendi la dashboard interattiva: lo switch deve sospendere il monitoraggio, “Aggiungi servizio” deve aprire un Dialog, il salvataggio deve aggiungere una riga e mostrare uno Snackbar. Consulta di nuovo MUI MCP per le proprietà di accessibilità e per il corretto pattern di chiusura del Dialog.
```

**Risposta AI attesa:**

- introduce stato React locale;
- collega `open` e `onClose` al dialogo;
- aggiunge etichette accessibili agli icon button e agli switch;
- mostra conferma tramite Snackbar.

Prova dal vivo:

1. disattivare `Payment Worker`;
2. aggiungere `Reporting API`;
3. chiudere lo Snackbar;
4. cambiare ambiente da Produzione a Collaudo.

## Dialogo 4 — chiedere una revisione

**Relatore:**

```text
Esegui una revisione finale usando MUI MCP: controlla componenti deprecati, responsive design, accessibilità di controlli e colori, poi esegui la build. Correggi solo problemi dimostrabili e riassumi le verifiche effettuate.
```

**Risposta AI attesa:**

- consulta la documentazione prima delle correzioni;
- distingue errori reali da preferenze stilistiche;
- esegue `npm run build`;
- comunica chiaramente eventuali limiti della verifica.

## Chiusura

Da dire:

> MCP non scrive magicamente una buona interfaccia: fornisce all'AI fonti e strumenti affidabili. Prompt espliciti, verifica nel browser e build restano parte del lavoro dello sviluppatore.

## Piano B senza rete

Il server `@mui/mcp` e tutte le dipendenze sono installati localmente. Se la rete non è disponibile durante il seminario:

1. mostrare `codex mcp list`;
2. usare il copione come dialogo simulato;
3. avviare la versione finale con `./start-demo.sh`;
4. spiegare che il risultato è stato costruito applicando le API recuperate via MCP.
