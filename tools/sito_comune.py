# -*- coding: utf-8 -*-
"""
Parti condivise dai generatori statici (genera-news.py, genera-progetti.py):
costanti del sito, blocchi di ripiego di header/footer, blocco JSON-LD
dell'organizzazione, utilita' sui testi e UNICO scrittore della sitemap.xml.

La sitemap viene ricostruita ogni volta scansionando le pagine fisse, news/ e
progetti/: qualunque generatore la scriva, non perde mai gli URL dell'altro.
"""
import json, io, os, re, html, datetime, subprocess
from pathlib import Path

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.tecnitaliagroup.it"
TOKEN_CF = "b1b41ac259974446a2f3e3f691c122ee"


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

def _footer_fallback(rientro=' ' * 8):
    """Markup di footer.html (fonte unica), rientrato per l'inserimento nei
    template: la prima riga segue il segnaposto, le altre ricevono il rientro."""
    righe = (Path(__file__).resolve().parent.parent / 'footer.html').read_text(encoding='utf-8').strip().splitlines()
    return '\n'.join([righe[0]] + [(rientro + r) if r.strip() else '' for r in righe[1:]])


FOOTER_FALLBACK = _footer_fallback()

CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline' https://static.cloudflareinsights.com; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; "
       "connect-src 'self' https://api.emailjs.com https://cloudflareinsights.com; "
       "frame-src https://maps.google.com https://www.google.com; "
       "object-src 'none'; base-uri 'self'; form-action 'self'")

_INDIRIZZO = {'@type': 'PostalAddress', 'streetAddress': 'Via Pastorelli 4E', 'postalCode': '20143', 'addressLocality': 'Milano', 'addressRegion': 'MI', 'addressCountry': 'IT'}

SUB_ORGANIZZAZIONI = [{'@type': 'Organization', '@id': 'https://www.tecnitaliagroup.it/#tecnitalia-ingegneria', 'name': 'Tecnitalia Ingegneria', 'legalName': 'Tecnitalia Ingegneria Studio Associato di Bressi e Micco', 'vatID': 'IT06874430967', 'taxID': '06874430967', 'address': _INDIRIZZO, 'url': 'https://www.tecnitaliagroup.it/dettaglio-ingegneria.html'}, {'@type': 'Organization', '@id': 'https://www.tecnitaliagroup.it/#tecnitalia-servizi', 'name': 'Tecnitalia Servizi', 'legalName': 'Tecnitalia Servizi S.r.l.', 'vatID': 'IT03923790962', 'taxID': '03923790962', 'address': _INDIRIZZO, 'url': 'https://www.tecnitaliagroup.it/dettaglio-servizi.html'}]

ORGANIZZAZIONE = {
    "@type": "ProfessionalService",
    "@id": BASE + "/#organization",
    "name": "Tecnitalia Group",
    "url": BASE + "/",
    "sameAs": ["https://www.linkedin.com/company/71564171/"],
    "subOrganization": SUB_ORGANIZZAZIONI,
    "logo": BASE + "/assets/img/logo.png",
    "telephone": "+390276000206",
    "email": "info@tecnitaliagroup.it",
    "foundingDate": "1986",
    "address": {"@type": "PostalAddress", "streetAddress": "Via Pastorelli 4E",
                "postalCode": "20143", "addressLocality": "Milano",
                "addressRegion": "MI", "addressCountry": "IT"},
    "areaServed": {"@type": "Country", "name": "Italia"},
}



# ---------------------------------------------------------------- sitemap ---

def _lastmod_git(percorso_rel):
    """Data dell'ultimo commit che ha toccato il file; oggi se il file non e'
    tracciato o ha modifiche non committate. Stabile fra un'esecuzione e l'altra."""
    oggi = datetime.date.today().isoformat()
    try:
        sporco = subprocess.run(["git", "status", "--porcelain", "--", percorso_rel],
                                cwd=RADICE, capture_output=True, text=True, check=True).stdout.strip()
        if sporco:
            return oggi
        data = subprocess.run(["git", "log", "-1", "--format=%cs", "--", percorso_rel],
                              cwd=RADICE, capture_output=True, text=True, check=True).stdout.strip()
        return data or oggi
    except Exception:
        return oggi


def _date_news():
    """slug -> data ISO di pubblicazione, da data/news.json."""
    mesi = {"gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4, "maggio": 5, "giugno": 6,
            "luglio": 7, "agosto": 8, "settembre": 9, "ottobre": 10, "novembre": 11, "dicembre": 12}
    percorso = os.path.join(RADICE, "data", "news.json")
    if not os.path.exists(percorso):
        return {}
    with io.open(percorso, encoding="utf-8") as f:
        news = json.load(f)
    date = {}
    for n in news:
        m = re.match(r"\s*(\d{1,2})\s+([A-Za-zàèéìòù]+)\s+(\d{4})\s*$", n.get("data", ""))
        if m and m.group(2).lower() in mesi:
            date[n["slug"]] = "%04d-%02d-%02d" % (int(m.group(3)), mesi[m.group(2).lower()], int(m.group(1)))
    return date


def scrivi_sitemap():
    """Riscrive sitemap.xml scansionando pagine fisse, news/ e progetti/."""
    voci = []
    for p, prio, freq in PAGINE_FISSE:
        rel = p or "index.html"
        if not os.path.exists(os.path.join(RADICE, rel)):
            print("  ATTENZIONE: pagina fissa mancante: %s" % rel)
            continue
        voci.append((BASE + "/" + p, _lastmod_git(rel), freq, prio))

    date = _date_news()
    cartella = os.path.join(RADICE, "news")
    for nome in sorted(os.listdir(cartella)) if os.path.isdir(cartella) else []:
        if nome.endswith(".html"):
            slug = nome[:-5]
            voci.append((BASE + "/news/" + nome, date.get(slug) or _lastmod_git("news/" + nome),
                         "yearly", "0.7"))

    cartella = os.path.join(RADICE, "progetti")
    for nome in sorted(os.listdir(cartella)) if os.path.isdir(cartella) else []:
        if nome.endswith(".html"):
            voci.append((BASE + "/progetti/" + nome, _lastmod_git("progetti/" + nome),
                         "yearly", "0.6"))

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
    nuovo = "\n".join(righe) + "\n"
    percorso = os.path.join(RADICE, "sitemap.xml")
    attuale = None
    if os.path.exists(percorso):
        with io.open(percorso, encoding="utf-8") as f:
            attuale = f.read()
    if attuale != nuovo:
        with io.open(percorso, "w", encoding="utf-8") as f:
            f.write(nuovo)
    print("  sitemap.xml: %d URL" % len(voci))
    return len(voci)
