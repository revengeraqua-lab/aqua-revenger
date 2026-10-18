/* Revenger: local, dependency-free interactions. */
(() => {
  const $ = (selector) => document.querySelector(selector);
  const $$ = (selector) => [...document.querySelectorAll(selector)];
  const products = [...document.querySelectorAll('[data-product]')].map(card => ({id: card.dataset.product, name: card.querySelector('h3').textContent, pack: card.querySelector('.product-info > div > span').textContent, size: card.querySelector('.size-stamp').textContent}));
  let bag = {};
  try { const saved = JSON.parse(localStorage.getItem('revenger-bag') || '{}'); for (const p of products) if (Number.isInteger(saved?.[p.id]) && saved[p.id] > 0 && saved[p.id] <= 100) bag[p.id] = saved[p.id]; } catch { /* Storage is optional. */ }
  const save = () => { try { localStorage.setItem('revenger-bag', JSON.stringify(bag)); } catch {} };
  let toastTimer;
  function toast(message) { $('#toast').textContent = message; $('#toast').classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => $('#toast').classList.remove('show'), 2800); }
  function updateBag() {
    $('#bag-count').textContent = Object.values(bag).reduce((a,b) => a+b, 0);
    const container = $('#bag-items'); container.replaceChildren();
    for (const p of products.filter(p => bag[p.id])) {
      const row = document.createElement('div'); row.className = 'bag-item';
      const artwork = document.createElement('div'); artwork.append(document.querySelector('.product-bottle .bottle-model').cloneNode(true));
      const description = document.createElement('div'); const heading = document.createElement('h3'); heading.textContent = p.size + ' · ' + p.name; const pack = document.createElement('p'); pack.textContent = p.pack;
      const remove = document.createElement('button'); remove.type='button'; remove.className='remove-item'; remove.textContent='Remove'; remove.setAttribute('aria-label','Remove '+p.size+' cases'); remove.onclick=()=>{delete bag[p.id];save();updateBag();}; description.append(heading,pack,remove);
      const controls = document.createElement('div'); controls.className='quantity-controls';
      for (const [label, value] of [['−',-1],['+',1]]) { const button=document.createElement('button'); button.type='button';button.textContent=label;button.setAttribute('aria-label',(value<0?'Decrease ':'Increase ')+p.size+' cases');button.onclick=()=>{bag[p.id]=Math.min(100,bag[p.id]+value);if(!bag[p.id])delete bag[p.id];save();updateBag();};controls.append(button);if(value<0){const count=document.createElement('span');count.textContent=bag[p.id];count.setAttribute('aria-label',bag[p.id]+' cases');controls.append(count);} }
      row.append(artwork,description,controls);container.append(row);
    }
    const empty = !Object.keys(bag).length;
    if(empty){const text=document.createElement('p');text.className='empty-bag';text.textContent='A fresh start. Add your favourite size to get an order quote.';container.append(text);}
    $('#enquire-order').disabled=empty;
  }
  $$('[data-add]').forEach(button=>button.addEventListener('click',()=>{const id=button.dataset.add;bag[id]=Math.min(100,(bag[id]||0)+1);save();updateBag();toast(products.find(p=>p.id===id).size+' case added to your bag');}));
  updateBag();
  function openDialog(id) { $$( 'dialog[open]').forEach(d=>d.close()); $(id).showModal(); document.body.style.overflow='hidden'; }
  $$('dialog').forEach(dialog=>{dialog.addEventListener('close',()=>{document.body.style.overflow='';});dialog.querySelector('.close-dialog').addEventListener('click',()=>dialog.close());dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();}});});
  $('.bag-button').onclick=()=>openDialog('#bag-dialog');
  $('.continue-shopping').onclick=()=>$('#bag-dialog').close();
  function enquiry(kind) { $('#enquiry-form').reset(); $('#form-status').textContent='';$('#form-status').className='';const submit=$('#enquiry-form button[type=submit]');submit.disabled=false;submit.innerHTML='Send enquiry <span>↗</span>';$('#enquiry-form select').value=kind;openDialog('#enquiry-dialog'); }
  $$('.partner-button').forEach(button=>button.onclick=()=>enquiry('distributor'));
  $('#enquire-order').onclick=()=>enquiry('order');
  $('#privacy-button').onclick=()=>openDialog('#privacy-dialog');
  $('#enquiry-form').addEventListener('submit',async event=>{
    event.preventDefault();const form=event.currentTarget;const button=form.querySelector('[type=submit]');const status=$('#form-status');
    const data=Object.fromEntries(new FormData(form));data.items=data.kind==='order'?Object.entries(bag).map(([id,quantity])=>({id,quantity})):[];
    button.disabled=true;status.className='';status.textContent='Saving your enquiry…';
    try {const response=await fetch('/api/enquiries',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const result=await response.json();if(!response.ok)throw new Error(result.error||'Please try again.');status.className='success';status.textContent=`Thank you, ${data.name}. Your enquiry is saved. Reference: ${result.reference}. Pricing and availability will be confirmed separately.`;if(data.kind==='order'){bag={};save();updateBag();}form.reset();button.textContent='Enquiry saved ✓';}
    catch(error){status.className='error';status.textContent=error instanceof TypeError?'Connection interrupted. Please try again.':error.message;button.disabled=false;}
  });
  $('.menu-button').onclick=()=>{const expanded=$('.menu-button').getAttribute('aria-expanded')==='true';$('.menu-button').setAttribute('aria-expanded',String(!expanded));$('.header nav').classList.toggle('open',!expanded);};
  $$('.header nav a').forEach(link=>link.onclick=()=>{$('.header nav').classList.remove('open');$('.menu-button').setAttribute('aria-expanded','false');});
  const motion = $('.motion-toggle'); const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  function setMotion(paused){document.body.classList.toggle('motion-paused',paused);motion.setAttribute('aria-pressed',String(paused));motion.setAttribute('aria-label',paused?'Resume ambient animations':'Pause ambient animations');motion.querySelector('span').textContent=paused?'Resume motion':'Pause motion';document.dispatchEvent(new Event('revenger:motion'));}
  setMotion(reduced.matches);motion.onclick=()=>setMotion(!document.body.classList.contains('motion-paused'));
  if('IntersectionObserver' in window){document.body.classList.add('js-ready');const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');observer.unobserve(entry.target);}}),{threshold:.12});$$('.reveal').forEach((element,index)=>{element.style.transitionDelay=`${index%4*65}ms`;observer.observe(element);});}
})();
