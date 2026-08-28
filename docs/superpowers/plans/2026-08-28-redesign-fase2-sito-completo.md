# Redesign Fase 2 — Home completa + resto del sito Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Assegnazione modelli per task:** i task 1, 3, 6 sono modifiche mirate e ben specificate (CSS/HTML puntuali, codice già scritto in questo piano) — adatti a un modello economico. I task 2, 4, 5, 7 toccano più punti di un file o richiedono di seguire un pattern ripetuto con attenzione — modello standard. Il Task 8 (verifica end-to-end su 7 pagine) richiede il modello più capace. Indicato per ciascun task nella sezione "Model".

**Goal:** Completare il redesign visivo avviato nel pilota home (fascia statistiche, griglia progetti editoriale, design system) estendendolo a: (a) le sezioni della home rimaste con il vecchio linguaggio visivo (Chi Siamo, Ingegneria, Servizi, Team, News), e (b) tutte le altre 6 pagine del sito (chi-siamo.html, dettaglio-ingegneria.html, dettaglio-servizi.html, elenco-progetti.html, archivio-news.html, news-singola.html).

**Architecture:** Nessun build step. Si introducono due nuovi elementi di sistema in `css/style.css` (etichette "eyebrow" numerate in stile editoriale, link testuali con sottolineatura animata al posto dei pulsanti pillola per le call-to-action secondarie) e si applicano pagina per pagina. `chi-siamo.html` riceve anche una timeline verticale per la sua storia già divisa in 3 fasi cronologiche (nessuna riscrittura dei contenuti). Le altre pagine ricevono l'importazione del font Bricolage Grotesque (finora solo su `index.html`) e la rimozione dei blu inline superstiti sui titoli, oltre alle stesse etichette eyebrow.

**Tech Stack:** HTML/CSS statico, nessuna nuova libreria.

## Global Constraints

- Il blu Tecnitalia `#00427A` (`--blue`) resta un accento (usato ora anche per le etichette eyebrow e per l'hover dei link testuali) — mai come colore di titoli o sfondi diffusi.
- Titoli/display in Bricolage Grotesque (va importato su tutte le pagine, non solo `index.html`); corpo testo in Manrope, invariato.
- Nessuna nuova libreria o dipendenza.
- Nessuna modifica al contenuto testuale esistente (i testi storici di `chi-siamo.html`, le descrizioni dei servizi, ecc. restano gli stessi — cambia solo la presentazione visiva).
- Nessuna modifica alla logica EmailJS/honeypot al di fuori del fix esplicito del Task 1, ai dati JSON, o all'architettura di navigazione/routing.
- Si lavora sul branch `ottimizzazione-frontend` (già esistente, `main` resta il punto sicuro).
- Verifica locale con il server già configurato in `.claude/launch.json` (nome `tecnitalia-site`, porta 8123) dopo ogni task.
- Ogni task fa un commit a sé; nessun task lascia il sito in uno stato che non carica (niente errori console bloccanti) su nessuna delle 7 pagine.

---

### Task 1: Nuovi elementi di sistema in CSS + fix del bug honeypot preesistente

**Model:** economico — regole CSS già scritte per intero.

**Files:**
- Modify: `css/style.css` (aggiunte in coda al file, più un fix puntuale a `.hp-field` e `.member`/`.member img`)

**Interfaces:**
- Produces: classe `.eyebrow` (etichetta numerata uppercase), classe `.text-link` (link testuale con sottolineatura animata all'hover, per le call-to-action secondarie), `.member`/`.member img` flattening con hover grayscale→colore. Tutti i task successivi (2, 4, 5, 6, 7) consumano `.eyebrow` e `.text-link`.

- [ ] **Step 1: Aggiungere `.eyebrow` e `.text-link` in fondo a `css/style.css`**

Aggiungi in coda al file:
```css

/* --- 13. EYEBROW LABEL E TEXT-LINK --- */
.eyebrow { display: block; color: var(--blue); font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 12px; }
.text-link { color: var(--ink); font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; border-bottom: 2px solid transparent; padding-bottom: 4px; transition: border-color 0.3s ease, color 0.3s ease; }
.text-link:hover { border-color: var(--blue); color: var(--blue); }
```

- [ ] **Step 2: Appiattire `.member` e aggiungere l'effetto grayscale→colore sulle foto del team**

Trova:
```css
.member { text-align: center; width: 240px; background: #ffffff; padding: 30px 20px; border-radius: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.06); transition: transform 0.3s ease, box-shadow 0.3s ease; }
.member:hover { transform: translateY(-8px); box-shadow: 0 12px 35px rgba(0,0,0,0.12); }
.member img { width: 130px; height: 130px; border-radius: 50%; object-fit: cover; border: 3px solid var(--blue); margin-bottom: 15px; }
```
Sostituisci con:
```css
.member { text-align: center; width: 240px; background: #ffffff; padding: 30px 20px; border-radius: 8px; border: 1px solid #e5e5e0; transition: transform 0.3s ease, border-color 0.3s ease; }
.member:hover { transform: translateY(-6px); border-color: var(--blue); }
.member img { width: 130px; height: 130px; border-radius: 50%; object-fit: cover; border: 3px solid var(--blue); margin-bottom: 15px; filter: grayscale(1); transition: filter 0.4s ease; }
.member:hover img { filter: grayscale(0); }
```
(la riga `.member h4 { margin-bottom: 5px; }` subito dopo resta invariata, non toccarla)

- [ ] **Step 3: Correggere il bug preesistente del campo honeypot**

Trova:
```css
.hp-field { position: absolute !important; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; }
```
Sostituisci con:
```css
.hp-field { position: absolute !important; width: 1px !important; height: 1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; }
```
(il problema: `.form-box input { width: 100% }` ha specificità più alta di `.hp-field { width: 1px }` senza `!important`, quindi il campo nascosto anti-spam si espandeva a tutta larghezza, causando overflow orizzontale della pagina, specialmente su mobile. Aggiungere `!important` anche a `width` risolve definitivamente.)

- [ ] **Step 4: Verificare nel browser**

Avvia il server (`tecnitalia-site`, porta 8123), naviga su `http://localhost:8123/index.html`, esegui:
```js
JSON.stringify({
    hpWidth: getComputedStyle(document.querySelector('.hp-field')).width,
    scrollOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth
});
```
Risultato atteso: `hpWidth` è `"1px"`, `scrollOverflow` è `0` (o un numero molto piccolo, 1-2px al massimo — non più decine/centinaia di pixel).

Controlla la console: nessun errore. Nota: `.eyebrow`/`.text-link`/il restyling di `.member` non hanno ancora nessun elemento HTML che li usi in questo task — è normale, verranno usati dai task successivi. Non serve verificarli visivamente qui, solo che il CSS sia sintatticamente corretto (nessun errore nel caricamento del foglio di stile).

- [ ] **Step 5: Commit**

```bash
git add css/style.css
git commit -m "feat: aggiunge eyebrow label, text-link e corregge bug preesistente overflow honeypot"
```

---

### Task 2: Home — eyebrow label su tutte le sezioni, text-link sulle CTA, fix colore news statiche

**Model:** standard — molti punti di modifica nello stesso file, va seguito un pattern ripetuto con attenzione a non alterare altro.

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: `.eyebrow`, `.text-link` (da Task 1).
- Produces: nessuna nuova interfaccia — solo markup.

- [ ] **Step 1: Eyebrow "01 — Chi Siamo"**

Trova:
```html
    <section id="chi-siamo" class="section">
        <div class="fade-element">
            <h2 style="font-size:3rem; margin-bottom:30px;">Chi Siamo</h2>
```
Sostituisci con:
```html
    <section id="chi-siamo" class="section">
        <div class="fade-element">
            <span class="eyebrow">01 — Chi Siamo</span>
            <h2 style="font-size:3rem; margin-bottom:30px;">Chi Siamo</h2>
```

- [ ] **Step 2: Text-link sulla CTA di Chi Siamo**

Trova:
```html
            <div style="text-align: center; margin-top: 40px; width: 100%;">
                <a href="chi-siamo.html" class="filter-btn" style="display: inline-block; text-decoration: none;">La nostra storia completa ➔</a>
            </div>
```
Sostituisci con:
```html
            <div style="text-align: center; margin-top: 40px; width: 100%;">
                <a href="chi-siamo.html" class="text-link">La nostra storia completa ➔</a>
            </div>
```

- [ ] **Step 3: Eyebrow "02 — News" e fix colore titoli news statiche**

Trova:
```html
    <section id="news" class="section bg-gray">
        <div class="fade-element" style="text-align:center; margin-bottom: 40px;">
            <h2 style="font-size:3rem;">Ultime News</h2>
```
Sostituisci con:
```html
    <section id="news" class="section bg-gray">
        <div class="fade-element" style="text-align:center; margin-bottom: 40px;">
            <span class="eyebrow">02 — News</span>
            <h2 style="font-size:3rem;">Ultime News</h2>
```

Poi, le 3 card news statiche hanno ancora `color:var(--blue)` sul titolo (residuo del vecchio schema colori — il template JS che le sostituisce a runtime era già stato corretto in un lavoro precedente, ma il fallback HTML statico no). Trova (compare 3 volte, con testo diverso ogni volta — usa `replace_all` se il tuo editor lo supporta, altrimenti applica la stessa modifica a ciascuna delle 3 occorrenze):
```html
                    <h4 style="color:var(--blue); margin: 10px 0 15px 0; font-size: 1.3rem;">
```
Sostituisci ogni occorrenza con:
```html
                    <h4 style="margin: 10px 0 15px 0; font-size: 1.3rem;">
```
(Il testo dopo il tag, es. "Nuove direttive Terre e Rocce da Scavo", resta invariato — stai solo togliendo `color:var(--blue); ` dall'attributo `style`. Ci sono esattamente 3 occorrenze di questo pattern nel file, una per ogni card news statica.)

- [ ] **Step 4: Text-link sulla CTA News**

Trova:
```html
        <div class="fade-element" style="text-align: center; margin-top: 50px;">
            <a href="archivio-news.html" class="filter-btn" style="display: inline-block; text-decoration: none;">Vai all'Archivio completo News ➔</a>
        </div>
```
Sostituisci con:
```html
        <div class="fade-element" style="text-align: center; margin-top: 50px;">
            <a href="archivio-news.html" class="text-link">Vai all'Archivio completo News ➔</a>
        </div>
```

- [ ] **Step 5: Eyebrow "03 — Ingegneria" e text-link**

Trova:
```html
    <section id="ingegneria" class="section">
        <div class="division-block">
            <div class="div-text fade-element">
                <h3>Tecnitalia Ingegneria</h3>
```
Sostituisci con:
```html
    <section id="ingegneria" class="section">
        <div class="division-block">
            <div class="div-text fade-element">
                <span class="eyebrow">03 — Ingegneria</span>
                <h3>Tecnitalia Ingegneria</h3>
```

Trova:
```html
                <a href="dettaglio-ingegneria.html" class="filter-btn" style="display: inline-block; margin-top:20px; text-decoration: none;">Dettaglio Metodologie ➔</a>
```
Sostituisci con:
```html
                <a href="dettaglio-ingegneria.html" class="text-link" style="margin-top:20px;">Dettaglio Metodologie ➔</a>
```

- [ ] **Step 6: Eyebrow "04 — Servizi" e text-link**

Trova:
```html
    <section id="servizi" class="section bg-gray">
        <div class="division-block reversed">
            <div class="div-text fade-element">
                <h3>Tecnitalia Servizi</h3>
```
Sostituisci con:
```html
    <section id="servizi" class="section bg-gray">
        <div class="division-block reversed">
            <div class="div-text fade-element">
                <span class="eyebrow">04 — Servizi</span>
                <h3>Tecnitalia Servizi</h3>
```

Trova:
```html
                <a href="dettaglio-servizi.html" class="filter-btn" style="display: inline-block; margin-top:20px; text-decoration: none;">Dettaglio Laboratorio ➔</a>
```
Sostituisci con:
```html
                <a href="dettaglio-servizi.html" class="text-link" style="margin-top:20px;">Dettaglio Laboratorio ➔</a>
```

- [ ] **Step 7: Eyebrow "05 — Progetti" e text-link**

Trova:
```html
    <section id="progetti" class="section">
        <div class="fade-element" style="text-align:center;">
            <h2 style="font-size:3rem; margin-bottom:10px;">Progetti</h2>
```
Sostituisci con:
```html
    <section id="progetti" class="section">
        <div class="fade-element" style="text-align:center;">
            <span class="eyebrow">05 — Progetti</span>
            <h2 style="font-size:3rem; margin-bottom:10px;">Progetti</h2>
```

Trova:
```html
        <div class="fade-element" style="text-align: center; margin-top: 40px; width: 100%;">
            <a href="elenco-progetti.html" class="filter-btn" style="display: inline-block; text-decoration: none;">Visualizza Archivio Progetti Completo ➔</a>
        </div>
    </section>

    <section id="team" class="section bg-gray">
```
Sostituisci con:
```html
        <div class="fade-element" style="text-align: center; margin-top: 40px; width: 100%;">
            <a href="elenco-progetti.html" class="text-link">Visualizza Archivio Progetti Completo ➔</a>
        </div>
    </section>

    <section id="team" class="section bg-gray">
```

- [ ] **Step 8: Eyebrow "06 — Team"**

Trova:
```html
    <section id="team" class="section bg-gray">
        <h2 class="fade-element" style="text-align:center; margin-bottom:50px;">Il Team</h2>
```
Sostituisci con:
```html
    <section id="team" class="section bg-gray">
        <div class="fade-element" style="text-align:center;">
            <span class="eyebrow">06 — Team</span>
            <h2 style="margin-bottom:50px;">Il Team</h2>
        </div>
```

- [ ] **Step 9: Verificare nel browser**

Naviga su `http://localhost:8123/index.html`. Esegui:
```js
JSON.stringify({
    eyebrowCount: document.querySelectorAll('.eyebrow').length,
    textLinkCount: document.querySelectorAll('.text-link').length,
    newsH4Color: getComputedStyle(document.querySelector('#news h4')).color
});
```
Risultato atteso: `eyebrowCount` = 6, `textLinkCount` = 5, `newsH4Color` = `"rgb(10, 10, 10)"` (non più blu).

Controlla la console: nessun errore. Verifica visivamente con uno screenshot che le etichette "01 — CHI SIAMO" ecc. appaiano sopra ai rispettivi titoli.

- [ ] **Step 10: Commit**

```bash
git add index.html
git commit -m "feat: aggiunge eyebrow label e text-link a tutte le sezioni della home"
```

---

### Task 3: Propagare il font Bricolage Grotesque e rimuovere il blu residuo su tutte le altre pagine

**Model:** economico — modifica meccanica ripetuta, stesso pattern su più file, tutto già specificato riga per riga.

**Files:**
- Modify: `chi-siamo.html`, `dettaglio-ingegneria.html`, `dettaglio-servizi.html`, `elenco-progetti.html`, `archivio-news.html`, `news-singola.html`, `index.html`

**Interfaces:** nessuna — solo tipografia/colore, nessun JS coinvolto.

- [ ] **Step 1: Importare Bricolage Grotesque su 6 pagine**

In ciascuno di questi 6 file, la riga è **identica**. Trova (una sola volta per file):
```html
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;800&display=swap" rel="stylesheet">
```
Sostituisci con:
```html
    <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=Manrope:wght@300;400;600;800&display=swap" rel="stylesheet">
```
Applicala in: `chi-siamo.html`, `dettaglio-ingegneria.html`, `dettaglio-servizi.html`, `elenco-progetti.html`, `archivio-news.html`, `news-singola.html`.

- [ ] **Step 2: Rimuovere il blu inline dai titoli di `chi-siamo.html`**

Trova le 3 occorrenze in `chi-siamo.html`:
```html
        <h2 style="color: var(--blue); margin-bottom: 20px;">Le Origini (1986)</h2>
```
```html
        <h3 style="color: var(--blue); margin-top: 40px; margin-bottom: 15px;">L'evoluzione Ambientale</h3>
```
```html
        <h3 style="color: var(--blue); margin-top: 40px; margin-bottom: 15px;">Il Presente e le Certificazioni</h3>
```
Sostituiscile rispettivamente con:
```html
        <h2 style="margin-bottom: 20px;">Le Origini (1986)</h2>
```
```html
        <h3 style="margin-top: 40px; margin-bottom: 15px;">L'evoluzione Ambientale</h3>
```
```html
        <h3 style="margin-top: 40px; margin-bottom: 15px;">Il Presente e le Certificazioni</h3>
```

- [ ] **Step 3: Rimuovere il blu inline dai titoli di `dettaglio-ingegneria.html`**

Trova le 3 occorrenze:
```html
        <h2 style="color: var(--blue); margin-bottom: 20px;">Il nostro approccio tecnico</h2>
```
```html
        <h3 style="color: var(--blue); margin-top: 40px; margin-bottom: 15px;">Aree di Intervento e Tematiche Ambientali</h3>
```
```html
        <h3 style="color: var(--blue); margin-top: 40px; margin-bottom: 15px;">Tecnologie Applicate</h3>
```
Sostituiscile rispettivamente con:
```html
        <h2 style="margin-bottom: 20px;">Il nostro approccio tecnico</h2>
```
```html
        <h3 style="margin-top: 40px; margin-bottom: 15px;">Aree di Intervento e Tematiche Ambientali</h3>
```
```html
        <h3 style="margin-top: 40px; margin-bottom: 15px;">Tecnologie Applicate</h3>
```

- [ ] **Step 4: Rimuovere il blu inline dai titoli di `dettaglio-servizi.html`**

Trova le 3 occorrenze:
```html
        <h2 style="color: var(--blue); margin-bottom: 20px;">Operatività e Supporto Diretto</h2>
```
```html
        <h3 style="color: var(--blue); margin-top: 40px; margin-bottom: 15px;">I nostri servizi principali</h3>
```
```html
        <h3 style="color: var(--blue); margin-top: 40px; margin-bottom: 15px;">Certificazioni e Sistemi di Gestione</h3>
```
Sostituiscile rispettivamente con:
```html
        <h2 style="margin-bottom: 20px;">Operatività e Supporto Diretto</h2>
```
```html
        <h3 style="margin-top: 40px; margin-bottom: 15px;">I nostri servizi principali</h3>
```
```html
        <h3 style="margin-top: 40px; margin-bottom: 15px;">Certificazioni e Sistemi di Gestione</h3>
```

- [ ] **Step 5: Rimuovere il blu inline dal titolo della modale progetti, in 2 file**

In `elenco-progetti.html`, trova:
```html
                <h2 id="m-title" style="color:var(--blue); margin-bottom:20px; font-size:2rem; line-height:1.2;"></h2>
```
Sostituisci con:
```html
                <h2 id="m-title" style="margin-bottom:20px; font-size:2rem; line-height:1.2;"></h2>
```

In `index.html`, trova la stessa identica riga e applica la stessa modifica.

- [ ] **Step 6: Verificare nel browser**

Naviga su ciascuna di queste pagine e controlla `getComputedStyle` sul titolo principale:
- `http://localhost:8123/chi-siamo.html`: `getComputedStyle(document.querySelector('h2')).fontFamily` deve contenere `"Bricolage Grotesque"`, e `getComputedStyle(document.querySelector('h2')).color` deve essere `"rgb(10, 10, 10)"`.
- Ripeti lo stesso controllo su `dettaglio-ingegneria.html`, `dettaglio-servizi.html`, `elenco-progetti.html`, `archivio-news.html`, `news-singola.html` (per queste ultime due basta verificare `fontFamily` sul titolo, dato che non avevano blu inline da rimuovere).
- Su `elenco-progetti.html` e `index.html`: apri una scheda progetto (`openProject(0)` via `javascript_tool`) e controlla che `getComputedStyle(document.getElementById('m-title')).color` sia `"rgb(10, 10, 10)"`.

Controlla la console: nessun errore su nessuna delle 7 pagine.

- [ ] **Step 7: Commit**

```bash
git add chi-siamo.html dettaglio-ingegneria.html dettaglio-servizi.html elenco-progetti.html archivio-news.html news-singola.html index.html
git commit -m "feat: propaga il font Bricolage Grotesque e rimuove il blu residuo su tutte le pagine"
```

---

### Task 4: Chi Siamo — timeline verticale della storia aziendale

**Model:** standard — nuovo componente strutturale, non solo sostituzione di stringhe.

**Files:**
- Modify: `chi-siamo.html`
- Modify: `css/style.css` (nuove regole `.timeline*`)

**Interfaces:**
- Consumes: `.eyebrow`, `.text-link` (da Task 1); nessuna riscrittura del testo storico esistente.
- Produces: nessuna nuova interfaccia consumata da altri task.

- [ ] **Step 1: Aggiungere le regole CSS della timeline**

In fondo a `css/style.css`, aggiungi:
```css

/* --- 14. TIMELINE CHI SIAMO --- */
.timeline { position: relative; max-width: 800px; margin: 50px auto 0; padding-left: 40px; border-left: 2px solid #e5e5e0; }
.timeline-item { position: relative; padding-bottom: 50px; }
.timeline-item:last-child { padding-bottom: 0; }
.timeline-item::before { content: ''; position: absolute; left: -46px; top: 4px; width: 12px; height: 12px; border-radius: 50%; background: var(--blue); border: 3px solid var(--paper); box-shadow: 0 0 0 2px var(--blue); }
.timeline-year { display: block; color: var(--blue); font-family: 'Bricolage Grotesque', 'Manrope', sans-serif; font-weight: 800; font-size: 1.5rem; margin-bottom: 8px; }
.timeline-item h3 { margin-top: 0; margin-bottom: 15px; }
```

- [ ] **Step 2: Sostituire i 3 blocchi di testo con una timeline**

In `chi-siamo.html`, trova:
```html
    <main class="page-content">
        <img src="https://images.unsplash.com/photo-1541888086425-d81bb19240f5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" alt="Storia Tecnitalia" loading="lazy" decoding="async" style="width: 100%; border-radius: 10px; margin-bottom: 30px; object-fit: cover; height: 400px;">
        
        <h2 style="margin-bottom: 20px;">Le Origini (1986)</h2>
        <p>Il Gruppo Tecnitalia è nato nel 1986 con l'obiettivo primario di prestare consulenza tecnica e servizi specialistici alle imprese. Nelle fasi iniziali del nostro sviluppo, ci siamo dedicati prevalentemente al settore della sicurezza, con un focus particolare sull’antincendio e sull’analisi del rischio per le attività industriali complesse soggette al DPR 175/88 (Direttiva Seveso). In quegli anni, abbiamo anche consolidato un solido servizio di consulenza tecnica fornito alle principali Compagnie di Assicurazione.</p>
        
        <h3 style="margin-top: 40px; margin-bottom: 15px;">L'evoluzione Ambientale</h3>
        <p>Successivamente, facendo seguito al recepimento nazionale delle Direttive Comunitarie in materia di tutela ambientale ed ai connessi e stringenti obblighi per le imprese, è stato avviato e potenziato il settore ambientale. Tecnitalia si è progressivamente concentrata sulle complesse problematiche di recupero delle aree industriali dismesse.</p>
        <p>Abbiamo sviluppato un forte know-how specifico riferito alla bonifica dei terreni contaminati, al trattamento delle acque di falda e reflue, e alla gestione integrata dei rifiuti, diventando un partner affidabile per grandi gruppi industriali e immobiliari.</p>

        <h3 style="margin-top: 40px; margin-bottom: 15px;">Il Presente e le Certificazioni</h3>
        <p>Di recente, seguendo le esigenze di un mercato sempre più normato, sono state consolidate anche le competenze per far fronte alla crescente domanda di certificazione delle imprese (ISO 9000, ISO 14000, EMAS) e dei prodotti (marcatura CE degli aggregati), con specifico e approfondito riferimento al settore del riciclaggio dei rifiuti inerti derivanti da demolizione.</p>

        <a href="index.html" class="filter-btn" style="display: inline-block; text-decoration: none; margin-top: 40px;">⬅ Torna alla Home</a>
    </main>
```
Sostituisci con:
```html
    <main class="page-content">
        <span class="eyebrow" style="text-align:center;">La nostra storia</span>

        <div class="timeline fade-element">
            <div class="timeline-item">
                <span class="timeline-year">1986</span>
                <h3>Le Origini</h3>
                <p>Il Gruppo Tecnitalia è nato nel 1986 con l'obiettivo primario di prestare consulenza tecnica e servizi specialistici alle imprese. Nelle fasi iniziali del nostro sviluppo, ci siamo dedicati prevalentemente al settore della sicurezza, con un focus particolare sull’antincendio e sull’analisi del rischio per le attività industriali complesse soggette al DPR 175/88 (Direttiva Seveso). In quegli anni, abbiamo anche consolidato un solido servizio di consulenza tecnica fornito alle principali Compagnie di Assicurazione.</p>
            </div>
            <div class="timeline-item">
                <span class="timeline-year">Anni '90-2000</span>
                <h3>L'evoluzione Ambientale</h3>
                <p>Successivamente, facendo seguito al recepimento nazionale delle Direttive Comunitarie in materia di tutela ambientale ed ai connessi e stringenti obblighi per le imprese, è stato avviato e potenziato il settore ambientale. Tecnitalia si è progressivamente concentrata sulle complesse problematiche di recupero delle aree industriali dismesse.</p>
                <p>Abbiamo sviluppato un forte know-how specifico riferito alla bonifica dei terreni contaminati, al trattamento delle acque di falda e reflue, e alla gestione integrata dei rifiuti, diventando un partner affidabile per grandi gruppi industriali e immobiliari.</p>
            </div>
            <div class="timeline-item">
                <span class="timeline-year">Oggi</span>
                <h3>Il Presente e le Certificazioni</h3>
                <p>Di recente, seguendo le esigenze di un mercato sempre più normato, sono state consolidate anche le competenze per far fronte alla crescente domanda di certificazione delle imprese (ISO 9000, ISO 14000, EMAS) e dei prodotti (marcatura CE degli aggregati), con specifico e approfondito riferimento al settore del riciclaggio dei rifiuti inerti derivanti da demolizione.</p>
            </div>
        </div>

        <div style="text-align:center; margin-top: 40px;">
            <a href="index.html" class="text-link">⬅ Torna alla Home</a>
        </div>
    </main>
```

(Nota: la foto Unsplash generica viene rimossa perché la timeline la rende superflua e non era comunque una foto reale dell'azienda — è una modifica intenzionale, non un errore. `.eyebrow` viene qui centrato con uno style inline invece di usare le classi di sezione della home, dato che questa pagina non ha la stessa struttura a sezioni.)

- [ ] **Step 3: Verificare nel browser**

Naviga su `http://localhost:8123/chi-siamo.html`. Esegui:
```js
JSON.stringify({
    timelineItems: document.querySelectorAll('.timeline-item').length,
    years: [...document.querySelectorAll('.timeline-year')].map(el => el.textContent),
    unsplashImgGone: document.querySelector('img[src*="unsplash"]') === null
});
```
Risultato atteso: `timelineItems` = 3, `years` = `["1986", "Anni '90-2000", "Oggi"]`, `unsplashImgGone` = `true`.

Controlla la console: nessun errore. Fai uno screenshot per verifica visiva (i pallini blu sulla linea verticale devono essere allineati con l'inizio di ogni blocco di testo).

- [ ] **Step 4: Commit**

```bash
git add chi-siamo.html css/style.css
git commit -m "feat: aggiunge timeline verticale alla pagina Chi Siamo"
```

---

### Task 5: Dettaglio Ingegneria e Dettaglio Servizi — eyebrow e text-link

**Model:** economico — stesso pattern ripetuto su 2 file, codice già scritto.

**Files:**
- Modify: `dettaglio-ingegneria.html`, `dettaglio-servizi.html`

**Interfaces:**
- Consumes: `.eyebrow`, `.text-link` (da Task 1).

- [ ] **Step 1: Eyebrow e text-link in `dettaglio-ingegneria.html`**

Trova:
```html
    <main class="page-content">
        <img src="./assets/img/ingegneria.png" onerror="this.src='https://via.placeholder.com/900x400'" alt="Ingegneria" style="width: 100%; border-radius: 10px; margin-bottom: 30px; object-fit: cover; height: 400px;">
        
        <h2 style="margin-bottom: 20px;">Il nostro approccio tecnico</h2>
```
Sostituisci con:
```html
    <main class="page-content">
        <img src="./assets/img/ingegneria.png" onerror="this.src='https://via.placeholder.com/900x400'" alt="Ingegneria" style="width: 100%; border-radius: 10px; margin-bottom: 30px; object-fit: cover; height: 400px;">
        
        <span class="eyebrow">Tecnitalia Ingegneria</span>
        <h2 style="margin-bottom: 20px;">Il nostro approccio tecnico</h2>
```

Trova:
```html
        <a href="index.html" class="filter-btn" style="display: inline-block; text-decoration: none; margin-top: 40px;">⬅ Torna alla Home</a>
```
Sostituisci con:
```html
        <a href="index.html" class="text-link" style="margin-top: 40px;">⬅ Torna alla Home</a>
```

- [ ] **Step 2: Eyebrow e text-link in `dettaglio-servizi.html`**

Trova:
```html
    <main class="page-content">
        <img src="./assets/img/servizi.png" onerror="this.src='https://via.placeholder.com/900x400'" alt="Servizi" style="width: 100%; border-radius: 10px; margin-bottom: 30px; object-fit: cover; height: 400px;">
        
        <h2 style="margin-bottom: 20px;">Operatività e Supporto Diretto</h2>
```
Sostituisci con:
```html
    <main class="page-content">
        <img src="./assets/img/servizi.png" onerror="this.src='https://via.placeholder.com/900x400'" alt="Servizi" style="width: 100%; border-radius: 10px; margin-bottom: 30px; object-fit: cover; height: 400px;">
        
        <span class="eyebrow">Tecnitalia Servizi</span>
        <h2 style="margin-bottom: 20px;">Operatività e Supporto Diretto</h2>
```

Trova:
```html
        <a href="index.html" class="filter-btn" style="display: inline-block; text-decoration: none; margin-top: 40px;">⬅ Torna alla Home</a>
```
Sostituisci con:
```html
        <a href="index.html" class="text-link" style="margin-top: 40px;">⬅ Torna alla Home</a>
```

- [ ] **Step 3: Verificare nel browser**

Su entrambe le pagine, verifica:
```js
JSON.stringify({ eyebrow: document.querySelector('.eyebrow')?.textContent, textLink: document.querySelector('.text-link')?.textContent });
```
Su `dettaglio-ingegneria.html` attesa: `eyebrow` = `"Tecnitalia Ingegneria"`. Su `dettaglio-servizi.html` attesa: `eyebrow` = `"Tecnitalia Servizi"`. In entrambi i casi `textLink` deve contenere "Torna alla Home".

Controlla la console: nessun errore su entrambe le pagine.

- [ ] **Step 4: Commit**

```bash
git add dettaglio-ingegneria.html dettaglio-servizi.html
git commit -m "feat: aggiunge eyebrow e text-link alle pagine di dettaglio Ingegneria e Servizi"
```

---

### Task 6: Elenco Progetti — eyebrow e verifica coerenza filtri/griglia/modale

**Model:** economico — piccola modifica di markup più verifica.

**Files:**
- Modify: `elenco-progetti.html`

**Interfaces:**
- Consumes: `.eyebrow` (da Task 1); `.project-card`/`.projects-full-grid` (già esistenti, non modificati da questo task — la griglia archivio eredita già il linguaggio "flat" introdotto nel pilota home perché condivide la classe `.project-card`).

- [ ] **Step 1: Aggiungere l'eyebrow dentro il `<main>` esistente**

Trova:
```html
    <main class="page-content" style="max-width: 1200px;">
        
        <div class="filter-container">
```
Sostituisci con:
```html
    <main class="page-content" style="max-width: 1200px;">
        <span class="eyebrow" style="text-align:center; display:block; margin-bottom:20px;">Il nostro lavoro</span>

        <div class="filter-container">
```
(C'è un solo `<main>` nel file — non crearne un secondo, l'eyebrow va inserita come primo elemento dentro quello esistente, subito prima di `<div class="filter-container">`.)

- [ ] **Step 2: Verificare nel browser**

Naviga su `http://localhost:8123/elenco-progetti.html`. Esegui:
```js
JSON.stringify({
    mainCount: document.querySelectorAll('main.page-content').length,
    eyebrowText: document.querySelector('.eyebrow')?.textContent,
    gridCards: document.querySelectorAll('#projects-grid-full .project-card').length
});
```
Risultato atteso: `mainCount` = 1, `eyebrowText` = `"Il nostro lavoro"`, `gridCards` > 0 (il numero reale di progetti, es. 28).

Clicca su un filtro (es. "Bonifiche") e verifica che la griglia si aggiorni (`filterProjects` esistente, non toccato da questo task). Apri una card e verifica che la modale funzioni. Controlla la console: nessun errore.

- [ ] **Step 3: Commit**

```bash
git add elenco-progetti.html
git commit -m "feat: aggiunge eyebrow alla pagina Elenco Progetti"
```

---

### Task 7: Archivio News e News Singola — eyebrow e text-link

**Model:** standard — due file con struttura leggermente diversa, richiede attenzione al contesto di ciascuno.

**Files:**
- Modify: `archivio-news.html`, `news-singola.html`

**Interfaces:**
- Consumes: `.eyebrow`, `.text-link` (da Task 1).

- [ ] **Step 1: Eyebrow e text-link in `archivio-news.html`**

Trova:
```html
    <main class="page-content" style="max-width: 1200px;">
        
        <div id="news-grid-full" class="news-grid"></div>
        
        <div style="text-align: center; margin-top: 50px;">
            <a href="index.html" class="filter-btn" style="display: inline-block; text-decoration: none;">⬅ Torna alla Home</a>
        </div>
    </main>
```
Sostituisci con:
```html
    <main class="page-content" style="max-width: 1200px;">
        <span class="eyebrow" style="text-align:center; display:block;">Tutte le novità</span>

        <div id="news-grid-full" class="news-grid"></div>
        
        <div style="text-align: center; margin-top: 50px;">
            <a href="index.html" class="text-link">⬅ Torna alla Home</a>
        </div>
    </main>
```

- [ ] **Step 2: Text-link in `news-singola.html`**

Trova:
```html
            <div style="margin-top: 50px; border-top: 1px solid #eee; padding-top: 30px;">
                <a href="archivio-news.html" class="filter-btn" style="display: inline-block; text-decoration: none;">⬅ Torna all'Archivio News</a>
            </div>
```
Sostituisci con:
```html
            <div style="margin-top: 50px; border-top: 1px solid #eee; padding-top: 30px;">
                <a href="archivio-news.html" class="text-link">⬅ Torna all'Archivio News</a>
            </div>
```

(`news-singola.html` non riceve un eyebrow statico: il suo titolo `<h1 id="n-titolo">` è già popolato dinamicamente dal JS esistente con il titolo dell'articolo, e non ha un sottotitolo di sezione fisso a cui appendere un'etichetta — nessuna modifica necessaria oltre al text-link.)

- [ ] **Step 3: Verificare nel browser**

Su `http://localhost:8123/archivio-news.html`:
```js
JSON.stringify({ eyebrow: document.querySelector('.eyebrow')?.textContent, textLink: document.querySelector('.text-link')?.textContent, newsCards: document.querySelectorAll('#news-grid-full .project-card').length });
```
Atteso: `eyebrow` = `"Tutte le novità"`, `textLink` contiene "Torna alla Home", `newsCards` > 0.

Su `http://localhost:8123/news-singola.html?id=news-001`:
```js
document.querySelector('.text-link')?.textContent
```
Atteso: contiene "Torna all'Archivio News".

Controlla la console su entrambe le pagine: nessun errore.

- [ ] **Step 4: Commit**

```bash
git add archivio-news.html news-singola.html
git commit -m "feat: aggiunge eyebrow e text-link alle pagine Archivio News e News Singola"
```

---

### Task 8: Verifica end-to-end su tutte le 7 pagine e checkpoint finale

**Model:** capace (il più capace disponibile) — richiede giudizio visivo complessivo su più pagine, non solo eseguire comandi.

**Files:** nessuna modifica — solo verifica.

**Interfaces:** Consumes: tutto quanto prodotto dai Task 1-7. Produces: nessuna modifica di codice; l'esito è un report per l'utente.

- [ ] **Step 1: Avviare il server e controllare ciascuna delle 7 pagine**

Per ciascuna di `index.html`, `chi-siamo.html`, `dettaglio-ingegneria.html`, `dettaglio-servizi.html`, `elenco-progetti.html`, `archivio-news.html`, `news-singola.html?id=news-001`:
- Naviga alla pagina.
- Controlla la console (nessun errore) e le richieste di rete (nessun 404, in particolare il font Bricolage Grotesque e le immagini).
- Fai uno screenshot desktop.
- Verifica che nav e footer siano coerenti con lo stile navy/ink su tutte.

- [ ] **Step 2: Controlli specifici per pagina**

- `index.html`: le 6 eyebrow numerate (01-06) sono visibili sopra i rispettivi titoli; la fascia statistiche e la griglia progetti editoriale (dal pilota precedente) funzionano ancora; il team ha le foto che passano da bianco/nero a colore all'hover (puoi verificarlo forzando lo stato `:hover` via CSS o controllando che `getComputedStyle` cambi il filtro se simuli l'hover, oppure semplicemente descrivi il comportamento atteso dal codice se non riesci a simularlo).
- `chi-siamo.html`: la timeline con i 3 nodi (1986 / Anni '90-2000 / Oggi) è presente e allineata.
- `elenco-progetti.html`: un solo `<main class="page-content">`, filtri funzionanti, modale funzionante.
- Tutte le pagine: nessun testo blu residuo sui titoli principali (`h1`, `h2`, `h3` — verifica a campione con `getComputedStyle`).
- Controlla che il bug dell'overflow orizzontale del campo honeypot (Task 1) sia davvero risolto su almeno 2 pagine diverse con un footer (es. `index.html` e `chi-siamo.html`): `document.documentElement.scrollWidth - document.documentElement.clientWidth` deve essere vicino a 0.

- [ ] **Step 3: Verifica mobile**

Ridimensiona a preset `mobile` (375×812), ricarica `index.html` e `chi-siamo.html`, controlla che il menu hamburger funzioni, che la fascia statistiche sia a 2 colonne, che la timeline resti leggibile. Ripristina il preset `desktop` al termine.

- [ ] **Step 4: Report all'utente**

Riassumi (in italiano) cosa è cambiato su ciascuna pagina, segnala qualsiasi problema trovato con dettagli precisi (file, riga, come riprodurlo) — **non correggerlo tu stesso**, riportalo soltanto. Indica se il lavoro è pronto per essere mostrato all'utente così com'è, o se qualcosa va corretto prima.

Non fare commit in questo task (solo verifica).
