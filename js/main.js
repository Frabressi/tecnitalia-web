let newsDati = [];

document.addEventListener("DOMContentLoaded", () => {
    // Pipeline asincrona parallela per il caricamento delle risorse
    Promise.all([
        fetch('/header.html').then(res => {
            if (!res.ok) throw new Error(`HTTP error header! status: ${res.status}`);
            return res.text();
        }),
        fetch('/footer.html').then(res => {
            if (!res.ok) throw new Error(`HTTP error footer! status: ${res.status}`);
            return res.text();
        }),
        fetch('/data/news.json').then(res => res.ok ? res.json() : []).catch(() => [])
    ]).then(([headerData, footerData, newsJson]) => {
        const navPlaceholder = document.getElementById('nav-placeholder');
        const footerPlaceholder = document.getElementById('footer-placeholder');
        
        // Iniezione componenti strutturali nel DOM
        if (navPlaceholder) navPlaceholder.innerHTML = headerData;
        if (footerPlaceholder) footerPlaceholder.innerHTML = footerData;
        
        // --- INTEGRAZIONE EMAILJS ---
        // Deve essere eseguita qui, altrimenti il form non esiste ancora nel DOM
        inizializzaEmailJS();
        // -----------------------------
        
        newsDati = newsJson;

        // Le card dei progetti (archivio e home) sono HTML statico generato da
        // tools/genera-progetti.py: qui non si renderizzano, si attivano solo i comportamenti.
        renderNews();
        setupWorkScroller();

        initNavbar();
        initStatsCounters();
        initScrollReveals();

        // Ricalcolo layout per GSAP dopo il rendering dinamico
        setTimeout(() => {
            if (typeof ScrollTrigger !== 'undefined') {
                ScrollTrigger.refresh();
            }
        }, 150);
        
    }).catch(error => {
        console.error("Errore nell'inizializzazione:", error);
    });
});

function initNavbar() {
    const nav = document.querySelector('nav');
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (!nav) return;

    // Le pagine senza .hero (tutte tranne la home) non hanno nulla di scuro
    // dietro la nav fissa: la nav deve partire già nello stato "scrolled"
    // (sfondo opaco, testo scuro) e restarci sempre.
    const hasHero = !!document.querySelector('.hero');
    const isNavSolid = () => hasHero ? window.scrollY > 50 : true;

    if (!hasHero) {
        nav.classList.add('scrolled');
    } else {
        window.addEventListener('scroll', () => {
            if (isNavSolid()) {
                nav.classList.add('scrolled');
                if(navLinks && !navLinks.classList.contains('active') && hamburger) hamburger.style.color = "#1d1d1f";
            } else {
                nav.classList.remove('scrolled');
                if(navLinks && !navLinks.classList.contains('active') && hamburger) hamburger.style.color = "white";
            }
        });
    }

    if(hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const isOpen = navLinks.classList.contains('active');
            hamburger.setAttribute('aria-expanded', String(isOpen));
            hamburger.setAttribute('aria-label', isOpen ? 'Chiudi menu di navigazione' : 'Apri menu di navigazione');
            if(isOpen) {
                hamburger.innerHTML = "×";
                hamburger.style.color = "#1d1d1f";
            } else {
                hamburger.innerHTML = "☰";
                hamburger.style.color = isNavSolid() ? "#1d1d1f" : "white";
                chiudiDropdown();
            }
        });
    }

    // --- Sottomenu a tendina "Tecnitalia Ingegneria" ---
    // Su desktop il sottomenu si apre in hover/focus via CSS (:hover, :focus-within);
    // qui teniamo solo gli attributi aria-expanded sincronizzati per la lettura
    // assistiva e gestiamo il tap su mobile (niente hover sul touch), Escape e il
    // click fuori dal menu.
    const dropdown = document.querySelector('.nav-item-dropdown');
    const dropdownToggle = dropdown ? dropdown.querySelector('.nav-dropdown-toggle') : null;
    const dropdownBtn = dropdown ? dropdown.querySelector('.nav-dropdown-btn') : null;

    const apriDropdown = () => {
        if (!dropdown) return;
        dropdown.classList.add('open');
        if (dropdownToggle) dropdownToggle.setAttribute('aria-expanded', 'true');
        if (dropdownBtn) dropdownBtn.setAttribute('aria-expanded', 'true');
    };
    const chiudiDropdown = () => {
        if (!dropdown) return;
        dropdown.classList.remove('open');
        if (dropdownToggle) dropdownToggle.setAttribute('aria-expanded', 'false');
        if (dropdownBtn) dropdownBtn.setAttribute('aria-expanded', 'false');
    };

    if (dropdown) {
        // Tap sul pulsante freccia (visibile solo su mobile): apre/chiude il
        // sottomenu senza seguire il link principale.
        if (dropdownBtn) {
            dropdownBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (dropdown.classList.contains('open')) chiudiDropdown();
                else apriDropdown();
            });
        }

        // Sincronizza aria-expanded anche quando l'apertura avviene via hover/focus CSS.
        dropdown.addEventListener('mouseenter', apriDropdown);
        dropdown.addEventListener('mouseleave', () => {
            if (!dropdown.classList.contains('open')) return;
            // Su mobile l'apertura è manuale (classe "open"): l'hover non deve richiuderla.
            if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) chiudiDropdown();
        });
        dropdown.addEventListener('focusin', apriDropdown);
        dropdown.addEventListener('focusout', (e) => {
            if (!dropdown.contains(e.relatedTarget)) chiudiDropdown();
        });

        // Escape chiude il sottomenu e riporta il focus sulla voce principale.
        dropdown.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                chiudiDropdown();
                if (dropdownToggle) dropdownToggle.focus();
            }
        });

        // Click fuori dal dropdown lo chiude (utile soprattutto su mobile).
        document.addEventListener('click', (e) => {
            if (!dropdown.contains(e.target)) chiudiDropdown();
        });
    }

    if(navLinks) {
        navLinks.querySelectorAll('a').forEach(l => {
            l.addEventListener('click', () => {
                navLinks.classList.remove('active');
                chiudiDropdown();
                if(hamburger) {
                    hamburger.setAttribute('aria-expanded', 'false');
                    hamburger.setAttribute('aria-label', 'Apri menu di navigazione');
                    hamburger.innerHTML = "☰";
                    hamburger.style.color = isNavSolid() ? "#1d1d1f" : "white";
                }
            });
        });
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && navLinks && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            chiudiDropdown();
            if(hamburger) {
                hamburger.setAttribute('aria-expanded', 'false');
                hamburger.setAttribute('aria-label', 'Apri menu di navigazione');
                hamburger.innerHTML = "☰";
                hamburger.style.color = isNavSolid() ? "#1d1d1f" : "white";
            }
        }
    });
}

function renderNews() {
    const newsGridHome = document.querySelector('#news .news-grid'); 
    const newsGridArchivio = document.getElementById('news-grid-full'); 
    const paginaDettaglio = document.getElementById('dettaglio-news-container'); 

    const targetGrid = newsGridHome || newsGridArchivio;
    if (targetGrid && newsDati.length > 0) {
        targetGrid.innerHTML = '';
        let newsDaMostrare = newsGridHome ? newsDati.slice(0, 3) : newsDati;
        
        newsDaMostrare.forEach(news => {
            targetGrid.innerHTML += `
                <div class="project-card" style="min-width: unset; position: relative;">
                    <img src="${news.immagine}" style="width:100%; height:200px; object-fit:cover;" loading="lazy" decoding="async" onerror="this.style.display='none'" alt="${news.titolo}">
                    <div class="p-content">
                        <span style="font-size: 0.8rem; color: #888; font-weight: 600;">${news.data}</span>
                        <h4 style="margin: 10px 0 15px 0; font-size: 1.3rem;">${news.titolo}</h4>
                        <p style="font-size:0.95rem; margin-bottom: 0;">${news.riassunto}</p>
                        <a href="/news/${news.slug}.html" class="news-link-stretched">Leggi l'articolo ➔</a>
                    </div>
                </div>`;
        });
    }

    if (paginaDettaglio) {
        // news-singola.html?id=N e' l'indirizzo storico: ogni articolo ha ora una pagina
        // propria in /news/<slug>.html. Reindirizziamo, cosi' i vecchi link e i preferiti
        // continuano a portare all'articolo giusto invece che a una pagina duplicata.
        const urlParams = new URLSearchParams(window.location.search);
        const newsId = urlParams.get('id');
        const articolo = newsDati.find(n => n.id === newsId);

        if (articolo && articolo.slug) {
            window.location.replace('/news/' + articolo.slug + '.html');
            return;
        }

        paginaDettaglio.innerHTML = "<h2 style='color:var(--blue);'>Articolo non trovato.</h2>" +
            "<p>La news richiesta non esiste. <a href='/archivio-news.html'>Vai all'archivio</a>.</p>";
    }
}

// La rotella resta alla pagina: la striscia si muove con le frecce, col trascinamento
// e avvicinando il puntatore ai bordi.
function tweenScroll(el, delta, durata) {
    const partenza = el.scrollLeft;
    const arrivo = Math.max(0, Math.min(partenza + delta, el.scrollWidth - el.clientWidth));
    const t0 = performance.now();
    if (el._tween) cancelAnimationFrame(el._tween);
    (function passo(t) {
        const k = Math.min(1, (t - t0) / durata);
        const e = 1 - Math.pow(1 - k, 3); // ease-out cubica
        el.scrollLeft = partenza + (arrivo - partenza) * e;
        if (k < 1) el._tween = requestAnimationFrame(passo); else el._tween = null;
    })(t0);
}

window.scrollWorkScroller = function(direction) {
    const scroller = document.getElementById('work-scroller');
    if (!scroller) return;
    const card = scroller.querySelector('.work-card');
    const step = card ? card.getBoundingClientRect().width + 24 : 300;
    tweenScroll(scroller, direction * step * 2, 450);
};

function setupWorkScroller() {
    const wrap = document.querySelector('.work-scroller-wrap');
    const scroller = document.getElementById('work-scroller');
    if (!wrap || !scroller || scroller.dataset.pronto) return;
    scroller.dataset.pronto = '1';

    // le card sono link: senza questo il browser avvia il drag nativo di link/immagini
    scroller.addEventListener('dragstart', (e) => e.preventDefault());

    // trascinamento col mouse
    let giu = false, xPartenza = 0, scrollPartenza = 0, spostato = 0;
    scroller.addEventListener('pointerdown', (e) => {
        if (e.pointerType === 'touch') return; // su touch basta lo swipe nativo
        giu = true; spostato = 0;
        xPartenza = e.clientX; scrollPartenza = scroller.scrollLeft;
    });
    scroller.addEventListener('pointermove', (e) => {
        if (!giu) return;
        const d = e.clientX - xPartenza;
        spostato = Math.max(spostato, Math.abs(d));
        if (spostato > 4) {
            scroller.classList.add('is-dragging');
            scroller.scrollLeft = scrollPartenza - d;
        }
    });
    const finiscoDrag = () => {
        giu = false;
        // un drag non deve aprire la scheda: il click parte subito dopo il pointerup
        if (spostato > 4) setTimeout(() => scroller.classList.remove('is-dragging'), 0);
        else scroller.classList.remove('is-dragging');
    };
    scroller.addEventListener('pointerup', finiscoDrag);
    scroller.addEventListener('pointerleave', finiscoDrag);
    scroller.addEventListener('click', (e) => {
        if (spostato > 4) { e.preventDefault(); e.stopPropagation(); spostato = 0; }
    }, true);

    // avvicinando il mouse ai bordi la striscia scorre da sola
    if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
        const ZONA = 0.12, VMAX = 11;
        let velocita = 0, anim = null;
        const passo = () => {
            if (!velocita) { anim = null; return; }
            scroller.scrollLeft += velocita;
            anim = requestAnimationFrame(passo);
        };
        wrap.addEventListener('mousemove', (e) => {
            if (giu) { velocita = 0; return; }
            const b = scroller.getBoundingClientRect();
            if (!b.width) return;
            const x = (e.clientX - b.left) / b.width;
            if (x > 1 - ZONA)  velocita =  VMAX * Math.min(1, (x - (1 - ZONA)) / ZONA);
            else if (x < ZONA) velocita = -VMAX * Math.min(1, (ZONA - x) / ZONA);
            else               velocita = 0;
            if (velocita && !anim) anim = requestAnimationFrame(passo);
        });
        wrap.addEventListener('mouseleave', () => {
            velocita = 0;
            if (anim) { cancelAnimationFrame(anim); anim = null; }
        });
    }
}

// Filtro dell'archivio: lavora sulle card statiche (data-tags, separati da "|").
window.filterProjects = function(tag, btnElement) {
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    if(btnElement) btnElement.classList.add('active');
    document.querySelectorAll('#projects-grid-full .project-card').forEach(card => {
        const tags = (card.dataset.tags || '').split('|');
        card.style.display = (tag === 'tutti' || tags.includes(tag)) ? '' : 'none';
    });
};

var lenis;
if (typeof Lenis !== 'undefined') {
    lenis = new Lenis({ smooth: true, duration: 1.2 });
    function raf(time) { lenis.raf(time); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
}

// Funzione dedicata alla gestione dell'API SMTP di EmailJS
function inizializzaEmailJS() {
    if (typeof emailjs === 'undefined') {
        console.error('SDK EmailJS non rilevato. Controllare CDN in footer.html');
        return;
    }

    emailjs.init({
        publicKey: "IxQp4s1e-bTQOqX3J",
    });

    const form = document.getElementById('contact-form');
    if (!form) return;

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        if (form.website && form.website.value.trim() !== '') {
            form.reset();
            return;
        }

        const btn = document.getElementById('submit-btn');
        const statusDiv = document.getElementById('form-status');

        btn.textContent = 'Invio in corso...';
        btn.disabled = true;

        emailjs.sendForm('service_x33x9c9', 'template_3vrsw8r', form)
            .then(() => {
                btn.textContent = 'Invia Messaggio';
                btn.disabled = false;
                statusDiv.style.color = '#4CAF50';
                statusDiv.textContent = 'Messaggio inviato con successo!';
                statusDiv.style.display = 'block';
                form.reset(); 
                
                setTimeout(() => { statusDiv.style.display = 'none'; }, 5000);
            }, (error) => {
                btn.textContent = 'Invia Messaggio';
                btn.disabled = false;
                statusDiv.style.color = '#F44336';
                statusDiv.textContent = "Errore durante l'invio. Riprova più tardi.";
                statusDiv.style.display = 'block';
                console.error('EmailJS Error:', error);
            });
    });
}

function initStatsCounters() {
    const statsSection = document.querySelector('.stats-row');
    if (!statsSection) return;

    const counters = statsSection.querySelectorAll('.stat-number[data-count]');

    // L'HTML contiene già i valori finali (crawler e utenti senza JS). Chi non chiede
    // meno animazioni li vede ripartire da 0 solo quando la sezione entra in vista:
    // l'azzeramento avviene qui, prima che la sezione sia visibile.
    if (!('IntersectionObserver' in window) ||
        window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    counters.forEach(el => {
        if (el.getAttribute('data-format') !== 'year') el.textContent = '0';
    });

    const animateCounter = (el) => {
        if (el.getAttribute('data-format') === 'year') return;
        const target = parseInt(el.getAttribute('data-count'), 10);
        if (isNaN(target)) return;
        const duration = 1200;
        const start = performance.now();
        const step = (now) => {
            const progress = Math.min((now - start) / duration, 1);
            el.textContent = Math.floor(progress * target);
            if (progress < 1) requestAnimationFrame(step);
            else el.textContent = String(target);
        };
        requestAnimationFrame(step);
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                counters.forEach(animateCounter);
                observer.disconnect();
            }
        });
    }, { threshold: 0.3 });

    observer.observe(statsSection);
}

function initScrollReveals() {
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;
    gsap.registerPlugin(ScrollTrigger);

    gsap.utils.toArray('.fade-element').forEach((el) => {
        gsap.fromTo(el,
            { opacity: 0, y: 30 },
            {
                opacity: 1, y: 0, duration: 0.8, ease: 'power2.out',
                scrollTrigger: {
                    trigger: el, start: 'top 85%', toggleActions: 'play none none none',
                    onRefresh: (self) => { if (self.progress > 0) self.animation.progress(1); }
                }
            }
        );
    });

    gsap.utils.toArray('.reveal-img').forEach((el) => {
        gsap.fromTo(el,
            { opacity: 0, scale: 0.96 },
            {
                opacity: 1, scale: 1, duration: 1, ease: 'power2.out',
                scrollTrigger: {
                    trigger: el, start: 'top 85%', toggleActions: 'play none none none',
                    onRefresh: (self) => { if (self.progress > 0) self.animation.progress(1); }
                }
            }
        );
    });

    const heroBg = document.querySelector('.hero-bg');
    if (heroBg) {
        gsap.to(heroBg, {
            yPercent: 15,
            ease: 'none',
            scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
        });
    }
}
