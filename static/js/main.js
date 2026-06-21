(function () {
    "use strict";

    function initMobileNav() {
        const toggle = document.querySelector(".nav-toggle");
        const nav = document.querySelector(".site-nav");
        if (!toggle || !nav) return;

        toggle.addEventListener("click", function () {
            const isOpen = nav.classList.toggle("open");
            toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
            toggle.innerHTML = isOpen
                ? '<i class="fa-solid fa-xmark"></i>'
                : '<i class="fa-solid fa-bars"></i>';
        });

        nav.querySelectorAll(".nav-link").forEach(function (link) {
            link.addEventListener("click", function () {
                nav.classList.remove("open");
                toggle.setAttribute("aria-expanded", "false");
                toggle.innerHTML = '<i class="fa-solid fa-bars"></i>';
            });
        });
    }

    function initScrollSpy() {
        const sections = document.querySelectorAll("section[id]");
        const navLinks = document.querySelectorAll(".nav-link");
        const header = document.querySelector(".site-header");
        const scrollTop = document.querySelector(".scroll-top");

        if (!sections.length) return;

        function onScroll() {
            const scrollY = window.scrollY;

            if (header) {
                header.classList.toggle("scrolled", scrollY > 50);
            }

            if (scrollTop) {
                scrollTop.classList.toggle("visible", scrollY > 400);
            }

            let current = "";
            sections.forEach(function (section) {
                const top = section.offsetTop - 120;
                if (scrollY >= top) {
                    current = section.getAttribute("id");
                }
            });

            navLinks.forEach(function (link) {
                link.classList.remove("active");
                const href = link.getAttribute("href");
                if (href && href.endsWith("#" + current)) {
                    link.classList.add("active");
                }
            });
        }

        window.addEventListener("scroll", onScroll, { passive: true });
        onScroll();
    }

    function initTypingEffect() {
        const el = document.querySelector(".typing-text");
        if (!el) return;

        const roles = (el.dataset.roles || "Developer").split("|");
        let roleIndex = 0;
        let charIndex = 0;
        let isDeleting = false;

        function type() {
            const current = roles[roleIndex];
            const displayed = isDeleting
                ? current.substring(0, charIndex - 1)
                : current.substring(0, charIndex + 1);

            el.textContent = displayed;

            if (!isDeleting) {
                charIndex++;
                if (charIndex === current.length + 1) {
                    isDeleting = true;
                    setTimeout(type, 2000);
                    return;
                }
            } else {
                charIndex--;
                if (charIndex === 0) {
                    isDeleting = false;
                    roleIndex = (roleIndex + 1) % roles.length;
                }
            }

            setTimeout(type, isDeleting ? 50 : 100);
        }

        type();
    }

    function initScrollAnimations() {
        const elements = document.querySelectorAll(".fade-in");
        if (!elements.length) return;

        if (!("IntersectionObserver" in window)) {
            elements.forEach(function (el) {
                el.classList.add("visible");
            });
            return;
        }

        const observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.1, rootMargin: "0px 0px -30px 0px" }
        );

        elements.forEach(function (el) {
            observer.observe(el);
        });
    }

    function initSmoothScroll() {
        document.querySelectorAll('a[href*="#"]').forEach(function (anchor) {
            anchor.addEventListener("click", function (event) {
                const href = anchor.getAttribute("href");
                const hashIndex = href.indexOf("#");
                if (hashIndex === -1) return;

                const targetId = href.substring(hashIndex);
                if (targetId.length <= 1) return;

                const target = document.querySelector(targetId);
                if (target) {
                    event.preventDefault();
                    target.scrollIntoView({ behavior: "smooth" });
                    history.pushState(null, "", targetId);
                }
            });
        });
    }

    function initToastDismiss() {
        const toasts = document.querySelectorAll(".toast");
        toasts.forEach(function (toast) {
            setTimeout(function () {
                toast.style.opacity = "0";
                toast.style.transform = "translateX(100%)";
                setTimeout(function () {
                    toast.remove();
                }, 400);
            }, 4000);
        });
    }

    function scrollToHashOnLoad() {
        if (window.location.hash) {
            const target = document.querySelector(window.location.hash);
            if (target) {
                setTimeout(function () {
                    target.scrollIntoView({ behavior: "smooth" });
                }, 300);
            }
        }
    }

    document.addEventListener("DOMContentLoaded", function () {
        initMobileNav();
        initScrollSpy();
        initTypingEffect();
        initScrollAnimations();
        initSmoothScroll();
        initToastDismiss();
        scrollToHashOnLoad();
    });
})();
