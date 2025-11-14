document.addEventListener('DOMContentLoaded', () => {
    const prefersReducedMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    const hasTestimonials = !!document.querySelector('.testimonial-slider');
    const hasStats = !!document.querySelector('.stats-section');
    const hasFaqs = document.querySelectorAll('.faq-item, .new-faq-item').length > 0;
    
    const sectionLinks = document.querySelectorAll('.nav-links a[href^="#"]');
    const sections = Array.from(sectionLinks).map(link => {
        const id = link.getAttribute('href')?.slice(1);
        return id && id !== '' ? document.getElementById(id) : null;
    }).filter(Boolean);

    const navElCached = document.querySelector('nav.main-nav');
    let navHeightCached = navElCached?.offsetHeight || 80;
    const recalcNavHeight = () => { navHeightCached = navElCached?.offsetHeight || 80; };

    const highlightActiveMenu = () => {
        let activeIndex = -1;
        sections.forEach((section, i) => {
            const rect = section.getBoundingClientRect();
            if (rect.top <= navHeightCached && rect.bottom > navHeightCached) activeIndex = i;
        });
        sectionLinks.forEach((link, idx) => link.classList.toggle('active', idx === activeIndex));
    };

    let ticking = false;
    const onScroll = () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => { highlightActiveMenu(); ticking = false; });
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    highlightActiveMenu();
    window.addEventListener('resize', recalcNavHeight, { passive: true });


    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', e => {
            const href = link.getAttribute('href');
            if (!href || href === '#') { e.preventDefault(); return; }
            const target = document.getElementById(href.slice(1));
            if (!target) return;
            e.preventDefault();
            window.scrollTo({ 
                top: target.getBoundingClientRect().top + window.pageYOffset - navHeightCached - 8, 
                behavior: prefersReducedMotion ? 'auto' : 'smooth' 
            });
        });
    });
    
    // Logo scroll to top
    const logoLink = document.querySelector('.logo');
    if (logoLink) logoLink.addEventListener('click', e => { 
        e.preventDefault(); 
        window.scrollTo({ top: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' }); 
    });

    // Testimonials Slider (carga condicional)
    if (hasTestimonials) {
        const slider = document.querySelector('.testimonial-slider');
        const slides = document.querySelectorAll('.testimonial-slide');
        const prevButton = document.querySelector('.slider-nav.prev');
        const nextButton = document.querySelector('.slider-nav.next');
        const paginationContainer = document.querySelector('.slider-pagination');
        
        if (slides.length > 0) {
            let currentSlide = 0;
            const totalSlides = slides.length;
            let paginationDots = [];
            
            if (paginationContainer) {
                slides.forEach((_, index) => {
                    const dot = document.createElement('span');
                    dot.className = 'pagination-dot';
                    dot.addEventListener('click', () => goToSlide(index));
                    paginationContainer.appendChild(dot);
                    paginationDots.push(dot);
                });
            }
            
            const goToSlide = (slideIndex) => {
                currentSlide = (slideIndex + totalSlides) % totalSlides;
                slider.style.transform = `translateX(-${currentSlide * 100}%)`;
                paginationDots.forEach((dot, idx) => dot.classList.toggle('active', idx === currentSlide));
            };
            
            if (prevButton) prevButton.addEventListener('click', () => goToSlide(currentSlide - 1));
            if (nextButton) nextButton.addEventListener('click', () => goToSlide(currentSlide + 1));
            goToSlide(0);
        }
    }


    // Stats Animation (carga condicional)
    if (hasStats) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.querySelectorAll('.stat-number').forEach(counter => {
                        const target = +counter.getAttribute('data-target');
                        let count = 0;
                        const increment = Math.ceil(target / 100);
                        const update = () => {
                            count = Math.min(count + increment, target);
                            counter.textContent = count;
                            if (count < target) requestAnimationFrame(update);
                        };
                        update();
                    });
                    observer.disconnect();
                }
            });
        }, { threshold: 0.5 });
        observer.observe(document.querySelector('.stats-section'));
    }

    // Fecha y año
    const dateEl = document.getElementById('dynamic-date');
    if (dateEl) dateEl.textContent = new Date().toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    const yearEl = document.getElementById('copyright-year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();


    // Menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        if (!navLinks.id) navLinks.id = 'primary-navigation';
        menuToggle.setAttribute('aria-controls', navLinks.id);
        menuToggle.setAttribute('aria-expanded', 'false');

        const closeMenu = () => {
            navLinks.classList.remove('open', 'active');
            menuToggle.setAttribute('aria-expanded', 'false');
            document.body.classList.remove('menu-open', 'menu-open-landscape');
            recalcNavHeight();
        };

        menuToggle.addEventListener('click', e => {
            e.preventDefault();
            const isOpen = navLinks.classList.contains('open');
            if (isOpen) {
                closeMenu();
            } else {
                navLinks.classList.add('open', 'active');
                menuToggle.setAttribute('aria-expanded', 'true');
                document.body.classList.add('menu-open');
                recalcNavHeight();
            }
        });

        navLinks.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
        document.addEventListener('click', e => { if (!navLinks.contains(e.target) && !menuToggle.contains(e.target)) closeMenu(); });
        window.addEventListener('resize', () => { if (window.innerWidth >= 992) closeMenu(); });
        document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
    }

    // Sticky nav
    const nav = document.getElementById('nav-section');
    const header = document.getElementById('header-section');
    if (nav && header) {
        const headerHeight = header.offsetHeight;
        window.addEventListener('scroll', () => {
            nav.classList.toggle('sticky', window.scrollY > headerHeight);
        }, { passive: true });
    }


    // FAQ (carga condicional)
    if (hasFaqs) {
        const accordionItems = Array.from(document.querySelectorAll('.faq-item, .new-faq-item'));

        const updateFaqHash = (id, replace = true) => {
            try {
                const url = id ? '#' + id : location.pathname + location.search;
                history[replace ? 'replaceState' : 'pushState'](null, '', url);
            } catch { location.hash = id || ''; }
        };

        const closeFaq = item => {
            if (!item) return;
            const answer = item.querySelector('.faq-answer, .new-faq-answer');
            const question = item.querySelector('.faq-question, .new-faq-question');
            if (answer) {
                answer.style.maxHeight = answer.scrollHeight + 'px';
                requestAnimationFrame(() => answer.style.maxHeight = '0px');
                const cleanup = () => {
                    item.classList.remove('active');
                    if (question) question.setAttribute('aria-expanded', 'false');
                    answer.style.maxHeight = '';
                };
                answer.addEventListener('transitionend', function onEnd(e) {
                    if (!e || e.propertyName === 'max-height') {
                        cleanup();
                        answer.removeEventListener('transitionend', onEnd);
                    }
                });
                setTimeout(cleanup, 800); // fallback
            } else {
                item.classList.remove('active');
                if (question) question.setAttribute('aria-expanded', 'false');
            }
        };

        const closeAllFaqs = () => accordionItems.forEach(item => item.classList.contains('active') && closeFaq(item));

        const openFaqById = (id, scroll = true) => {
            const item = document.getElementById(id);
            if (!item) return false;
            const answer = item.querySelector('.faq-answer, .new-faq-answer');
            const question = item.querySelector('.faq-question, .new-faq-question');
            closeAllFaqs();
            item.classList.add('active');
            if (question) question.setAttribute('aria-expanded', 'true');
            if (answer) {
                answer.style.maxHeight = answer.scrollHeight + 'px';
                answer.addEventListener('transitionend', function onEnd(e) {
                    if (e.propertyName === 'max-height') {
                        answer.style.maxHeight = '';
                        answer.removeEventListener('transitionend', onEnd);
                    }
                });
            }
            if (scroll) {
                requestAnimationFrame(() => {
                    const top = item.getBoundingClientRect().top + window.pageYOffset - navHeightCached - 8;
                    window.scrollTo({ top, behavior: prefersReducedMotion ? 'auto' : 'smooth' });
                    setTimeout(() => window.scrollTo({ top, behavior: 'auto' }), 120);
                });
            }
            return true;
        };

        accordionItems.forEach(item => {
            const question = item.querySelector('.faq-question, .new-faq-question');
            if (question) {
                question.addEventListener('click', e => {
                    e.preventDefault();
                    if (item.classList.contains('active')) {
                        closeFaq(item);
                        updateFaqHash(null);
                    } else if (item.id) {
                        openFaqById(item.id);
                        updateFaqHash(item.id);
                    } else {
                        item.classList.add('active');
                        question.setAttribute('aria-expanded', 'true');
                    }
                });
            }
        });

        document.addEventListener('click', e => {
            const anchor = e.target.closest('a[href^="#faq"]');
            if (anchor) {
                e.preventDefault();
                const id = anchor.getAttribute('href')?.slice(1);
                if (id) {
                    openFaqById(id);
                    updateFaqHash(id);
                }
                e.stopPropagation();
            }
        }, true);

        if (location.hash?.startsWith('#faq')) {
            setTimeout(() => openFaqById(location.hash.slice(1)), 80);
        }

        window.addEventListener('hashchange', () => {
            if (location.hash?.startsWith('#faq')) {
                setTimeout(() => openFaqById(location.hash.slice(1)), 40);
            }
        });

        window.addEventListener('resize', () => {
            accordionItems.forEach(item => {
                if (item.classList.contains('active')) {
                    const answer = item.querySelector('.faq-answer, .new-faq-answer');
                    if (answer) {
                        answer.style.maxHeight = answer.scrollHeight + 'px';
                        setTimeout(() => answer.style.maxHeight = '', 400);
                    }
                }
            });
        });

        document.addEventListener('click', e => {
            const activeFaqItem = document.querySelector('.faq-item.active');
            if (!activeFaqItem) return;
            const activeSection = activeFaqItem.closest('.faq-section');
            if (activeSection?.contains(e.target)) return;
            closeFaq(activeFaqItem);
            updateFaqHash(null);
        });

        accordionItems.forEach(item => {
            const answer = item.querySelector('.faq-answer, .new-faq-answer');
            answer?.querySelectorAll('img').forEach(img => img.addEventListener('load', () => {
                if (item.classList.contains('active')) {
                    answer.style.maxHeight = answer.scrollHeight + 'px';
                    setTimeout(() => answer.style.maxHeight = '', 350);
                }
            }));
        });
    }

    // Fix WhatsApp links - remover target blank para evitar popup blockers
    document.querySelectorAll('a[href*="wa.me"], a[href*="whatsapp.com"]').forEach(link => {
        link.removeAttribute('target');
        if (!link.getAttribute('rel')) link.setAttribute('rel', 'noopener');
    });
});
