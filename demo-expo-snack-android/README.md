# Cloud Readiness Check — tutorial React Native per Expo Snack

Piccola applicazione Android per valutare una checklist cloud. La demo usa soltanto React e i componenti base di React Native: non richiede dipendenze aggiuntive.

Durata suggerita: 12–15 minuti.

## Preparazione

1. Aprire [Expo Snack](https://snack.expo.dev/).
2. Sostituire il contenuto di `App.js` con il file dello step scelto.
3. Usare l'anteprima **Android** oppure aprire il progetto con Expo Go tramite QR code, se disponibile.
4. Salvare o condividere lo Snack solo se serve conservare il risultato.

## Step 1 — Componenti nativi e stile

File: `step-01-ui/App.js`

### Cosa dire

> React Native usa componenti come `View`, `Text` e `SafeAreaView`, non elementi HTML. Gli stili sono oggetti JavaScript creati con `StyleSheet.create()`.

Da evidenziare:

- la funzione `App` restituisce una descrizione dell'interfaccia;
- le parentesi graffe permettono di inserire valori JavaScript nel markup JSX;
- `flex`, padding e colori vengono tradotti in primitive native;
- la stessa base può funzionare su Android, iOS e web.

## Step 2 — Stato e interazione touch

File: `step-02-stato/App.js`

### Cosa dire

> `useState` conserva i requisiti selezionati. Quando l'utente tocca un `Pressable`, React aggiorna lo stato e ridisegna soltanto ciò che dipende da quel valore.

Il flusso è:

```text
tap → toggleRequirement(id) → nuovo Set → re-render → UI aggiornata
```

Prova dal vivo: aggiungere un requisito all'array `requirements` e verificare che appaia automaticamente.

## Step 3 — App completa con punteggio

File: `step-03-finale/App.js`

La versione finale aggiunge:

- barra di avanzamento;
- messaggio calcolato in base al punteggio;
- pulsante di reset;
- feedback visuale e proprietà di accessibilità;
- `FlatList`, adatta a liste che possono crescere.

### Spiegazione durante il seminario

> I dati sono separati dalla vista. `FlatList` trasforma ogni requisito in una riga; lo stato contiene soltanto gli identificativi selezionati; punteggio e messaggio sono valori derivati, quindi non vengono duplicati nello stato.

Domande da fare all'aula:

1. Perché si crea un nuovo `Set` invece di modificare direttamente quello esistente?
2. Quali valori sono stato e quali sono semplicemente derivati?
3. Che differenza c'è tra un `Pressable` mobile e un pulsante HTML?
4. Dove collocheremmo una chiamata a un'API reale?

## Estensioni rapide

- assegnare un peso diverso a ogni requisito;
- salvare il risultato con `AsyncStorage`;
- aggiungere una seconda schermata con Expo Router;
- inviare il report a un backend;
- sostituire la checklist con domande provenienti da un'API.

Fonti:

- [Snack come ambiente React Native nel browser](https://docs.expo.dev/develop/tools/)
- [Componenti core di React Native](https://reactnative.dev/docs/components-and-apis)
- [Pressable](https://reactnative.dev/docs/pressable)
- [FlatList](https://reactnative.dev/docs/flatlist)

