# Redesign Frontend — Design System & Pilota Home Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Assegnazione modelli per task:** i task 1-5 sono modifiche mirate e ben specificate (CSS/HTML/JS puntuali, codice già scritto in questo piano) — adatti a un modello più economico. Il Task 6 (verifica visiva/funzionale end-to-end, giudizio su cosa "sembra giusto") richiede un modello più capace. Indicato per ciascun task nella sezione "Model".

**Goal:** Introdurre il nuovo design system (tipografia Bricolage Grotesque, palette ink/paper/navy-deep, card più piatte) e applicarlo come pilota alla home (`index.html`): fascia statistiche animata e griglia editoriale progetti al posto dello slider.

**Architecture:** Nessun build step. Si lavora direttamente su `css/style.css` (variabili + nuove classi), `index.html` (markup nuove sezioni + rimozione colori inline in blu), `js/main.js` (nuova funzione contatori + render griglia editoriale, sostituendo il render dello slider). Nav e footer sono condivisi (`header.html`/`footer.html`) quindi il restyling di Task 4 si propaga automaticamente a tutte le pagine.

**Tech Stack:** HTML/CSS/JS statico, GSAP + ScrollTrigger + Lenis (già caricati via CDN, nessuna nuova libreria), Google Fonts (Bricolage Grotesque, nuovo import).

## Global Constraints

- Il blu Tecnitalia `#00427A` (`--blue`) resta il colore-firma ma va usato come accento (link, hover, dettagli) — non più come colore di titoli o sfondi diffusi.
- Titoli/display in **Bricolage Grotesque**; corpo testo resta in **Manrope** (invariato, nessuna modifica ai pesi/link già caricati).
- Nessuna nuova libreria o dipendenza: si riusano GSAP/ScrollTrigger/Lenis già presenti.
- Nessuna modifica alla logica EmailJS/honeypot (`inizializzaEmailJS`), alla struttura dei file JSON, o all'architettura di navigazione/routing.
- Si lavora sul branch `ottimizzazione-frontend` (già esistente, `main` resta il punto sicuro).
- Verifica locale con il server già configurato in `.claude/launch.json` (nome `tecnitalia-site`, porta 8123) dopo ogni task.
- Ogni task fa un commit a sé; nessun task lascia il sito in uno stato che non carica (niente errori console bloccanti).

---

### Task 1: Design system — variabili colore, font Bricolage Grotesque, migrazione titoli

**Model:** economico (sonnet/haiku) — modifiche puntuali già specificate riga per riga.

**Files:**
- Modify: `css/style.css:1-6` (variabili), `css/style.css:19` (regola h1-h4), `css/style.css:101` (`.div-text h3`), `css/style.css:173` (`.member h4`)
- Modify: `index.html:26` (import font), `index.html:44,63,141,157` (rimozione `color:var(--blue)` inline)
- Modify: `js/main.js:131` (colore h4 card news nel template)

**Interfaces:**
- Produces: variabili CSS `--ink: #0A0A0A`, `--paper: #FAFAF8`, `--navy-deep: #071B2E` in `:root`; regola globale `h1, h2, h3, h4` con `font-family: 'Bricolage Grotesque', 'Manrope', sans-serif` e `color: var(--ink)`. I task successivi (2, 3, 4) usano queste variabili e presuppongono che i titoli non abbiano più `color:var(--blue)` inline sulla home.

- [ ] **Step 1: Aggiungere le nuove variabili colore**

In `css/style.css`, sostituisci:
```css
:root { 
    --blue: #00427A; 
    --text: #1d1d1f; 
    --gray: #f5f5f7; 
}
```
con:
```css
:root { 
    --blue: #00427A; 
    --text: #1d1d1f; 
    --gray: #f5f5f7; 
    --ink: #0A0A0A;
    --paper: #FAFAF8;
    --navy-deep: #071B2E;
}
```

- [ ] **Step 2: Applicare Bricolage Grotesque e il colore ink ai titoli, e lo sfondo "carta" al body**

Nello stesso file, sostituisci:
```css
h1, h2, h3, h4 { margin: 0; font-weight: 800; letter-spacing: -0.02em; }
```
con:
```css
h1, h2, h3, h4 { margin: 0; font-weight: 800; letter-spacing: -0.02em; font-family: 'Bricolage Grotesque', 'Manrope', sans-serif; color: var(--ink); }
```

Poco più su, nella stessa regola `body, html`, sostituisci:
```css
body, html { 
    margin: 0; 
    padding: 0; 
    font-family: 'Manrope', sans-serif; 
    overflow-x: hidden; 
    width: 100%; 
}
```
con:
```css
body, html { 
    margin: 0; 
    padding: 0; 
    font-family: 'Manrope', sans-serif; 
    overflow-x: hidden; 
    width: 100%; 
    background: var(--paper);
}
```
(`--paper` è quasi indistinguibile dal bianco puro a occhio nudo — è intenzionale, è la sottile calda "carta" della spec, non deve saltare all'occhio come un cambio cromatico.)

- [ ] **Step 3: Aggiornare le regole che coloravano i titoli in blu**

Sostituisci:
```css
.div-text h3 { font-size: 2.5rem; color: var(--blue); margin-bottom: 20px; }
```
con:
```css
.div-text h3 { font-size: 2.5rem; margin-bottom: 20px; }
```

Sostituisci:
```css
.member h4 { color: var(--blue); margin-bottom: 5px; }
```
con:
```css
.member h4 { margin-bottom: 5px; }
```

- [ ] **Step 4: Importare il font Bricolage Grotesque in `index.html`**

In `index.html`, sostituisci la riga:
```html
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;800&display=swap" rel="stylesheet">
```
con:
```html
    <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=Manrope:wght@300;400;600;800&display=swap" rel="stylesheet">
```

- [ ] **Step 5: Rimuovere il blu inline dai titoli di `index.html`**

Sostituisci (riga 44):
```html
            <h2 style="font-size:3rem; color:var(--blue); margin-bottom:30px;">Chi Siamo</h2>
```
con:
```html
            <h2 style="font-size:3rem; margin-bottom:30px;">Chi Siamo</h2>
```

Sostituisci (riga 63):
```html
            <h2 style="font-size:3rem; color:var(--blue);">Ultime News</h2>
```
con:
```html
            <h2 style="font-size:3rem;">Ultime News</h2>
```

Sostituisci (riga 141):
```html
            <h2 style="font-size:3rem; margin-bottom:10px; color:var(--blue);">Progetti</h2>
```
con:
```html
            <h2 style="font-size:3rem; margin-bottom:10px;">Progetti</h2>
```

Sostituisci (riga 157):
```html
        <h2 class="fade-element" style="text-align:center; margin-bottom:50px; color:var(--blue);">Il Team</h2>
```
con:
```html
        <h2 class="fade-element" style="text-align:center; margin-bottom:50px;">Il Team</h2>
```

- [ ] **Step 6: Rimuovere il blu inline dal titolo delle card news nel JS**

In `js/main.js` riga 131, sostituisci:
```js
                        <h4 style="color:var(--blue); margin: 10px 0 15px 0; font-size: 1.3rem;">${news.titolo}</h4>
```
con:
```js
                        <h4 style="margin: 10px 0 15px 0; font-size: 1.3rem;">${news.titolo}</h4>
```

- [ ] **Step 7: Verificare nel browser**

Avvia il server locale (`preview_start` con name `tecnitalia-site`), naviga su `http://localhost:8123/index.html`, poi esegui:
```js
const h2 = document.querySelector('#chi-siamo h2');
const style = getComputedStyle(h2);
JSON.stringify({ font: style.fontFamily, color: style.color, bodyBg: getComputedStyle(document.body).backgroundColor });
```
Risultato atteso: `font` contiene `"Bricolage Grotesque"`, `color` è `"rgb(10, 10, 10)"`, `bodyBg` è `"rgb(250, 250, 248)"`.

Controlla anche la console (`read_console_messages`, `onlyErrors: true`): nessun errore.

- [ ] **Step 8: Commit**

```bash
git add css/style.css index.html js/main.js
git commit -m "feat: introduce design system Bricolage Grotesque + palette ink/paper/navy-deep"
```

---

### Task 2: Fascia statistiche animata in home

**Model:** economico (sonnet/haiku) — markup, CSS e funzione JS già scritti per intero in questo task.

**Files:**
- Modify: `index.html:40-41` (inserimento nuova sezione tra hero e Chi Siamo)
- Modify: `css/style.css` (fine file, nuove regole `.stats-band` / `.stats-grid` / `.stat-item` / `.stat-number` / `.stat-suffix` / `.stat-label` + media query)
- Modify: `js/main.js:38-41` (chiamata `initStatsCounters()`), fine file (nuova funzione `initStatsCounters`)

**Interfaces:**
- Consumes: `--navy-deep`, font Bricolage Grotesque da Task 1; variabile globale `projectsData` (array, già popolato in `js/main.js:31` prima della chiamata).
- Produces: funzione globale `initStatsCounters()` (nessun parametro, nessun return) — non consumata da altri task di questo piano, ma deve restare disponibile per eventuali pagine future che vogliano riusare la stessa fascia.

- [ ] **Step 1: Inserire il markup della fascia statistiche in `index.html`**

Sostituisci:
```html
    </header>

    <section id="chi-siamo" class="section">
```
con:
```html
    </header>

    <section id="stats" class="stats-band">
        <div class="stats-grid">
            <div class="stat-item">
                <span class="stat-number" data-count="1986" data-format="year">1986</span>
                <span class="stat-label">Anno di fondazione</span>
            </div>
            <div class="stat-item">
                <span class="stat-number" data-count="40">0</span><span class="stat-suffix">+</span>
                <span class="stat-label">Anni di attività</span>
            </div>
            <div class="stat-item">
                <span class="stat-number" data-count-projects="true">0</span>
                <span class="stat-label">Progetti realizzati</span>
            </div>
            <div class="stat-item">
                <span class="stat-number" data-count="5">0</span>
                <span class="stat-label">Aree di competenza</span>
            </div>
        </div>
    </section>

    <section id="chi-siamo" class="section">
```

- [ ] **Step 2: Aggiungere le regole CSS della fascia statistiche**

In fondo a `css/style.css`, aggiungi:
```css

/* --- 12. FASCIA STATISTICHE --- */
.stats-band { background: var(--navy-deep); padding: 80px 10%; width: 100vw; margin-left: calc(-50vw + 50%); box-sizing: border-box; }
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 40px; max-width: 1200px; margin: 0 auto; text-align: center; }
.stat-item { display: flex; flex-direction: column; gap: 8px; align-items: center; }
.stat-number, .stat-suffix { font-family: 'Bricolage Grotesque', 'Manrope', sans-serif; font-weight: 800; font-size: clamp(2.5rem, 5vw, 4rem); color: #ffffff; line-height: 1; letter-spacing: -0.02em; }
.stat-label { color: rgba(255,255,255,0.7); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em; }

@media(max-width: 900px) {
    .stats-grid { grid-template-columns: repeat(2, 1fr); gap: 30px 20px; }
}
```

- [ ] **Step 3: Aggiungere la funzione `initStatsCounters` in `js/main.js`**

In fondo a `js/main.js`, aggiungi:
```js

function initStatsCounters() {
    const statsSection = document.querySelector('.stats-band');
    if (!statsSection) return;

    const projectCountEl = statsSection.querySelector('[data-count-projects]');
    if (projectCountEl) projectCountEl.setAttribute('data-count', String(projectsData.length));

    const counters = statsSection.querySelectorAll('.stat-number[data-count]');

    const animateCounter = (el) => {
        if (el.getAttribute('data-format') === 'year') return;
        const target = parseInt(el.getAttribute('data-count'), 10);
        if (isNaN(target)) return;
        const duration = 1200;
        const start = performance.now();
        const step = (now) => {
            const progress = Math.min((now - start) / duration, 1);
            el.textContent = Math.floor(progress * target);
            if (progress < 1) requestAnimationFrame(step);
            else el.textContent = String(target);
        };
        requestAnimationFrame(step);
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                counters.forEach(animateCounter);
                observer.disconnect();
            }
        });
    }, { threshold: 0.3 });

    observer.observe(statsSection);
}
```

- [ ] **Step 4: Chiamare `initStatsCounters()` nell'inizializzazione**

In `js/main.js`, sostituisci:
```js
        renderNews();
        renderProjects('tutti');
        
        initNavbar();
```
con:
```js
        renderNews();
        renderProjects('tutti');
        
        initNavbar();
        initStatsCounters();
```

- [ ] **Step 5: Verificare nel browser**

Naviga su `http://localhost:8123/index.html`. Esegui:
```js
document.querySelector('.stats-band') ? 'presente' : 'ASSENTE';
```
Poi forza manualmente l'osserver scrollando la sezione in viewport (`scroll_to` sull'elemento `.stats-band` o `computer` scroll) e attendi ~1.5s, poi:
```js
[...document.querySelectorAll('.stat-number[data-count]')].map(el => el.textContent);
```
Risultato atteso: `["1986", "40", <numero progetti reale, es. "28">, "5"]` (non più `"0"`).

Controlla la console: nessun errore.

- [ ] **Step 6: Commit**

```bash
git add index.html css/style.css js/main.js
git commit -m "feat: aggiunge fascia statistiche animata in home"
```

---

### Task 3: Griglia editoriale progetti in home (sostituisce lo slider)

**Model:** economico (sonnet/haiku) — sostituzione di markup/funzione con codice già scritto qui.

**Files:**
- Modify: `index.html:139-154` (sezione `#progetti`)
- Modify: `css/style.css:115-148` (rimuove `.projects-slider-container`, `.projects-grid`, `.slider-btn*`; aggiunge `.projects-editorial-grid`), `css/style.css:219,221` (rimuove riferimenti a `.projects-grid` nella media query mobile)
- Modify: `js/main.js:162-185` (funzione `renderProjects`), `js/main.js:214-217` (rimuove `window.scrollSlider`)

**Interfaces:**
- Consumes: `projectsData` (array globale, già ordinato per `endYear` decrescente prima della chiamata a `renderProjects`); funzione esistente `window.openProject(index)` (non modificata, resta il modo per aprire il dettaglio dal click sulla card).
- Produces: `renderProjects(filterTag)` mantiene la stessa firma e viene chiamata dagli stessi punti (`js/main.js` init, e da `window.filterProjects` in `elenco-progetti.html` — quel path, `#projects-grid-full`, NON viene toccato da questo task).

- [ ] **Step 1: Sostituire il markup della sezione Progetti in `index.html`**

Sostituisci:
```html
    <section id="progetti" class="section">
        <div class="fade-element" style="text-align:center;">
            <h2 style="font-size:3rem; margin-bottom:10px;">Progetti</h2>
            <p></p>
        </div>

        <div class="projects-slider-container fade-element">
            <button class="slider-btn prev" onclick="scrollSlider(-1)">&#10094;</button>
            <div class="projects-grid" id="projects-slider"></div>
            <button class="slider-btn next" onclick="scrollSlider(1)">&#10095;</button>
        </div>
        
        <div class="fade-element" style="text-align: center; margin-top: 40px; width: 100%;">
            <a href="elenco-progetti.html" class="filter-btn" style="display: inline-block; text-decoration: none;">Visualizza Archivio Progetti Completo ➔</a>
        </div>
    </section>
```
con:
```html
    <section id="progetti" class="section">
        <div class="fade-element" style="text-align:center;">
            <h2 style="font-size:3rem; margin-bottom:10px;">Progetti</h2>
            <p></p>
        </div>

        <div class="projects-editorial-grid fade-element" id="projects-editorial-grid"></div>

        <div class="fade-element" style="text-align: center; margin-top: 40px; width: 100%;">
            <a href="elenco-progetti.html" class="filter-btn" style="display: inline-block; text-decoration: none;">Visualizza Archivio Progetti Completo ➔</a>
        </div>
    </section>
```

- [ ] **Step 2: Sostituire le regole CSS dello slider con la griglia editoriale**

In `css/style.css`, sostituisci:
```css
.projects-slider-container { position: relative; width: 100%; display: flex; align-items: center; margin-top: 30px; }
.projects-grid { display: flex; gap: 30px; overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: 20px; scroll-behavior: smooth; -ms-overflow-style: none; scrollbar-width: none; }
.projects-grid::-webkit-scrollbar { display: none; }
```
con:
```css
.projects-editorial-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    max-width: 1400px;
    margin: 40px auto 0;
}
.projects-editorial-grid .project-card:first-child { grid-column: span 2; grid-row: span 2; }
.projects-editorial-grid .project-card:first-child .p-img-box { height: 100%; min-height: 420px; }
```

Sostituisci:
```css
.slider-btn {
    background: var(--blue); color: white; border: none; border-radius: 50%; width: 50px; height: 50px; font-size: 1.5rem; cursor: pointer;
    position: absolute; z-index: 10; box-shadow: 0 4px 10px rgba(0,0,0,0.2); display: flex; align-items: center; justify-content: center; transition: background 0.3s, transform 0.2s;
}
.slider-btn:hover { background: #002d54; transform: scale(1.1); }
.slider-btn.prev { left: -25px; }
.slider-btn.next { right: -25px; }
```
con: (rimuovi il blocco, nessuna riga sostitutiva — lo slider non esiste più in home)

- [ ] **Step 3: Rimuovere i riferimenti a `.projects-grid` dalla media query mobile e aggiungere quelli per la nuova griglia**

Nello stesso file, sostituisci:
```css
    .division-block, .division-block.reversed, .footer-grid, .text-cols { grid-template-columns: 1fr; }
    .div-img-wrapper { height: 300px; position: relative; top: 0; margin-top: 30px;}
    .hero h1 { font-size: 3rem; }
    .projects-grid { padding: 0 10px 20px 10px; gap: 15px; }
    
    .projects-grid .project-card { min-width: 220px; width: 220px; scroll-snap-align: start; }
    .news-grid .project-card { min-width: unset; width: 100%; }
```
con:
```css
    .division-block, .division-block.reversed, .footer-grid, .text-cols { grid-template-columns: 1fr; }
    .div-img-wrapper { height: 300px; position: relative; top: 0; margin-top: 30px;}
    .hero h1 { font-size: 3rem; }
    .projects-editorial-grid { grid-template-columns: 1fr; gap: 15px; }
    .projects-editorial-grid .project-card:first-child { grid-column: span 1; grid-row: span 1; }
    .projects-editorial-grid .project-card:first-child .p-img-box { min-height: 220px; }
    .news-grid .project-card { min-width: unset; width: 100%; }
```

Poi, più in basso nella stessa media query, sostituisci:
```css
    .slider-btn { display: flex; width: 40px; height: 40px; font-size: 1.2rem; }
    .slider-btn.prev { left: 5px; } 
    .slider-btn.next { right: 5px; }
```
con: (rimuovi il blocco — `.slider-btn` non esiste più)

- [ ] **Step 4: Aggiornare `renderProjects` in `js/main.js` per popolare la griglia editoriale**

Sostituisci:
```js
function renderProjects(filterTag = 'tutti') {
    const sliderContainer = document.getElementById('projects-slider');
    const gridContainer = document.getElementById('projects-grid-full');
    
    if (sliderContainer) {
        sliderContainer.innerHTML = ''; 
        const recentProjects = projectsData.slice(0, 6); 
        
        recentProjects.forEach(p => {
            const originalIndex = projectsData.indexOf(p);
            sliderContainer.innerHTML += `
                <div class="project-card" onclick="openProject(${originalIndex})">
                    <div class="p-img-box">
                        <img src="${p.images[0]}" alt="${p.title}" loading="lazy" decoding="async" onerror="this.style.display='none'">
                        <div class="hover-reveal">APRI SCHEDA</div>
                    </div>
                    <div class="p-content">
                        <span style="font-size: 0.8rem; color: #888; font-weight: 600;">Anno: ${p.endYear}</span>
                        <h4 style="color:var(--blue); margin: 5px 0 5px 0;">${p.title}</h4>
                        <p style="margin:0; font-size:0.9rem">${p.cardSubtitle}</p>
                    </div>
                </div>`;
        });
    }
```
con:
```js
function renderProjects(filterTag = 'tutti') {
    const editorialGrid = document.getElementById('projects-editorial-grid');
    const gridContainer = document.getElementById('projects-grid-full');
    
    if (editorialGrid) {
        editorialGrid.innerHTML = '';
        const featured = projectsData.slice(0, 5);
        
        featured.forEach(p => {
            const originalIndex = projectsData.indexOf(p);
            editorialGrid.innerHTML += `
                <div class="project-card" onclick="openProject(${originalIndex})">
                    <div class="p-img-box">
                        <img src="${p.images[0]}" alt="${p.title}" loading="lazy" decoding="async" onerror="this.style.display='none'">
                        <div class="hover-reveal">APRI SCHEDA</div>
                    </div>
                    <div class="p-content">
                        <span style="font-size: 0.8rem; color: #888; font-weight: 600;">Anno: ${p.endYear}</span>
                        <h4 style="margin: 5px 0 5px 0;">${p.title}</h4>
                        <p style="margin:0; font-size:0.9rem">${p.cardSubtitle}</p>
                    </div>
                </div>`;
        });
    }
```

(il blocco `if (gridContainer) { ... }` successivo resta invariato, non toccarlo)

- [ ] **Step 5: Rimuovere `window.scrollSlider`, ora inutilizzata**

In `js/main.js`, sostituisci:
```js
window.scrollSlider = function(direction) {
    const slider = document.getElementById('projects-slider');
    if(slider) slider.scrollBy({ left: direction * 380, behavior: 'smooth' });
};

let currentProjectIndex = 0;
```
con:
```js
let currentProjectIndex = 0;
```

- [ ] **Step 6: Verificare nel browser**

Naviga su `http://localhost:8123/index.html`. Esegui:
```js
JSON.stringify({
    count: document.querySelectorAll('#projects-editorial-grid .project-card').length,
    sliderGone: document.getElementById('projects-slider') === null,
    scrollSliderGone: typeof window.scrollSlider === 'undefined'
});
```
Risultato atteso: `count` = 5, `sliderGone` = `true`, `scrollSliderGone` = `true`.

Poi clicca (o esegui `openProject(0)` via `javascript_tool`) sulla prima card e verifica che la modale si apra con i dati del progetto (`document.getElementById('projectModal').classList.contains('active')` deve essere `true`).

Controlla la console: nessun errore.

- [ ] **Step 7: Commit**

```bash
git add index.html css/style.css js/main.js
git commit -m "feat: sostituisce lo slider progetti in home con una griglia editoriale"
```

---

### Task 4: Restyling card, navigazione e footer (piatto, hairline, coerente col nuovo sistema)

**Model:** economico (sonnet/haiku) — solo regole CSS puntuali, valori già specificati.

**Files:**
- Modify: `css/style.css:65` (già presente, non tocca), `css/style.css:51-59` (`.nav-links a`), `css/style.css:122-128` (`.project-card`), `css/style.css:176` (`.footer-sec`)

**Interfaces:**
- Consumes: `--navy-deep` da Task 1.
- Produces: nessuna nuova interfaccia — solo valori visivi. Essendo nav (`header.html`) e footer (`footer.html`) condivisi via `js/main.js` (iniettati in ogni pagina), questo task cambia l'aspetto di nav/footer su **tutte** le 7 pagine, non solo sulla home: è previsto e coerente con la spec ("nav/footer condivisi ereditano il restyling").

- [ ] **Step 1: Letter-spacing sulle voci di navigazione**

In `css/style.css`, sostituisci:
```css
.nav-links a {
    text-decoration: none; 
    color: #ffffff; 
    font-weight: 600; 
    margin-left: 30px; 
    font-size: 0.95rem; 
    text-transform: uppercase; 
    text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    transition: color 0.3s;
}
```
con:
```css
.nav-links a {
    text-decoration: none; 
    color: #ffffff; 
    font-weight: 600; 
    margin-left: 30px; 
    font-size: 0.9rem; 
    letter-spacing: 0.08em;
    text-transform: uppercase; 
    text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    transition: color 0.3s;
}
```

- [ ] **Step 2: Card più piatte (hairline invece di ombra pesante)**

Sostituisci:
```css
.project-card {
    background: white; border-radius: 16px; overflow: hidden; cursor: pointer;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05); transition: transform 0.3s;
    min-width: 350px; flex: 0 0 auto; scroll-snap-align: start; animation: fadeIn 0.5s ease-out forwards;
}
```
con:
```css
.project-card {
    background: white; border-radius: 8px; overflow: hidden; cursor: pointer;
    border: 1px solid #e5e5e0; box-shadow: none; transition: transform 0.3s, border-color 0.3s;
    min-width: 350px; flex: 0 0 auto; scroll-snap-align: start; animation: fadeIn 0.5s ease-out forwards;
}
```

Poi, poco sotto, sostituisci:
```css
.project-card:hover { transform: translateY(-10px); }
```
con:
```css
.project-card:hover { transform: translateY(-6px); border-color: var(--blue); }
```

- [ ] **Step 3: Footer sullo stesso navy della fascia statistiche**

Sostituisci:
```css
.footer-sec { background: #111; color: #888; padding: 60px 10%; }
```
con:
```css
.footer-sec { background: var(--navy-deep); color: #888; padding: 60px 10%; }
```

- [ ] **Step 4: Verificare nel browser**

Naviga su `http://localhost:8123/index.html`. Esegui:
```js
JSON.stringify({
    navLetterSpacing: getComputedStyle(document.querySelector('.nav-links a')).letterSpacing,
    cardBorder: getComputedStyle(document.querySelector('.project-card')).borderColor,
    footerBg: getComputedStyle(document.querySelector('.footer-sec')).backgroundColor
});
```
Risultato atteso: `cardBorder` non è più trasparente/bianco (dev'essere un grigio chiaro, es. `rgb(229, 229, 224)`), `footerBg` è `rgb(7, 27, 46)`.

Poi naviga anche su `http://localhost:8123/chi-siamo.html` e controlla che nav e footer si vedano correttamente (stesso stile) e che non ci siano errori console — il corpo della pagina non è ancora restyled (previsto, sarà nel prossimo piano) ma nav/footer devono apparire coerenti col nuovo stile.

- [ ] **Step 5: Commit**

```bash
git add css/style.css
git commit -m "feat: restyling piatto per card, nav e footer coerente col nuovo design system"
```

---

### Task 5: Movimento — reveal GSAP su `.fade-element`/`.reveal-img` e parallax hero

**Model:** economico (sonnet/haiku) — funzione già scritta per intero in questo task, nessuna decisione di design da prendere.

> **Nota per chi esegue questo task:** la spec di design presume che le classi `.fade-element` e `.reveal-img` (già presenti in `index.html` e nelle altre pagine) siano animate via GSAP ScrollTrigger — il README del progetto lo lascia intendere. **Non è così**: in `js/main.js` non esiste nessuna chiamata a `gsap.*` o `ScrollTrigger.*` che le animi; sono classi CSS senza alcuna regola associata (verificato leggendo l'intero `css/style.css` e `js/main.js`). Questo task implementa l'animazione da zero, non la "raffina".

**Files:**
- Modify: `js/main.js` (fine file: nuova funzione `initScrollReveals`; dentro la catena di inizializzazione: chiamata alla funzione)

**Interfaces:**
- Consumes: `gsap`, `ScrollTrigger` (globali da CDN, già caricati con `defer` nell'head — se assenti la funzione non fa nulla e gli elementi restano visibili come oggi, nessuna regressione).
- Produces: funzione globale `initScrollReveals()` (nessun parametro, nessun return).

- [ ] **Step 1: Aggiungere `initScrollReveals` in `js/main.js`**

In fondo al file, aggiungi:
```js

function initScrollReveals() {
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;
    gsap.registerPlugin(ScrollTrigger);

    gsap.utils.toArray('.fade-element').forEach((el) => {
        gsap.fromTo(el,
            { opacity: 0, y: 30 },
            {
                opacity: 1, y: 0, duration: 0.8, ease: 'power2.out',
                scrollTrigger: { trigger: el, start: 'top 85%', toggleActions: 'play none none none' }
            }
        );
    });

    gsap.utils.toArray('.reveal-img').forEach((el) => {
        gsap.fromTo(el,
            { opacity: 0, scale: 0.96 },
            {
                opacity: 1, scale: 1, duration: 1, ease: 'power2.out',
                scrollTrigger: { trigger: el, start: 'top 85%', toggleActions: 'play none none none' }
            }
        );
    });

    const heroBg = document.querySelector('.hero-bg');
    if (heroBg) {
        gsap.to(heroBg, {
            yPercent: 15,
            ease: 'none',
            scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
        });
    }
}
```

- [ ] **Step 2: Chiamare `initScrollReveals()` nell'inizializzazione**

Sostituisci:
```js
        renderNews();
        renderProjects('tutti');
        
        initNavbar();
        initStatsCounters();
```
con:
```js
        renderNews();
        renderProjects('tutti');
        
        initNavbar();
        initStatsCounters();
        initScrollReveals();
```

- [ ] **Step 3: Verificare nel browser**

Naviga su `http://localhost:8123/index.html`. Esegui subito dopo il caricamento:
```js
JSON.stringify({
    chiSiamoOpacity: getComputedStyle(document.querySelector('#chi-siamo .fade-element')).opacity
});
```
Risultato atteso: `"0"` (la sezione Chi Siamo è sotto la piega, non ancora animata).

Poi scrolla la pagina fino a portare `#chi-siamo` in viewport (`scroll_to` o `computer` scroll ripetuto), attendi ~1s, e ripeti la stessa lettura: deve essere `"1"`.

Controlla la console: nessun errore (in particolare nessun errore relativo a `ScrollTrigger` non definito — se GSAP non si carica per qualche motivo di rete, la funzione deve uscire silenziosamente e gli elementi restare visibili di default, non bloccare la pagina).

- [ ] **Step 4: Commit**

```bash
git add js/main.js
git commit -m "feat: aggiunge reveal GSAP ScrollTrigger e parallax hero in home"
```

---

### Task 6: Verifica end-to-end del pilota e checkpoint di revisione

**Model:** capace (opus/sonnet di punta) — richiede giudizio visivo complessivo, non solo eseguire comandi.

**Files:** nessuna modifica — solo verifica.

**Interfaces:** Consumes: tutto quanto prodotto dai Task 1-5. Produces: nessuna modifica di codice; l'esito è un report (screenshot + note) per l'utente.

- [ ] **Step 1: Avviare il server e caricare la home**

`preview_start` con `name: "tecnitalia-site"`, poi `navigate` su `http://localhost:8123/index.html`.

- [ ] **Step 2: Controllo console ed errori di rete**

`read_console_messages` (`onlyErrors: true`) → deve essere vuoto.
`read_network_requests` → nessuna risorsa in 404 (in particolare font Bricolage Grotesque, immagini progetti).

- [ ] **Step 3: Screenshot desktop**

`computer` screenshot della viewport iniziale (hero + fascia statistiche visibile scrollando). Verificare a occhio: titoli in Bricolage Grotesque e colore ink (non più blu), fascia statistiche su sfondo navy con numeri animati, griglia progetti editoriale (non più slider) con la prima card più grande delle altre, sezioni che appaiono con un leggero fade/slide allo scroll (Task 5) invece di essere semplicemente statiche.

- [ ] **Step 4: Screenshot mobile**

`resize_window` preset `mobile`, ricaricare la pagina, screenshot. Verificare: fascia statistiche a 2 colonne, griglia progetti a colonna unica, nav hamburger ancora funzionante (aprire/chiudere via click o `dispatchEvent` come già validato in precedenza su questo branch). Ripristinare `resize_window` preset `desktop` al termine.

- [ ] **Step 5: Verifica funzionale rapida**

- Aprire una card progetto dalla griglia editoriale → la modale si apre con i dati corretti e si chiude con Esc (comportamento già esistente, verificarne solo la sopravvivenza dopo il restyling).
- Scrollare fino al footer → verificare che il form contatti sia ancora presente e visivamente coerente (non serve inviare un'email di prova).

- [ ] **Step 6: Report all'utente**

Riassumere in chat (con screenshot allegati) cosa è cambiato visivamente sulla home, segnalare eventuali problemi trovati e NON risolti nei task precedenti, e chiedere conferma esplicita prima di procedere con un piano separato per estendere lo stesso linguaggio visivo alle altre 6 pagine (chi-siamo con timeline, elenco-progetti con griglia/modale restyled, dettaglio-ingegneria/servizi, archivio-news, news-singola).

Non fare commit in questo task (solo verifica).
