(() => {
  const $ = s => document.querySelector(s), cfg = window.MM_CONFIG, L = cfg.labels;
  const read = k => { try { return localStorage.getItem(k); } catch { return null; } };
  const write = (k,v) => { try { localStorage.setItem(k,v); } catch {} };
  const theme = $('.theme-toggle');
  const setTheme = dark => { document.body.classList.toggle('dark',dark); theme.setAttribute('aria-pressed',String(dark)); };
  setTheme(read('montshire-theme') ? read('montshire-theme') === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches);
  theme.onclick = () => { setTheme(!document.body.classList.contains('dark')); write('montshire-theme',document.body.classList.contains('dark')?'dark':'light'); };
  $('.mobile-menu').onclick = e => { const on = $('#navigation').classList.toggle('open'); e.currentTarget.setAttribute('aria-expanded',String(on)); };
  document.addEventListener('keydown',e => { if(e.key==='Escape') { document.querySelectorAll('details[open]').forEach(x=>x.open=false); $('#navigation').classList.remove('open'); $('.mobile-menu').setAttribute('aria-expanded','false'); } });
  const banner = $('#cookie-banner');
  banner.hidden = ['essential','analytics'].includes(MMConsent.choice);
  let consentOpener = null;
  $('#cookie-settings').onclick = e => { consentOpener=e.currentTarget; banner.hidden=false; banner.querySelector('button').focus(); };
  document.querySelectorAll('[data-consent]').forEach(b=>b.onclick=()=>{ MMConsent.set(b.dataset.consent); banner.hidden=true; if(consentOpener)consentOpener.focus(); });
  document.querySelectorAll('a.button,a.nav-cta,a.mobile-cta').forEach(a=>a.addEventListener('click',()=>mmEvent('cta_click')));
  document.querySelectorAll('.booking-link').forEach(a=>a.addEventListener('click',()=>mmEvent('booking_click')));
  if($('#load-booking')) $('#load-booking').onclick = e => { const frame=document.createElement('iframe');frame.src=cfg.booking_url;frame.title='Book a strategy call';frame.loading='lazy';frame.referrerPolicy='no-referrer';frame.className='calendar-frame';$('#booking-slot').replaceChildren(frame);e.currentTarget.hidden=true;mmEvent('booking_click'); };
  if($('#service-filter')) {
    const filter=()=>{let count=0;document.querySelectorAll('.work-card').forEach(c=>{c.hidden=($('#service-filter').value!=='all'&&c.dataset.service!==$('#service-filter').value)||($('#industry-filter').value!=='all'&&c.dataset.industry!==$('#industry-filter').value);if(!c.hidden)count++;});$('#filter-status').textContent=count?`${count} ${L.template_count}`:L.no_results;};
    $('#service-filter').onchange=filter;$('#industry-filter').onchange=filter;filter();
  }
  if($('#article-filter')) $('#article-filter').onchange=e=>{let n=0;document.querySelectorAll('.article-list .insight').forEach(a=>{a.hidden=e.target.value!=='all'&&a.dataset.category!==e.target.value;if(!a.hidden)n++;});$('#article-status').textContent=n?`${n} articles`:L.no_results;};
  /* Animate only near-viewport items. Content is visible if JS or IntersectionObserver fails. */
  if('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('reveal-enter');observer.unobserve(entry.target);}}),{threshold:.12});
    document.querySelectorAll('.beliefs article,.work-card,.engagement,.insight').forEach(el=>observer.observe(el));
  }
  let blobURL; const form=$('#lead-form');
  if(form)form.onsubmit=async e=>{
    e.preventDefault();if(!form.reportValidity())return;
    const data=Object.fromEntries(new FormData(form));data.marketing=!!form.elements.marketing.checked;
    const status=$('#form-status'),button=form.querySelector('[type=submit]');
    if(!cfg.lead.enabled) {
      const text=['Montshire Media — draft enquiry','NOT SUBMITTED',...['kind','name','email','company','website','budget','service','message'].map(k=>`${k.toUpperCase()}: ${data[k]||''}`)].join('\n\n');
      if(blobURL)URL.revokeObjectURL(blobURL);blobURL=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));
      const a=$('#download-enquiry');a.href=blobURL;a.download='montshire-enquiry.txt';a.hidden=false;status.textContent=L.prepared;status.focus();return;
    }
    button.disabled=true;button.textContent=L.sending;status.textContent='';
    const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),15000);
    try {
      const response=await fetch(cfg.lead.endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data),signal:controller.signal,credentials:'same-origin'});
      const result=await response.json();
      if(!response.ok||result.accepted!==true)throw Error('not accepted');
      status.textContent=L.success;form.reset();mmEvent('form_submit');
    } catch { status.textContent=L.failure; }
    finally { clearTimeout(timeout);button.disabled=false;button.textContent=L.submit;status.focus(); }
  };
})();
