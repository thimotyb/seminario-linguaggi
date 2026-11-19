# alt
Confronto tra approccio monolitico e approccio a microservizi: nel monolite si clona l'intera applicazione su più server, nei microservizi ogni servizio si distribuisce in modo indipendente.
# descrizione
Figura in due metà separate da una linea verticale, con testi in inglese. A sinistra, "Monolithic deployment approach": un'applicazione tradizionale ("App 1", un riquadro grigio con tre quadrati colorati: rosso, giallo, verde) ha la maggior parte delle funzioni in pochi processi; si scala clonando l'intera app su più server o macchine virtuali. Sotto, tre server (icone di monitor) contengono ciascuno una copia completa dei tre quadrati. Due fumetti rossi: "Coarse-grained density of apps/services" (densità di servizi a grana grossa) e "Need to deploy the full application" (occorre distribuire l'intera applicazione). A destra, "Microservices application approach": un'applicazione a microservizi separa le funzioni in servizi più piccoli; "App 1" e "App 2" sono riquadri tratteggiati con tre esagoni colorati ciascuno; si scala distribuendo ogni servizio in modo indipendente con più istanze su server o VM. Sotto, sei server disposti in cerchio, ciascuno con un diverso insieme di esagoni (servizi di colori diversi, anche di app diverse). Due fumetti verdi: "Independent deployment of microservice" e "Fine-grained density of services" (densità di servizi a grana fine).
# testo
Monolithic deployment approach
- A traditional application has most of its functionality within a few processes that are componentized with layers and libraries.
- Scales by cloning the app on multiple servers/VMs
App 1. Fumetti: "Coarse-grained density of apps/services"; "Need to deploy the full application".
Microservices application approach
- A microservice application segregates functionality into separate smaller services.
- Scales out by deploying each service independently with multiple instances across servers/VMs.
App 1, App 2. Fumetti: "Independent deployment of microservice"; "Fine-grained density of services".
