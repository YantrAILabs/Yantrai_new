const reveals = document.querySelectorAll('.reveal');

if ('IntersectionObserver' in window) {
  const obs = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  reveals.forEach((el) => obs.observe(el));
} else {
  reveals.forEach((el) => el.classList.add('in'));
}

/* Demo form submit */
(function initDemoForm() {
  const form = document.getElementById('demoForm');
  const success = document.getElementById('formSuccess');
  if (!form || !success) return;
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    form.style.display = 'none';
    success.style.display = 'block';
  });
})();

/* Agent tab switcher */
(function initTabs() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabPanels = document.querySelectorAll('.tab-panel');
  if (!tabButtons.length) return;
  tabButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;
      tabButtons.forEach((b) => {
        const active = b.dataset.tab === target;
        b.classList.toggle('is-active', active);
        b.setAttribute('aria-selected', active ? 'true' : 'false');
      });
      tabPanels.forEach((p) => {
        p.classList.toggle('is-active', p.dataset.panel === target);
      });
    });
  });
  window.__tabsBound = true;
})();
