let newsDati = [];
let projectsData = [];

document.addEventListener("DOMContentLoaded", () => {
    // Pipeline asincrona parallela per il caricamento delle risorse
    Promise.all([
        fetch('./header.html').then(res => {
            if (!res.ok) throw new Error(`HTTP error header! status: ${res.status}`);
            return res.text();
        }),
        fetch('./footer.html').then(res => {
            if (!res.ok) throw new Error(`HTTP error footer! status: ${res.status}`);
            return res.text();
        }),
        fetch('./data/news.json').then(res => res.ok ? res.json() : []).catch(() => []),
        fetch('./data/projects.json').then(res => res.ok ? res.json() : []).catch(() => [])
    ]).then(([headerData, footerData, newsJson, projectsJson]) => {
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
        projectsData = projectsJson;
        
        // Ordina i progetti dal più recente al più vecchio
        if(projectsData.length > 0) {
            projectsData.sort((a, b) => b.endYear - a.endYear);
        }
        
        renderNews();
        renderProjects('tutti');
        
        initNavbar();

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
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
            if(navLinks && !navLinks.classList.contains('active') && hamburger) hamburger.style.color = "#1d1d1f";
        } else {
            nav.classList.remove('scrolled');
            if(navLinks && !navLinks.classList.contains('active') && hamburger) hamburger.style.color = "white";
        }
    });

    if(hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            if(navLinks.classList.contains('active')) {
                hamburger.innerHTML = "×";
                hamburger.style.color = "#1d1d1f"; 
            } else {
                hamburger.innerHTML = "☰";
                hamburger.style.color = (window.scrollY > 50) ? "#1d1d1f" : "white";
            }
        });
    }

    if(navLinks) {
        navLinks.querySelectorAll('a').forEach(l => {
            l.addEventListener('click', () => {
                navLinks.classList.remove('active');
                if(hamburger) {
                    hamburger.innerHTML = "☰";
                    hamburger.style.color = (window.scrollY > 50) ? "#1d1d1f" : "white";
                }
            });
        });
    }
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
                <div class="project-card" style="min-width: unset; box-shadow: 0 4px 15px rgba(0,0,0,0.1); position: relative;">
                    <img src="${news.immagine}" style="width:100%; height:200px; object-fit:cover;" onerror="this.style.display='none'" alt="${news.titolo}">
                    <div class="p-content">
                        <span style="font-size: 0.8rem; color: #888; font-weight: 600;">${news.data}</span>
                        <h4 style="color:var(--blue); margin: 10px 0 15px 0; font-size: 1.3rem;">${news.titolo}</h4>
                        <p style="font-size:0.95rem; margin-bottom: 0;">${news.riassunto}</p>
                        <a href="news-singola.html?id=${news.id}" class="news-link-stretched">Leggi l'articolo ➔</a>
                    </div>
                </div>`;
        });
    }

    if (paginaDettaglio) {
        const urlParams = new URLSearchParams(window.location.search);
        const newsId = urlParams.get('id');
        const articolo = newsDati.find(n => n.id === newsId);

        if (articolo) {
            document.getElementById('n-titolo').innerText = articolo.titolo;
            document.getElementById('n-data').innerText = articolo.data;
            document.getElementById('n-contenuto').innerHTML = articolo.contenuto;
            const img = document.getElementById('n-img');
            if (img) {
                img.src = articolo.immagine;
                img.onerror = () => img.style.display = 'none';
            }
        } else {
            paginaDettaglio.innerHTML = "<h2 style='color:var(--blue);'>Articolo non trovato.</h2><p>La news richiesta non esiste.</p>";
        }
    }
}

function renderProjects(filterTag = 'tutti') {
    const sliderContainer = document.getElementById('projects-slider');
    const gridContainer = document.getElementById('projects-grid-full');
    
    if (sliderContainer) {
        sliderContainer.innerHTML = ''; 
        const recentProjects = projectsData.slice(0, 6); 
        
        recentProjects.forEach(p => {
            const originalIndex = projectsData.indexOf(p);
            sliderContainer.innerHTML += `
                <div class="project-card" onclick="openProject(${originalIndex})">
                    <div class="p-img-box">
                        <img src="${p.images[0]}" alt="${p.title}" onerror="this.style.display='none'">
                        <div class="hover-reveal">APRI SCHEDA</div>
                    </div>
                    <div class="p-content">
                        <span style="font-size: 0.8rem; color: #888; font-weight: 600;">Anno: ${p.endYear}</span>
                        <h4 style="color:var(--blue); margin: 5px 0 5px 0;">${p.title}</h4>
                        <p style="margin:0; font-size:0.9rem">${p.cardSubtitle}</p>
                    </div>
                </div>`;
        });
    }

    if (gridContainer) {
        gridContainer.innerHTML = ''; 
        projectsData.forEach((p, index) => {
            if (filterTag === 'tutti' || (p.tags && p.tags.includes(filterTag))) {
                gridContainer.innerHTML += `
                    <div class="project-card" onclick="openProject(${index})">
                        <div class="p-img-box">
                            <img src="${p.images[0]}" alt="${p.title}" onerror="this.style.display='none'">
                            <div class="hover-reveal">APRI SCHEDA</div>
                        </div>
                        <div class="p-content">
                            <span style="font-size: 0.8rem; color: #888; font-weight: 600;">Anno: ${p.endYear}</span>
                            <h4 style="color:var(--blue); margin: 5px 0 5px 0;">${p.title}</h4>
                            <p style="margin:0; font-size:0.9rem">${p.cardSubtitle}</p>
                        </div>
                    </div>`;
            }
        });
    }
}

window.filterProjects = function(tag, btnElement) {
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    if(btnElement) btnElement.classList.add('active');
    renderProjects(tag);
};

window.scrollSlider = function(direction) {
    const slider = document.getElementById('projects-slider');
    if(slider) slider.scrollBy({ left: direction * 380, behavior: 'smooth' });
};

let currentProjectIndex = 0;
let currentImageIndex = 0;

window.openProject = function(index) {
    currentProjectIndex = index;
    currentImageIndex = 0;
    const p = projectsData[index];
    const modal = document.getElementById('projectModal');
    if(!modal) return;
    
    document.getElementById('m-title').innerHTML = p.title;
    document.getElementById('m-client').innerHTML = p.client;
    document.getElementById('m-period').innerHTML = p.period;
    document.getElementById('m-val').innerHTML = p.val;
    document.getElementById('m-type').innerHTML = p.type;
    document.getElementById('m-desc').innerHTML = p.desc;
    
    const wrapper = document.getElementById('m-slides-wrapper');
    wrapper.innerHTML = ''; 
    p.images.forEach((imgSrc, i) => {
        const img = document.createElement('img');
        img.src = imgSrc;
        img.onerror = function() { this.style.display = 'none' };
        img.className = 'm-slide' + (i === 0 ? ' active' : '');
        wrapper.appendChild(img);
    });

    const showArrows = p.images.length > 1 ? 'block' : 'none';
    const btnPrev = document.getElementById('m-btn-prev');
    const btnNext = document.getElementById('m-btn-next');
    if(btnPrev) btnPrev.style.display = showArrows;
    if(btnNext) btnNext.style.display = showArrows;

    modal.classList.add('active');
    if (typeof lenis !== 'undefined') lenis.stop(); 
};

window.changeModalImg = function(direction) {
    const p = projectsData[currentProjectIndex];
    const slides = document.querySelectorAll('.m-slide');
    if(slides.length === 0) return;
    
    slides[currentImageIndex].classList.remove('active');
    currentImageIndex += direction;
    if (currentImageIndex < 0) currentImageIndex = p.images.length - 1;
    if (currentImageIndex >= p.images.length) currentImageIndex = 0;
    slides[currentImageIndex].classList.add('active');
};

window.closeProject = function() {
    const modal = document.getElementById('projectModal');
    if(modal) modal.classList.remove('active');
    if (typeof lenis !== 'undefined') lenis.start(); 
};

document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById('projectModal');
    if (modal) { 
        modal.addEventListener('click', (e) => { 
            if(e.target === modal) closeProject(); 
        }); 
    }
});

if (typeof Lenis !== 'undefined') {
    const lenis = new Lenis({ smooth: true, duration: 1.2 });
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

        const btn = document.getElementById('submit-btn');
        const statusDiv = document.getElementById('form-status');

        btn.textContent = 'Invio in corso...';
        btn.disabled = true;

        emailjs.sendForm('service_x33x9c9', 'template_6u6e1jo', form)
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