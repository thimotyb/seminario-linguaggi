# alt
Slide del corso Java Performance: "The runtime environment", con il funzionamento dello stack di valutazione in quattro passi.
# descrizione
Screenshot di una slide in inglese del corso "Java Performance" (pagina 25). A sinistra cinque punti elenco sulla macchina a stack della JVM. A destra, in alto, una figura con quattro colonne affiancate: in ognuna c'è lo stato dello stack di valutazione e sotto l'elenco delle istruzioni "iconst_1, iconst_2, iadd" con l'istruzione corrente in grassetto. Nella prima colonna lo stack è vuoto; dopo iconst_1 contiene il valore 1; dopo iconst_2 contiene 2 sopra 1; dopo iadd contiene solo 3, la somma. In basso a destra un riquadro con due paragrafi di spiegazione.
# testo
THE RUNTIME ENVIRONMENT
- Understanding the stack machine used by the JVM is crucial to comprehend bytecode.
- Unlike hardware CPUs, the JVM does not have processor registers and instead utilizes an evaluation stack for all calculations and operations.
- The evaluation stack, also known as the operand stack, is specific to each method, and a new stack is created when a method is called.
- Additionally, the JVM has a call stack for each Java thread, which keeps track of executed methods and is used for generating stack traces in Java.
- It is important to distinguish between the per-thread call stack and the per-method evaluation stack.
Figura: quattro stati dello stack. Stack vuoto; poi 1 (dopo iconst_1); poi 2 e 1 (dopo iconst_2); poi 3 (dopo iadd). Sotto ogni stato: iconst_1, iconst_2, iadd.
Riquadro: As a method runs, it needs an area of memory to use as an evaluation stack, for computing new values. In addition, every running thread needs a call stack that records which methods are currently in flight (the stack that would be reported by a stack trace). These two stacks will interact in some cases.
Piè di pagina: June, 2023 · Java Performance · 25
