# Redesign frontend Tecnitalia Group — Design

## Obiettivo

Rifare l'estetica e l'interazione del sito (7 pagine HTML statiche, CSS/JS condivisi) per trasmettere l'autorevolezza di una grande società di ingegneria/consulenza, in uno stile editoriale moderno che si ispira ad Arup e ad altri siti "big company" senza copiarli, mantenendo il blu Tecnitalia (`#00427A`) come colore-firma. Lo studio ha solo 4 dipendenti ma un posizionamento alto: il sito deve trasmettere fiducia e prestigio più che dimensione.

Contenuti e dati (JSON progetti/news, form contatti) non cambiano nella loro architettura: è un restyling + alcune nuove sezioni editoriali, non una riscrittura della logica applicativa.

## Principi di design

- **Meno colore, più impatto**: il blu resta il colore-firma ma usato come accento mirato, non di sfondo ovunque. Titoli in un "ink" quasi-nero, non più in blu.
- **Tipografia con carattere**: titoli grandi ed editoriali (font display distintivo), testo corrente resta leggibile e familiare.
- **Aria**: più whitespace, meno elementi decorativi (ombre pesanti, angoli molto arrotondati) sulle card.
- **Autorevolezza dei contenuti**: numeri (anni di attività, progetti realizzati) e una timeline storica, pattern tipico delle grandi società di ingegneria/consulenza — utile per un'azienda piccola che vuole trasmettere solidità.
- **Movimento curato ma mai vistoso**: micro-interazioni eleganti (hover, reveal, contatori), non effetti da landing page commerciale.

## Design system

### Tipografia
- **Corpo testo**: Manrope (invariato — già caricato, già leggibile).
- **Titoli/display**: **Bricolage Grotesque** (Google Fonts, variabile) per h1/h2/h3 e numeri della fascia statistiche. Scala fluida con `clamp()`, es. hero `clamp(3rem, 7vw, 6.5rem)`, titoli di sezione `clamp(2.2rem, 4vw, 3.5rem)`. Letter-spacing leggermente negativo sui titoli grandi.
- Pesi: extrabold/black per i titoli principali, regular/medium per sottotitoli.

### Colore
Nuove variabili CSS (in aggiunta a `--blue` esistente, che resta invariato per compatibilità con eventuali usi non ancora migrati):
- `--ink: #0A0A0A` — colore dei titoli e testo ad alto contrasto (sostituisce l'uso di `--blue` nei titoli).
- `--paper: #FAFAF8` — sfondo "caldo" per sezioni chiare (sostituisce il bianco puro dove serve profondità).
- `--navy-deep: #071B2E` — sezione scura ad alto contrasto (footer, eventuale fascia statistiche), più profondo del blu brand.
- `--blue` (`#00427A`) resta l'accento: usato su link, hover, piccoli dettagli, numeri chiave — non più come colore di titoli/sfondi diffusi.
- `--gray` esistente (`#f5f5f7`) resta per sezioni chiare alternate.

### Layout e spaziatura
- Max-width dei blocchi di testo più stretta per leggibilità (~700-760px) dove il testo è lungo (chi-siamo, dettaglio pagine), mentre gli elementi editoriali (titoli, immagini) possono restare full-bleed o a griglia larga.
- Griglie asimmetriche per hero/sezioni testo+immagine (es. 5/7 invece di 1fr/1fr) dove aiuta la lettura.
- Hairline (`1px solid`, colore chiaro) al posto di `box-shadow` pesanti sulle card; angoli meno arrotondati (`8px` invece di `16-25px`) per un linguaggio più piatto/editoriale.

## Componenti

### Navigazione
Stessa struttura (trasparente su hero → bianca allo scroll, hamburger mobile già accessibile). Restyling: voci in maiuscolo con letter-spacing ampio, tipografia più sottile, transizioni invariate.

### Hero (home)
Titolo enorme in Bricolage Grotesque, meno testo, leggero effetto parallax sull'immagine di sfondo via GSAP (già disponibile). Il preload/priorità immagine già impostati in precedenza restano.

### Fascia statistiche (nuova, home)
Sezione con 3-4 numeri grandi, animati con un contatore GSAP al primo ingresso in viewport:
- "1986" — anno di fondazione
- "40+" — anni di attività
- numero progetti totali, calcolato **dinamicamente** da `projectsData.length` (oggi 28) per non dover aggiornare il numero a mano ogni volta che si aggiunge un progetto
- "5" — aree di competenza (bonifiche, amianto, acque, rifiuti, demolizioni — riprese dai tag esistenti)

Sfondo `--navy-deep` per contrasto drammatico rispetto al resto della pagina, unica sezione così scura oltre al footer.

### Timeline (nuova, chi-siamo.html)
Il testo esistente è già diviso in 3 fasi cronologiche (Origini 1986 → Evoluzione Ambientale → Presente e Certificazioni). Diventano 3 nodi di una timeline verticale con anno in evidenza, mantenendo il testo originale (nessuna riscrittura dei contenuti storici).

### Card progetti/news
Restyling piatto: hairline invece di ombra pesante, angoli meno arrotondati, hover che anima leggermente l'immagine (non solo scale) e mostra tag/anno con un dettaglio tipografico invece del box overlay attuale.

### Portfolio progetti — home e archivio
- **Home**: lo slider orizzontale di card piccole viene sostituito da una griglia editoriale con 4-6 progetti in evidenza, immagini grandi (le foto sono già state migliorate in un lavoro precedente).
- **Archivio (`elenco-progetti.html`)**: griglia esistente ristilizzata con lo stesso linguaggio (hairline, tipografia), filtri mantenuti ma restyled come tab/pill minimali.
- **Modale dettaglio**: stessa struttura funzionale (galleria immagini, specifiche, descrizione, già accessibile con Esc/focus), ma tipografia e spaziature aggiornate al nuovo linguaggio, tabella specifiche più pulita.

### Team
Foto più grandi, leggero trattamento desaturato che torna a colore pieno all'hover (dettaglio moderno, basso rischio).

### Footer
Sfondo `--navy-deep` (già scuro, resta scuro ma coerente con la nuova palette), layout a 3 colonne invariato nella struttura, tipografia aggiornata. Form contatti: input con solo bordo inferiore invece delle caselle scure piene attuali (l'honeypot e la logica di invio non cambiano).

### Pagine di dettaglio (ingegneria, servizi) e pagine testuali
Stessa struttura (`page-header` + `page-content`), tipografia aggiornata; eventuali pull-quote o numeri chiave possono essere aggiunti in modo mirato se il testo lo consente, senza riscrivere i contenuti.

## Movimento

- Lenis (smooth scroll) invariato.
- GSAP ScrollTrigger: reveal più curati per testo/immagini (stagger leggero, non solo fade), parallax leggero sull'immagine hero, contatore numerico animato per la fascia statistiche.
- Hover: sottolineatura animata sui link testuali, transizione immagine sulle card (non solo `scale`).
- Nessuna libreria nuova: si lavora con GSAP/ScrollTrigger già caricati.

## Contenuti nuovi necessari

- Numeri fascia statistiche: 1986, 40+, conteggio progetti (dinamico da JSON), 5 aree di competenza. Nessun dato da inventare — tutti derivabili da contenuti già pubblicati sul sito.
- Timeline chi-siamo: riuso del testo esistente, solo nuova presentazione visiva.

## Fuori scope (rimandato)

- CMS per la gestione contenuti, analytics, cookie banner: non toccati in questo lavoro (discussi in una fase precedente come miglioramenti "backend/infrastruttura" a sé stanti).
- Nessuna modifica alla logica EmailJS/honeypot già implementata.
- Nessuna modifica alla struttura dei dati JSON (`news.json`, `projects.json`) oltre ai 4 progetti già aggiunti.

## Percorso di lavoro e rischio

- Si continua sul branch `ottimizzazione-frontend` (già esistente); `main` resta il punto sicuro a cui tornare.
- **Pilota**: si costruisce prima il design system (variabili colore/tipografia in `css/style.css`, font import) e si applica alla home (`index.html`), inclusa la fascia statistiche e il nuovo portfolio home. Si mostra il risultato per approvazione.
- **Estensione**: una volta approvato il linguaggio visivo sulla home, si applica alle altre 6 pagine con lo stesso sistema (nav/footer condivisi already ereditano il restyling; le pagine con contenuto proprio — chi-siamo con timeline, elenco-progetti, dettaglio-ingegneria/servizi, archivio-news, news-singola — vengono aggiornate una per una).
- Verifica in browser locale (come già fatto per le modifiche precedenti) ad ogni fase: nessun errore console, animazioni funzionanti, responsive mobile testato.
