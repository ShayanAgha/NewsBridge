// NewsBridge — Main JS

document.addEventListener('DOMContentLoaded', () => {

  // ── Auto-submit filter selects ─────────────────────────────
  document.querySelectorAll('.filter-select[data-auto-submit]').forEach(sel => {
    sel.addEventListener('change', () => sel.closest('form').submit());
  });

  // ── Navbar scroll effect ───────────────────────────────────
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.style.background = window.scrollY > 30
        ? 'rgba(10, 14, 26, 0.98)'
        : 'rgba(10, 14, 26, 0.85)';
    }, { passive: true });
  }

  // ── Live search with debounce ──────────────────────────────
  const searchInput = document.querySelector('#navbar-search');
  if (searchInput) {
    let timeout;
    searchInput.addEventListener('input', () => {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        const q = searchInput.value.trim();
        if (q.length >= 2 || q.length === 0) {
          const form = searchInput.closest('form');
          if (form) form.submit();
        }
      }, 600);
    });
  }

  // ── Duplicate ticker for seamless loop ─────────────────────
  const track = document.querySelector('.ticker-track');
  if (track && track.children.length > 0) {
    const clone = track.innerHTML;
    track.innerHTML += clone; // duplicate for seamless infinite scroll
  }

  // ── Image lazy loading: handled natively via loading="lazy" attr ──
  // (Custom IntersectionObserver removed — native lazy loading is more reliable)


  // ── Confirm delete dialogs ─────────────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (!confirm(btn.dataset.confirm || 'Are you sure?')) {
        e.preventDefault();
        e.stopPropagation();
      }
    });
  });

  // ── Mobile hamburger menu ──────────────────────────────────
  const navToggle = document.getElementById('nav-toggle');
  const navMenu   = document.getElementById('navbar-nav');
  const navOverlay = document.getElementById('nav-overlay');

  function openNav() {
    navMenu.classList.add('open');
    navToggle.classList.add('open');
    navToggle.setAttribute('aria-expanded', 'true');
    if (navOverlay) { navOverlay.classList.add('open'); navOverlay.removeAttribute('aria-hidden'); }
    document.body.style.overflow = 'hidden';
  }
  function closeNav() {
    navMenu.classList.remove('open');
    navToggle.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
    if (navOverlay) { navOverlay.classList.remove('open'); navOverlay.setAttribute('aria-hidden', 'true'); }
    document.body.style.overflow = '';
  }

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      navMenu.classList.contains('open') ? closeNav() : openNav();
    });
    if (navOverlay) navOverlay.addEventListener('click', closeNav);
    // Close on Escape key
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeNav(); });
    // Close when a nav link is clicked (page navigation)
    navMenu.querySelectorAll('.nav-link').forEach(link => link.addEventListener('click', closeNav));
  }

  // ── Animate elements on scroll (stagger) ──────────────────
  const animateTargets = document.querySelectorAll('.card, .stat-card, .mini-article');
  if ('IntersectionObserver' in window && animateTargets.length) {
    const animObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          animObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    animateTargets.forEach((el, i) => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = `opacity 0.4s ease ${i * 0.06}s, transform 0.4s ease ${i * 0.06}s`;
      animObserver.observe(el);
    });
  }

  // ── Share buttons ─────────────────────────────────────────
  document.querySelectorAll('[data-share]').forEach(btn => {
    btn.addEventListener('click', () => {
      const platform = btn.dataset.share;
      const url = encodeURIComponent(window.location.href);
      const title = encodeURIComponent(document.title);
      let shareUrl = '';
      if (platform === 'facebook') shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
      else if (platform === 'twitter') shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
      else if (platform === 'linkedin') shareUrl = `https://www.linkedin.com/shareArticle?mini=true&url=${url}&title=${title}`;
      else if (platform === 'whatsapp') shareUrl = `https://wa.me/?text=${title}%20${url}`;
      if (shareUrl) window.open(shareUrl, '_blank', 'width=600,height=400');
    });
  });

});
