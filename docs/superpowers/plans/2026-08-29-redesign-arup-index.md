# Rimpaginazione Home (index.html) in stile Arup — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Rimpaginare index.html con un'impaginazione editoriale ispirata ad arup.com (non una copia): hero minimale con dichiarazione forte, blocco filosofia, un singolo progetto in evidenza a piena larghezza al posto della griglia di 5 card, colore brand corretto sul colore reale del logo, logo bianco per contrasto sullo sfondo scuro dell'hero.

**Architecture:** Sito statico, nessun build step. Un solo task che tocca index.html, css/style.css, js/main.js, header.html. Nessuna nuova pagina, nessuna nuova dipendenza.

**Tech Stack:** HTML/CSS/JS puro, GSAP+ScrollTrigger già presenti (initScrollReveals in js/main.js gestisce già `.fade-element`/`.reveal-img`), font Bricolage Grotesque + Manrope già importati.

## Global Constraints

- Colore brand: sostituire `--blue: #00427A;` con `--blue: #004F87;` in `css/style.css:3` — è il colore reale dominante del logo (verificato via analisi pixel di `assets/img/logo.png`: rgba(0,79,135) è il colore di gran lunga più frequente). Nessun altro punto del CSS va toccato per questo valore: essendo una CSS variable, l'aggiornamento si propaga automaticamente a tutti gli usi (`nav.scrolled .nav-links a:hover`, `.filter-btn`, `.project-card:hover`, `.member`, `.eyebrow`, `.timeline`, ecc.).
- Logo bianco già pronto: `assets/img/logo-white.png` (stesso identico logo, pixel non trasparenti resi bianco puro, alpha channel intatto — generato e verificato su sfondo navy in questa sessione). Non rigenerarlo, usarlo così com'è.
- Testo "chi siamo" (storia dell'azienda): NON modificare — l'utente ha chiesto esplicitamente di mantenere il testo esistente (index.html sezione `#chi-siamo`, e il file chi-siamo.html non è in scope di questo task).
- Testo dei servizi Ingegneria: la nuova copy DEVE riflettere l'attività reale dell'azienda risultante da `data/projects.json` (28 progetti): la stragrande maggioranza è bonifica di suoli contaminati, una parte consistente è bonifica/rimozione amianto (MCA/FAV), e la Direzione Lavori è il ruolo ricorrente su quasi tutti i progetti. Acque di falda ed emissioni sono temi presenti ma minoritari. La copy fornita in Task 1 Step 3 rispetta questo bilanciamento — non inventare percentuali o numeri non presenti nei dati.
- Non inventare virgolette/testimonianze attribuite a persone reali (i membri del team) — questo task non tocca la sezione Team.
- Non toccare `chi-siamo.html`, `dettaglio-ingegneria.html`, `dettaglio-servizi.html`, `elenco-progetti.html`, `archivio-news.html`, `news-singola.html`, `footer.html` — sono fuori scope, verranno affrontate una alla volta in piani successivi.
- Il progetto in evidenza deve usare dati reali e verbatim da `data/projects.json` (titolo "Nuova Scuola Politecnica", committente "Università di Genova", importo "ca. 260.000.000 €", immagine `./assets/img/genova1.jpg`) — non alterare questi valori.
- Mantenere l'iniezione di header/footer via fetch in js/main.js (nav-placeholder/footer-placeholder) intatta.
- Mantenere `.fade-element`/`.reveal-img` sulle nuove sezioni dove ha senso, così che `initScrollReveals()` (già esistente in js/main.js) le animi senza modifiche a quella funzione.

---

### Task 1: Hero, blocco filosofia, copy Ingegneria, progetto in evidenza, colore/logo

**Files:**
- Modify: `css/style.css` (variabile `--blue`; nuovi stili per hero ristilizzato, blocco statement, componente progetto in evidenza, logo bianco/colore in nav)
- Modify: `index.html` (hero, nuovo blocco statement, testo sezione Ingegneria, sezione Progetti sostituita da progetto in evidenza)
- Modify: `js/main.js` (piccola funzione per aprire la modale del progetto in evidenza cercandolo per titolo in `projectsData`, così l'indice non è mai hardcoded)
- Modify: `header.html` (doppio logo: bianco + colore, toggle via CSS su `nav.scrolled`)

**Interfaces:**
- Consumes: `projectsData` (array globale già popolato in js/main.js da `data/projects.json`), funzione già esistente `window.openProject(index)`.
- Produces: `window.openFeaturedProject()` — nuova funzione globale che cerca `projectsData.findIndex(p => p.title === "Nuova Scuola Politecnica")` e, se trovata, chiama `window.openProject(idx)`; se non trovata (guardia per il caso in cui il progetto venga rinominato/rimosso in futuro da projects.json), non fa nulla silenziosamente (nessun errore in console).

- [ ] **Step 1: Colore brand e logo bianco in nav**

In `css/style.css:3`, cambia:
```css
--blue: #00427A;
```
in:
```css
--blue: #004F87;
```

In `header.html`, sostituisci il singolo `<img>` del logo con due immagini sovrapposte, una bianca (visibile di default, sopra l'hero trasparente) e una a colori (visibile quando la nav è scrollata):
```html
<a href="index.html" class="logo-container">
    <img src="./assets/img/logo-white.png" alt="Tecnitalia Group" class="logo-img logo-img-white">
    <img src="./assets/img/logo.png" alt="Tecnitalia Group" class="logo-img logo-img-color">
</a>
```

In `css/style.css`, subito dopo la regola esistente `.logo-container { ... }` (circa riga 50), aggiungi:
```css
.logo-container { display: flex; align-items: center; }
.logo-img-color { display: none; }
nav.scrolled .logo-img-white { display: none; }
nav.scrolled .logo-img-color { display: block; }
```
Nota: `.logo-container` ha già `display: block` nella regola esistente — sovrascrivilo con `display: flex` (stessa specificità, l'ordine nel file decide: questa nuova regola va DOPO quella esistente) così le due `<img>` si sovrappongono in flusso normale senza position:absolute (una sola è visibile alla volta, quindi non serve stacking assoluto). Verifica che `.logo-img` esistente (`height: 70px; width: auto;` e la variante scrolled `height: 50px`) continui ad applicarsi a entrambe le immagini (si applica automaticamente perché entrambe hanno la classe `logo-img`).

- [ ] **Step 2: Hero ristilizzato con nuova headline**

In `index.html`, sostituisci il contenuto dell'hero (righe 33-40 circa):
```html
<header class="hero">
    <div class="hero-bg" style="background-image: url('./assets/img/scavo.jpg');"></div>
    <div class="hero-overlay"></div>
    <div class="hero-text" id="hero-content">
        <h1>Tecnitalia Group</h1>
        <p>Dal 1986, Ingegneria e Ambiente.</p>
    </div>
</header>
```
con:
```html
<header class="hero">
    <div class="hero-bg" style="background-image: url('./assets/img/scavo.jpg');"></div>
    <div class="hero-overlay"></div>
    <div class="hero-text" id="hero-content">
        <h1>Bonifichiamo il suolo.<br>Costruiamo ciò che verrà.</h1>
        <p>Dal 1986 progettiamo e dirigiamo bonifiche di suoli, rimozione amianto e demolizioni per le aree industriali che cambiano volto.</p>
        <a href="chi-siamo.html" class="text-link hero-cta">La nostra storia ➔</a>
    </div>
</header>
```
In `css/style.css`, sezione `/* --- 4. HERO (Home) --- */` (circa riga 88-94), aggiorna la tipografia per una scala più grande ed editoriale e aggiungi lo stile del link CTA su sfondo scuro:
```css
.hero-text { position: relative; z-index: 3; color: white; text-align: center; max-width: 900px; padding: 20px; }
.hero h1 { color: #ffffff; font-size: clamp(2.8rem, 7vw, 5.5rem); line-height: 1.05; margin-bottom: 24px; text-shadow: 0 10px 30px rgba(0,0,0,0.5); }
.hero-text p { color: #ffffff; font-size: 1.3rem; max-width: 640px; margin: 0 auto 30px; text-shadow: 0 5px 15px rgba(0,0,0,0.5); }
.hero-cta { color: #ffffff !important; }
.hero-cta:hover { color: #ffffff !important; border-color: #ffffff !important; }
```
(Il `!important` è necessario perché `.text-link` di base usa `color: var(--ink)`, illeggibile su sfondo scuro; qui serve lo stesso trattamento bianco dell'h1/p sovrastanti, non il trattamento standard del link.)

- [ ] **Step 3: Blocco filosofia (nuovo, tra hero e stats)**

In `index.html`, subito dopo la chiusura di `</header>` (fine hero) e prima di `<section id="stats" class="stats-band">`, inserisci una nuova sezione:
```html
<section class="statement-block">
    <p class="fade-element">Non bonifichiamo soltanto un terreno: restituiamo lo spazio per ciò che nascerà al suo posto.</p>
</section>
```
In `css/style.css`, aggiungi (vicino alla sezione HERO o STATS, in un punto coerente):
```css
.statement-block { padding: 100px 10% 60px; max-width: 900px; margin: 0 auto; text-align: center; }
.statement-block p { font-family: 'Bricolage Grotesque', 'Manrope', sans-serif; font-weight: 700; font-size: clamp(1.6rem, 3.2vw, 2.6rem); line-height: 1.3; color: var(--ink); margin: 0; }
```

- [ ] **Step 4: Riscrittura copy sezione Ingegneria (home)**

In `index.html`, dentro `<section id="ingegneria">`, sostituisci il paragrafo introduttivo e la lista (righe ~127-135):
```html
<p>Grazie all'ormai trentennale esperienza, supportata da studio e ricerca costanti, offriamo un servizio completo. Dalla fine degli anni '90 ci siamo specializzati nel recupero delle aree dismesse e nelle bonifiche.</p>
<p><strong>Tematiche Ambientali (Cosa facciamo):</strong></p>
<ul>
    <li>Trattamenti di acque di approvvigionamento, rifiuto e reflui particolari.</li>
    <li>Trattamenti delle emissioni gassose.</li>
    <li>Gestione di rifiuti speciali, urbani e flussi particolari.</li>
    <li>Recupero delle aree dismesse e bonifica di siti contaminati.</li>
    <li>Supporto nella compravendita di siti industriali.</li>
</ul>
```
con:
```html
<p>Progettiamo e dirigiamo interventi di bonifica dei suoli contaminati, rimozione di materiali contenenti amianto (MCA e FAV) e assumiamo il ruolo di Direzione Lavori sui cantieri più complessi: dal 1986 è il cuore della nostra attività.</p>
<p><strong>Cosa facciamo:</strong></p>
<ul>
    <li>Bonifica di suoli, acque di falda e siti contaminati.</li>
    <li>Bonifica e rimozione di amianto (MCA) e Fibre Artificiali Vetrose (FAV).</li>
    <li>Direzione Lavori e Coordinamento Sicurezza nei cantieri di bonifica e demolizione.</li>
    <li>Trattamento di acque ed emissioni industriali.</li>
    <li>Due Diligence ambientale nella compravendita di siti industriali.</li>
</ul>
```
Non toccare il resto della sezione (span eyebrow, h3, link, immagine).

- [ ] **Step 5: Progetto in evidenza (sostituisce la griglia di 5 progetti)**

In `index.html`, sostituisci l'intera `<section id="progetti">` (righe ~164-176):
```html
<section id="progetti" class="section">
    <div class="fade-element" style="text-align:center;">
        <span class="eyebrow">05 — Progetti</span>
        <h2 style="font-size:3rem; margin-bottom:10px;">Progetti</h2>
        <p></p>
    </div>

    <div class="projects-editorial-grid fade-element" id="projects-editorial-grid"></div>
    
    <div class="fade-element" style="text-align: center; margin-top: 40px; width: 100%;">
        <a href="elenco-progetti.html" class="text-link">Visualizza Archivio Progetti Completo ➔</a>
    </div>
</section>
```
con:
```html
<section id="progetti" class="section">
    <div class="fade-element" style="text-align:center; margin-bottom:50px;">
        <span class="eyebrow">05 — Progetti</span>
        <h2 style="font-size:3rem; margin-bottom:10px;">Un progetto</h2>
    </div>

    <div class="featured-project fade-element" onclick="openFeaturedProject()" role="button" tabindex="0" onkeydown="if(event.key==='Enter')openFeaturedProject()">
        <div class="featured-project-img">
            <img src="./assets/img/genova1.jpg" alt="Nuova Scuola Politecnica di Genova">
        </div>
        <div class="featured-project-text">
            <span class="eyebrow">Progetto in corso</span>
            <h3>La bonifica dell'amianto naturale per la nuova Scuola Politecnica di Genova</h3>
            <p>Nel sito della nuova sede del Politecnico di Genova dirigiamo le attività di scavo in presenza di amianto naturale (Tremolite), con posa in opera di un capping e valutazione della recuperabilità in sito dei terreni scavati.</p>
            <div class="featured-project-meta">
                <div><strong>Committente</strong><span>Università di Genova</span></div>
                <div><strong>Importo</strong><span>ca. 260.000.000 €</span></div>
                <div><strong>Ruolo</strong><span>Direzione Lavori di bonifica suoli contenenti amianto</span></div>
            </div>
            <span class="text-link">Scopri la scheda completa ➔</span>
        </div>
    </div>

    <div class="fade-element" style="text-align: center; margin-top: 40px; width: 100%;">
        <a href="elenco-progetti.html" class="text-link">Visualizza Archivio Progetti Completo ➔</a>
    </div>
</section>
```
Nota: rimuovendo `<div class="projects-editorial-grid fade-element" id="projects-editorial-grid"></div>` dalla home, la chiamata `renderProjects('tutti')` in js/main.js (che popola sia `#projects-editorial-grid` che `#projects-grid-full`) userà `document.getElementById('projects-editorial-grid')` che ora sarà `null` su questa pagina — verifica che quel ramo della funzione in js/main.js sia già guardato con un controllo `if (container)` prima di scrivere (se non lo è, la funzione lancerebbe un errore che romperebbe anche il rendering della sezione news sulla stessa pagina). Se manca la guardia, aggiungila senza alterare il comportamento su elenco-progetti.html.

In `css/style.css`, aggiungi il nuovo componente:
```css
.featured-project { display: grid; grid-template-columns: 1.1fr 1fr; gap: 60px; align-items: center; max-width: 1300px; margin: 0 auto; cursor: pointer; }
.featured-project-img { width: 100%; height: 500px; border-radius: 12px; overflow: hidden; }
.featured-project-img img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease; }
.featured-project:hover .featured-project-img img { transform: scale(1.04); }
.featured-project-text h3 { font-size: clamp(1.8rem, 3vw, 2.4rem); line-height: 1.2; margin: 10px 0 20px; }
.featured-project-meta { display: flex; flex-wrap: wrap; gap: 30px; margin: 25px 0; padding: 20px 0; border-top: 1px solid #e5e5e0; border-bottom: 1px solid #e5e5e0; }
.featured-project-meta div { display: flex; flex-direction: column; gap: 4px; }
.featured-project-meta strong { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: #888; }
.featured-project-meta span { font-weight: 700; color: var(--ink); }
@media (max-width: 900px) {
    .featured-project { grid-template-columns: 1fr; gap: 30px; }
    .featured-project-img { height: 320px; }
}
```

In `js/main.js`, aggiungi (vicino a `window.openProject`/`window.closeProject`, non dentro nessun'altra funzione):
```javascript
window.openFeaturedProject = function() {
    const idx = projectsData.findIndex(p => p.title === "Nuova Scuola Politecnica");
    if (idx !== -1) window.openProject(idx);
};
```

- [ ] **Step 6: Verifica in browser**

Avvia il server locale (`mcp__Claude_Browser__preview_start` con name `tecnitalia-site`), naviga su `http://localhost:8123`, e verifica via `read_console_messages` (zero errori), `get_page_text`/`read_page` (nuovo hero, blocco statement, nuova copy ingegneria, progetto in evidenza tutti presenti con il testo esatto sopra), e via `javascript_tool` (getComputedStyle) che:
- `getComputedStyle(document.documentElement).getPropertyValue('--blue').trim()` sia `#004F87`
- il logo bianco sia visibile in cima alla pagina (nav non scrollata) e il logo a colori compaia dopo aver impostato `window.scrollY` / dopo che la classe `scrolled` viene applicata alla nav (verifica leggendo la classe della nav dopo uno scroll simulato, non fidarti dello screenshot se la pagina è scrollata — usa `read_page`/`getComputedStyle` come da nota tecnica di questa sessione).
- click su `.featured-project` apra la modale con titolo "Nuova Scuola Politecnica" (verifica `document.getElementById('m-title').textContent`).

- [ ] **Step 7: Commit**

```bash
git add index.html css/style.css js/main.js header.html
git commit -m "feat: rimpagina la home in stile editoriale (hero, statement, progetto in evidenza, colore brand reale)"
```
Non includere `assets/img/logo-white.png` in questo commit se già presente/staged da un commit precedente — verificare con `git status` prima di committare ed eventualmente includerlo se ancora non versionato.
