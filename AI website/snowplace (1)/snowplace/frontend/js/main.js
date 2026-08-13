/* ============================================================
   MAIN.JS — shared across all pages
   ============================================================ */
const API = '';  // same-origin; backend serves frontend

/* ── Mobile nav ── */
const navToggle = document.getElementById('navToggle');
const navMobile = document.getElementById('navMobile');
if (navToggle && navMobile) {
  navToggle.addEventListener('click', () => navMobile.classList.toggle('open'));
  navMobile.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => navMobile.classList.remove('open'))
  );
}

/* ── Back to top ── */
const btt = document.getElementById('btt');
if (btt) {
  window.addEventListener('scroll', () =>
    btt.classList.toggle('visible', window.scrollY > 400)
  );
  btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

/* ── Active nav link ── */
(function () {
  const page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a, .nav-mobile a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === page || (page === '' && href === 'index.html')) {
      a.classList.add('active');
    }
  });
})();

/* ── Scroll reveal ── */
const ro = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach(el => ro.observe(el));

/* ── Snowflakes (used on pages that include .snowflakes div) ── */
document.querySelectorAll('.snowflakes').forEach(container => {
  const flakes = ['❄', '❅', '❆', '✦', '•'];
  for (let i = 0; i < 12; i++) {
    const s = document.createElement('span');
    s.className = 'snowflake';
    s.textContent = flakes[Math.floor(Math.random() * flakes.length)];
    s.style.left = Math.random() * 100 + '%';
    s.style.animationDuration = (6 + Math.random() * 8) + 's';
    s.style.animationDelay = -(Math.random() * 10) + 's';
    s.style.fontSize = (0.7 + Math.random() * 1) + 'rem';
    container.appendChild(s);
  }
});

/* ── Animated counters ── */
function animateCounter(el, target, suffix = '') {
  let cur = 0;
  const steps = 50, inc = target / steps;
  const t = setInterval(() => {
    cur = Math.min(cur + inc, target);
    el.textContent = Math.round(cur) + suffix;
    if (cur >= target) clearInterval(t);
  }, 30);
}
const cntObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.querySelectorAll('[data-count]').forEach(el => {
        const val = parseFloat(el.dataset.count);
        const suf = el.dataset.suffix || '';
        animateCounter(el, val, suf);
      });
      cntObs.unobserve(e.target);
    }
  });
}, { threshold: 0.4 });
document.querySelectorAll('[data-count-group]').forEach(el => cntObs.observe(el));

/* ── FAQ accordion ── */
document.querySelectorAll('.faq-q').forEach(q => {
  q.addEventListener('click', () => {
    const answer = q.nextElementSibling;
    const isOpen = answer.classList.contains('open');
    document.querySelectorAll('.faq-a').forEach(a => a.classList.remove('open'));
    document.querySelectorAll('.faq-q').forEach(x => x.classList.remove('open'));
    if (!isOpen) { answer.classList.add('open'); q.classList.add('open'); }
  });
});

/* ── Lightbox (gallery) ── */
const lb = document.getElementById('lightbox');
if (lb) {
  document.querySelectorAll('.gallery-item').forEach(item => {
    item.addEventListener('click', () => {
      lb.querySelector('.lb-content').textContent = item.dataset.emoji || item.textContent.trim();
      lb.querySelector('p').textContent = item.dataset.label || '';
      lb.classList.add('open');
    });
  });
  lb.querySelector('.lightbox-close').addEventListener('click', () => lb.classList.remove('open'));
  lb.addEventListener('click', e => { if (e.target === lb) lb.classList.remove('open'); });
}
