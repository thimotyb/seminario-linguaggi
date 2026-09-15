# Microservizi con kubectl su Killercoda

Demo guidata per mostrare due microservizi che interagiscono dentro Kubernetes:

```text
orders Pod ──HTTP──> catalog Service ──> catalog Pod(s)
```

`catalog` espone una semplice risposta HTTP. `orders` la richiama ogni cinque secondi e scrive il risultato nei log. Non servono codice sorgente, registry privati o credenziali.

Durata suggerita: 15–20 minuti.

## Preparazione

1. Aprire [Killercoda Kubernetes](https://killercoda.com/kubernetes).
2. Avviare un playground Kubernetes.
3. Attendere che il terminale sia pronto.
4. Verificare il cluster:

```bash
kubectl cluster-info
kubectl get nodes
```

### Cosa dire

> `kubectl` non esegue direttamente i container: invia dichiarazioni e comandi al Kubernetes API Server. I controller lavorano per portare lo stato reale verso quello desiderato.

## Step 1 — Creare uno spazio isolato

```bash
kubectl create namespace seminario
kubectl config set-context --current --namespace=seminario
kubectl get namespaces
```

### Cosa dire

> Il namespace separa logicamente le risorse della demo. Non è una macchina o un cluster distinto, ma uno scope per nomi, configurazioni e policy.

## Step 2 — Avviare il microservizio catalog

Creare un `Deployment` con una piccola immagine HTTP:

```bash
kubectl create deployment catalog \
  --image=hashicorp/http-echo:1.0.0 \
  -- -listen=:5678 '-text={"service":"catalog","status":"ok","items":3}'
```

Esporlo con un `Service` stabile:

```bash
kubectl expose deployment catalog \
  --name=catalog \
  --port=80 \
  --target-port=5678
```

Controllare le risorse:

```bash
kubectl get deployments,pods,services
kubectl rollout status deployment/catalog
```

### Cosa dire

> Il Pod può essere sostituito e cambiare indirizzo. Il Service mantiene invece un nome DNS stabile: `catalog`. I consumer non devono conoscere l'IP del singolo Pod.

## Step 3 — Provare catalog da un client temporaneo

```bash
kubectl run client \
  --image=busybox:1.36 \
  --restart=Never \
  --rm -i \
  -- wget -qO- http://catalog
```

Output atteso:

```json
{"service":"catalog","status":"ok","items":3}
```

Mostrare il DNS e gli endpoint:

```bash
kubectl run dns-check \
  --image=busybox:1.36 \
  --restart=Never \
  --rm -i \
  -- nslookup catalog

kubectl get service catalog
kubectl get endpointslices -l kubernetes.io/service-name=catalog
```

## Step 4 — Avviare il microservizio orders

`orders` chiama `catalog` ogni cinque secondi:

```bash
kubectl create deployment orders \
  --image=busybox:1.36 \
  -- /bin/sh -c 'while true; do echo "$(date +%FT%T%z) orders -> catalog"; wget -qO- http://catalog; echo; sleep 5; done'
```

Attendere l'avvio e seguire i log:

```bash
kubectl rollout status deployment/orders
kubectl logs deployment/orders --follow
```

Interrompere la visualizzazione con `Ctrl+C`; il Pod continua a funzionare.

### Cosa dire

> Qui osserviamo una vera chiamata HTTP fra due workload. `orders` conosce soltanto il contratto e il nome del Service. Kubernetes risolve il nome e instrada la richiesta verso un endpoint disponibile.

## Step 5 — Scalare catalog

```bash
kubectl scale deployment catalog --replicas=3
kubectl rollout status deployment/catalog
kubectl get pods -l app=catalog -o wide
kubectl get endpointslices -l kubernetes.io/service-name=catalog
```

### Cosa dire

> Cambia il numero di Pod, ma non cambia l'indirizzo usato da `orders`. Il Service distribuisce le connessioni fra gli endpoint pronti.

Per rendere visibile il bilanciamento bisognerebbe far restituire a ogni replica il proprio hostname; questa immagine restituisce intenzionalmente una risposta identica, così il contratto resta stabile.

## Step 6 — Simulare un guasto e osservare il consumer

Portare temporaneamente `catalog` a zero repliche:

```bash
kubectl scale deployment catalog --replicas=0
kubectl get pods
kubectl logs deployment/orders --tail=12
```

Nei log di `orders` compariranno errori di connessione perché il Service esiste, ma non ha endpoint disponibili.

Ripristinare il servizio:

```bash
kubectl scale deployment catalog --replicas=2
kubectl rollout status deployment/catalog
kubectl logs deployment/orders --tail=12
```

### Cosa dire

> Kubernetes ripristina lo stato desiderato del provider, ma non rende automaticamente resiliente il consumer. Timeout, retry, circuit breaker e idempotenza restano responsabilità dell'architettura applicativa.

## Step 7 — Ispezionare lo stato dichiarato

```bash
kubectl get deployment catalog -o yaml
kubectl describe service catalog
kubectl get all
```

Domande per l'aula:

1. Che cosa accade se cancelliamo manualmente un Pod di `catalog`?
2. Perché `orders` usa `catalog` invece dell'indirizzo IP?
3. Lo scaling risolve anche i problemi di consistenza dei dati?
4. Dove configureremmo timeout, retry e osservabilità?

Prova facoltativa:

```bash
kubectl delete pod -l app=catalog
kubectl get pods --watch
```

Interrompere con `Ctrl+C` quando i nuovi Pod risultano `Running`.

## Pulizia finale

Il comando seguente elimina tutte le risorse create nella demo:

```bash
kubectl delete namespace seminario
kubectl config set-context --current --namespace=default
```

## Copione ultrarapido da 5 minuti

```bash
kubectl create namespace seminario
kubectl config set-context --current --namespace=seminario
kubectl create deployment catalog --image=hashicorp/http-echo:1.0.0 -- -listen=:5678 '-text={"service":"catalog","status":"ok","items":3}'
kubectl expose deployment catalog --name=catalog --port=80 --target-port=5678
kubectl create deployment orders --image=busybox:1.36 -- /bin/sh -c 'while true; do echo "$(date +%FT%T%z) orders -> catalog"; wget -qO- http://catalog; echo; sleep 5; done'
kubectl rollout status deployment/catalog
kubectl rollout status deployment/orders
kubectl logs deployment/orders --tail=10
kubectl scale deployment catalog --replicas=3
kubectl get pods,services,endpointslices
```

Fonti:

- [Kubernetes Learning Environment](https://kubernetes.io/docs/setup/learning-environment/)
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Killercoda Kubernetes](https://killercoda.com/kubernetes)
