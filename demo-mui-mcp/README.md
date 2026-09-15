# Demo MUI MCP

Laboratorio per mostrare come un assistente AI usa il server MCP ufficiale di MUI per consultare documentazione ed esempi mentre costruisce una dashboard React.

## Avvio rapido

```bash
cd /home/thimoty/git/seminario-linguaggi/demo-mui-mcp
./start-demo.sh
```

Aprire <http://127.0.0.1:5175>.

Il server di sviluppo resta attivo finché non si preme `Ctrl+C`.

## Materiale didattico

- `COPIONE-DEMO.md`: dialogo completo relatore–AI e prove da eseguire;
- `src/App.jsx`: dashboard finale interattiva;
- `src/theme.js`: tema MUI centralizzato;
- `../.codex/config.toml`: configurazione project-scoped del server MUI MCP.

## Verifica MCP

La configurazione viene caricata da Codex quando il progetto è considerato attendibile. Dopo l'installazione, riavviare Codex nella directory del repository e controllare:

```bash
codex mcp list
codex mcp get mui-mcp
```

Nel client interattivo si può usare anche `/mcp`.

## Architettura della demo

```text
Codex ──stdio──> @mui/mcp ──> documentazione ed esempi MUI
  │
  └── modifica il progetto React/Vite
                         │
                         └──> browser: http://127.0.0.1:5175
```

MUI MCP viene usato durante lo sviluppo. Non viene incluso nel bundle destinato al browser.

La consultazione della documentazione tramite `fetchDocs` richiede accesso alla rete. Lo strumento opzionale `generateReactCode` richiede inoltre una variabile `MUI_RECIPES_API_KEY`; il copione del seminario usa `fetchDocs` e non richiede questa chiave.

Riferimenti:

- [MUI MCP ufficiale](https://mui.com/material-ui/getting-started/mcp/)
- [MCP in Codex](https://developers.openai.com/codex/mcp/)
