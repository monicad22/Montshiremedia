"""Render the existing Montshire Media site from editable JSON. No third-party build dependencies."""
import html, json, pathlib, re
from urllib.parse import urlparse
R=pathlib.Path(__file__).resolve().parent; D=R/'dist'; D.mkdir(exist_ok=True)
config=json.loads((R/'content.json').read_text()); C=R/config['content_directory']
def load(n): return json.loads((C/(n+'.json')).read_text())
def e(v):return html.escape(str(v),quote=True)
def js(v):return json.dumps(v,ensure_ascii=False).replace('<','\\u003c')
services=load('services'); cases=load('case-studies'); articles=load('articles'); industries=load('industries'); phases=load('process'); team=load('team'); shared=load('shared'); labels=shared['labels']; manifesto=load('manifesto'); engagements=load('engagements')
origin=config['origin'].rstrip('/'); name=config['name']; pages={}
assert urlparse(origin).scheme=='https'
for group in [services,cases,articles,industries]:
 slugs=[x['slug'] for x in group]
 assert len(slugs)==len(set(slugs)), 'Duplicate content slugs'
 assert all(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',s) for s in slugs), 'Unsafe slug'
service_by_slug={s['slug']:s for s in services}
for x in industries:assert all(s in service_by_slug for s in x['services']), 'Unknown industry service'
for a in articles:
 if a.get('verified'):
  assert a['status']=='published' and a.get('date_published') and a.get('author'), 'Verified articles need publication details'

def intro(k,t,d):return f'<section class="page-intro"><div class="eyebrow">{e(k)}</div><h1>{e(t)}</h1><p class="lead">{e(d)}</p></section>'
def sections(items):return ''.join(f'<article><h2>{e(x["heading"])}</h2><p>{e(x["text"])}</p></article>' for x in items)
def service_cards():return ''.join(f'<a class="service-row" href="/services/{s["slug"]}/"><span class="num">{i+1:02}</span><h3>{e(s["name"])}</h3><span class="arrow" aria-hidden="true">↗</span><p>{e(s["description"])}</p></a>' for i,s in enumerate(services))
def case_cards():return ''.join(f'<a class="work-card" href="/work/{s["slug"]}/" data-service="{e(s["service"])}" data-industry="{e(s["industry"])}"><div class="work-art w{i%3}" aria-hidden="true"><span>{i+1:02} / MM</span><div></div><b>↗</b></div><div class="eyebrow">{e(s["industry"])} / {e(s["service"])}</div><h3>{e(s["title"])}</h3><p>{e(s["description"])}</p>'+ (f'<small>{e(labels["case_placeholder"])}</small>' if s['placeholder'] else '')+'</a>' for i,s in enumerate(cases))
def article_cards():return ''.join(f'<a class="insight" data-category="{e(a["category"])}" href="/insights/{a["slug"]}/"><div class="eyebrow">{e(a["category"])}'+(f' / {e(labels["article_draft"])}' if a['status']=='draft' else '')+f'</div><h3>{e(a["title"])}</h3><span>{e(labels["read_article"])}</span></a>' for a in articles)
def select(id_,label,values,all_label):return f'<label>{e(label)}<select id="{id_}"><option value="all">{e(all_label)}</option>'+''.join(f'<option>{e(v)}</option>' for v in sorted(set(values)))+'</select></label>'
def manifesto_html():return f'<section class="section manifesto"><div><div class="eyebrow">{e(manifesto["eyebrow"])}</div><h2>{manifesto["title"]}</h2><p class="lead">{e(manifesto["intro"])}</p></div><div class="beliefs">'+''.join(f'<article><span>{i+1:02}</span><div><h3>{e(b["title"])}</h3><p>{e(b["text"])}</p></div></article>' for i,b in enumerate(manifesto['beliefs']))+'</div></section>'
def form(kind='enquiry'):
 f=shared['form']; live=config['lead']['enabled']; review=kind=='review'
 fields=''.join(f'<label>{e(x["label"])}<input name="{x["name"]}" type="{x["type"]}" autocomplete="{x["autocomplete"]}" maxlength="{x["max"]}" '+('required' if x['required'] or (review and x['name']=='website') else '')+'></label>' for x in f['fields'])
 opts=''.join(f'<option value="{e(v) if i else ""}">{e(v)}</option>' for i,v in enumerate(f['budgets']))
 service_opts=f'<option>{e(f["service_default"])}</option>'+''.join(f'<option>{e(s["name"])}</option>' for s in services)
 lead=config['lead']; marketing=bool(live and lead['marketing_enabled'] and all(lead.get(k) for k in ['sender_name','postal_address','contact_email','unsubscribe_url']))
 consent=e(labels['marketing'].format(sender=lead['sender_name'])) if marketing else e(labels['marketing_disabled'])
 if marketing:consent+=f' {e(lead["postal_address"])} · {e(lead["contact_email"])} · <a href="{e(lead["unsubscribe_url"])}">Unsubscribe</a>'
 return f'''<form id="lead-form" data-kind="{kind}"><input type="hidden" name="kind" value="{kind}"><div class="form-grid">{fields}<label>{e(f['budget_label'])}<select name="budget" {'required' if not review else ''}>{opts}</select></label><label>{e(f['service_label'])}<select name="service">{service_opts}</select></label></div><label>{e(f['message_label'])}<textarea name="message" rows="5" maxlength="5000" required></textarea></label><div class="honeypot" aria-hidden="true"><label>Leave this field empty<input name="fax" tabindex="-1" autocomplete="off" maxlength="200"></label></div><label class="check"><input type="checkbox" name="marketing" {'disabled' if not marketing else ''}>{consent}</label><p class="fine"><a href="/privacy/">{e(labels['privacy_form'])}</a></p><button class="button" type="submit">{e(labels['submit'] if live else labels['prepare'])}</button><p id="form-status" role="status" tabindex="-1"></p><a id="download-enquiry" class="text-link" hidden>{e(labels['download'])}</a><noscript><p>{e(labels['contact_unavailable'])} JavaScript is required for this form.</p></noscript></form>'''
def booking():
 url=config['booking_url']
 if not url:return '<p class="notice">'+e(labels['booking_pending'])+'</p>'
 assert urlparse(url).scheme=='https' and not urlparse(url).username
 return f'<div class="booking"><p>{e(labels["booking_notice"])}</p><button class="button" id="load-booking">{e(labels["booking_load"])}</button><p><a class="text-link booking-link" href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(labels["booking_open"])}</a></p><div id="booking-slot"></div></div>'
def team_html():
 return ''.join('<section class="section green split">'+(f'<img class="team-photo" src="{e(t["photo"])}" alt="{e(t["photo_alt"])}" width="480" height="480" loading="lazy">' if t['photo'] else f'<div class="portrait-placeholder">{e(t["photo_alt"])}</div>')+f'<div><div class="eyebrow">{e(t["role"])}</div><h2>{e(t["name"])}</h2><p>{e(t["note"])}</p><p>{e(t["bio"])}</p></div></section>' for t in team)
def industries_html():
 out=''
 for ind in industries:
  links=''.join(f'<a class="text-link" href="/services/{s}/">{e(service_by_slug[s]["name"])} ↗</a>' for s in ind['services'])
  out+=f'<article class="industry" id="{ind["slug"]}"><h2>{e(ind["name"])}</h2><p class="lead">{e(ind["description"])}</p><div class="eyebrow">{e(labels["industry_services"])}</div><div class="related-links">{links}</div></article>'
 return out
components={'service_cards':service_cards(),'case_cards':case_cards(),'article_cards':article_cards(),'manifesto':manifesto_html(),'team':team_html(),'industry_details':industries_html(),'lead_form':form(),'review_form':form('review'),'booking':booking(),'contact_status':f'<p class="notice">{e(labels["contact_available"] if config["lead"]["enabled"] else labels["contact_unavailable"])}</p>', 'closing_cta':shared['closing_cta'],'review_cta':shared['review_cta'],'process_cards':''.join(f'<a href="/process/#step-{i+1}"><small>{i+1:02}</small><h3>{e(s["title"])}</h3><span aria-hidden="true">↗</span></a>' for i,s in enumerate(phases)),'process_details':''.join(f'<article class="phase" id="step-{i+1}"><div class="eyebrow">{i+1:02}</div><h2>{e(s["title"])}</h2><h3>{e(s["headline"])}</h3><p>{e(s["description"])}</p></article>' for i,s in enumerate(phases)), 'case_filters':'<div class="filters">'+select('service-filter','Service',[c['service'] for c in cases],labels['all_services'])+select('industry-filter','Industry',[c['industry'] for c in cases],labels['all_industries'])+'</div>', 'article_filters':'<section class="section filter-section">'+select('article-filter','Category',[a['category'] for a in articles],labels['all_categories'])+'<p id="article-status" role="status"></p></section>', 'engagement_models':''.join(f'<article class="engagement"><div class="eyebrow">{i+1:02} / ENGAGEMENT</div><h2>{e(m["title"])}</h2><h3>{e(m["fit"])}</h3><p>{e(m["text"])}</p><ul>'+''.join(f'<li>{e(x)}</li>' for x in m['outputs'])+f'</ul><p class="notice">{e(m["owner_fields"])}</p></article>' for i,m in enumerate(engagements))}
def add(path,title,description,body,extra=None):
 assert path not in pages, 'Duplicate page route'
 pages[path]=dict(title=title,description=description,body=body,extra=extra)
for p in load('pages'):
 body=re.sub(r'\{\{([a-z_]+)\}\}',lambda m:components[m[1]],p['body_html'])
 add(p['path'],p['title'],p['description'],body)
for s in services:
 related=[ind for ind in industries if s['slug'] in ind['services']]
 body=intro(s['name'],s['headline'],s['description'])+f'<section class="section split"><h2>{e(labels["service_problem_heading"])}</h2><div><p class="lead">{e(labels["service_problem"])}</p><h3>{e(labels["approach_heading"])}</h3><p>{e(labels["approach"])}</p></div></section><section class="section green"><h2>{e(labels["deliverables"])}</h2><div class="deliverables">'+''.join(f'<div><span aria-hidden="true">↗</span><h3>{e(d.title())}</h3></div>' for d in s['deliverables'])+f'</div></section><section class="section split"><div><div class="eyebrow">{e(labels["tools"])}</div><h3>{e(s["stack"])}</h3><p>{e(labels["stack_note"])}</p></div><div><div class="eyebrow">{e(labels["measurement"])}</div><h3>{e(s["kpis"])}</h3><p>{e(labels["measurement_note"])}</p></div></section><section class="section narrow"><h2>{e(labels["faq"])}</h2>'+''.join(f'<details><summary>{e(f["question"])}</summary><p>{e(f["answer"])}</p></details>' for f in s['faq'])+'</section>'
 if related:body+=f'<section class="section"><h2>{e(labels["service_industries"])}</h2><div class="three">'+''.join(f'<article><h3>{e(i["name"])}</h3><p>{e(i["description"])}</p><a class="text-link" href="/industries/#{i["slug"]}">{e(i["name"])} ↗</a></article>' for i in related)+'</div></section>'
 body+=shared['review_cta']+shared['closing_cta']
 add('/services/'+s['slug']+'/',s['name']+' agency in Vancouver',s['description'],body,{'@type':'FAQPage','mainEntity':[{'@type':'Question','name':f['question'],'acceptedAnswer':{'@type':'Answer','text':f['answer']}} for f in s['faq']]})
for c in cases:
 body=intro(c['industry']+' / '+c['service'],c['title'],c['description'])+'<section class="section narrow">'+(f'<p class="notice">{e(labels["case_notice"])}</p>' if c['placeholder'] else '')+sections(c['sections'])+f'<blockquote>{e(c["quote"])}</blockquote></section>'+shared['closing_cta']
 add('/work/'+c['slug']+'/',c['title']+(' — case study placeholder' if c['placeholder'] else ''),c['description'],body)
for a in articles:
 body=intro(a['category'],a['title'],a['description'])+'<article class="section narrow">'+(f'<p class="notice">{e(labels["article_notice"])}</p>' if a['status']=='draft' else '')+f'<p class="byline">{e(a["author"])} · {e(a["reading_time"])}'+(f' · {e(a["date_published"])}' if a.get('date_published') else '')+'</p>'+sections(a['sections'])+f'</article><section class="section"><h2>{e(labels["related"])}</h2><div class="three">'+article_cards()+'</div></section>'
 schema={'@type':'Article','headline':a['title'],'description':a['description'],'author':{'@type':'Person','name':a['author']},'datePublished':a['date_published'],'mainEntityOfPage':origin+'/insights/'+a['slug']+'/'} if a.get('verified') and a['status']=='published' else None
 add('/insights/'+a['slug']+'/',a['title'],a['description'],body,schema)
# These are source templates; editorial content is exclusively in content/*.json.
nav=shared['nav_html']; footer=shared['footer_html']
client_config={'analytics':config['analytics'],'lead':config['lead'],'booking_url':config['booking_url'],'labels':labels}
(D/'config.js').write_text('window.MM_CONFIG = '+js(client_config)+';\n')
for path,p in pages.items():
 title=p['title'];description=p['description']; graph=[{'@type':'Organization','name':name,'url':origin}]
 crumbs=[{'@type':'ListItem','position':1,'name':'Home','item':origin+'/'}]
 if path!='/':crumbs.append({'@type':'ListItem','position':2,'name':title,'item':origin+path})
 graph.append({'@type':'BreadcrumbList','itemListElement':crumbs})
 if path.startswith('/services/') and path!='/services/':graph.append({'@type':'Service','name':title,'provider':{'@type':'Organization','name':name},'areaServed':['Canada','United States']})
 if p['extra']:graph.append(p['extra'])
 business=config['local_business']
 if business['verified']:
  assert all(business.get(k) for k in ['telephone','email','streetAddress','postalCode']), 'Verified business details incomplete'
  graph.append({'@type':'LocalBusiness','name':name,'url':origin,'telephone':business['telephone'],'email':business['email'],'address':{'@type':'PostalAddress',**{k:business[k] for k in ['streetAddress','addressLocality','addressRegion','postalCode','addressCountry']}}})
 menu=''.join(f'<a href="/services/{s["slug"]}/">{e(s["name"])}</a>' for s in services)
 preview=f'<div class="preview-note">{e(labels["preview"])}</div>' if config['preview'] else ''
 robots='noindex,nofollow' if config['preview'] else 'index,follow'
 doc=f'''<!doctype html><html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | {e(name)}</title><meta name="description" content="{e(description)}"><meta name="robots" content="{robots}"><link rel="canonical" href="{origin+path}"><link rel="alternate" hreflang="en-CA" href="{origin+path}"><link rel="alternate" hreflang="en-US" href="{origin+path}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{origin+path}"><meta property="og:type" content="website"><meta name="twitter:card" content="summary"><meta name="theme-color" content="#173e35"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="preload" href="/fonts/fraunces-display.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/style.css"><script type="application/ld+json">{js({'@context':'https://schema.org','@graph':graph})}</script><script src="/config.js"></script><script src="/consent.js"></script><script defer src="/app.js"></script></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="/" aria-label="Montshire Media home">Montshire<span>Media</span><b aria-hidden="true">✳</b></a><button class="plain mobile-menu" aria-expanded="false" aria-controls="navigation">Menu +</button><nav id="navigation" aria-label="Main"><details class="mega"><summary>Services</summary><div><a href="/services/">All capabilities ↗</a>{menu}</div></details>{nav}<a class="nav-cta" href="/contact/">Let’s talk ↗</a></nav><button class="theme-toggle" aria-label="Switch colour theme" aria-pressed="false">◐</button></header>{preview}<main id="main">{p['body']}</main>{footer}<a class="mobile-cta" href="/seo-site-review/">Free SEO & site health review ↗</a><aside id="cookie-banner" aria-label="Cookie preferences" hidden><h3>{e(labels['cookie_title'])}</h3><p>{e(labels['cookie_description'])}</p><div><button data-consent="essential">{e(labels['cookie_essential'])}</button><button data-consent="analytics">{e(labels['cookie_allow'])}</button></div></aside></body></html>'''
 out=D/path.strip('/')/'index.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(doc)
# Remove only generated HTML pages whose content has been removed; preserve assets.
expected={D/p.strip('/')/'index.html' for p in pages}
for f in D.rglob('index.html'):
 if f not in expected:f.unlink()
(D/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{e(origin+p)}</loc></url>' for p in pages)+'</urlset>')
(D/'robots.txt').write_text('User-agent: *\n'+('Disallow: /' if config['preview'] else 'Allow: /')+'\nSitemap: '+origin+'/sitemap.xml\n')
print(f'Generated {len(pages)} pages; preview={config["preview"]}; live enquiries={config["lead"]["enabled"]}')
