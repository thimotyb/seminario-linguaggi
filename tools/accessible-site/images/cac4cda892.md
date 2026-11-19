# alt
Schema ArchiMate che collega progetti, servizi, processo, componente applicativo e server con relazioni "Realizes" e "Used by".
# descrizione
Diagramma in notazione ArchiMate, in inglese, organizzato in tre colonne. Colonna centrale, dall'alto in basso: "Business service" (giallo), "Business process" (giallo), "Application service" (azzurro), "Application component" (azzurro) e "Server" (verde). Le relazioni sono: il Business process realizza il Business service ("Realizes"); l'Application service è usato dal Business process ("Used by"); l'Application component realizza l'Application service; il Server realizza l'Application component. Colonna sinistra (riquadri rosa): "Business Transformation Project", che realizza il Business service, e "IT Development Project", che realizza l'Application service. Colonna destra (riquadri viola): "Business Goal", realizzato dal Business service, e "IT Goal", realizzato dall'Application service.
# testo
Business Transformation Project —Realizes→ Business service —Realizes→ Business Goal
Business process —Realizes→ Business service
Application service —Used by→ Business process
IT Development Project —Realizes→ Application service —Realizes→ IT Goal
Application component —Realizes→ Application service
Server —Realizes→ Application component
