# Prompt per Claude in Chrome — Pagina LinkedIn di Tecnitalia Group

Aggiornato al 30 agosto 2026.

**Obiettivo:** completare la pagina aziendale con tutto quello che serve, senza pubblicare post.
Una pagina completa vale anche per la ricerca su Google: LinkedIn è uno dei primi risultati sulle
ricerche di marca e concorre a definire l'entità "Tecnitalia Group" agli occhi dei motori.

**Prima di iniziare:** serve essere amministratore della pagina aziendale. Se la pagina non esiste
ancora, il prompt 0 la crea. Claude in Chrome opererà sulla tua sessione LinkedIn già autenticata:
ti chiederà conferma prima di salvare le modifiche, quindi rileggi sempre prima di approvare.

Esegui i prompt **nell'ordine**, uno alla volta.

---

## Prompt 0 — Verifica preliminare (solo lettura, non modifica nulla)

```
Vai su linkedin.com e cerca se esiste già una pagina aziendale per "Tecnitalia Group" o
"Tecnitalia" (studio di ingegneria ambientale, Milano). Controlla anche se esistono pagine
duplicate o pagine generate automaticamente da LinkedIn che nessuno ha rivendicato.

Non modificare nulla. Riportami:
1. quante pagine hai trovato e i loro URL
2. per ciascuna: se risulta rivendicata, quanti follower ha, quali sezioni sono vuote
3. quanti dipendenti risultano associati a ciascuna pagina
4. se ho i permessi di amministratore su una di esse

Se ne esistono più di una, dimmelo chiaramente: due pagine sullo stesso nome si annullano a
vicenda e va deciso quale tenere prima di procedere.
```

---

## Prompt 1 — Dati identificativi

```
Apri la pagina aziendale LinkedIn di Tecnitalia Group in modalità amministratore e vai nella
sezione di modifica delle informazioni della pagina.

Compila o correggi questi campi con i valori esatti che ti do:

- Nome: Tecnitalia Group
- Slogan / Tagline: Ingegneria ambientale dal 1986. Bonifica di siti contaminati, amianto, decommissioning industriale.
- Sito web: https://www.tecnitaliagroup.it/
- Settore: cerca "Servizi ambientali" (in inglese "Environmental Services"). Se non esiste,
  usa "Servizi di consulenza ambientale" o l'opzione più vicina, e dimmi quale hai scelto.
- Dimensioni azienda: chiedimelo prima di impostarlo, non lo conosco
- Tipo di società: Società di persone o Libero professionista — chiedimelo prima di scegliere
- Anno di fondazione: 1986
- Sede principale: Via Pastorelli 4E, 20143 Milano, Italia
- Telefono: 02 76000206

Controlla anche l'URL pubblico della pagina: se contiene numeri o caratteri casuali, proponimi
una versione pulita tipo linkedin.com/company/tecnitalia-group.

Mostrami un riepilogo di tutte le modifiche PRIMA di salvare. Se un campo obbligatorio ti
manca, fermati e chiedimelo invece di inventarlo.
```

---

## Prompt 2 — Descrizione e specializzazioni

```
Nella pagina aziendale LinkedIn di Tecnitalia Group, in modalità amministratore, apri la
modifica delle informazioni.

Incolla questo testo nel campo "Descrizione" / "Panoramica" (About), esattamente come te lo do,
senza riscriverlo né riassumerlo:

---INIZIO TESTO---
Tecnitalia Group è uno studio di ingegneria ambientale con sede a Milano, attivo dal 1986.

Ci occupiamo di siti contaminati e di compendi industriali dismessi seguendo il procedimento nella sua interezza: dalla caratterizzazione all'analisi di rischio, dalla progettazione della bonifica alla Direzione Lavori, fino alla certificazione finale di avvenuta bonifica.

AREE DI COMPETENZA

• Bonifica di siti contaminati — suolo, sottosuolo e acque di falda ai sensi del Titolo V della Parte IV del D.Lgs. 152/2006, con messa in sicurezza operativa e permanente dove la bonifica integrale non è praticabile. Tecnologie pump & treat con impianti TAF, soil vapor extraction, bioventing, soil washing, biopile, capping.

• Amianto — censimento e mappatura dei materiali contenenti amianto, valutazione dello stato di degrado, progettazione e Direzione Lavori della rimozione, amianto friabile e compatto, FAV. Dal 2017 curiamo il censimento dell'amianto negli edifici del Comune di Milano.

• Caratterizzazione e analisi di rischio — piani di caratterizzazione, analisi di rischio sanitario-ambientale sito-specifica, due diligence ambientale nelle compravendite industriali, perizie e consulenza tecnica di parte e d'ufficio.

• Demolizioni e decommissioning — smantellamento controllato di compendi industriali sotto un'unica Direzione Lavori, con recupero degli inerti direttamente in cantiere tramite impianti mobili autorizzati ex art. 208 del D.Lgs. 152/2006.

Lavoriamo su tempi lunghi. Sui siti più complessi seguiamo l'intero percorso: l'ex Industrie Chimiche Baslini di Treviglio dal 2007 al 2023, l'ex Zincheria Origoni dal 2004 al 2021, l'ex Saponificio Sirio dal 2003 al 2022.

Fra gli interventi realizzati: i Gasometri della Bovisa, le ex Cartiere Binda, le ex Officine Metallurgiche Broggi oggi sede del Politecnico, l'area della Fondazione Prada, Cascina Merlata, l'ex Novaceta di Magenta.

www.tecnitaliagroup.it
---FINE TESTO---

Poi, nel campo "Specializzazioni" (Specialties), inserisci queste 20 voci, una per una:

Bonifica siti contaminati
Bonifica amianto
Censimento amianto
Caratterizzazione ambientale
Analisi di rischio sanitario-ambientale
Bonifica acque di falda
Messa in sicurezza operativa
Messa in sicurezza permanente
Decommissioning industriale
Demolizioni industriali
Strip-out
Recupero inerti in cantiere
Gestione rifiuti speciali
Terre e rocce da scavo
Due diligence ambientale
Direzione Lavori
Coordinamento della sicurezza
Perizie ambientali
Trattamento acque reflue
Riqualificazione aree industriali dismesse

Verifica che il testo non sia stato troncato dal limite di caratteri: se LinkedIn ti segnala
che è troppo lungo, dimmelo e NON tagliarlo di tua iniziativa.

Mostrami come appare prima di salvare.
```

---

## Prompt 3 — Logo e immagine di copertina

```
Nella pagina aziendale LinkedIn di Tecnitalia Group, controlla lo stato di logo e immagine di
copertina.

Dimmi:
1. se il logo è presente, e se ha una risoluzione adeguata (LinkedIn consiglia almeno 300x300 px)
2. se l'immagine di copertina è presente e con quali dimensioni (consigliato 1128x191 px)
3. come appaiono entrambi nell'anteprima, sia da desktop che da mobile

Non caricare nulla: dimmi solo cosa manca e con quali dimensioni devo preparare i file, così te
li fornisco io.
```

---

## Prompt 4 — Pulsante, hashtag e sezioni aggiuntive

```
Nella pagina aziendale LinkedIn di Tecnitalia Group, in modalità amministratore:

1. Imposta il pulsante personalizzato in alto sulla pagina su "Visita il sito web", puntato a
   https://www.tecnitaliagroup.it/

2. Configura i tre hashtag associati alla pagina (le "community" che la pagina segue):
   #bonifiche #amianto #ingegneriaambientale

3. Verifica se la pagina ha a disposizione una sezione "Servizi" o "Prodotti". Se sì, dimmi come
   funziona e quali campi richiede, senza compilarla: te la faccio compilare dopo con i testi giusti.

4. Controlla se esistono altre sezioni della pagina rimaste vuote (sedi aggiuntive, lingue della
   pagina, sezione "Vita aziendale"). Elencamele senza compilarle.

Mostrami cosa cambierai prima di salvare.
```

---

## Prompt 5 — Dipendenti collegati e verifica finale

```
Sulla pagina aziendale LinkedIn di Tecnitalia Group:

1. Dimmi quante persone risultano attualmente associate alla pagina come dipendenti. È un
   segnale importante di credibilità: se sono poche, spiegami come i colleghi devono impostare
   il campo azienda nel proprio profilo per collegarsi alla pagina corretta (con l'URL esatto
   della pagina da usare).

2. Controlla se LinkedIn offre la verifica della pagina aziendale e, se sì, dimmi quali requisiti
   chiede e quali passaggi devo fare. Non avviare la procedura.

3. Fai un ultimo controllo completo della pagina come la vedrebbe un visitatore esterno non
   collegato: aprila in una finestra anonima e dimmi cosa risulta ancora incompleto, sbagliato o
   poco chiaro.

Riportami un elenco puntato delle cose che restano da sistemare, in ordine di importanza.
```

---

## Dopo, tornando al sito

Quando la pagina è pronta, **mandami l'URL definitivo**: va inserito nella proprietà `sameAs` dei
dati strutturati JSON-LD del sito. È il collegamento che dice a Google e agli assistenti AI che il
sito e la pagina LinkedIn sono la stessa entità, e rafforza entrambi.

Stesso discorso per la scheda Google Business Profile: vedi `docs/checklist-visibilita.md`.
