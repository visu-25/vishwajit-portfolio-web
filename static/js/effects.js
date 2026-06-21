(function () {
    "use strict";

    var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function initLevitasField() {
        var canvas = document.querySelector(".global-canvas");
        var glow = document.querySelector(".global-glow");
        var hero = document.querySelector(".hero");
        var magneticWrap = document.querySelector(".magnetic-wrap");

        if (!canvas) return;

        var ctx = canvas.getContext("2d");
        var particles = [];
        var mouse = { x: -9999, y: -9999, active: false };
        var animationId = null;
        var particleCount = prefersReducedMotion ? 0 : 65;

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        function createParticles() {
            particles = [];
            for (var i = 0; i < particleCount; i++) {
                particles.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    vx: (Math.random() - 0.5) * 0.3,
                    vy: -(Math.random() * 0.6 + 0.2),
                    size: Math.random() * 2.2 + 0.8,
                    alpha: Math.random() * 0.4 + 0.12,
                });
            }
        }

        function drawParticles() {
            if (!ctx || prefersReducedMotion) return;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (var i = 0; i < particles.length; i++) {
                var p = particles[i];

                if (mouse.active) {
                    var dx = p.x - mouse.x;
                    var dy = p.y - mouse.y;
                    var dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 80 && dist > 0) {
                        var force = (80 - dist) / 80;
                        p.vx += (dx / dist) * force * 0.32;
                        p.vy += (dy / dist) * force * 0.32;
                    }
                }

                p.vy -= 0.006;
                p.vx *= 0.98;
                p.vy *= 0.98;

                p.x += p.vx;
                p.y += p.vy;

                if (p.y < -10) {
                    p.y = canvas.height + 10;
                    p.x = Math.random() * canvas.width;
                }
                if (p.y > canvas.height + 10) p.y = -10;
                if (p.x < -10) p.x = canvas.width + 10;
                if (p.x > canvas.width + 10) p.x = -10;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fillStyle = "rgba(245, 197, 24, " + p.alpha + ")";
                ctx.fill();
            }

            for (var a = 0; a < particles.length; a++) {
                for (var b = a + 1; b < particles.length; b++) {
                    var p1 = particles[a];
                    var p2 = particles[b];
                    var ddx = p1.x - p2.x;
                    var ddy = p1.y - p2.y;
                    var distance = Math.sqrt(ddx * ddx + ddy * ddy);
                    if (distance < 95) {
                        ctx.beginPath();
                        ctx.moveTo(p1.x, p1.y);
                        ctx.lineTo(p2.x, p2.y);
                        ctx.strokeStyle = "rgba(245, 197, 24, " + (0.07 * (1 - distance / 95)) + ")";
                        ctx.lineWidth = 0.6;
                        ctx.stroke();
                    }
                }
            }

            animationId = requestAnimationFrame(drawParticles);
        }

        function updateMagneticLogo() {
            if (!magneticWrap || !hero) return;

            var rect = hero.getBoundingClientRect();
            var inHero =
                mouse.x >= rect.left &&
                mouse.x <= rect.right &&
                mouse.y >= rect.top &&
                mouse.y <= rect.bottom;

            if (inHero) {
                var centerX = rect.left + rect.width / 2;
                var centerY = rect.top + rect.height / 2;
                var offsetX = (mouse.x - centerX) / (rect.width / 2);
                var offsetY = (mouse.y - centerY) / (rect.height / 2);
                magneticWrap.style.transform =
                    "translate(" + offsetX * 14 + "px, " + offsetY * 10 + "px)";
            } else {
                magneticWrap.style.transform = "translate(0, 0)";
            }
        }

        function onMouseMove(event) {
            mouse.x = event.clientX;
            mouse.y = event.clientY;
            mouse.active = true;

            if (glow) {
                glow.style.left = mouse.x + "px";
                glow.style.top = mouse.y + "px";
                glow.classList.add("active");
            }

            updateMagneticLogo();
        }

        function onMouseLeave() {
            mouse.active = false;
            mouse.x = -9999;
            mouse.y = -9999;
            if (glow) glow.classList.remove("active");
            if (magneticWrap) magneticWrap.style.transform = "translate(0, 0)";
        }

        resize();
        createParticles();
        if (!prefersReducedMotion) {
            drawParticles();
        }

        window.addEventListener("resize", function () {
            resize();
            createParticles();
        });

        document.addEventListener("mousemove", onMouseMove);
        document.addEventListener("mouseleave", onMouseLeave);

        document.addEventListener("visibilitychange", function () {
            if (document.hidden && animationId) {
                cancelAnimationFrame(animationId);
                animationId = null;
            } else if (!document.hidden && !prefersReducedMotion && !animationId) {
                drawParticles();
            }
        });
    }

    function initStaggerReveal() {
        var grids = document.querySelectorAll(
            ".skills-grid, .education-grid, .projects-grid, .experience-grid"
        );

        grids.forEach(function (grid) {
            var items = grid.children;
            for (var i = 0; i < items.length; i++) {
                items[i].classList.add("fade-in", "stagger-item");
                items[i].style.transitionDelay = i * 0.1 + "s";
            }
        });

        if (!("IntersectionObserver" in window)) return;

        var observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.08, rootMargin: "0px 0px -20px 0px" }
        );

        document.querySelectorAll(".stagger-item").forEach(function (el) {
            observer.observe(el);
        });
    }

    function initSectionReveal() {
        var targets = document.querySelectorAll(
            ".section-title, .section-subtitle, .case-section, .page-hero, .about-grid, .contact-wrap"
        );

        if (!("IntersectionObserver" in window)) {
            targets.forEach(function (t) { t.classList.add("visible"); });
            return;
        }

        var observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12, rootMargin: "0px 0px -30px 0px" }
        );

        targets.forEach(function (el) {
            if (!el.classList.contains("fade-in")) {
                el.classList.add("fade-in");
            }
            observer.observe(el);
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        initLevitasField();
        initSectionReveal();
        initStaggerReveal();
    });
})();
