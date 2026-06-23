<p align="center">
  <img src="https://readme-design-kit.vercel.app/api/banners/gradient?title=Tecnitalia%20Group&subtitle=Ingegneria%20%26%20Ambiente%20%7C%20Jamstack%20Architecture&theme=cyberpunk" alt="Tecnitalia Group Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Stage-Production%20Ready-4CAF50?style=flat-square&logo=github" alt="Status">
  <img src="https://img.shields.io/badge/Architecture-Jamstack%20%2F%20Decoupled-0078D4?style=flat-square" alt="Architecture">
  <img src="https://img.shields.io/badge/UI--Engine-Vanilla%20JS%20%28ES6%2B%29-F7DF1E?style=flat-square&logo=javascript" alt="Engine">
  <img src="https://img.shields.io/badge/Animations-GSAP%20%2B%20Lenis-61DAFB?style=flat-square" alt="Animations">
</p>

---

## 🧭 Navigazione Rapida
* [Core Concept](#-core-concept) • [Caratteristiche Principali](#-caratteristiche-principali-features) • [Tech Stack Matrix](#%EF%B8%8F-tech-stack-matrix) • [Architettura File System](#-architettura-file-system) • [Analisi del Core Engine](#-analisi-del-core-engine-mainjs) • [Modelli Dati (JSON Database)](#-modelli-dati-json-database) • [Setup Locale](#-setup-locale-e-sviluppo) • [Configurazione EmailJS](#-configurazione-del-form-di-contatto-emailjs)

---

## ⚡ Core Concept

Il portale di **Tecnitalia Group** è un'applicazione web ad alte prestazioni ingegnerizzata secondo i paradigmi del **Modern Jamstack**. Il sistema adotta un modello di rendering disaccoppiato (*decoupled UI*): la struttura scheletrica è immutabile e statica, mentre le aree ad alto aggiornamento (News e Progetti) vengono idratate asincronamente a runtime manipolando direttamente il DOM tramite pipeline JavaScript natie. 

> [!TIP]
> Questo approccio azzera la necessità di un database relazionale (SQL) sul server, annullando i costi di hosting, massimizzando la sicurezza contro attacchi informatici e garantendo un punteggio di *Core Web Vitals* vicino al 100%.

---

## 🚀 Caratteristiche Principali (Features)

- **Architettura a Componenti Modulari:** L'intestazione (`header.html`) e il piè di pagina (`footer.html`) sono file isolati e indipendenti, iniettati dinamicamente nel DOM per garantire il principio DRY (*Don't Repeat Yourself*).
- **Data-Driven UI (JSON Database):** Le sezioni "News" e "Progetti" non sono scritte a mano nell'HTML. Vengono popolate dinamicamente leggendo array di oggetti da file JSON (`.json`), agendo come un database statico locale.
- **Pipeline Asincrona Parallela:** Sfrutta `Promise.all` per caricare contemporaneamente layout e dati, minimizzando i tempi di caricamento strutturale (Time to Interactive).
- **Routing Dinamico per News:** Il sistema legge i parametri URL query (`?id=...`) tramite `URLSearchParams` per generare dinamicamente le pagine di dettaglio del singolo articolo (`news-singola.html`) da un unico file matrice.
- **Sistema di Filtraggio Avanzato:** I progetti possono essere filtrati in tempo reale sul client in base ai tag di competenza senza ricaricare la pagina.
- **Ordinamento Automatico:** I progetti vengono riordinati programmaticamente lato client dal più recente al più vecchio basandosi sull'anno di completamento (`endYear`).
- **Esperienza Visiva Premium:**
  - *Fluid Scrolling:* Integrazione con *Lenis Smooth Scroll* per uno scorrimento morbido e cinematico.
  - *Scroll-Driven Animations:* Animazioni fluide guidate dallo scorrimento tramite *GSAP* e *ScrollTrigger*.
  - *Modal Gallery Slider:* Finestra modale interattiva per i dettagli dei progetti, dotata di slider interno per scorrere le immagini e blocco temporaneo dello smooth-scroll sullo sfondo (`lenis.stop() / lenis.start()`) per ottimizzare la UX.
- **Integrazione SMTP Client-Side:** Modulo di contato integrato nativamente con l'SDK di **EmailJS** per l'invio di email direttamente dal client tramite API, completo di gestioni di caricamento (*loading state*) e validazione dei feedback visivi (successo/errore).

---

## 🛠️ Tech Stack Matrix

| Tecnologia / Libreria | Ambito di Applicazione | Impatto sulla UX / Performance |
| :--- | :--- | :--- |
| **HTML5 & CSS3** | Struttura & Design System | Layout responsivo fluido basato su CSS Custom Properties (Variabili). |
| **Vanilla ES6+** | Core Logic & Routing | Idratazione dati asincrona parallela tramite `Promise.all` senza framework pesanti. |
| **GSAP & ScrollTrigger** | Motion Design | Animazioni guidate dallo scorrimento riallineate dinamicamente al caricamento dati. |
| **Lenis Scroll** | Smooth Layout Interaction | Scorrimento cinematico fluido e controllo degli eventi inerziali. |
| **EmailJS Browser SDK** | Serverless SMTP Tunneling | Invio form client-side con crittografia asimmetrica delle chiavi di sicurezza. |
| **JSON Schema** | Flat-File Database | Strutturazione dei contenuti in array di oggetti indicizzati e facilmente scalabili. |

---

## 📁 Architettura File System

Il codice segue una suddivisione rigorosa e modulare per separare la logica computazionale dagli asset statici e dai file strutturali:

```text
├── assets/                  # Risorse statiche multimediali
│   └── img/                 # Immagini del team, background ed elementi grafici
├── css/
│   └── style.css            # Foglio di stile globale (Layout, Variabili e Responsive)
├── data/                    # I "Database" JSON del sito
│   ├── news.json            # Archivio dati degli articoli e aggiornamenti
│   └── projects.json        # Archivio dati di tutti i progetti eseguiti
├── js/
│   └── main.js              # Controller logico globale del sito (Core Engine)
├── archivio-news.html       # Pagina contenente l'elenco completo degli articoli
├── chi-siamo.html           # Pagina della storia e della vision aziendale
├── dettaglio-ingegneria.html# Pagina di approfondimento divisione Ingegneria
├── dettaglio-servizi.html   # Pagina di approfondimento divisione Servizi / Laboratorio
├── elenco-progetti.html     # Portfolio completo dei progetti con filtri interattivi
├── footer.html              # Componente parziale del Piè di pagina (Senza HEAD/BODY)
├── header.html              # Componente parziale della Barra di Navigazione (Senza HEAD/BODY)
├── index.html               # Landing page principale (Home Page)
├── news-singola.html        # Template matrice per il dettaglio del singolo articolo
└── README.md                # Questo file di documentazione
```

---

## 🧠 Analisi del Core Engine (`main.js`)

Il file `js/main.js` funge da orchestratore centralizzato dell'applicazione e si sviluppa su 4 fasi cardine:

1. **Il Ciclo di Vita `DOMContentLoaded`:** All'avvio, viene inizializzato un ciclo `Promise.all` che esegue le richieste di rete `fetch` asincrone contemporaneamente anziché in modo sequenziale, eliminando i colli di bottiglia.
2. **Iniezione dei Componenti:** Una volta scaricati `header.html` e `footer.html`, il software individua nel DOM i selettori id `#nav-placeholder` e `#footer-placeholder` e vi inietta le stringhe HTML corrispondenti.
3. **Inizializzazione dei Servizi condizionati:** Subito dopo l'iniezione, viene invocata la funzione `inizializzaEmailJS()` che aggancia il listener sull'evento `submit` del form (che ora esiste nel DOM, prevenendo errori di riferimento).
4. **Rendering Dinamico & GSAP Patch:** > [!IMPORTANT]  
> **Il GSAP Patch Meccanismo:** Poiché GSAP calcola le posizioni degli elementi per le animazioni all'avvio del file, l'inserimento di dati asincroni (come le card dei progetti) altererebbe le altezze effettive della pagina sfalsando i trigger. Per risolvere questo problema, il codice implementa un meccanismo di riallineamento geometrico ritardato:
> ```javascript
> setTimeout(() => {
>     if (typeof ScrollTrigger !== 'undefined') {
>         ScrollTrigger.refresh(); // Forza ScrollTrigger a ricalcolare le geometrie del DOM
>     }
> }, 150);
> ```

---

## 📊 Modelli Dati (JSON Database)

Per aggiungere, rimuovere o modificare elementi all'interno del sito, non serve toccare i file HTML. Basta editare i file strutturati all'interno della cartella `/data/`.

<details>
<summary>📰 Clicca per espandere il Modello e lo Schema di <code>news.json</code></summary>

```json
[
  {
    "id": "nuove-direttive-terre",
    "titolo": "Nuove direttive Terre e Rocce da Scavo",
    "data": "14 Maggio 2026",
    "immagine": "./assets/img/news-terre.jpg",
    "riassunto": "Aggiornamento sulle recenti modifiche normative per la gestione...",
    "contenuto": "<p>Testo esteso dell'articolo. Supporta tag HTML come <strong>grassetti</strong> o paragrafi multipli.</p>"
  }
]
```
</details>

<details>
<summary>📦 Clicca per espandere il Modello e lo Schema di <code>projects.json</code></summary>

```json
[
  {
    "title": "Bonifica Area Industriale Ex-Fiat",
    "client": "Ente Sviluppo Urbano S.p.A.",
    "period": "2024 - 2026",
    "endYear": 2026,
    "val": "€ 1.200.000",
    "type": "Ingegneria Ambientale / Bonifiche",
    "cardSubtitle": "Caratterizzazione e messa in sicurezza permanente dei terreni.",
    "desc": "<p>Descrizione estesa visibile solo all'interno del pop-up modale...</p>",
    "images": [
      "./assets/img/progetto1-cover.jpg",
      "./assets/img/progetto1-dettaglio.jpg"
    ],
    "tags": ["bonifiche", "ingegneria"]
  }
]
```
</details>

---

## 💻 Setup Locale e Sviluppo

> [!WARNING]  
> **Blocco di Sicurezza del Browser (CORS):** A causa delle politiche di sicurezza dei browser moderni (*Cross-Origin Resource Sharing*), **non è possibile** aprire il file `index.html` facendo semplicemente doppio clic sopra. Le chiamate `fetch` verso i file JSON locali e i componenti HTML fallirebbero lanciando un errore di sicurezza. È obbligatorio simulare un ambiente server.

### Opzione A: Tramite VS Code (Consigliata)
1. Installa l'estensione **Live Server** di Ritwick Dey.
2. Apri la cartella del progetto in VS Code.
3. Seleziona il file `index.html`.
4. Clicca sul pulsante **Go Live** in basso a destra sulla barra di stato.

### Opzione B: Tramite Terminale (Python)
Se hai Python installato sul tuo sistema (Windows/Mac/Linux), apri il terminale o la PowerShell all'interno della cartella del progetto ed esegui:
```bash
python -m http.server 8000
```
Dopodiché apri il browser e naviga all'indirizzo `http://localhost:8000`.

### Opzione C: Tramite Node.js
Se usi l'ambiente Node, puoi lanciare un server istantaneo senza installare pacchetti globali:
```bash
npx live-server
```

---

## ✉️ Configurazione del Form di Contatto (EmailJS)

Il modulo di contatto è interamente integrato e pre-configurato client-side nel file `main.js`. Se desideri collegarlo al tuo account personale per ricevere le email reali:

1. Registrati sul sito ufficiale di [EmailJS](https://www.emailjs.com/).
2. Collega un servizio email (ad esempio la tua casella Gmail aziendale).
3. Crea un *Email Template* inserendo i parametri corrispondenti ai campi strutturati nel form (`name`, `email`, e `message`).
4. Apri il file `js/main.js`, individua la funzione `inizializzaEmailJS()` e sostituisci le credenziali con i tuoi identificativi personali:

```javascript
function inizializzaEmailJS() {
    if (typeof emailjs === 'undefined') return;

    emailjs.init({
        publicKey: "IL_TUO_PUBLIC_KEY_REALE", // Inserisci qui la tua Public Key
    });

    // ... codice intermedio ...

    // Sostituisci i primi due argomenti con il tuo Service ID e il tuo Template ID:
    emailjs.sendForm('ID_SERVIZIO_SMTP', 'ID_TEMPLATE_EMAILJS', form)
}
```

---
*Documentazione tecnica ad alta fedeltà aggiornata a Giugno 2026 per l'infrastruttura web di Tecnitalia Group.*