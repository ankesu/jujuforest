/* ============================================================
   THEME SYSTEM — Light / Dark toggle
   更多下载：https://www.bootstrapmb.com 
   ------------------------------------------------------------
   • Single source of truth: the `dark-mode` class on <body>.
     The flag lives on <body> (not <html>) because some rules
     are compound with the page-layout class, e.g.
     `.dark-mode.home-3 ...`, so both classes must share an
     element. `light-mode` is kept for the existing toggle CSS.
   • <html>.theme-dark is set by a tiny inline <head> script
     BEFORE first paint to prevent a flash of light (FOUC);
     we keep the two in sync here.
   • Default theme = LIGHT. Only an explicit saved "dark" opts
     in. The choice persists across pages/refreshes via
     localStorage, so it survives navigation.
   • A short-lived `.theme-anim` class drives the smooth colour
     transition ONLY while switching — never during normal page
     load or hover, so existing animations stay untouched.

   NOTE: this replaces two earlier, conflicting handlers — one
   that toggled `body.dark-mode` and a dead one that set an
   unused `data-theme` attribute and defaulted to the system
   preference (which broke the "default = light" rule).
   ============================================================ */
(function () {
    const STORAGE_KEY = "theme";

    function getStoredTheme() {
        try {
            return localStorage.getItem(STORAGE_KEY);
        } catch (e) {
            return null;
        }
    }

    function storeTheme(value) {
        try {
            localStorage.setItem(STORAGE_KEY, value);
        } catch (e) { }
    }

    // Theme Apply
    function applyTheme(theme) {
        const isDark = theme === "dark";

        document.body.classList.toggle("dark-mode", isDark);
        document.body.classList.toggle("light-mode", !isDark);
    }

    document.addEventListener("DOMContentLoaded", function () {

        // Default Theme
        const savedTheme = getStoredTheme() || "light";
        applyTheme(savedTheme);

        // Toggle Button
        const toggle = document.getElementById("themeToggle");

        if (toggle) {

            toggle.setAttribute("role", "button");
            toggle.setAttribute("tabindex", "0");
            toggle.setAttribute("aria-label", "Toggle dark mode");

            const flipTheme = function () {

                // Smooth Transition Start
                document.body.classList.add("theme-transition");

                const nextTheme = document.body.classList.contains("dark-mode")
                    ? "light"
                    : "dark";

                applyTheme(nextTheme);
                storeTheme(nextTheme);

                // Transition Remove
                setTimeout(() => {
                    document.body.classList.remove("theme-transition");
                }, 400);
            };

            toggle.addEventListener("click", flipTheme);

            toggle.addEventListener("keydown", function (e) {
                if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    flipTheme();
                }
            });
        }
    });
})();

// Header fixed
if ($('.header-section').length) {
    $(window).on('scroll', function () {
        if ($(this).scrollTop() > 50) {
            $('.header-section').addClass('fix-header');
        } else {
            $('.header-section').removeClass('fix-header');
        }
    });
}


// Menu toggle
if ($('.menu-toggler').length) {
    $('.menu-toggler').on('click', function () {
        $(this).toggleClass('active');
    });
}


// Dropdown
if ($('.dropdown-toggle').length) {
    $('.dropdown-toggle').on('click', function (e) {
        if ($(window).width() < 992) {
            e.preventDefault();
            e.stopPropagation();

            let parent = $(this).parent();

            $('.nav-item.dropdown').not(parent).removeClass('show');
            $('.dropdown-menu, .mega-dropdown')
                .not(parent.find('.dropdown-menu, .mega-dropdown'))
                .removeClass('show');

            parent.toggleClass('show');
            parent.find('> .dropdown-menu, > .mega-dropdown').toggleClass('show');
        }
    });
}


// Stories Slider
if ($('.stories-slider').length) {

    const $slider = $('.stories-slider');

    $slider.slick({
        slidesToShow: 1,
        arrows: false,
        autoplay: true,
        autoplaySpeed: 5000,
        fade: true,
        speed: 600
    });

    function updateThumbs(index) {
        const total = $slider.find('.story-slide').length;
        const nextIndex = (index + 1) % total;

        const currentThumb = $slider.find('.story-slide').eq(index).data('thumb');
        const nextThumb = $slider.find('.story-slide').eq(nextIndex).data('thumb');

        $('.thumb-current img').attr('src', currentThumb);
        $('.thumb-next img').attr('src', nextThumb);
    }

    function updateProgress(index) {
        const total = $('.stories-slider .story-slide').length;
        const percent = ((index + 1) / total) * 100;

        $('.progress-fill').css('width', percent + '%');
    }

    updateThumbs(0);
    updateProgress(0);

    $slider.on('afterChange', function (event, slick, currentSlide) {
        updateThumbs(currentSlide);
        updateProgress(currentSlide);
    });

    $('.nav-btn.next').on('click', () => $slider.slick('slickNext'));
    $('.nav-btn.prev').on('click', () => $slider.slick('slickPrev'));
}


// Animation
const boxes = document.querySelectorAll('.fade-animation');

if (boxes.length) {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
            }
        });
    }, { threshold: 0.2 });

    boxes.forEach(el => observer.observe(el));
}


// Web story slider
if ($('.web-story-slider').length) {

    $('.web-story-slider')
        .on('init reInit afterChange', function (event, slick, currentSlide) {
            let i = currentSlide ? currentSlide : 0;

            $('.web-story .slick-dots li').removeClass('visited');

            for (let j = 0; j < i; j++) {
                $('.web-story .slick-dots li').eq(j).addClass('visited');
            }
        })
        .slick({
            slidesToShow: 1,
            autoplay: true,
            dots: true,
            arrows: true,
            speed: 2000,
            cssEase: 'ease-in-out',
            nextArrow: '<button class="slick-next-arrow bg-transparent p-0"><img src="dist/images/web-story-next-icon.svg"></button>',
            prevArrow: false
        });
}


// Blog Slider 4 (Accordion)
const cards = document.querySelectorAll('.blog-slid .slider-card');

if (cards.length) {

    const progressBar = document.querySelector('.progress-bar');
    const nextBtn = document.querySelector('.next-arrow');
    const prevBtn = document.querySelector('.prev-arrow');

    let activeIndex = Math.floor(cards.length / 2);

    setActive(activeIndex);

    cards.forEach((card, index) => {
        card.addEventListener('click', () => setActive(index));
    });

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            activeIndex = (activeIndex + 1) % cards.length;
            setActive(activeIndex);
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            activeIndex = (activeIndex - 1 + cards.length) % cards.length;
            setActive(activeIndex);
        });
    }

    function setActive(index) {
        cards.forEach(c => c.classList.remove('active'));
        cards[index].classList.add('active');

        if (progressBar) {
            const percent = ((index + 1) / cards.length) * 100;
            progressBar.style.width = percent + '%';
        }
    }
}


// Category auto slider
if ($('.category-auto-slid').length) {
    $('.category-auto-slid').slick({
        slidesToShow: 6,
        autoplay: true,
        autoplaySpeed: 0,
        speed: 3000,
        cssEase: 'linear',
        infinite: true,
        arrows: false,
        dots: false,
        pauseOnHover: false,
        variableWidth: true
    });
}


// Hero Banner Slider
if ($('.hero-banner-slider').length) {
    $('.hero-banner-slider').slick({
        slidesToShow: 1,
        infinite: true,
        arrows: false,
        dots: true,
        autoplay: true,
        autoplaySpeed: 4000,
        speed: 600,
        fade: true,
        cssEase: 'linear',
        adaptiveHeight: true
    });
}

// Copy URL to clipboard
const btn = document.getElementById("copyUrlBtn");

if (btn) {
    btn.addEventListener("click", () => {
        const url = window.location.href;

        navigator.clipboard.writeText(url).then(() => {
            const span = btn.querySelector("span");

            if (span) {
                span.innerText = "Copied!";

                setTimeout(() => {
                    span.innerText = "Copy URL to clipboard";
                }, 2000);
            }
        }).catch(() => {
            console.error("Copy failed");
        });
    });
}

// Trending Post Slider
$(document).ready(function () {

    if ($('.trending-post-slider').length && $.fn.slick) {

        $('.trending-post-slider').slick({
            slidesToShow: 3,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 3000,
            arrows: false,
            dots: false,
            infinite: true,
            speed: 800,

            responsive: [
                {
                    breakpoint: 992,
                    settings: {
                        slidesToShow: 2
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 1
                    }
                }
            ]
        });

    }

});

// Parters slider
$(document).ready(function () {
    if ($('.parters-slider').length > 0 && $.fn.slick) {
        $('.parters-slider').slick({
            speed: 10000,
            autoplay: true,
            autoplaySpeed: 0,
            cssEase: 'linear',
            slidesToShow: 5,
            slidesToScroll: 1,
            infinite: true,
            arrows: false,
            dots: false,
            pauseOnHover: false,
            pauseOnFocus: false,
            variableWidth: true
        });
    }
});

// Testimonial slider
if ($('.trusted-slider').length) {
    $('.trusted-slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        infinite: true,
        arrows: false,
        dots: true,
        autoplay: true,
        autoplaySpeed: 4000,
        speed: 600,
        adaptiveHeight: true
    });
}


// Team slider
if ($('.creative-team-slider').length) {

    $('.creative-team-slider').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        infinite: true,
        arrows: false,
        dots: false,
        autoplay: true,
        autoplaySpeed: 6000,
        speed: 800,
        pauseOnHover: false,

        responsive: [
            {
                breakpoint: 1200,
                settings: {
                    slidesToShow: 3
                }
            },

            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 2
                }
            },

            {
                breakpoint: 576,
                settings: {
                    slidesToShow: 1
                }
            }
        ]
    });

}


// FAQ accordion
const faqItems = document.querySelectorAll(".faq-item");
if (faqItems.length > 0) {
    faqItems.forEach(item => {
        const button = item.querySelector(".faq-question");
        const icon = item.querySelector(".faq-icon");
        if (button && icon) {
            button.addEventListener("click", () => {
                const isActive = item.classList.contains("active");
                faqItems.forEach(faq => {
                    faq.classList.remove("active");
                    const faqIcon = faq.querySelector(".faq-icon");
                    if (faqIcon) {
                        faqIcon.innerHTML = "+";
                    }
                });
                if (!isActive) {
                    item.classList.add("active");
                    icon.innerHTML = "−";
                }
            });
        }
    });
}


// Lightweight image lightbox for post content images
(function () {
    const targets = document.querySelectorAll('.single-blog-img img, .blog-inner-img, img.zoomable');
    if (!targets.length) return;

    const overlay = document.createElement('div');
    overlay.className = 'np-lightbox';
    overlay.innerHTML = '' +
        '<button class="np-lightbox-close" aria-label="Close">&times;</button>' +
        '<button class="np-lightbox-prev" aria-label="Previous">&#10094;</button>' +
        '<figure class="np-lightbox-figure">' +
        '<img alt="">' +
        '<figcaption></figcaption>' +
        '</figure>' +
        '<button class="np-lightbox-next" aria-label="Next">&#10095;</button>';
    document.body.appendChild(overlay);

    const imgEl = overlay.querySelector('img');
    const captionEl = overlay.querySelector('figcaption');
    let currentIndex = 0;
    const items = Array.from(targets);

    function show(index) {
        currentIndex = (index + items.length) % items.length;
        const target = items[currentIndex];
        imgEl.src = target.getAttribute('src');
        imgEl.alt = target.getAttribute('alt') || '';
        captionEl.textContent = target.getAttribute('alt') || '';
        overlay.classList.add('is-open');
        document.body.style.overflow = 'hidden';
    }

    function close() {
        overlay.classList.remove('is-open');
        document.body.style.overflow = '';
    }

    items.forEach((el, i) => {
        el.style.cursor = 'zoom-in';
        el.addEventListener('click', function (e) {
            e.preventDefault();
            show(i);
        });
    });

    overlay.querySelector('.np-lightbox-close').addEventListener('click', close);
    overlay.querySelector('.np-lightbox-prev').addEventListener('click', () => show(currentIndex - 1));
    overlay.querySelector('.np-lightbox-next').addEventListener('click', () => show(currentIndex + 1));
    overlay.addEventListener('click', function (e) {
        if (e.target === overlay) close();
    });
    document.addEventListener('keydown', function (e) {
        if (!overlay.classList.contains('is-open')) return;
        if (e.key === 'Escape') close();
        if (e.key === 'ArrowRight') show(currentIndex + 1);
        if (e.key === 'ArrowLeft') show(currentIndex - 1);
    });
})();


// Newsletter & inline form feedback (prevents dead submit buttons)
document.querySelectorAll('form.js-inline-feedback').forEach(function (form) {
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const status = form.querySelector('.form-status') || (function () {
            const el = document.createElement('div');
            el.className = 'form-status';
            el.setAttribute('role', 'status');
            form.appendChild(el);
            return el;
        })();
        status.textContent = 'Thanks! Your submission has been received.';
        status.style.color = '#16a34a';
        status.style.marginTop = '10px';
        status.style.fontSize = '14px';
        form.reset();
    });
});