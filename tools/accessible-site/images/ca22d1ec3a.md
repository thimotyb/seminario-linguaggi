# alt
Slide del corso Java Performance: "GC basics", con diagramma di stack e heap e riferimenti agli oggetti.
# descrizione
Screenshot di una slide in inglese del corso "Java Performance" (pagina 75). A sinistra sei punti elenco sul garbage collector. A destra un diagramma con due aree: a sinistra "Stack", una colonna di caselle di cui due colorate in azzurro; a destra "Heap", un trapezio che contiene tanti piccoli oggetti. Dalle due caselle dello stack partono frecce verso oggetti dell'heap, e da questi altre frecce portano ad altri oggetti: gli oggetti raggiungibili sono colorati in azzurro, quelli non più raggiungibili sono in grigio chiaro e sono quelli che il garbage collector può liberare. In alto a destra e in basso compaiono due indirizzi web.
# testo
GC BASICS
- The standard Java process has both a stack and a heap. The stack is where local variables are stored. Local variables that hold primitives directly store the primitive value in the stack.
- Local variables of reference type will point at a location in Java's heap, which is where the objects will actually be created.
- The primitive fields of an object are still allocated at addresses within the heap.
- As a Java program runs, new objects are created in the heap, and the relationships between the objects changes (as fields are updated).
- Eventually, the heap will run out of space for new objects to be created. However, many of the objects that have been created will no longer be needed (e.g., temporary objects that were created in one method and not passed to any other method, or returned to the caller).
- Space in the heap can therefore be reclaimed, and the program can continue to run. The mechanism by which the platform recovers and reuses heap memory that is no longer in use by application code is called garbage collection.
Diagramma: etichette "Stack" e "Heap".
Indirizzi web nell'immagine: https://drive.google.com/file/d/1Epmq574uzd_nEtXt4G8Ps4V3KtK4qjVc/view?usp=sharing e https://betterprogramming.pub/understanding-the-jvm-memory-model-heap-vs-non-heap-c14aa6fa703e
Piè di pagina: June, 2023 · Java Performance · 75
