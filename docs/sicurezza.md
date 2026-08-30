# Sicurezza — stato e rischi aperti

Aggiornato al 30 agosto 2026. Cosa è stato verificato, cosa resta aperto, cosa sapere prima di toccare l'infrastruttura.

## Premessa

Il repository `Frabressi/tecnitalia-web` è **pubblico su GitHub** (verificato via API: `private: false`). Essere pubblico non espone solo i file presenti oggi ma **l'intera storia git**: 118 commit, permanenti e recuperabili anche dopo la cancellazione di un file. Cancellare un file dall'albero corrente non lo rimuove dalla cronologia.

## Controlli già eseguiti

| Controllo | Esito |
|---|---|
| Ricerca di credenziali su tutti i commit della storia (chiavi private, token, `client_secret`, password, chiavi AWS `AKIA*`, token GitHub `ghp_*`, token Slack `xox*`) | Nessun riscontro |
| Indirizzi email presenti nel repository | Solo `info@tecnitaliagroup.it` (ricorre in 13 pagine HTML) e `jack@greensock.com`, l'email dell'autore di GSAP contenuta nella libreria self-hostata |
| Numeri di telefono presenti | Solo quello aziendale, `02 76000206` / `+39 02 76000206` |
| File cancellati ma ancora presenti nella storia | `assets/img/logo.jpg` (caricato come `Logo-TecnGroup.jpg`, poi rinominato in `logo.jpg` con il commit "Rename Logo-TecnGroup.jpg to logo.jpg", infine rimosso come duplicato) e `assets/img/prova.txt`. Entrambi innocui |
| File di configurazione tracciati | Solo `.claude/launch.json` (avvia un server statico Python locale sulla porta 8791); non contiene segreti |
| Documenti d'ufficio nell'albero (`.pdf`, `.doc*`, `.xls*`, `.msg`) | Nessuno presente |

## Credenziali pubbliche del progetto — perché non sono un problema

- **Public key EmailJS** (`IxQp4s1e-bTQOqX3J`, in `js/main.js`): è un identificativo pubblico, non una chiave crittografica, e compare comunque in chiaro nel JavaScript servito al browser. La protezione effettiva è l'**allow-list del dominio** nel pannello EmailJS (Account → Security → Domains), che impedisce l'uso della chiave da qualunque altro sito. **Il domain whitelist NON è disponibile nel piano gratuito di EmailJS** (verificato sulla pagina pricing ufficiale il 30 agosto 2026: il piano Free offre 200 richieste mensili e 2 template, mentre l'allow-list dei domini compare solo dai piani a pagamento — il primo è Personal, 9 $/mese con 2.000 richieste). Il tentativo di aggiungere anche un solo dominio produce l'errore "Subscription Limitation". La protezione resta quindi **non attiva**, e va gestita diversamente.

**Portata reale del rischio, per non sovrastimarlo:** la chiave pubblica consente di inviare esclusivamente attraverso il template configurato, che ha il destinatario fisso. Chi la usasse non potrebbe leggere dati né inviare email a terzi a nome dello studio: potrebbe soltanto recapitare messaggi indesiderati a `info@tecnitaliagroup.it` ed esaurire le 200 richieste mensili, lasciando il form inutilizzabile fino al rinnovo della quota. È un disservizio, non una violazione di dati.

**Mitigazioni disponibili senza costi:** l'honeypot già presente nel form (campo nascosto `website` in `footer.html`, controllato in `js/main.js`) ferma i bot più elementari; la verifica reCAPTCHA v2 si configura nelle impostazioni del template EmailJS ed è la difesa più efficace contro l'abuso automatizzato, che è l'unico vettore realistico. **Decisione presa il 30 agosto 2026: si mantiene il solo honeypot e si accetta il rischio residuo**, proporzionato alla portata descritta sopra. Le alternative valutate e scartate sono reCAPTCHA v2, il piano Personal e il cambio di servizio. Da riaprire se la quota mensile si esaurisce senza motivo o se compaiono invii automatici: in quel caso il piano Personal è la via più rapida, perché non richiede modifiche al codice. Vedi `stato-progetto.md`.
- **Token Cloudflare Web Analytics**: pubblico per progetto, presente nell'HTML di ogni pagina. Non dà accesso all'account Cloudflare.

## Rischi aperti

### Rischio 1 — repository pubblico dentro il OneDrive aziendale

È il rischio più serio, ed è strutturale. La directory di lavoro è
`OneDrive - Tecnitalia Ingegneria…\Documenti\Tecnitalia`: la stessa cartella dove si depositano
documenti di studio è la working copy di un repository pubblico. Basta che ci finisca un PDF
di commessa, un'offerta o una relazione per cliente, seguito da un `git add -A` non controllato,
perché quel file diventi pubblico in modo irreversibile.

**Mitigazione già applicata:** è stato creato un `.gitignore` in radice che esclude:
- documenti d'ufficio (`*.pdf`, `*.doc`, `*.docx`, `*.dot`, `*.dotx`, `*.xls`, `*.xlsx`, `*.xlsm`, `*.ppt`, `*.pptx`, `*.odt`, `*.ods`, `*.msg`, `*.eml`, `*.dwg`, `*.dxf`, `*.zip`, `*.rar`, `*.7z`)
- credenziali e file di ambiente (`.env`, `.env.*`, `*.key`, `*.pem`, `*.p12`, `*.pfx`, `credentials*`, `secrets*`)
- configurazioni locali non condivisibili (`*.local.json`, `.claude/settings.local.json`)
- file temporanei e di conflitto di OneDrive/Office (`~$*`, `*conflitto*`, `*conflicted copy*`, `*.tmp`)
- artefatti di sistema (`Thumbs.db`, `ehthumbs.db`, `desktop.ini`, `.DS_Store`)

Il file stesso apre con un commento che ribadisce la regola operativa e non è un dettaglio secondario.

**Regola operativa:** controllare sempre `git status` prima di ogni commit ed evitare `git add -A`
alla cieca su questo repository; preferire l'aggiunta dei file per nome esplicito.

### Rischio 2 — le librerie self-hostate non si aggiornano da sole

In `assets/vendor/` sono presenti quattro librerie self-hostate, verificate nei rispettivi header/campi interni:

| Libreria | Versione verificata | URL di origine per riscaricarla |
|---|---|---|
| GSAP | 3.12.2 (header del file) | `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js` |
| ScrollTrigger | 3.12.2 (header del file) | `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js` |
| Lenis | 1.0.29 (stringa nel bundle) | `https://cdn.jsdelivr.net/gh/studio-freight/lenis@1.0.29/bundled/lenis.min.js` |
| @emailjs/browser | 4.4.1 | `https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js` |

Il self-host ha eliminato il rischio supply-chain: Lenis, in particolare, arrivava da un percorso
GitHub mutabile su jsdelivr (`cdn.jsdelivr.net/gh/...`), modificabile da chi controlla quel
repository upstream. Ma introduce un rischio di manutenzione: la cartella `assets/vendor/` non ha
un manifest (`package.json` o simile), quindi **Dependabot e il controllo vulnerabilità di GitHub
non la vedono**. Un aggiornamento di sicurezza a monte non genera alcun alert automatico qui.

Si propone una revisione periodica manuale delle quattro versioni, per esempio semestrale.

### Rischio 3 — l'archivio progetti è scaricabile in blocco

`https://www.tecnitaliagroup.it/data/projects.json` risponde 200 e restituisce un file di circa
77 KB. Verificato nel file: **57 progetti**, **46 committenti distinti**, **30 progetti con valore di commessa indicato (23 importi distinti)
distinti** (il campo `val` è vuoto in un progetto), il maggiore pari a **circa 260.000.000 €**
(Nuova Scuola Politecnica, Università di Genova).

**Non è una fuga di dati:** committente, valore, periodo e tipo intervento sono già mostrati nella
scheda di dettaglio del singolo progetto sul sito. Verificato in `js/main.js` (riga 431): i campi
`p.client`, `p.period`, `p.val`, `p.type` vengono scritti rispettivamente negli elementi
`m-client`, `m-period`, `m-val`, `m-type` della modale.

Ma la forma aggregata è diversa dal dato mostrato uno alla volta: con una sola richiesta HTTP un
concorrente ottiene l'intero storico commerciale in formato strutturato e riutilizzabile, invece
di doverlo ricostruire pagina per pagina. Va presentata come **decisione da prendere
consapevolmente**, non come un difetto da correggere:

- lasciare `projects.json` così com'è, oppure
- rimuovere il campo `val` dal JSON pubblico (la modale dovrebbe allora leggere il valore da
  un'altra fonte, o mostrare solo un ordine di grandezza)

### Rischio 4 — la sicurezza del sito coincide con quella dell'account GitHub

Con GitHub Pages su repository pubblico, chi ottiene accesso all'account può modificare o
reindirizzare il sito pubblicato. Da verificare, fuori dal codice:

- autenticazione a due fattori attiva sull'account GitHub
- protezione del ramo `main` (branch protection)
- secret scanning e push protection abilitati (sono gratuiti sui repository pubblici)

## Limiti noti e accettati

**CSP permissiva.** Verificato: la CSP (via meta tag, non header HTTP) è presente su 12 pagine
HTML e richiede `'unsafe-inline'` sia per `script-src` che per `style-src`:

```
default-src 'self'; script-src 'self' 'unsafe-inline' https://static.cloudflareinsights.com;
style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;
img-src 'self' data: https:; connect-src 'self' https://api.emailjs.com https://cloudflareinsights.com;
frame-src https://maps.google.com https://www.google.com; object-src 'none'; base-uri 'self'; form-action 'self'
```

Il motivo è verificabile nel codice: `js/main.js` genera 3 handler `onclick` inline
(in `elenco-progetti.html` se ne trovano altri 10, generati a runtime dallo stesso script) e gli
attributi `style="..."` inline sono diffusi in tutte le pagine (da un minimo di 4 a un massimo di
40 occorrenze in `index.html`). Con `'unsafe-inline'` attivo la CSP non blocca l'esecuzione di
script iniettati via inline event handler o `<style>` iniettato: la protezione XSS è quindi
parziale. Stringerla richiede un refactor verso l'event delegation (rimuovere gli `onclick`
generati da `main.js`) e verso classi CSS al posto degli attributi `style` inline.

`footer.html` è un frammento incluso via JavaScript nelle altre pagine e non ha una propria CSP:
non essendo servito come documento a sé stante, non ne ha bisogno.

**Nessun header HTTP di sicurezza.** GitHub Pages non consente header personalizzati, quindi CSP
e Referrer-Policy sono veicolate tramite tag `<meta>` invece che tramite header HTTP, e HSTS non è
impostabile sul dominio personalizzato.

**`Istruzioni dns.md` è pubblico** e documenta topologia DNS, provider e nome utente GitHub. Il
valore di ricognizione è modesto: l'informazione è in gran parte deducibile da altre fonti
pubbliche (whois, record DNS stessi). Non richiede rimozione.

## Nota operativa

Allo stato attuale l'allow-list non è attiva, quindi **il form di contatto funziona anche da `localhost`**: un invio riuscito in locale recapita un messaggio reale alla casella aziendale, quindi conviene usare testi riconoscibili durante le prove. Se in futuro l'allow-list venisse attivata, il comportamento si invertirebbe e gli invii da `localhost` fallirebbero: sarebbe il comportamento voluto, non un guasto.
