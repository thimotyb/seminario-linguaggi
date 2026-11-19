# alt
Schermata di Kiali, il grafico del traffico tra microservizi nel namespace travel-agency, con servizi collegati da frecce e tempi di risposta.
# descrizione
Screenshot parziale (tagliato in basso) di Kiali, la console di osservabilità per Istio. In alto una barra di controllo: namespace "travel-agency", vista "Traffic", tipo "App graph", intervallo "Last 1m", pulsanti Pause e aggiorna, "Graph tour". Al centro il grafo: ogni servizio è un riquadro con un triangolo (workload) e un quadrato (servizio): "flights", "insurances", "mysqldb", "discounts", più "voyages (travel-portal)" in basso a sinistra. Le frecce mostrano il traffico: verdi se le richieste vanno a buon fine, rosse se ci sono errori (una freccia rossa parte da "voyages"), con etichette del tempo di risposta (20 ms, 23 ms, 35 ms, 6 ms). A destra un pannello con l'applicazione "travels" e la tabella delle richieste HTTP al secondo: In 0,80 totali, 86,25% successi, 13,75% errori; Out 1,71 totali, 93,57% successi, 6,43% errori; sotto due barre orizzontali quasi interamente verdi con una piccola parte rossa.
# testo
Namespace: travel-agency · Traffic · App graph · Last 1m · Pause · Display · Find… · Hide… · Graph tour
Oct 11, 01:39:03 PM … 01:40:03 PM
Nodi: flights (1 host), flights, insurances, mysqldb, discounts, voyages (travel-portal). Tempi: 20ms, 23ms, 35ms, 6ms.
Pannello: A travels · health · S travels
HTTP (requests per second): Total / %Success / %Error — In 0.80 / 86.25 / 13.75; Out 1.71 / 93.57 / 6.43
Legenda: OK, 3xx, 4xx, 5xx, NR
