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
    for (const name of ['city', 'product']) {
      const select = form.elements.namedItem(name);
      if ([...select.options].some(option => option.value === params.get(name))) select.value = params.get(name);
    }
    form.addEventListener('submit', event => {
      event.preventDefault();
      const data = new FormData(form);
      const product = form.elements.product.selectedOptions[0].text;
      const subject = 'Revenger enquiry — ' + data.get('city') + ' — ' + product;
      const body = 'Name: ' + data.get('name') + '\nCity: ' + data.get('city') + '\nInterest: ' + product + '\n\n' + data.get('message');
      location.href = 'mailto:GangaShreeroots@gmail.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      form.querySelector('[role="status"]').textContent = 'Email draft prepared. If your email app did not open, email GangaShreeroots@gmail.com or call +91 81694 56633. Nothing has been submitted on this website.';
    });
  }
})();
