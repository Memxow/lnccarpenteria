// Funzione per cambiare il tema
function setTheme(theme) {
    let activeTheme = theme;

    if (theme === 'auto') {
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        activeTheme = systemPrefersDark ? 'dark' : 'light';
        document.documentElement.setAttribute('data-bs-theme', activeTheme);
    } else {
        document.documentElement.setAttribute('data-bs-theme', theme);
    }

    localStorage.setItem('user-theme', theme);

    const iconImg = document.getElementById('theme-icon');
    if (iconImg) {
        if (theme === 'light') {
            iconImg.setAttribute('src', 'images/sun.svg');
            
        } else if (theme === 'dark') {
            iconImg.setAttribute('src', 'images/moon-stars.svg');
            iconImg.style.color = "bg-primary";
        } else {
            iconImg.setAttribute('src', 'images/circle-half.svg');
        }
    }

    const themeButtons = document.querySelectorAll('[onclick*="setTheme"], [data-bs-theme-value]');

    themeButtons.forEach(btn => {
        const isSelected = btn.getAttribute('onclick')?.includes(`'${theme}'`) || btn.getAttribute('data-bs-theme-value') === theme;

        if(isSelected) {
            btn.classList.add('active', 'text-info', 'fw-bold');
            if(!btn.querySelector('.theme-check')) {
                const checkMark = document.createElement('span');
                checkMark.className="theme-check float-end ms-2";
                checkMark.innerHTML = '<img src="images/check2.svg" alt="check" width="16" height="16">';
                btn.appendChild(checkMark);
            }
        } else {
            btn.classList.remove('active', 'text-info', 'fw-bold');
            const checkMark = btn.querySelector('.theme-check');
            if(checkMark) {
                checkMark.remove();
            }
        }
    });
}

// All'avvio ripristina il tema salvato
window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('user-theme') || 'light';
    setTheme(savedTheme);
});


// Caricamento della nvbar e inizializzazione all'avvio
document.addEventListener('DOMContentLoaded', function() {
    fetch('header.html')
        .then(response => {
            if(!response.ok)
                throw new Error("Errore nel caricamento della navbar");
            return response.text();
        })
        .then(data => {
            document.getElementById('navbar-placeholder').innerHTML = data;
            highlightActiveLink();

            const transCookie = getCookie('googtrans');
            if(transCookie) {
                const lang = transCookie.split('/')[2];
                if(lang) {
                    updateLanguageUI(lang);
                }
            }
        })
        .catch(error => console.error('Errore: ', error));

        // Caricamento del footer all'avvio
        fetch('footer.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('footer-placeholder').innerHTML = data;
        })
        .catch(error => console.error('Errore nel caricamento del footer:', error));
});


// Funzione per cambiare lingua con i bottoni personalizzati
function changeLanguage(lang) {
    // Imposta il cookie in modo sicuro per tutto il dominio
    document.cookie = `googtrans=/it/${lang}; path=/`;
    
    // Ricarica la pagina per applicare la traduzione
    window.location.reload();
}

// Installazione del traduttore di Google (necessaria in backgorund)
function googleTranslateElementInit(){
    new google.translate.TranslateElement({
        pageLanguage: 'it',
        includedLanguages: 'en,de',
        autoDisplay: false
    }, 'google_translate_hidden');
}

// Funzione di supporto per leggere i cookie
function getCookie(name) {
    const value = `; {document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length === 2) return parts.pop().split(';').shift();
}

// Aggiorna l'aspetto visivo del bottone principale della lingua
function updateLanguageUI(lang) {
    const flagImg = document.getElementById('currentFlag');
    const langText = document.getElementById('currentLangText');
    
    if (flagImg && langText) {
        if (lang === 'en') {
            flagImg.src = 'images/flag-gb.svg';
            langText.textContent = 'English';
        } else if (lang === 'de') {
            flagImg.src = 'images/flag-de.svg';
            langText.textContent = 'Deutsch';
        } else {
            flagImg.src = 'images/flag-it.svg';
            langText.textContent = 'Italiano';
        }
    }
}


function highlightActiveLink(){
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        if(link.getAttribute('href') === currentPage) {
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
        } else {
            link.classList.remove('active');
            link.removeAttribute('aria-current');
        }
    });
}

// All'avvio della pagina: ripristina tema E aggiorna la lingua selezionata nella navbar
window.addEventListener('DOMContentLoaded', () => {
    // 1. Controlla se c'è un cookie di traduzione attivo
    const transCookie = getCookie('googtrans');
    if (transCookie) {
        // Estrae la lingua dal cookie (es. da "/it/en" prende "en")
        const lang = transCookie.split('/')[2];
        if (lang) {
            updateLanguageUI(lang);
        }
    }
});