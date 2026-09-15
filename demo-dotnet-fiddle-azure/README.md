# Azure Event Grid Console Demo — tutorial per .NET Fiddle

Questa demo mostra una piccola console C# che crea ed elabora eventi di deployment destinati ad Azure Event Grid. Non invia dati nel cloud: usa localmente i tipi dell'SDK ufficiale, quindi funziona senza account Azure, endpoint o credenziali.

Durata suggerita: 12–15 minuti.

## Preparazione di .NET Fiddle

1. Aprire [.NET Fiddle](https://dotnetfiddle.net/).
2. Selezionare **C#**, progetto **Console** e compilatore **Latest (.NET 10)**.
3. Per gli step 2 e 3, aprire **NuGet Packages**, cercare `Azure.Messaging.EventGrid` e aggiungere l'ultima versione stabile disponibile.
4. Sostituire tutto il codice dell'editor con il contenuto del file `Program.cs` dello step.
5. Premere **Run**.

Se l'interfaccia propone una versione .NET più recente, va bene usare **Latest**. Lo step 1 non richiede pacchetti NuGet.

## Step 1 — Modellare un evento con un record C#

File: `step-01-record/Program.cs`

### Cosa dire

> Un `record` rappresenta bene un messaggio immutabile. Il compilatore genera costruttore, proprietà, uguaglianza per valore e una rappresentazione testuale utile per il debugging.

Il programma crea due eventi applicativi e usa:

- una collezione tipizzata;
- interpolazione di stringhe;
- una property calcolata;
- pattern matching su una tupla per determinare l'azione operativa.

Prova dal vivo: cambiare `Successful: false` in `true` per l'evento di produzione e rilanciare.

## Step 2 — Usare il tipo ufficiale di Azure Event Grid

File: `step-02-event-grid/Program.cs`

Prima di eseguire, aggiungere il pacchetto NuGet `Azure.Messaging.EventGrid`.

### Cosa dire

> Qui il modello applicativo viene inserito nell'envelope standard di Event Grid. L'SDK gestisce subject, tipo evento, versione e serializzazione del payload.

Da evidenziare:

- `EventGridEvent` proviene dall'SDK Azure ufficiale per .NET;
- `Subject` identifica la risorsa logica;
- `EventType` permette il routing e la selezione del gestore;
- `Data` è un `BinaryData`, adatto a trasportare JSON senza legare il consumer a una stringa grezza.

## Step 3 — Elaborare un batch e decidere l'azione

File: `step-03-finale/Program.cs`

### Cosa dire

> Il consumer deserializza il payload nel record C#, applica regole tramite pattern matching e calcola un piccolo riepilogo con LINQ. In una Azure Function, la stessa logica potrebbe essere invocata dal trigger Event Grid.

Prove dal vivo:

1. cambiare l'ambiente `staging` in `production`;
2. aggiungere un quarto evento alla lista;
3. introdurre un nuovo caso nello `switch`;
4. modificare la soglia che produce `CHECK PERFORMANCE`.

Output atteso, in forma equivalente:

```text
✅ billing-api 2.4.0 [production] -> RELEASE COMPLETED
❌ catalog-api 3.1.0 [production] -> START ROLLBACK
✅ portal 8.0.2 [staging] -> CHECK PERFORMANCE

Summary: 2/3 successful - average duration 84s
```

## Perché C# è una scelta particolarmente naturale qui

C# non è l'unico linguaggio utilizzabile con Azure: esistono SDK Azure anche per Java, Python e JavaScript. In un'organizzazione già centrata su Microsoft, C# può però ridurre l'attrito perché offre:

- SDK Azure di prima parte con modelli fortemente tipizzati;
- integrazione diretta con ASP.NET Core, Azure Functions, Microsoft Entra ID e Managed Identity;
- un unico ecosistema fra sviluppo applicativo, tooling .NET, diagnostica e deployment Azure;
- costrutti come record, pattern matching, LINQ e `async`/`await`, adatti a consumer di eventi e servizi cloud.

La decisione è quindi contestuale: **integrazione e competenze esistenti**, non una superiorità assoluta su Java.

## Passaggio al cloud reale

Per pubblicare davvero servirebbero endpoint e autenticazione. In produzione è preferibile usare Microsoft Entra ID o Managed Identity invece di inserire chiavi nel codice. Non incollare mai credenziali reali in un playground pubblico.

Fonti:

- [SDK Azure Event Grid per .NET](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/messaging.eventgrid-readme?view=azure-dotnet)
- [Classe EventGridEvent](https://learn.microsoft.com/en-us/dotnet/api/azure.messaging.eventgrid.eventgridevent?view=azure-dotnet)
- [Autenticazione tramite Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/event-grid/authenticate-with-microsoft-entra-id)

