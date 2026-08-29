# Task 1 — Rimpaginazione Home (index.html) in stile Arup — Report

Piano eseguito: `docs/superpowers/plans/2026-08-29-redesign-arup-index.md`, Task 1, tutti i 7 step.

## Addendum — Fix round 2 (commit `4f14d6f`, dopo revisione live dell'utente su `deb54f2`)

L'utente ha revisionato dal vivo il risultato del round precedente e ha segnalato ("non mi piace nelle altre sezioni la striscia grossa blu. e il titolo così proprio brutto. ispirati a arup"): la fascia statistiche piena larghezza in `var(--navy-deep)` subito sotto l'hero, e i titoli di sezione in Bricolage Grotesque nero pesantissimo, giudicati "brutti" e poco ispirati allo stile arup.com. Il coordinatore ha confermato via screenshot entrambi i punti e ha fornito indicazioni implementative precise, seguite alla lettera.

**1. Font serif editoriale per i grandi titoli**
   - Aggiunto **Fraunces** (`opsz,wght@9..144,300..700`) alla stessa URL combinata di Google Fonts già usata per Bricolage Grotesque + Manrope, in **tutte** le pagine che avevano quell'import (`index.html`, `chi-siamo.html`, `archivio-news.html`, `elenco-progetti.html`, `dettaglio-servizi.html`, `dettaglio-ingegneria.html`, `news-singola.html`) — nessuna seconda richiesta di rete aggiunta.
   - Nuova classe `.display-serif` in `css/style.css` (dopo la regola globale `h1,h2,h3,h4`, mai modificata): `font-family: 'Fraunces', 'Bricolage Grotesque', serif; font-weight: 500; letter-spacing: -0.01em; line-height: 1.2;`.
   - Applicata come classe aggiuntiva (classi esistenti mantenute) a: `.hero h1`, `.statement-block p`, e ai 4 `<h2>` di sezione con `font-size:3rem` inline (Chi Siamo, Ultime News, I Nostri Progetti, Il Team). **Nessun h3/h4 toccato** (card, nomi team, sottotitoli division-block restano Bricolage Grotesque peso 800).
   - Dettaglio di specificità gestito: `.hero h1` e `.statement-block p` sono selettori compound (classe+tag) con specificità più alta di `.display-serif` da sola — dove la regola compound impostava già `font-family`/`font-weight` in conflitto (`.statement-block p` aveva `font-family: Bricolage...; font-weight: 700;` hardcoded), quei valori sono stati rimossi dalla regola compound per lasciare che `.display-serif` li fornisca. Il `line-height` dell'hero h1 è stato aggiustato direttamente nella regola `.hero h1` (1.05 → 1.1, la stessa regola vince per specificità), mentre gli h2 di sezione (nessun'altra regola con specificità più alta imposta line-height) ricevono 1.2 direttamente da `.display-serif`.

**2. Fascia statistiche: da striscia navy a layout leggero**
   - `index.html`: `<section id="stats" class="stats-band">` → `class="stats-row"` (markup interno/attributi `data-*` invariati).
   - `css/style.css`: `.stats-band` (navy piena larghezza) sostituita da `.stats-row` (sfondo `var(--paper)`, `border-bottom: 1px solid #e5e5e0`); `.stat-number`/`.stat-suffix` da bianco a `var(--ink)`; `.stat-label` da bianco trasparente a `#777`; aggiunti separatori verticali sottili tra le colonne (`border-right` su tutti tranne l'ultimo item). Nel breakpoint mobile esistente (`@media max-width:900px`, già presente, grid a 2 colonne) ho adattato i separatori per non lasciare un bordo verticale "orfano" a metà griglia: bordo destro solo sugli item di indice dispari, più un separatore orizzontale sopra la seconda riga.
   - `js/main.js`: `initStatsCounters()` — unica riga toccata, selettore `document.querySelector('.stats-band')` → `.stats-row`; nessun'altra modifica alla logica del contatore/IntersectionObserver.

**Verifica in browser** (nuova tab pulita ogni volta, stesso approccio con `{cache:'no-store'}` per bypassare il quirk di cache noto di questa sessione):
   - Zero errori console in tutti i test.
   - `getComputedStyle(document.querySelector('.hero h1')).fontFamily` → `"Fraunces, \"Bricolage Grotesque\", serif"`, `fontWeight` → `"500"`, `lineHeight` → `52.8px` (= 1.1 × 48px alla dimensione clamp risolta nel viewport di test).
   - Tutti e 4 gli `<h2>` di sezione (`Chi Siamo`, `Ultime News`, `I Nostri Progetti`, `Il Team`) hanno `.display-serif` con `fontFamily` Fraunces, `fontWeight` 500, `lineHeight` 57.6px (= 1.2 × 48px).
   - `h3` (es. "Tecnitalia Servizi") e `h4` (es. nome membro team) confermati **non toccati**: `fontFamily` = `"Bricolage Grotesque", Manrope, sans-serif`, `fontWeight` = `800`.
   - `getComputedStyle(document.querySelector('.stats-row')).backgroundColor` → `rgb(250, 250, 248)` (= `var(--paper)`, non più navy); `borderBottomColor` → `rgb(229, 229, 224)` (= `#e5e5e0`).
   - Screenshot dell'hero (una volta che il pannello browser è stato reso visibile — vedi nota sotto) conferma visivamente il titolo in un vero carattere serif editoriale, non più il sans-serif ultra-bold precedente.
   - **Limite di verifica riscontrato e documentato**: in questo giro la tab del browser di automazione è risultata "hidden" (pannello non visibile all'utente) per gran parte dei test; in questo stato `window.innerHeight`/`innerWidth` risultavano `0` e — più significativo — sia un `IntersectionObserver` di prova sia un semplice ciclo `requestAnimationFrame` **non scattavano affatto** (timeout), anche dopo aver portato la tab in primo piano. Questo ha impedito di osservare empiricamente l'animazione dei contatori (`initStatsCounters`) scattare allo scroll in questo ambiente. Non è imputabile alla modifica: la funzione `animateCounter`/`IntersectionObserver` in `js/main.js` non è stata toccata in alcun modo, l'unica riga cambiata è il selettore CSS (`.stats-band` → `.stats-row`), verificato risolvere correttamente l'elemento (`document.querySelector('.stats-row')` non null, nessun errore). Il rAF/IntersectionObserver bloccati sono coerenti con la sospensione del rendering quando il pannello di questo tool non è attivamente visualizzato (Page Visibility/compositor), un limite già noto di questa sessione (vedi note precedenti su screenshot vuoti/in timeout), non un difetto del sito.

**Commit**: `4f14d6f` — "feat: sostituisce la striscia blu delle statistiche con un layout leggero e introduce un font serif editoriale per i titoli principali" — file: `index.html`, `css/style.css`, `js/main.js`, `archivio-news.html`, `chi-siamo.html`, `dettaglio-ingegneria.html`, `dettaglio-servizi.html`, `elenco-progetti.html`, `news-singola.html` (9 file, 25 inserimenti, 20 rimozioni).

**Concern**: nessuno bloccante. L'unica nota è la limitazione di verifica sull'animazione dei contatori descritta sopra, dovuta al tooling di automazione di questa sessione e non al codice consegnato — la logica non è stata modificata e il selettore risolve correttamente l'elemento nel DOM reale.

## Addendum — Fix round 1 (commit `deb54f2`, dopo revisione live dell'utente su `1b8f3fb`)

L'utente ha revisionato dal vivo il risultato del commit `1b8f3fb` e ha chiesto due correzioni, entrambe dentro `index.html` / `css/style.css` / `js/main.js`:

1. **Titolo hero**: "voglio il titolo come prima" — l'`<h1>` è tornato a `Tecnitalia Group` (testo esatto del brand originale). Sottotitolo (`<p>`) e CTA `.hero-cta` introdotti nel Task 1 sono stati mantenuti invariati, come richiesto.

2. **Sezione Progetti**: l'utente ha giudicato negativamente sia l'idea di un singolo progetto in evidenza sia la foto di Genova usata ("fa schifo la foto"), chiedendo esplicitamente una striscia orizzontale scorrevole multi-progetto in stile arup.com ("Our Work"). Il blocco `.featured-project` (progetto Genova/Nuova Scuola Politecnica) è stato rimosso e sostituito da `.work-scroller` con 6 card.

   **Selezione immagini** — ho ispezionato con il tool Read le prime (e in alcuni casi seconde) foto di tutti i progetti candidati indicati dal coordinatore, per scartare quelle "brutte" (fango/trincee/detriti in primo piano o scansioni di planimetrie non fotografiche):
   - `sofer1.jpg` e `sofer2.jpg` (Ex Sofer, il progetto di valore più alto, 20.000.000 €): entrambe scartate (trincea di fango la prima, big-bags/pozzanghera la seconda) — **Ex Sofer escluso dalla striscia nonostante il valore economico più alto**, per assenza di una foto presentabile.
   - `bovisa1.jpg` (Oasi Bovisa): scartata, è una scansione di planimetria aerea, non una foto. `bovisa2.jpg`: rendering/illustrazione stilizzata con vignettatura, giudicata troppo ambigua per una card full-bleed — **Oasi Bovisa escluso**.
   - `reggiani1.jpg` (Area Ex Reggiani): scartata, è una scansione di planimetria con overlay colorati. `reggiani2.jpg`: foto reale buona (edificio con insegna "REGGIANI", cielo azzurro) — **usata come immagine di card tramite l'override `imageIndex: 1`** nella configurazione `workScrollerProjects` di `js/main.js`.
   - `feltrinelli1.jpg` (Ex Fratelli Feltrinelli): scartata, è uno screenshot di mappa satellitare. `feltrinelli2.jpg` sarebbe stata accettabile (edificio, cielo azzurro) ma il progetto è stato comunque escluso dalla selezione finale per valore economico più basso (ca. 1.000.000 €) rispetto ai 6 scelti.
   - `origoni1.jpg` (Ex Zincheria Origoni): accettabile ma cielo coperto e valore economico basso (ca. 500.000 €) — escluso a favore di candidati con valore/recency migliori.
   - `prada1.jpg` (Fondazione Prada) e `novaceta1.jpg` (Ex Novaceta): confermate ottime dal coordinatore, usate come prime due card.
   - `merlata1.jpg` (Cascina Merlata) e `binda1.jpg` (Ex Cartiere Binda): foto reali accettabili (silos su cielo azzurro; vista aerea di fabbricato riconoscibile, seppur granulosa) — incluse.
   - `prysmian1.jpg` (Ex Stabilimento Prysmian Group): foto reale accettabile (impianto di raffreddamento industriale su cielo azzurro) — incluso, valore/recency più recenti (2025) tra i candidati minori.

   **6 progetti finali nella striscia** (ordine come compaiono, valore e anno tra parentesi):
   1. Fondazione Prada (ca. 4.500.000 €, 2013) — `prada1.jpg`
   2. Ex Novaceta (ca. 12.000.000 €, 2025) — `novaceta1.jpg`
   3. Area Ex Reggiani (ca. 3.000.000 €, 2023) — `reggiani2.jpg`
   4. Cascina Merlata (ca. 2.000.000 €, 2013) — `merlata1.jpg`
   5. Ex Cartiere Binda (ca. 2.700.000 €, 2007) — `binda1.jpg`
   6. Ex Stabilimento Prysmian Group (ca. 1.500.000 €, 2025) — `prysmian1.jpg`

   "Nuova Scuola Politecnica" (Genova) è stata rimossa dalla striscia visuale come richiesto (entrambe le sue foto, `genova1.jpg`/`genova2.jpg`, erano già state segnalate come inadatte); resta comunque visibile e apribile dall'archivio progetti completo (`elenco-progetti.html`), non essendo stata toccata `data/projects.json`.

   **Implementazione**:
   - `index.html`: `<div class="featured-project" ...>` → `<div class="work-scroller fade-element" id="work-scroller"></div>`; titolo sezione "Un progetto" → "I Nostri Progetti".
   - `css/style.css`: regole `.featured-project*` rimosse, sostituite da `.work-scroller` (flex, `overflow-x: auto`, `scroll-snap-type: x mandatory`, scrollbar nascosta coerente con `body::-webkit-scrollbar { display:none }` già presente nel sito) e `.work-card`/`.work-card-img`/`.work-card-overlay` (immagine full-bleed `object-fit: cover`, overlay a gradiente in basso con titolo/`cardSubtitle`, stesso hover-scale del vecchio `.featured-project-img`). Padding della sezione lasciato ereditato da `.section { padding: 100px 10%; }`, nessun valore one-off introdotto.
   - `js/main.js`: rimossa `window.openFeaturedProject`; aggiunta `window.openProjectByTitle(title)` (generica, cerca per titolo esatto in `projectsData`, guardia silenziosa se non trovato) e `renderWorkScroller()` (itera un array di configurazione `workScrollerProjects` con override opzionale `imageIndex`, e viene chiamata subito dopo `renderProjects('tutti')` nello stesso punto di inizializzazione).

   **Verifica in browser**: nuova tab pulita, console senza errori. Anche in questo round la cache HTTP di questa sessione del browser-tool ha servito versioni stale di `css/style.css`, `header.html` e `data/projects.json` fino a quando non sono stati rifetchati con `{cache:'no-store'}` e reiniettati (stesso quirk già documentato sopra) — confermato però che:
   - `document.querySelector('.hero h1').textContent` === `"Tecnitalia Group"`
   - `renderWorkScroller()` produce esattamente 6 `.work-card`, con titoli/immagini corrispondenti alla selezione sopra (incluso l'override `reggiani2.jpg`)
   - Il click su una card (`Ex Cartiere Binda`) chiama `openProjectByTitle` e apre la modale con `#m-title` = "Ex Cartiere Binda", `#m-client` = "Euromilano S.p.A., Milano"
   - `#work-scroller` ha `display: flex` e `overflow-x: auto`; impostare `scrollLeft` manualmente sposta correttamente il contenuto (scroll nativo funzionante)

   **Commit**: `deb54f2` — "fix: ripristina il titolo hero e trasforma i progetti in una striscia scorrevole stile Arup" — file: `index.html`, `css/style.css`, `js/main.js` (3 file, 60 inserimenti, 31 rimozioni).

   **Concern**: nessuno. Unica nota: l'esclusione di "Ex Sofer" (valore economico più alto in assoluto, 20M€) dalla striscia è una scelta deliberata dettata dalla mancanza di foto presentabili tra le due disponibili — se in futuro venisse caricata una foto migliore per quel progetto, ha senso reinserirlo nell'array `workScrollerProjects` in `js/main.js`.

## Stato pre-esistente (da `git status` iniziale)

- `js/main.js` era già stato modificato (unstaged) con il fix della parentesi mancante a fine `initScrollReveals()`, come indicato nelle note del task.
- `assets/img/logo-white.png` era in staging come nuovo file.
- Nessuno dei due è stato toccato/rigenerato da questo task, salvo l'aggiunta additiva di `window.openFeaturedProject` in `js/main.js` (Step 5).

## Step eseguiti

1. **Colore brand e logo bianco in nav**
   - `css/style.css:3`: `--blue: #00427A;` → `--blue: #004F87;`
   - `header.html`: doppio `<img>` (logo bianco + logo colore) con classi `logo-img-white` / `logo-img-color`
   - `css/style.css`: aggiunta regola `.logo-container { display: flex; ... }` + toggle `nav.scrolled .logo-img-white/.logo-img-color` subito dopo il blocco `.logo-container`/`.logo-img` esistente

2. **Hero ristilizzato**
   - `index.html`: nuova headline "Bonifichiamo il suolo. Costruiamo ciò che verrà.", nuovo paragrafo, nuovo CTA `hero-cta` verso `chi-siamo.html`
   - `css/style.css`: nuova scala tipografica hero (`clamp` più ampio), stile `.hero-cta`/`.hero-cta:hover` con `!important` per leggibilità su sfondo scuro

3. **Blocco filosofia (statement)**
   - `index.html`: nuova `<section class="statement-block">` tra `</header>` e `<section id="stats">`
   - `css/style.css`: nuove regole `.statement-block` / `.statement-block p`

4. **Copy sezione Ingegneria**
   - `index.html`: paragrafo introduttivo e lista `<ul>` riscritti secondo il testo fornito nel piano (bonifica suoli, amianto MCA/FAV, Direzione Lavori, acque/emissioni, due diligence). Testo `#chi-siamo` non toccato.

5. **Progetto in evidenza**
   - `index.html`: sostituita l'intera `<section id="progetti">` con il blocco `.featured-project` (Nuova Scuola Politecnica di Genova), dati verbatim da `data/projects.json` (committente "Università di Genova", importo "ca. 260.000.000 €", immagine `./assets/img/genova1.jpg`)
   - `css/style.css`: nuovo componente `.featured-project` + media query mobile
   - `js/main.js`: aggiunta `window.openFeaturedProject` subito dopo `window.closeProject`, che cerca il progetto per titolo esatto in `projectsData` e chiama `window.openProject(idx)` con guardia silenziosa se non trovato
   - Verificato che `renderProjects()` in `js/main.js` avesse già la guardia `if (editorialGrid)` prima di scrivere — presente, nessuna modifica necessaria (il ramo `#projects-grid-full` per `elenco-progetti.html` resta intatto)

6. **Verifica in browser**
   - Server avviato via `mcp__Claude_Browser__preview_start` (name `tecnitalia-site`, porta 8123)
   - `read_console_messages`: zero errori in tutte le verifiche
   - `get_page_text`: confermato il testo esatto di hero, statement, copy Ingegneria e progetto in evidenza come da piano
   - **Nota tecnica rilevante**: la sessione browser di questo tool aveva una cache HTTP persistente (browser-profile-wide, non per-tab) che serviva versioni STALE di `header.html`, `css/style.css` e — soprattutto — `data/projects.json` (24 progetti invece di 28, senza "Nuova Scuola Politecnica"), nonostante `curl` diretto al server e il tool `Read` confermassero che i file su disco fossero already corretti. Ctrl+Shift+R e una tab completamente nuova NON hanno bypassato questa cache per le fetch dinamiche innescate da `js/main.js`. Verifica quindi eseguita forzando `fetch(..., {cache:'no-store'})` per `header.html`, `css/style.css` e `data/projects.json`, iniettando i contenuti freschi nel DOM/`<style>`/`projectsData` e ripetendo i controlli:
     - `getComputedStyle(document.documentElement).getPropertyValue('--blue').trim()` → `#004F87` ✓
     - Nav non scrollata: `.logo-img-white` → `display: block`, `.logo-img-color` → `display: none`; dopo `nav.classList.add('scrolled')`: invertito correttamente ✓
     - `window.openFeaturedProject()` con `projectsData` fresco (28 elementi, indice 25) → modale attiva, `#m-title` = "Nuova Scuola Politecnica", `#m-client` = "Università di Genova", `#m-val` = "ca. 260.000.000 €" ✓
   - `js/main.js` stesso risultava invece sempre fresco ad ogni richiesta (200, non 304/cache) — solo gli asset senza `Cache-Control` esplicito e con `Last-Modified` "vecchio" al momento della prima fetch di questa sessione ne sono stati affetti. Nessun impatto sul codice di produzione: il quirk è imputabile esclusivamente alla cache del browser di automazione di questa sessione, non al server locale né ai file sorgente.

7. **Commit**
   - `git status` prima del commit: `js/main.js` risultava senza diff rispetto a HEAD — un commit precedente (`1bc7a4b`, "fix: corregge errore di sintassi in js/main.js che impediva il caricamento di header/footer", autore Francesco Bressi, timestamp coincidente con questa sessione) aveva già assorbito sia il fix della parentesi sia l'aggiunta di `window.openFeaturedProject` fatta in questo task (probabilmente un meccanismo di auto-commit/checkpoint esterno a questo agente). `git add js/main.js` è stato quindi un no-op innocuo.
   - `assets/img/logo-white.png` risultava non versionato in nessun commit (`git log --all -- assets/img/logo-white.png` vuoto) → incluso nel commit come da istruzione del piano.
   - Commit creato: `1b8f3fb` — "feat: rimpagina la home in stile editoriale (hero, statement, progetto in evidenza, colore brand reale)" — file: `index.html`, `css/style.css`, `header.html`, `assets/img/logo-white.png` (4 file, 61 inserimenti, 18 rimozioni).

## File toccati

- `index.html`
- `css/style.css`
- `header.html`
- `js/main.js` (già committato in `1bc7a4b` prima di questo Step 7, contenuto verificato corretto)
- `assets/img/logo-white.png` (nuovo, committato in questo task)

## Fuori scope (non toccati, come da vincoli del piano)

`chi-siamo.html`, `dettaglio-ingegneria.html`, `dettaglio-servizi.html`, `elenco-progetti.html`, `archivio-news.html`, `news-singola.html`, `footer.html`, testo `#chi-siamo` in `index.html`.

## Concern

Nessun blocco reale: il codice è corretto e verificato. L'unico punto degno di nota è il comportamento di caching del browser di automazione di questa sessione (dettagliato sopra al punto 6), che ha richiesto un bypass manuale per la verifica ma non riflette un problema nel codice consegnato — un utente reale con un browser "puro"/prima visita non lo sperimenterebbe, e comunque `data/projects.json`, `css/style.css` e `header.html` non hanno header `Cache-Control` espliciti lato server (limite pre-esistente del semplice server Python di sviluppo, non introdotto da questo task).
