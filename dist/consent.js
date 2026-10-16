/* Basic consent mode: no Google request before explicit analytics opt-in. */
(() => {
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  const denied = { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' };
  gtag('consent', 'default', denied);
  gtag('set', 'ads_data_redaction', true);
  let choice = null;
  try { choice = localStorage.getItem('montshire-consent-v2'); } catch {}
  window.MMConsent = { choice, loaded: false };
  const load = () => {
    if (MMConsent.loaded || MMConsent.choice !== 'analytics') return;
    const cfg = window.MM_CONFIG.analytics;
    const script = document.createElement('script'); script.async = true;
    if (/^GTM-[A-Z0-9]+$/.test(cfg.gtm_id)) {
      dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
      script.src = 'https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(cfg.gtm_id);
    } else if (/^G-[A-Z0-9]+$/.test(cfg.ga4_id)) {
      script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(cfg.ga4_id);
      gtag('js', new Date());
      gtag('config', cfg.ga4_id, { send_page_view: false, allow_google_signals: false, allow_ad_personalization_signals: false });
      gtag('event', 'page_view', { page_location: location.origin + location.pathname, page_referrer: '', page_title: document.title });
    } else return;
    MMConsent.loaded = true; document.head.appendChild(script);
  };
  MMConsent.set = value => {
    MMConsent.choice = value;
    try { localStorage.setItem('montshire-consent-v2', value); } catch {}
    gtag('consent', 'update', { ...denied, analytics_storage: value === 'analytics' ? 'granted' : 'denied' });
    if (value === 'analytics') load();
    else if (MMConsent.loaded) location.reload();
  };
  if (choice === 'analytics') { gtag('consent', 'update', { ...denied, analytics_storage: 'granted' }); load(); }
  /* Only allow fixed event names and page context; never pass fields, URLs or free text. */
  window.mmEvent = name => {
    if (MMConsent.choice !== 'analytics' || !['form_submit','cta_click','booking_click'].includes(name)) return;
    const cfg = MM_CONFIG.analytics;
    if (cfg.gtm_id) dataLayer.push({ event: name, page_path: location.pathname });
    else if (cfg.ga4_id) gtag('event', name, { page_location: location.origin + location.pathname, page_referrer: '' });
  };
})();
