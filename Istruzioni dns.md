## Architettura di Risoluzione dei Nomi: Il Sistema DNS

Il DNS (Domain Name System, sistema dei nomi di dominio) funziona come un registro decentralizzato che traduce un nome di dominio testuale, o FQDN (Fully Qualified Domain Name, nome di dominio completamente qualificato), in un indirizzo IP (Internet Protocol, protocollo internet) numerico binario, necessario per l'instradamento dei pacchetti di dati nella rete globale.

Quando un utente digita `tecnitaliagroup.it`, il browser non sa dove inviare la richiesta HTTP (Hypertext Transfer Protocol, protocollo di trasferimento ipertestuale). Interroga quindi una catena di server DNS (Risolutore Locale, Root Nameserver, TLD Nameserver e infine il Nameserver Autorevole di OVH) per ottenere l'IP del server di destinazione.

---

## Mappatura e Configurazione dei Record nella Zona DNS di OVH

La Zona DNS è il file di configurazione ospitato su OVH che contiene i puntamenti specifici del dominio. Per far funzionare un sito web su un'infrastruttura moderna e ridondata (come GitHub Pages), si utilizzano due tipi di record fondamentali:

### 1. Record A (Address)
Il record A associa direttamente un nome di dominio a un indirizzo IPv4 (Internet Protocol version 4) statico a 32 bit. 
Nel caso di GitHub Pages, l'architettura richiede **quattro record A distanti** puntati sul dominio di secondo livello (`tecnitaliagroup.it` senza www).

| Tipo Record | Host / Sottodominio | Destinazione / Target | Funzione Tecnica |
| :--- | :--- | :--- | :--- |
| **A** | *Vuoto* (o `@`) | `185.199.108.153` | Instradamento primario e bilanciamento del carico |
| **A** | *Vuoto* (o `@`) | `185.199.109.153` | Tolleranza ai guasti (Failover) 1 |
| **A** | *Vuoto* (o `@`) | `185.199.110.153` | Tolleranza ai guasti (Failover) 2 |
| **A** | *Vuoto* (o `@`) | `185.199.111.153` | Tolleranza ai guasti (Failover) 3 |

### 2. Record CNAME (Canonical Name)
Il record CNAME crea un alias, associando un nome di sottodominio a un altro nome di dominio (e non a un IP). Si applica per gestire il traffico del terzo livello (`www.tecnitaliagroup.it`).

```text
Sottodominio: www
Tipo: CNAME
Target: [tuo-username].github.io.
```

> **Nota di Rigore Tecnico:** Su OVH, quando si inserisce il target di un CNAME esterno, è necessario inserire un punto finale (`.`) dopo `.io` se richiesto dall'interfaccia, per evitare che il sistema concateni automaticamente il nome del dominio nativo generando l'errore `username.github.io.tecnitaliagroup.it`.

---

## Meccanismo di Propagazione e Parametro TTL

Ogni modifica eseguita sul pannello OVH non è istantanea a livello mondiale. Questo fenomeno è regolato dal **TTL (Time To Live, tempo di vita)**, un valore espresso in secondi che indica per quanto tempo i server DNS intermedi (es. quelli di Telecom, Vodafone, Google) possono memorizzare in cache le vecchie informazioni prima di interrogare nuovamente OVH.

*   Se il TTL è impostato a 86400 secondi, i provider mondiali aggiorneranno il puntamento del sito solo dopo 24 ore.
*   **Approccio di ottimizzazione:** Prima di modificare i record A, è consigliabile abbassare il TTL della zona DNS a 3600 secondi (1 ora) o meno, se consentito dal piano OVH. Questo velocizza la transizione al nuovo sito riducendo il tempo di inattività (*downtime*).

---

## Flusso Operativo di Gestione (Interazione OVH - GitHub Pages)

L'architettura Jamstack (JavaScript, APIs, and Markup) scelta per il sito scinde la gestione logica da quella infrastrutturale:

```
[Utente] ---> Digita URL ---> [DNS OVH] (Risolve IP) ---> [Server Cloud GitHub] (Invia file HTML statici)
```

1.  **Richiesta iniziale:** L'utente richiede la pagina web.
2.  **Risoluzione:** I DNS di OVH rispondono comunicando uno dei 4 IP di GitHub.
3.  **Negoziazione TLS/SSL:** GitHub Pages intercetta la richiesta, verifica la corrispondenza del dominio nelle impostazioni della repository, genera automaticamente un certificato crittografico SSL (Secure Sockets Layer) / TLS (Transport Layer Security) tramite l'ente *Let's Encrypt* e avvia la sessione sicura HTTPS.
4.  **Consegna asset:** I file statici (HTML, CSS, JSON) vengono distribuiti istantaneamente tramite la rete di distribuzione dei contenuti (CDN, Content Delivery Network) di GitHub, garantendo tempi di caricamento ridotti.

---

## Strumenti di Diagnostica e Verifica della Configurazione

Per convalidare l'infrastruttura senza l'interferenza della cache locale del browser, si devono utilizzare strumenti di analisi di rete via terminale o CLI (Command Line Interface):

### Test dei record A tramite comando 'dig' (Sistemi Unix/macOS)
```bash
dig tecnitaliagroup.it +short
```
*Risultato atteso: l'elenco esatto dei 4 indirizzi IP di GitHub.*

### Test dei record A tramite comando 'nslookup' (Sistemi Windows)
```cmd
nslookup tecnitaliagroup.it
```

### Strumenti Web di Ottimizzazione
*   **WhatsMyDNS.net:** Consente di monitorare la propagazione globale del record A e CNAME su oltre 50 server dislocati in vari continenti in tempo reale.
*   **Pannello di Controllo GitHub:** Nella sezione *Settings > Pages* della repository, inserire il dominio e cliccare su *Check DNS*. Lo strumento effettua un test di coerenza automatizzato prima di abilitare l'HTTPS obbligatorio.

---
*Le informazioni fornite e i flussi di configurazione DNS descritti sono validati e conformi alle specifiche degli standard Internet RFC 1034 / RFC 1035 (Domain Names - Concepts and Facilities / Implementation and Specification) e alla documentazione tecnica ufficiale di OVHcloud e GitHub Enterprise.*