# Checklist visibilità — azioni fuori dal codice

Aggiornata al 30 agosto 2026. Le prime voci valgono più di tutto il lavoro fatto sul sito:
il codice rende il sito *indicizzabile*, queste lo rendono *trovato*.

## Quadro di stato

| | Voce | Stato |
|---|---|---|
| 1 | Google Business Profile | ✅ fatto |
| 2 | Google Search Console | ✅ verificata via CNAME su OVH |
| 3 | Bing Webmaster Tools | ✅ fatto |
| 4 | Cloudflare Web Analytics | ✅ attivo in produzione |
| 5 | EmailJS: protezione della chiave | **non risolvibile nel piano free** — vedi `sicurezza.md` |
| 6 | Pubblicazione del sito | ✅ online dal 30 agosto 2026 |
| 7 | News pubblicate | ✅ fatto |
| 8 | Invio sitemap in Search Console (ora 16 URL) | da fare |
| 9 | Secondo proprietario aziendale su Search Console e Bing | da fare |
| 10 | Verifica "Enforce HTTPS" e 2FA su GitHub | da fare |
| 11 | Partita IVA nell'informativa | facoltativa |
| 12 | Pagina LinkedIn | prompt pronti in `linkedin-prompts.md` |

**Le voci di questa lista riguardano gli account esterni.** Per lo stato del sito e degli
interventi tecnici aperti vedi `stato-progetto.md`; per la postura di sicurezza `sicurezza.md`.


## 1. Google Business Profile — ✅ attiva, ora è manutenzione

La scheda è stata aperta. Da qui in avanti il lavoro è tenerla viva: le schede aggiornate
di recente vengono mostrate più spesso di quelle ferme. Il resto di questa sezione resta come
riferimento per completare i campi e per la manutenzione periodica.

**Come si apre:** https://business.google.com → "Gestisci ora" → cerca prima
"Tecnitalia" per verificare che non esista già una scheda non rivendicata (capita che
Google le generi da solo). Se esiste, rivendicala invece di crearne una seconda: due schede
sullo stesso indirizzo si annullano a vicenda.

**Dati da inserire — devono coincidere carattere per carattere con quelli del sito:**

```
Nome:       Tecnitalia Group
Indirizzo:  Via Pastorelli 4E, 20143 Milano MI
Telefono:   02 76000206
Sito:       https://www.tecnitaliagroup.it/
```

**Categoria principale:** scegli quella che descrive il ricavo maggiore. Le candidate sono
"Consulente ambientale" o "Studio di ingegneria". La principale pesa molto più delle
secondarie.

**Categorie secondarie:** servizio di rimozione amianto, impresa di demolizioni, servizio di
bonifica, laboratorio o servizio di analisi ambientali. I nomi esatti variano nell'interfaccia:
digita la parola chiave e prendi la voce più vicina fra quelle proposte.

**Sezione "Servizi":** inserisci come voci separate — bonifica amianto, censimento amianto,
bonifica siti contaminati, bonifica acque di falda, piano di caratterizzazione, analisi di
rischio sanitario-ambientale, due diligence ambientale, demolizioni industriali,
decommissioning, direzione lavori ambientale. Ogni voce accetta una descrizione: usala,
riprendendo il testo delle pagine corrispondenti del sito.

**Area di servizio:** Milano e provincia, Lombardia, e l'indicazione che operate su tutto il
territorio nazionale.

**Foto:** è il fattore che più incide sulle interazioni. Caricane almeno 10 dai cantieri
reali — ne avete in `assets/img/`. Aggiungine qualcuna ogni mese.

**Verifica:** Google chiede una verifica per posta (cartolina con codice, 1-2 settimane),
telefonica o video. Finché non è verificata la scheda non compare.

**Dopo l'attivazione:** chiedi una recensione ai committenti storici con cui avete un buon
rapporto. Poche recensioni vere e dettagliate valgono più di molte generiche.

---

## 2. Google Search Console — è il pannello di controllo

Senza questo non sapremo mai se il lavoro sta funzionando: è l'unico posto dove si vede su
quali ricerche il sito compare e in che posizione.

1. https://search.google.com/search-console → aggiungi proprietà
2. Scegli **"Dominio"** (non "Prefisso URL"): copre `www`, apex e https insieme
3. Google fornisce un record **TXT** da inserire nella zona DNS su **OVH**
   (Domini → tecnitaliagroup.it → Zona DNS → Aggiungi voce → TXT, sottodominio vuoto)
4. Attendi la propagazione (da minuti a qualche ora) e premi "Verifica"
5. Menu **Sitemap** → inserisci `sitemap.xml` → Invia
6. Menu **Controllo URL** → incolla ciascuna pagina nuova → "Richiedi indicizzazione"

Da controllare dopo 2-3 settimane, nella sezione **Rendimento**: quali query generano
impressioni. Le prime saranno ricerche lunghe e specifiche, non *bonifica amianto Milano* —
è normale, e sono comunque il segnale che l'indicizzazione sta funzionando.

## 3. Bing Webmaster Tools

https://www.bing.com/webmasters — importa direttamente da Search Console, sono cinque minuti.
Vale la pena perché **Bing alimenta le risposte di ChatGPT e Copilot**: per farsi citare dagli
assistenti AI conta quanto Google.

---

## 4. Cloudflare Web Analytics — ✅ configurato

Fatto: account creato, hostname `www.tecnitaliagroup.it` registrato, e lo snippet con il token
`b1b41ac259974446a2f3e3f691c122ee` è inserito in tutte e 12 le pagine del sito.

Non è stato necessario spostare il DNS da OVH: si usa il beacon JavaScript. Nessun cookie,
nessun banner di consenso.

**Manca solo la pubblicazione del sito.** Finché le modifiche non sono su GitHub, la dashboard
resta vuota e può mostrare un avviso "no data received": è normale, non è un errore di
configurazione.

### Dove si vedono i dati

1. Vai su https://dash.cloudflare.com e accedi
2. Nella barra laterale sinistra: **Analytics & Logs → Web Analytics**
3. Scegli `www.tecnitaliagroup.it` dall'elenco dei siti
4. In alto a destra c'è il selettore del periodo: ultime 24 ore, 7 giorni, 30 giorni

### Cosa trovi, e come si legge

- **Page views** — pagine caricate in totale. **Visits** — visite iniziate da una fonte esterna.
  Sono numeri diversi: chi arriva e naviga cinque pagine conta come 1 visita e 5 visualizzazioni.
- **Top pages / Paths** — è la sezione da guardare per prima. Ti dice se le pagine nuove
  (`bonifica-amianto.html`, `bonifica-siti-contaminati.html`…) ricevono traffico e quali funzionano.
- **Referrers** — da dove arrivano. `google` significa ricerca organica; `linkedin.com` traffico
  dalla pagina aziendale; "direct" chi digita l'indirizzo o arriva da email.
- **Countries, Browsers, Operating systems, Device type** — desktop contro mobile è utile per
  capire se vale la pena curare di più una delle due rese.
- **Core Web Vitals** — velocità reale percepita dai visitatori, non simulata.

Puoi **cliccare su un valore per filtrare** tutto il resto su quello: per esempio clicca su
`/bonifica-amianto.html` per vedere solo da dove arriva chi legge quella pagina.

### Il limite da conoscere

Essendo senza cookie, Cloudflare non ricostruisce il percorso del singolo visitatore fra una
sessione e l'altra e non fa attribuzione delle conversioni. Vedi cosa succede in aggregato, non
chi lo fa. Per quello che serve qui — capire se le pagine si posizionano e portano gente — è
sufficiente. Il dato su *quali ricerche* portano traffico non sta qui ma in Search Console
(voce 2): i due strumenti si leggono insieme.

## 5. EmailJS — mettere in sicurezza il form

La chiave pubblica del form è visibile nel codice della pagina, come è normale per EmailJS.
Il problema è che **senza restrizioni chiunque può usarla per inviare email consumando la
vostra quota**, e il campo trappola antispam già presente non basta da solo.

Nel pannello https://dashboard.emailjs.com:

- **L'allow-list dei domini richiede un piano a pagamento** (verificato: il free dà l'errore
  "Subscription Limitation" già al primo dominio). Alternative: attivare la verifica reCAPTCHA v2
  nelle impostazioni del template EmailJS, oppure passare al piano Personal (9 $/mese).
  Se l'allow-list verrà attivata, il valore da inserire è `https://www.tecnitaliagroup.it`, non
  l'apex, che reindirizza a `www` e non è mai l'origine reale del form.
- Attiva il **rate limit** se disponibile nel piano.
- Valuta l'aggiunta di un CAPTCHA sul template.

Richiede 5 minuti ed è la cosa più utile di tutta questa lista sul fronte sicurezza.

---

## 6. Verifica che HTTPS resti obbligatorio

GitHub → repository `tecnitalia-web` → **Settings → Pages** → la casella **"Enforce HTTPS"**
deve essere spuntata. Ora nel repository c'è anche un file `CNAME`, quindi il dominio
personalizzato non dipende più solo dall'impostazione nel pannello.

---

## 7. Partita IVA — serve a me

Va inserita nell'informativa privacy (dove ora c'è un segnaposto evidenziato in
`privacy.html`) e nei dati strutturati. Mandamela e la sistemo.

---

## Cosa aspettarsi, onestamente

Il dominio è nuovo e non ha ancora autorità agli occhi di Google.

- **Settimane** — indicizzazione e prime impressioni su ricerche lunghe e specifiche:
  *obblighi Responsabile Rischio Amianto*, *analisi di rischio art. 242-bis*,
  *recupero inerti art. 208*, *D.Lgs. 213/2025*.
- **1-3 mesi** — comparsa nel blocco mappa sulle ricerche locali, ma **solo** se la scheda
  Google viene aperta e verificata.
- **6-12 mesi** — competizione sulle ricerche generiche e contese come *bonifica amianto
  Milano*, e solo continuando a pubblicare contenuti.

La leva più efficace nel tempo è la pubblicazione regolare sugli aggiornamenti normativi:
sono le pagine che gli altri linkano e che gli assistenti AI citano. Una ogni due o tre mesi,
quando esce qualcosa di rilevante, è un ritmo sostenibile e sufficiente.
