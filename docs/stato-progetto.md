# Stato del progetto

Fotografia al 30 agosto 2026, da rileggere fra sei mesi per sapere a che punto siamo.

## Stato attuale

**Pubblicato nel codice:**

- 4 pagine servizio ancorate alla normativa (bonifica amianto, bonifica siti contaminati,
  caratterizzazione e analisi di rischio, demolizioni e decommissioning)
- Hub di servizio e menu a tendina
- JSON-LD su 11 pagine (verificato: `grep -l "application/ld+json" *.html` restituisce 11 file)
- CSP e Referrer-Policy via meta tag su 12 pagine HTML (verificato nel codice; si veda
  `sicurezza.md` per il dettaglio della policy)
- NAP (nome, indirizzo, telefono) e link di navigazione presenti nell'HTML statico, non generati
  via JavaScript
- Sitemap a 11 URL (`sitemap.xml`, verificato con `grep -c "<loc>"`)
- `robots.txt` con elenco esplicito di crawler AI ammessi (GPTBot, OAI-SearchBot, ChatGPT-User,
  ClaudeBot, Claude-User, PerplexityBot, Google-Extended, Applebot-Extended, CCBot)
- `llms.txt` pubblicato
- Informativa privacy
- Self-host delle librerie front-end (dettaglio versioni in `sicurezza.md`)
- `CNAME` tracciato nel repository
- Cloudflare Web Analytics attivo

**Completati dall'utente, lato account:**

- Google Business Profile
- Google Search Console (verifica via record TXT su DNS OVH, proprietà di tipo dominio)
- Bing Webmaster Tools
- Allow-list del dominio su EmailJS
- Pubblicazione di news (archivio + pagine singole via `data/news.json`)

## Aperto, in ordine di rendimento

1. ~~News non indicizzabili singolarmente~~ — **RISOLTO il 30 agosto 2026.** Ogni articolo ha
   ora una pagina statica propria (`news-<slug>.html`), generata da `tools/genera-news.py` a
   partire da `data/news.json`, con JSON-LD `NewsArticle`, `datePublished` e canonical propri.
   Lo script rigenera anche `sitemap.xml` (16 URL) e il blocco statico delle ultime news in
   `index.html`, che altrimenti invecchiava a ogni pubblicazione. `news-singola.html` resta in
   servizio per i vecchi link `?id=N` ma è passata a `noindex`, per non competere con le pagine
   nuove.

2. **`sameAs` assente.** Verificato nel codice: nessuna delle pagine con JSON-LD espone la
   proprietà `sameAs` nel blocco `ProfessionalService` (`grep -c "sameAs" *.html` restituisce 0
   ovunque). Aggiungere gli URL della scheda Google Business Profile e della pagina LinkedIn
   collega sito, scheda Maps e profilo LinkedIn come la stessa entità agli occhi dei motori di
   ricerca e degli assistenti AI. Costo di implementazione bassissimo, rendimento atteso alto.

3. **Peso immagini e stabilità del layout.** Verificato: `assets/img` pesa 48 MB su 144 file, di
   cui 46 sopra i 500 KB (il più pesante, `arexpoprincipia2.jpg`, è circa 1,6 MB), tutti in JPG o
   PNG senza varianti moderne (WebP/AVIF). Inoltre, dei 20 tag `<img>` statici presenti nelle
   pagine HTML, nessuno dichiara `width`/`height`: questo produce spostamenti di layout al
   caricamento (CLS). Il punto è più rilevante ora che Cloudflare Web Analytics misura i Core Web
   Vitals reali del sito, CLS incluso.

4. **CSP permissiva.** Rimanda a `sicurezza.md` per il dettaglio tecnico e la causa (`onclick` ed
   `style` inline diffusi).

5. **Governance degli account.** Search Console e Bing Webmaster Tools sono verificati con un
   account personale, non aziendale. Aggiungere un secondo proprietario con indirizzo aziendale
   protegge lo storico dei dati raccolti, che non è recuperabile se l'account personale diventa
   inaccessibile. Nota pratica: Search Console accetta solo indirizzi registrati come account
   Google; un indirizzo aziendale non-Gmail va prima registrato su
   `accounts.google.com/signup` con l'opzione "Usa il mio indirizzo email attuale".

6. **Voci minori.**
   - Partita IVA assente dall'informativa privacy: facoltativa, il titolare del trattamento è già
     identificato da denominazione, sede e recapiti.
   - `lastmod` della sitemap aggiornato manualmente, non generato.
   - Da confermare l'opzione "Enforce HTTPS" nelle impostazioni di GitHub Pages.

## Pubblicare un nuovo articolo

1. Aggiungere l'oggetto **in testa** all'array di `data/news.json`, con i campi `id`, `slug`,
   `data` (formato `30 Agosto 2026`), `titolo`, `immagine`, `riassunto`, `contenuto`.
   Lo `slug` diventa l'URL: sceglierlo corto e con le parole chiave del tema.
2. Eseguire `python tools/genera-news.py` dalla radice del repository.
3. Committare i file generati insieme al JSON: `news-*.html`, `sitemap.xml` e `index.html`.
4. Dopo la pubblicazione, richiedere l'indicizzazione del nuovo URL in Google Search Console.

Lo script è idempotente: rieseguirlo non duplica nulla. Verifica l'esistenza delle immagini
referenziate e segnala slug duplicati o date non interpretabili.


## Decisioni prese

- **Protezione del form EmailJS: rischio accettato, nessun intervento** *(30 agosto 2026)*.
  L'allow-list dei domini richiede un piano a pagamento; sono state valutate e scartate la
  verifica reCAPTCHA v2, il passaggio al piano Personal (9 $/mese) e la migrazione a un altro
  servizio. La decisione è di mantenere il solo honeypot già presente nel form.
  **Motivazione:** la chiave pubblica consente di inviare esclusivamente attraverso il template
  configurato, con destinatario fisso. Non espone dati e non permette di inviare email a terzi
  a nome dello studio. Il danno massimo è il consumo delle 200 richieste mensili e messaggi
  indesiderati sulla casella aziendale: un disservizio temporaneo, non una violazione.
  **Da rivedere se:** la quota mensile si esaurisce senza motivo, arrivano messaggi automatici
  in quantità, oppure il form diventa un canale commerciale critico. In quel caso la strada più
  rapida è il piano Personal, che non richiede modifiche al codice.

Scelte deliberate, con la motivazione, perché non vengano riproposte come migliorie da chi
riprende in mano il progetto.

- **I 57 progetti restano NON indicizzabili singolarmente.** Scelta esplicita del committente. I
  progetti continuano a vivere in `data/projects.json` (verificato: 57 voci, 46 committenti
  distinti) e ad aprirsi nella modale di `elenco-progetti.html`, non in pagine HTML dedicate.
  Non è una lacuna da colmare: è una decisione presa. Chi propone di generare pagine statiche per
  i singoli progetti deve prima riaprire la discussione con il committente.

- **Analytics cookieless invece di Google Analytics 4.** Scelto Cloudflare Web Analytics per
  evitare banner di consenso e adempimenti sui cookie. Contropartita accettata: nessuna
  ricostruzione del percorso del singolo visitatore, nessuna attribuzione delle conversioni al
  canale di provenienza. Il dato su quali ricerche portano traffico si legge in Search Console,
  non in Cloudflare.

- **Niente testo nascosto o istruzioni occultate per gli assistenti AI.** Valutato e scartato:
  sono pratiche in violazione delle policy antispam di Google, sanzionabili fino alla
  deindicizzazione del sito. La strada scelta è quella legittima e verificabile nel codice:
  markup JSON-LD, `FAQPage` dove pertinente, `llms.txt`, e scrittura estraibile con riferimenti
  normativi puntuali (es. D.Lgs. 213/2025) nel testo visibile.

- **Librerie self-hostate invece che da CDN esterno.** Motivazione e contropartita (rischio di
  manutenzione senza scanning automatico) descritte in `sicurezza.md`, rischio 2.

## Riferimenti

- `docs/checklist-visibilita.md` — azioni operative sugli account esterni (Google Business
  Profile, Search Console, Bing)
- `docs/sicurezza.md` — postura di sicurezza, rischi aperti e limiti accettati
- `docs/linkedin-prompts.md` — prompt per i contenuti della pagina LinkedIn
- `Istruzioni dns.md` — topologia DNS e provider
- `README.md` — documentazione tecnica del repository
