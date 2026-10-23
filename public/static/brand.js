(() => {
  const root = document.documentElement;
  if (document.body.classList.contains('is-home')) {
    let scheduled = false;
    const syncHeader = () => { document.body.classList.toggle('header-scrolled', scrollY > 48); scheduled = false; };
    addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(syncHeader); } }, { passive: true });
    syncHeader();
  }
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#navigation');
  if (menu && nav) {
    root.classList.add('js-nav');
    const close = () => { document.body.classList.remove('nav-open'); nav.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      document.body.classList.toggle('nav-open', open);
      nav.classList.toggle('open', open);
      menu.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { close(); menu.focus(); } });
    nav.addEventListener('click', e => { if (e.target.closest('a')) close(); });
  }
  // Animate on entry without hiding off-screen content or making JS essential.
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  if ('IntersectionObserver' in window && Element.prototype.animate) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      observer.unobserve(entry.target);
      if (!reduceMotion.matches) entry.target.animate([
        { opacity: 0, transform: 'translateY(20px)' },
        { opacity: 1, transform: 'translateY(0)' }
      ], { duration: 650, easing: 'cubic-bezier(.2,.7,.2,1)', fill: 'backwards', delay: Number(entry.target.dataset.revealDelay || 0) });
    }), { threshold: .08 });
    document.querySelectorAll('.reveal,.value,.area-region,.office,.contact-compose,.two-col>div,.region-summary>div').forEach((el, i) => {
      el.dataset.revealDelay = String((i % 4) * 45);
      observer.observe(el);
    });
    reduceMotion.addEventListener('change', () => {
      if (reduceMotion.matches) document.getAnimations().forEach(animation => animation.finish());
    });
  }
  document.querySelectorAll('[data-step]').forEach(button => button.addEventListener('click', () => {
    const input = button.closest('.quantity-stepper').querySelector('input');
    if (Number(button.dataset.step) > 0) input.stepUp(); else input.stepDown();
    input.dispatchEvent(new Event('change', { bubbles: true }));
  }));
  const motion = document.querySelector('.motion-toggle');
  if (motion) motion.addEventListener('click', () => {
    const paused = document.body.classList.toggle('motion-paused');
    motion.setAttribute('aria-pressed', String(paused));
    motion.setAttribute('aria-label', paused ? 'Resume 3D animation' : 'Pause 3D animation');
    motion.innerHTML = paused ? '&#9654; <span>Resume motion</span>' : '&#8545; <span>Pause motion</span>';
    document.dispatchEvent(new Event('revenger:motion'));
  });
  const form = document.querySelector('#contact-draft');
  if (form) {
    const params = new URLSearchParams(location.search);
    for (const name of ['city', 'product', 'size']) {
      const select = form.elements.namedItem(name);
      if ([...select.options].some(option => option.value === params.get(name))) select.value = params.get(name);
    }
    const quantity = Number(params.get('quantity'));
    if (Number.isInteger(quantity) && quantity >= 1 && quantity <= 10000) form.elements.quantity.value = String(quantity);
    form.addEventListener('submit', event => {
      event.preventDefault();
      const data = new FormData(form);
      const product = form.elements.product.selectedOptions[0].text;
      const subject = 'Revenger enquiry — ' + data.get('city') + ' — ' + product;
      const body = 'Name: ' + data.get('name') + '\nCity: ' + data.get('city') + '\nInterest: ' + product + '\nPreferred size: ' + (data.get('size') || 'Confirm with team') + '\nQuantity (bottles): ' + data.get('quantity') + '\n\n' + data.get('message');
      location.href = 'mailto:GangaShreeroots@gmail.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      form.querySelector('[role="status"]').textContent = 'Email draft prepared. If your email app did not open, email GangaShreeroots@gmail.com or call +91 81694 56633. Nothing has been submitted on this website.';
    });
  }
  // Only load the globe when a visitor approaches the service section.
  const connections = document.querySelector('.connections-section');
  if (connections) {
    const loadGlobe = () => import('./service-globe.js?v=3').then(module => module.mountServiceGlobe(connections)).catch(() => {
      connections.querySelector('.service-globe').dataset.renderer = 'fallback';
    });
    if ('IntersectionObserver' in window) {
      const near = new IntersectionObserver(entries => {
        if (entries.some(entry => entry.isIntersecting)) { near.disconnect(); loadGlobe(); }
      }, { rootMargin: '300px' });
      near.observe(connections);
    } else loadGlobe();
  }
})();
