# -*- coding: utf-8 -*-
"""
Genera una pagina statica indicizzabile per ogni progetto di data/projects.json,
rigenera le card statiche in elenco-progetti.html e nella striscia della home,
aggiorna la sezione progetti di llms.txt e riscrive sitemap.xml.

Perche' esiste: i progetti erano renderizzati solo via JavaScript (griglia dell'archivio,
carosello della home, modale), quindi per i crawler i contenitori erano vuoti e nessun
progetto aveva un URL proprio. Qui ogni progetto diventa progetti/<slug>.html, con
contenuto, JSON-LD e canonical propri, e le card diventano veri link <a href>.

Uso:  uv run python tools/genera-progetti.py
      (dalla radice del repository; nessuna dipendenza esterna)

Va rieseguito ogni volta che si aggiunge o si modifica un progetto in
data/projects.json, e il risultato va committato.

Regole:
  - lo slug e' scritto nel JSON (campo "slug") alla prima esecuzione e poi mantenuto;
  - l'importo ("val") resta nei dati ma NON compare mai in HTML o JSON-LD.
"""
import json, io, os, re, html, sys, unicodedata

from sito_comune import (RADICE, BASE, TOKEN_CF, taglia, solo_testo, NAV_FALLBACK,
                         FOOTER_FALLBACK, CSP, ORGANIZZAZIONE, scrivi_sitemap)

# Progetti in evidenza nella striscia "I Nostri Progetti" della home. Per ogni voce si puo'
# indicare quale immagine usare (default: la prima) quando la prima foto non e' adatta a una
# card a tutta altezza.
SELEZIONE_HOME = [
    ("Fondazione Prada", 0),
    ("Ex Novaceta", 0),
    ("Ex SGL Carbon — Ascoli Piceno", 0),
    ("Area Ex Reggiani", 1),
    ("Ex Ospedali Riuniti — UMI 3, Bergamo", 0),
    ("Cascina Merlata", 0),
    ("Ex Caserma Cavalli — Novara", 1),
    ("Ex Cartiere Binda", 0),
    ("Ex Alemagna — Cornaredo (MI)", 0),
    ("Ex Stabilimento Prysmian Group", 0),
    ("Ex Riseria — Via Pienza, Milano", 0),
]

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
        <span class="eyebrow">Progetti</span>
        <h1 class="display-serif">{titolo_html}</h1>
        <p style="font-size: 1.2rem;">{sottotitolo}</p>
    </header>

    <main class="page-content project-page">
        <div class="breadcrumb" role="navigation" aria-label="Percorso di navigazione">
            <a href="/index.html">Home</a> <span aria-hidden="true">&rsaquo;</span>
            <a href="/elenco-progetti.html">Progetti</a> <span aria-hidden="true">&rsaquo;</span>
            <span aria-current="page">{titolo_html}</span>
        </div>

        <dl class="project-specs">
{specifiche}
        </dl>
{tag_html}
        <div class="project-desc">
{contenuto}
        </div>

        <section class="project-gallery" aria-label="Immagini del progetto">
{galleria}
        </section>
{correlati}
        <div style="margin-top: 50px; border-top: 1px solid #eee; padding-top: 30px;">
            <a href="/elenco-progetti.html" class="text-link">&#11013; Torna all'elenco dei progetti</a>
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


# ------------------------------------------------------------------ slug ---

def slugifica(titolo):
    t = unicodedata.normalize("NFKD", titolo)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t


def assegna_slug(progetti):
    """Mantiene gli slug gia' presenti; crea gli altri, unici. True se ha modificato i dati."""
    usati = {p["slug"] for p in progetti if p.get("slug")}
    modificato = False
    for p in progetti:
        if p.get("slug"):
            continue
        base = slugifica(p["title"])
        if not base:
            raise ValueError("titolo non slugificabile: %r" % p["title"])
        slug, n = base, 2
        while slug in usati:
            slug = "%s-%d" % (base, n)
            n += 1
        usati.add(slug)
        # "slug" subito dopo "title", per leggibilita' del JSON
        nuovo = {}
        for k, v in p.items():
            nuovo[k] = v
            if k == "title":
                nuovo["slug"] = slug
        p.clear()
        p.update(nuovo)
        modificato = True
    if len({p["slug"] for p in progetti}) != len(progetti):
        raise ValueError("slug duplicati in data/projects.json")
    return modificato


def scrivi_se_cambiato(percorso, contenuto):
    if os.path.exists(percorso):
        with io.open(percorso, encoding="utf-8") as f:
            if f.read() == contenuto:
                return False
    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    with io.open(percorso, "w", encoding="utf-8") as f:
        f.write(contenuto)
    return True


# --------------------------------------------------------------- helper ---

def img_rel(percorso):
    return "/" + percorso.lstrip("./")


def esc(t):
    return html.escape(t, quote=True)


def sottotitolo(p):
    return p["cardSubtitle"].strip()


def alt_immagine(p, i, n):
    base = "%s: %s" % (p["title"], sottotitolo(p).rstrip("."))
    return base if n == 1 else "%s (foto %d di %d)" % (base, i + 1, n)


def etichetta_tag(t):
    return t[:1].upper() + t[1:]


def periodo_iso(periodo):
    """'2025-2026 (in corso)' -> '2025/..'; '2003, 2013, 2020-2022' -> '2003/2022'; '2013' -> '2013'."""
    anni = [int(a) for a in re.findall(r"\b(?:19|20)\d{2}\b", periodo)]
    if not anni:
        return None
    a, b = min(anni), max(anni)
    if "in corso" in periodo.lower():
        return "%d/.." % a
    return str(a) if a == b else "%d/%d" % (a, b)


def correlati(p, tutti, n=3):
    """n progetti con piu' tag (e stesso committente) in comune; a parita' i piu' vicini nel tempo."""
    mio = set(p.get("tags", []))
    punteggi = []
    for i, q in enumerate(tutti):
        if q["slug"] == p["slug"]:
            continue
        comuni = len(mio & set(q.get("tags", [])))
        punti = comuni * 2 + (1 if p.get("client") and p["client"] == q.get("client") else 0)
        punteggi.append((-punti, abs(p["endYear"] - q["endYear"]), i, q))
    punteggi.sort(key=lambda x: x[:3])
    return [x[3] for x in punteggi[:n]]


# ------------------------------------------------------------------ card ---

def card_archivio(p, indent):
    """Card della griglia: stessa struttura e classi che js/main.js produceva, ma <a href>."""
    sp = " " * indent
    return (
        '{sp}<a class="project-card" href="/progetti/{slug}.html" data-tags="{tags}">\n'
        '{sp}    <div class="p-img-box">\n'
        '{sp}        <img src="{img}" alt="{alt}" loading="lazy" decoding="async" onerror="this.style.display=\'none\'">\n'
        '{sp}        <div class="hover-reveal">APRI SCHEDA</div>\n'
        '{sp}    </div>\n'
        '{sp}    <div class="p-content">\n'
        '{sp}        <span style="font-size: 0.8rem; color: #888; font-weight: 600;">Anno: {anno}</span>\n'
        '{sp}        <h4 style="margin: 5px 0 5px 0;">{titolo}</h4>\n'
        '{sp}        <p style="margin:0; font-size:0.9rem">{sub}</p>\n'
        '{sp}    </div>\n'
        '{sp}</a>'
    ).format(sp=sp, slug=p["slug"], tags=esc("|".join(p.get("tags", []))),
             img=esc(img_rel(p["images"][0])), alt=esc(alt_immagine(p, 0, 1)),
             anno=p["endYear"], titolo=html.escape(p["title"]), sub=html.escape(sottotitolo(p)))


def card_home(p, indice_img, indent):
    sp = " " * indent
    imm = p["images"][indice_img] if indice_img < len(p["images"]) else p["images"][0]
    return (
        '{sp}<a class="work-card" href="/progetti/{slug}.html" draggable="false">\n'
        '{sp}    <div class="work-card-img">\n'
        '{sp}        <img src="{img}" alt="{alt}" loading="lazy" decoding="async" draggable="false" onerror="this.style.display=\'none\'">\n'
        '{sp}        <div class="work-card-overlay">\n'
        '{sp}            <h3>{titolo}</h3>\n'
        '{sp}            <p>{sub}</p>\n'
        '{sp}        </div>\n'
        '{sp}    </div>\n'
        '{sp}</a>'
    ).format(sp=sp, slug=p["slug"], img=esc(img_rel(imm)), alt=esc(alt_immagine(p, 0, 1)),
             titolo=html.escape(p["title"]), sub=html.escape(sottotitolo(p)))


def sostituisci_blocco(percorso, inizio, fine, nuovo_corpo, descrizione):
    """Sostituisce il testo fra due marcatori (commenti HTML) di un file."""
    with io.open(percorso, encoding="utf-8") as f:
        pagina = f.read()
    if inizio not in pagina or fine not in pagina:
        raise ValueError("marcatori %s assenti in %s" % (inizio, percorso))
    a = pagina.index(inizio)
    a = pagina.index("-->", a) + 3
    b = pagina.index(fine)
    # rientro del marcatore di chiusura, mantenuto
    rientro = pagina[pagina.rfind("\n", 0, b) + 1:b]
    nuovo = pagina[:a] + "\n" + nuovo_corpo + "\n" + rientro + pagina[b:]
    if nuovo != pagina:
        with io.open(percorso, "w", encoding="utf-8") as f:
            f.write(nuovo)
    print("  %s: %s" % (os.path.basename(percorso), descrizione))


# ---------------------------------------------------------------- pagina ---

def genera_pagina(p, tutti):
    slug = p["slug"]
    url = "%s/progetti/%s.html" % (BASE, slug)
    n_img = len(p["images"])
    for i in p["images"]:
        if not os.path.exists(os.path.join(RADICE, i.lstrip("./").replace("/", os.sep))):
            print("  ATTENZIONE: immagine mancante per %s: %s" % (slug, i))

    primo_par = re.search(r"<p>(.*?)</p>", p["desc"], re.S)
    testo_desc = solo_testo(primo_par.group(1) if primo_par else p["desc"])
    descrizione_txt = taglia("%s. %s" % (p["title"], testo_desc), 157)
    descrizione = esc(descrizione_txt)
    img_abs = [BASE + img_rel(i) for i in p["images"]]

    # specifiche (committente / periodo / tipo); mai l'importo
    voci = []
    for etichetta, valore in (("Committente", p.get("client")), ("Periodo", p.get("period")),
                              ("Attività", p.get("type"))):
        if valore:
            voci.append('            <div><dt>%s</dt><dd>%s</dd></div>' % (etichetta, html.escape(valore)))
    specifiche = "\n".join(voci)

    tags = p.get("tags", [])
    tag_html = ""
    if tags:
        tag_html = ('        <ul class="project-tags" aria-label="Ambiti">' +
                    "".join("<li>%s</li>" % html.escape(etichetta_tag(t)) for t in tags) + '</ul>\n')

    galleria = []
    for i, src in enumerate(p["images"]):
        eager = 'loading="eager" fetchpriority="high"' if i == 0 else 'loading="lazy"'
        galleria.append(
            '            <figure><img src="%s" alt="%s" %s decoding="async" onerror="this.parentNode.style.display=\'none\'"></figure>'
            % (esc(img_rel(src)), esc(alt_immagine(p, i, n_img)), eager))

    cor = correlati(p, tutti)
    correlati_html = ""
    if cor:
        correlati_html = (
            '\n        <section class="related-projects" aria-labelledby="altri-progetti">\n'
            '            <h2 id="altri-progetti" class="display-serif">Altri progetti</h2>\n'
            '            <div class="projects-full-grid related-grid">\n' +
            "\n".join(card_archivio(q, 16) for q in cor) +
            '\n            </div>\n        </section>\n')

    creative = {"@type": "CreativeWork",
                "@id": url + "#progetto",
                "name": p["title"],
                "description": descrizione_txt,
                "image": img_abs,
                "url": url,
                "inLanguage": "it-IT",
                "creator": {"@id": BASE + "/#organization"},
                "mainEntityOfPage": {"@type": "WebPage", "@id": url}}
    tc = periodo_iso(p.get("period", ""))
    if tc:
        creative["temporalCoverage"] = tc
    if tags:
        creative["keywords"] = ", ".join(tags)
    grafo = [ORGANIZZAZIONE, creative,
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                 {"@type": "ListItem", "position": 2, "name": "Progetti", "item": BASE + "/elenco-progetti.html"},
                 {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]}]
    jsonld = json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False, indent=2)

    from sito_comune import assolutizza_link
    pagina = TEMPLATE.format(
        title=esc("%s | Tecnitalia Group" % p["title"]),
        og_title=esc(p["title"]),
        descrizione=descrizione,
        url=url,
        immagine_assoluta=img_abs[0],
        csp=esc(CSP),
        jsonld=jsonld,
        nav=NAV_FALLBACK,
        footer=FOOTER_FALLBACK,
        titolo_html=html.escape(p["title"]),
        sottotitolo=html.escape(sottotitolo(p)),
        specifiche=specifiche,
        tag_html=tag_html,
        contenuto=assolutizza_link(p["desc"]),
        galleria="\n".join(galleria),
        correlati=correlati_html,
        token=TOKEN_CF)
    return scrivi_se_cambiato(os.path.join(RADICE, "progetti", "%s.html" % slug), pagina)


# ------------------------------------------------------------- llms.txt ---

def aggiorna_llms(progetti):
    percorso = os.path.join(RADICE, "llms.txt")
    with io.open(percorso, encoding="utf-8") as f:
        testo = f.read()
    righe = ["## Progetti realizzati", "",
             "Una scheda per ciascun intervento: committente, periodo, attività svolta e immagini.", ""]
    for p in progetti:
        righe.append("- [%s](%s/progetti/%s.html): %s. Periodo: %s." % (
            p["title"], BASE, p["slug"], sottotitolo(p).rstrip("."), p["period"]))
    sezione = "\n".join(righe) + "\n\n"
    m = re.search(r"^## Progetti realizzati\n.*?(?=^## )", testo, re.S | re.M)
    if m:
        nuovo = testo[:m.start()] + sezione + testo[m.end():]
    else:
        pos = testo.index("## Note per i sistemi automatici")
        nuovo = testo[:pos] + sezione + testo[pos:]
    if nuovo != testo:
        with io.open(percorso, "w", encoding="utf-8") as f:
            f.write(nuovo)
    print("  llms.txt: sezione progetti (%d voci)" % len(progetti))


# ------------------------------------------------------------------ main ---

def genera():
    percorso_json = os.path.join(RADICE, "data", "projects.json")
    with io.open(percorso_json, encoding="utf-8") as f:
        progetti = json.load(f)

    for p in progetti:
        for campo in ("title", "cardSubtitle", "desc", "images", "endYear", "period"):
            if not p.get(campo):
                raise ValueError("progetto %r: campo '%s' mancante o vuoto" % (p.get("title"), campo))

    if assegna_slug(progetti):
        # stesso stile del file originale: indentazione a 4, UTF-8, niente newline finale
        with io.open(percorso_json, "w", encoding="utf-8") as f:
            f.write(json.dumps(progetti, ensure_ascii=False, indent=4))
        print("  data/projects.json: slug aggiunti")

    # ordine di visualizzazione: dal piu' recente (sort stabile, come in js/main.js)
    ordinati = sorted(progetti, key=lambda p: -p["endYear"])

    cambiate = 0
    for p in ordinati:
        if genera_pagina(p, ordinati):
            cambiate += 1
    print("  progetti/: %d pagine, %d scritte/aggiornate" % (len(ordinati), cambiate))

    sostituisci_blocco(
        os.path.join(RADICE, "elenco-progetti.html"),
        "<!-- PROGETTI-ARCHIVIO:INIZIO", "<!-- PROGETTI-ARCHIVIO:FINE -->",
        "\n".join(card_archivio(p, 12) for p in ordinati),
        "griglia statica rigenerata (%d card)" % len(ordinati))

    per_titolo = {p["title"]: p for p in progetti}
    card = []
    for titolo, i in SELEZIONE_HOME:
        if titolo not in per_titolo:
            raise ValueError("progetto della home non trovato: %r" % titolo)
        card.append(card_home(per_titolo[titolo], i, 16))
    sostituisci_blocco(
        os.path.join(RADICE, "index.html"),
        "<!-- PROGETTI-HOME:INIZIO", "<!-- PROGETTI-HOME:FINE -->",
        "\n".join(card), "striscia progetti rigenerata (%d card)" % len(card))

    aggiorna_llms(ordinati)
    scrivi_sitemap()
    return ordinati


if __name__ == "__main__":
    print("Generazione delle pagine progetto statiche")
    try:
        risultato = genera()
    except Exception as errore:
        print("ERRORE:", errore)
        sys.exit(1)
    print("Fatto: %d progetti." % len(risultato))
