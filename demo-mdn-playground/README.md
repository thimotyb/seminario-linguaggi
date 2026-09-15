# Runtime Explorer — tutorial per MDN Playground

Demo interattiva per mostrare, durante il seminario, la separazione fra:

- **HTML**: struttura e significato dei contenuti;
- **CSS**: presentazione e layout responsive;
- **JavaScript**: stato, eventi e aggiornamento del DOM.

Aprire [MDN Playground](https://developer.mozilla.org/en-US/play), quindi usare i tre pannelli **HTML**, **CSS** e **JavaScript**. A ogni step, copiare il file indicato nel pannello omonimo e conservare il contenuto già inserito negli altri pannelli, salvo quando viene richiesto di sostituirli tutti.

Durata suggerita: 15–20 minuti.

## Step 1 — Costruire la struttura HTML

Cartella: `step-01-html/`

1. Copiare `html.html` nel pannello **HTML**.
2. Lasciare vuoti i pannelli CSS e JavaScript.
3. Osservare che la pagina è già leggibile e semanticamente organizzata, ma non è ancora presentata come un'applicazione.

### Spiegazione durante il seminario

> HTML descrive che cosa sono gli elementi: titolo, controlli, stato e schede. Le classi servono come punti di aggancio per CSS e JavaScript; gli attributi `data-runtime` trasportano piccoli dati associati agli elementi.

Da evidenziare:

- `main`, `header`, `section` e `article` esprimono una struttura semantica;
- i pulsanti sono veri elementi `button`, quindi utilizzabili anche da tastiera;
- `aria-live="polite"` permetterà agli screen reader di annunciare il risultato del filtro;
- i pulsanti non funzionano ancora: HTML non contiene la logica applicativa.

## Step 2 — Aggiungere il CSS

Cartella: `step-02-css/`

1. Conservare l'HTML dello step precedente.
2. Copiare `css.css` nel pannello **CSS**.
3. Ridimensionare il pannello di anteprima per mostrare la griglia responsive.

### Spiegazione durante il seminario

> Il CSS cambia la rappresentazione, non il significato. Le custom properties raccolgono i colori del tema; Grid dispone le schede; le media query adattano i controlli agli schermi piccoli.

Da provare dal vivo:

- cambiare `--accent` da `#2563eb` a `#7c3aed`;
- modificare `minmax(220px, 1fr)` e osservare la griglia;
- disattivare temporaneamente una regola dagli strumenti di sviluppo.

## Step 3 — Rendere attivi i filtri

Cartella: `step-03-javascript/`

1. Conservare HTML e CSS degli step precedenti.
2. Copiare `js.js` nel pannello **JavaScript**.
3. Premere i pulsanti **Tutti**, **JVM**, **.NET**, **Browser** e **Python**.

### Spiegazione durante il seminario

> JavaScript ascolta un evento, legge lo stato scelto, confronta i dati e aggiorna il DOM. Lo stesso algoritmo viene applicato a tutte le schede con `forEach`.

Il flusso da raccontare è:

```text
click → filtro selezionato → confronto con data-runtime → mostra/nascondi → aggiorna stato
```

Da evidenziare:

- `querySelectorAll()` recupera gruppi di elementi;
- `addEventListener()` collega comportamento e interfaccia;
- `dataset.runtime` legge l'attributo `data-runtime`;
- la proprietà `hidden` comunica sia al browser sia alle tecnologie assistive che una scheda non è visibile;
- `aria-pressed` rende esplicito quale filtro è attivo.

## Step 4 — Ricerca e tema: versione completa

Cartella: `step-04-finale/`

Sostituire tutti e tre i pannelli con i file dello step finale. Ora si può:

- combinare filtro per runtime e ricerca testuale;
- azzerare la ricerca con **Reset**;
- cambiare tema mantenendo il filtro corrente;
- vedere il numero di tecnologie visibili aggiornarsi in tempo reale.

### Spiegazione durante il seminario

> Ora l'interfaccia ha più sorgenti di stato: runtime, testo cercato e tema. La funzione `render()` è l'unico punto che traduce lo stato nella vista. Questo piccolo esempio anticipa il principio delle UI dichiarative usato da framework come React.

Domande da fare all'aula:

1. Quale parte cambiereste per aggiungere una nuova tecnologia?
2. Perché il filtro e la ricerca vengono combinati con `&&`?
3. Che differenza c'è tra nascondere un elemento via CSS e impostare `hidden`?
4. Quando avrebbe senso passare da JavaScript diretto a un framework?

## Esecuzione locale

La cartella `finale-locale/` contiene la stessa demo con file separati. Aprire `index.html` nel browser; non serve un server né una fase di build.

## Messaggio conclusivo

> Il browser integra tre linguaggi con responsabilità diverse. HTML costruisce il documento, CSS ne controlla la presentazione e JavaScript reagisce agli eventi modificando lo stato e il DOM. Il playground rende immediato osservare questa collaborazione.

Fonti utili:

- [MDN Playground](https://developer.mozilla.org/en-US/play)
- [Introduzione ufficiale a MDN Playground](https://developer.mozilla.org/en-US/blog/introducing-the-mdn-playground/)
- [Introduzione agli eventi](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Events)
- [Uso degli attributi data](https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Solve_HTML_problems/Use_data_attributes)
