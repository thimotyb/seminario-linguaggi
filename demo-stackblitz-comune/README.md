# Demo StackBlitz — Comune di Valleverde

Scheda dimostrativa React per un ipotetico sito comunale. Usa il [Design React Kit ufficiale](https://github.com/italia/design-react-kit), basato su Bootstrap Italia, e simula:

- una pagina informativa per un servizio anagrafico;
- la scelta del documento richiesto;
- un form accessibile;
- validazione minima lato interfaccia;
- una ricevuta con protocollo simulato.

I nomi, i recapiti e il protocollo sono fittizi. Non inserire dati personali reali.

## Apertura in StackBlitz

Metodo più semplice:

1. aprire [StackBlitz](https://stackblitz.com/);
2. creare un progetto **Vite + React**;
3. caricare o copiare tutti i file di questa cartella, mantenendo `src/`;
4. attendere `npm install` e l'avvio automatico dell'anteprima.

In alternativa, pubblicando questa cartella in un repository GitHub, si può aprire direttamente:

```text
https://stackblitz.com/github/ORGANIZZAZIONE/REPOSITORY?file=demo-stackblitz-comune/src/App.jsx
```

## Esecuzione locale

```bash
cd /home/thimoty/git/seminario-linguaggi/demo-stackblitz-comune
npm install
npm run dev
```

Aprire l'indirizzo indicato da Vite, normalmente <http://localhost:5173>.

## Copione rapido per il seminario

1. **Mostrare `package.json`**: `design-react-kit` e `bootstrap-italia` sono dipendenze distinte; il kit React non include automaticamente CSS e font.
2. **Mostrare `main.jsx`**: vengono importati Bootstrap Italia e i tre font previsti dal kit.
3. **Mostrare `App.jsx`**: i componenti `Header`, `Breadcrumb`, `Card`, `Select`, `Input`, `TextArea`, `Button` e `Alert` provengono dal Design React Kit.
4. **Cambiare il documento**: la scheda informativa viene aggiornata tramite stato React.
5. **Compilare con dati inventati**: il pulsante si abilita solo quando i campi sono completi.
6. **Inviare**: compare una ricevuta simulata, senza chiamate di rete.
7. **Ridurre l'anteprima**: mostrare l'adattamento responsive del contenuto.

## Messaggio da leggere

> Il Design React Kit traduce il design system della Pubblica Amministrazione in componenti React riutilizzabili. Non basta applicare colori istituzionali: struttura dei contenuti, etichette, navigazione, accessibilità e messaggi di esito devono essere progettati come parte del servizio.

## Estensioni possibili

- aggiungere autenticazione SPID/CIE simulata;
- dividere il form in step;
- integrare un backend di protocollo;
- aggiungere caricamento di allegati;
- applicare controlli più completi e una privacy notice reale.

Riferimenti:

- [Design React Kit](https://github.com/italia/design-react-kit)
- [Bootstrap Italia](https://italia.github.io/bootstrap-italia/)
- [Designers Italia](https://designers.italia.it/)

