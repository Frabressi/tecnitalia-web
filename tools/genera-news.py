# -*- coding: utf-8 -*-
"""
Genera una pagina statica indicizzabile per ogni articolo di data/news.json,
e riscrive sitemap.xml.

Perche' esiste: il sito carica le news via JavaScript su news-singola.html?id=N,
quindi tutti gli articoli condividono un solo URL e nessuno di essi puo' essere
indicizzato singolarmente. Questo script produce un file per articolo, con il
contenuto gia' presente nell'HTML servito, JSON-LD NewsArticle e canonical propri.

Uso:  python tools/genera-news.py
      (dalla radice del repository; nessuna dipendenza esterna)

Va rieseguito ogni volta che si aggiunge o si modifica un articolo in
data/news.json, e il risultato va committato.

Le pagine sono generate nella cartella news/. Perche' funzionino da li', js/main.js
carica header, footer e JSON con percorsi assoluti (fetch('/header.html')), e le
pagine generate usano percorsi assoluti per asset e link interni.
"""
import json, io, os, re, html, datetime, sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.tecnitaliagroup.it"
TOKEN_CF = "b1b41ac259974446a2f3e3f691c122ee"

MESI = {"gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4, "maggio": 5, "giugno": 6,
        "luglio": 7, "agosto": 8, "settembre": 9, "ottobre": 10, "novembre": 11, "dicembre": 12}

# Pagine fisse del sito, per la sitemap: (percorso, priorita, frequenza)
PAGINE_FISSE = [
    ("", "1.0", "monthly"),
    ("bonifica-amianto.html", "0.9", "monthly"),
    ("bonifica-siti-contaminati.html", "0.9", "monthly"),
    ("caratterizzazione-analisi-rischio.html", "0.9", "monthly"),
    ("demolizioni-decommissioning.html", "0.9", "monthly"),
    ("dettaglio-ingegneria.html", "0.8", "monthly"),
    ("dettaglio-servizi.html", "0.8", "monthly"),
    ("elenco-progetti.html", "0.8", "monthly"),
    ("chi-siamo.html", "0.7", "yearly"),
    ("archivio-news.html", "0.6", "weekly"),
    ("privacy.html", "0.2", "yearly"),
]


def data_iso(testo):
    """'30 Agosto 2026' -> '2026-08-30'."""
    m = re.match(r"\s*(\d{1,2})\s+([A-Za-zàèéìòù]+)\s+(\d{4})\s*$", testo)
    if not m:
        raise ValueError("data non riconosciuta: %r" % testo)
    giorno, mese, anno = int(m.group(1)), m.group(2).lower(), int(m.group(3))
    if mese not in MESI:
        raise ValueError("mese non riconosciuto: %r" % mese)
    return "%04d-%02d-%02d" % (anno, MESI[mese], giorno)


def taglia(testo, n=157):
    t = re.sub(r"\s+", " ", testo).strip()
    if len(t) <= n:
        return t
    return t[:n].rsplit(" ", 1)[0].rstrip(" ,;:.") + "…"


PAGINE_ROOT = ["index", "chi-siamo", "archivio-news", "dettaglio-ingegneria", "bonifica-amianto",
               "bonifica-siti-contaminati", "caratterizzazione-analisi-rischio",
               "demolizioni-decommissioning", "dettaglio-servizi", "elenco-progetti", "privacy"]


def assolutizza_link(frammento):
    """I link relativi scritti negli articoli puntano a pagine della root.

    Le pagine generate stanno in /news/, quindi un href="bonifica-amianto.html"
    si risolverebbe in /news/bonifica-amianto.html. Li si porta a percorso assoluto."""
    frammento = frammento.replace('src="./assets/', 'src="/assets/')
    frammento = frammento.replace('href="./assets/', 'href="/assets/')
    for pagina in PAGINE_ROOT:
        frammento = frammento.replace('href="%s.html"' % pagina, 'href="/%s.html"' % pagina)
        frammento = frammento.replace('href="%s.html#' % pagina, 'href="/%s.html#' % pagina)
    return frammento


def solo_testo(frammento):
    t = re.sub(r"<[^>]+>", " ", frammento)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


# Il fallback statico deve essere identico, struttura e classi comprese, al
# markup realmente iniettato da js/main.js (contenuto di header.html /
# footer.html): altrimenti al caricamento si vede lo swap "flash" tra il
# fallback e il markup con stile reale. Percorsi assoluti: funzionano anche
# da /news/.
NAV_FALLBACK = (
    '<nav>\n'
    '            <a href="/index.html" class="logo-container">\n'
    '                <img src="/assets/img/logo-white.png" alt="Tecnitalia Group" class="logo-img logo-img-white">\n'
    '                <img src="/assets/img/logo.png" alt="Tecnitalia Group" class="logo-img logo-img-color">\n'
    '            </a>\n'
    '            <div class="nav-links" id="nav-links">\n'
    '                <a href="/index.html">Home</a> <a href="/chi-siamo.html">Chi Siamo</a>\n'
    '                <a href="/archivio-news.html">News</a>\n'
    '                <div class="nav-item-dropdown">\n'
    '                    <div class="nav-dropdown-head">\n'
    '                        <a href="/dettaglio-ingegneria.html" class="nav-dropdown-toggle" aria-haspopup="true" aria-expanded="false" aria-controls="nav-dropdown-menu-ingegneria">Tecnitalia Ingegneria <span class="nav-caret" aria-hidden="true">&#9662;</span></a>\n'
    '                        <button type="button" class="nav-dropdown-btn" aria-haspopup="true" aria-expanded="false" aria-controls="nav-dropdown-menu-ingegneria" aria-label="Mostra il sottomenu di Tecnitalia Ingegneria">\n'
    '                            <span class="nav-caret" aria-hidden="true">&#9662;</span>\n'
    '                        </button>\n'
    '                    </div>\n'
    '                    <div class="nav-dropdown-menu" id="nav-dropdown-menu-ingegneria">\n'
    '                        <a href="/dettaglio-ingegneria.html">Tecnitalia Ingegneria</a>\n'
    '                        <a href="/bonifica-amianto.html">Bonifica Amianto</a>\n'
    '                        <a href="/bonifica-siti-contaminati.html">Bonifica Siti Contaminati</a>\n'
    '                        <a href="/caratterizzazione-analisi-rischio.html">Caratterizzazione e Analisi di Rischio</a>\n'
    '                        <a href="/demolizioni-decommissioning.html">Demolizioni e Decommissioning</a>\n'
    '                    </div>\n'
    '                </div>\n'
    '                <a href="/dettaglio-servizi.html">Tecnitalia Servizi</a>\n'
    '                <a href="/elenco-progetti.html">Progetti</a>\n'
    '                <a href="/index.html#team">Team</a>\n'
    '            </div>\n'
    '            <button type="button" class="hamburger" aria-label="Apri menu di navigazione" aria-expanded="false" aria-controls="nav-links">☰</button>\n'
    '        </nav>')

FOOTER_FALLBACK = (
    '<footer id="contatti" class="footer-sec">\n'
    '            <div class="footer-grid">\n'
    '                <div>\n'
    '                    <h3 style="color:white; margin-bottom:20px;">Contattaci</h3>\n'
    '                    <p><strong>Tecnitalia Group</strong><br>Via Pastorelli 4E, 20143 Milano</p>\n'
    '                    <p>Tel: 02 76000206<br>Email: info@tecnitaliagroup.it</p>\n'
    '                    <a href="/privacy.html" class="footer-link">Informativa privacy</a>\n'
    '                </div>\n'
    '                <div class="footer-services-col">\n'
    '                    <h3 style="color:white; margin-bottom:20px;">Servizi</h3>\n'
    '                    <a href="/dettaglio-ingegneria.html" class="footer-link">Tecnitalia Ingegneria</a>\n'
    '                    <a href="/bonifica-amianto.html" class="footer-link">Bonifica Amianto</a>\n'
    '                    <a href="/bonifica-siti-contaminati.html" class="footer-link">Bonifica Siti Contaminati</a>\n'
    '                    <a href="/caratterizzazione-analisi-rischio.html" class="footer-link">Caratterizzazione e Analisi di Rischio</a>\n'
    '                    <a href="/demolizioni-decommissioning.html" class="footer-link">Demolizioni e Decommissioning</a>\n'
    '                    <a href="/dettaglio-servizi.html" class="footer-link">Tecnitalia Servizi</a>\n'
    '                </div>\n'
    '                <div class="form-box">\n'
    '                    <form id="contact-form">\n'
    '                        <input type="text" name="name" placeholder="Nome" required>\n'
    '                        <input type="email" name="email" placeholder="Email" required>\n'
    '                        <textarea name="message" rows="3" placeholder="Messaggio" required></textarea>\n'
    '                        <input type="text" name="website" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true">\n'
    '                        <button type="submit" class="submit-btn" id="submit-btn">Invia Messaggio</button>\n'
    '                    </form>\n'
    '                    <div id="form-status" style="display:none; color:white; margin-top:15px; text-align:center; font-weight:bold; font-size:0.9rem;"></div>\n'
    '                </div>\n'
    '                <div class="footer-map-box">\n'
    '                    <h3 style="color:white; margin-bottom:20px;">La Nostra Sede</h3>\n'
    '                    <div class="map-container" style="width:100%; border-radius:6px; overflow:hidden; background:#222;">\n'
    '                        <iframe \n'
    '                            src="https://maps.google.com/maps?q=Via%20Pastorelli%204E,%2020143%20Milano&t=&z=15&ie=UTF8&iwloc=&output=embed" \n'
    '                            width="100%" \n'
    '                            height="140" \n'
    '                            style="border:0; display:block;" \n'
    '                            allowfullscreen="" \n'
    '                            loading="lazy" \n'
    '                            referrerpolicy="no-referrer-when-downgrade">\n'
    '                        </iframe>\n'
    '                    </div>\n'
    '                    <a href="https://maps.google.com/maps?q=Via%20Pastorelli%204E,%2020143%20Milano" target="_blank" class="map-link" style="color:#aaa; text-decoration:none; font-size:0.85rem; margin-top:10px; display:inline-block; font-weight:600;">\n'
    '                        Apri in Google Maps ➔\n'
    '                    </a>\n'
    '                </div>\n'
    '            </div>\n'
    '            <div style="text-align:center; margin-top:50px; border-top:1px solid #333; padding-top:20px;">\n'
    '                © 2026 Tecnitalia Group. Tutti i diritti riservati.\n'
    '            </div>\n'
    '        </footer>')

CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline' https://static.cloudflareinsights.com; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; "
       "connect-src 'self' https://api.emailjs.com https://cloudflareinsights.com; "
       "frame-src https://maps.google.com https://www.google.com; "
       "object-src 'none'; base-uri 'self'; form-action 'self'")

ORGANIZZAZIONE = {
    "@type": "ProfessionalService",
    "@id": BASE + "/#organization",
    "name": "Tecnitalia Group",
    "url": BASE + "/",
    "logo": BASE + "/assets/img/logo.png",
    "telephone": "+390276000206",
    "email": "info@tecnitaliagroup.it",
    "foundingDate": "1986",
    "address": {"@type": "PostalAddress", "streetAddress": "Via Pastorelli 4E",
                "postalCode": "20143", "addressLocality": "Milano",
                "addressRegion": "MI", "addressCountry": "IT"},
    "areaServed": {"@type": "Country", "name": "Italia"},
}

TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{descrizione}">
    <link rel="canonical" href="{url}">
    <meta property="og:type" content="article">
    <meta property="og:locale" content="it_IT">
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{descrizione}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{immagine_assoluta}">
    <meta property="article:published_time" content="{iso}">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" type="image/png" href="/assets/img/favicon-32.png">
    <link rel="icon" href="/assets/img/favicon.ico" sizes="any">
    <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
    <script defer src="/assets/vendor/gsap.min.js"></script>
    <script defer src="/assets/vendor/ScrollTrigger.min.js"></script>
    <script defer src="/assets/vendor/lenis.min.js"></script>
    <script defer type="text/javascript" src="/assets/vendor/emailjs.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=Fraunces:opsz,wght@9..144,300..700&family=Manrope:wght@300;400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/style.css">
    <meta name="referrer" content="strict-origin-when-cross-origin">
    <meta http-equiv="Content-Security-Policy" content="{csp}">
    <script type="application/ld+json">
{jsonld}
    </script>
</head>
<body>

    <div id="nav-placeholder">
        {nav}
    </div>

    <header class="page-header">
        <span class="eyebrow">News</span>
        <h1 class="display-serif">{titolo_html}</h1>
        <p style="font-size: 1.2rem;">{data}</p>
    </header>

    <main class="page-content">
        <img src="{immagine}" alt="{alt}" loading="eager" fetchpriority="high" decoding="async" onerror="this.style.display='none'" style="width: 100%; border-radius: 10px; margin-bottom: 30px; object-fit: cover; max-height: 450px; display: block;">

        <div style="color:#333; line-height: 1.8;">
{contenuto}
        </div>

        <div style="margin-top: 50px; border-top: 1px solid #eee; padding-top: 30px;">
            <a href="/archivio-news.html" class="text-link">&#11013; Torna all'Archivio News</a>
        </div>
    </main>

    <div id="footer-placeholder">
        {footer}
    </div>

    <script defer src="/js/main.js"></script>

    <!-- Cloudflare Web Analytics -->
    <script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "{token}"}}'></script>
    <!-- End Cloudflare Web Analytics -->
</body>
</html>
"""


def genera():
    percorso = os.path.join(RADICE, "data", "news.json")
    with io.open(percorso, encoding="utf-8") as f:
        news = json.load(f)

    visti = set()
    generati = []
    for n in news:
        for campo in ("id", "slug", "titolo", "data", "riassunto", "contenuto", "immagine"):
            if not n.get(campo):
                raise ValueError("articolo %s: campo '%s' mancante o vuoto" % (n.get("id"), campo))
        if n["slug"] in visti:
            raise ValueError("slug duplicato: %r" % n["slug"])
        visti.add(n["slug"])

        iso = data_iso(n["data"])
        nome = "news/%s.html" % n["slug"]
        url = "%s/%s" % (BASE, nome)
        img_rel = "/" + n["immagine"].lstrip("./")
        img_abs = BASE + "/" + img_rel.lstrip("./")

        immagine_su_disco = os.path.join(RADICE, img_rel.lstrip("./").replace("/", os.sep))
        if not os.path.exists(immagine_su_disco):
            print("  ATTENZIONE: immagine mancante per %s: %s" % (n["id"], img_rel))

        descrizione = html.escape(taglia(n["riassunto"]), quote=True)
        titolo_esc = html.escape(n["titolo"], quote=True)

        grafo = [
            ORGANIZZAZIONE,
            {"@type": "NewsArticle",
             "headline": n["titolo"][:110],
             "description": taglia(n["riassunto"]),
             "image": [img_abs],
             "datePublished": iso,
             "dateModified": iso,
             "inLanguage": "it-IT",
             "author": {"@id": BASE + "/#organization"},
             "publisher": {"@id": BASE + "/#organization"},
             "mainEntityOfPage": {"@type": "WebPage", "@id": url},
             "url": url,
             "articleSection": "Aggiornamenti normativi"},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "News", "item": BASE + "/archivio-news.html"},
                {"@type": "ListItem", "position": 3, "name": n["titolo"], "item": url}]},
        ]
        jsonld = json.dumps({"@context": "https://schema.org", "@graph": grafo},
                            ensure_ascii=False, indent=2)

        pagina = TEMPLATE.format(
            title=html.escape("%s | Tecnitalia Group" % n["titolo"], quote=True),
            og_title=titolo_esc,
            descrizione=descrizione,
            url=url,
            immagine_assoluta=img_abs,
            immagine=html.escape(img_rel, quote=True),
            alt=titolo_esc,
            iso=iso,
            csp=html.escape(CSP, quote=True),
            jsonld=jsonld,
            nav=NAV_FALLBACK,
            footer=FOOTER_FALLBACK,
            titolo_html=html.escape(n["titolo"]),
            data=html.escape(n["data"]),
            contenuto=assolutizza_link(n["contenuto"]),
            token=TOKEN_CF)

        destinazione = os.path.join(RADICE, "news", "%s.html" % n["slug"])
        os.makedirs(os.path.dirname(destinazione), exist_ok=True)
        with io.open(destinazione, "w", encoding="utf-8") as f:
            f.write(pagina)

        parole = len(solo_testo(n["contenuto"]).split())
        generati.append((nome, iso, parole))
        print("  generata  %-56s %s  %4d parole" % (nome, iso, parole))

    scrivi_sitemap(generati)
    aggiorna_home(news)
    return generati


def aggiorna_home(news):
    """Rigenera il blocco statico delle ultime news in index.html.

    Il blocco e' contenuto di ripiego: js/main.js lo sostituisce al rendering.
    Serve pero' ai crawler, che leggono l'HTML prima di eseguire JavaScript, e
    senza rigenerazione automatica invecchia a ogni nuovo articolo.
    """
    percorso = os.path.join(RADICE, "index.html")
    with io.open(percorso, encoding="utf-8") as f:
        pagina = f.read()

    inizio = "<!-- NEWS-HOME:INIZIO"
    fine = "<!-- NEWS-HOME:FINE -->"
    if inizio not in pagina or fine not in pagina:
        print("  ATTENZIONE: marcatori NEWS-HOME assenti in index.html, blocco non aggiornato")
        return

    card = []
    for n in news[:3]:
        card.append(
            '            <div class="project-card" style="min-width: unset;">\n'
            '                <div class="p-content">\n'
            '                    <span style="font-size: 0.8rem; color: #888; font-weight: 600;">%s</span>\n'
            '                    <h4 style="margin: 10px 0 15px 0; font-size: 1.3rem;">%s</h4>\n'
            '                    <p style="font-size:0.95rem">%s</p>\n'
            '                    <a href="news-%s.html" style="color: var(--blue); font-weight: bold; '
            'text-decoration: none; font-size: 0.9rem;">Leggi l\'articolo &#10132;</a>\n'
            '                </div>\n'
            '            </div>' % (html.escape(n["data"]), html.escape(n["titolo"]),
                                    html.escape(taglia(n["riassunto"], 180)), n["slug"]))

    a = pagina.index(inizio)
    a = pagina.index("-->", a) + 3
    b = pagina.index(fine)
    nuovo = pagina[:a] + "\n" + "\n".join(card) + "\n            " + pagina[b:]
    with io.open(percorso, "w", encoding="utf-8") as f:
        f.write(nuovo)
    print("  index.html: blocco ultime news rigenerato (%d card)" % len(card))


def scrivi_sitemap(generati):
    oggi = datetime.date.today().isoformat()
    voci = [(BASE + "/" + p, oggi, freq, prio) for p, prio, freq in PAGINE_FISSE]
    voci += [(BASE + "/" + nome, iso, "yearly", "0.7") for nome, iso, _ in generati]

    righe = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, freq, prio in voci:
        righe += ["  <url>",
                  "    <loc>%s</loc>" % loc,
                  "    <lastmod>%s</lastmod>" % lastmod,
                  "    <changefreq>%s</changefreq>" % freq,
                  "    <priority>%s</priority>" % prio,
                  "  </url>"]
    righe.append("</urlset>")
    with io.open(os.path.join(RADICE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(righe) + "\n")
    print("  sitemap.xml aggiornata: %d URL" % len(voci))


if __name__ == "__main__":
    print("Generazione delle pagine news statiche")
    try:
        risultato = genera()
    except Exception as errore:
        print("ERRORE:", errore)
        sys.exit(1)
    print("Fatto: %d pagine generate." % len(risultato))
