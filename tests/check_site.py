import json,pathlib,re
from html.parser import HTMLParser
from urllib.parse import urlsplit
R=pathlib.Path(__file__).resolve().parents[1]; D=R/'dist'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.h1=0;self.links=[];self.ids=[];self.jsonld=[];self.inld=False;self.ld='';self.noindex=False
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='h1':self.h1+=1
  if 'id' in a:self.ids.append(a['id'])
  if t=='a':self.links.append(a.get('href',''))
  if t in ['script','link','img']:
   u=a.get('src',a.get('href',''))
   if u.startswith('/') and not (D/u.lstrip('/')).exists():raise AssertionError('Missing asset '+u)
  if t=='script' and a.get('type')=='application/ld+json':self.inld=True;self.ld=''
  if t=='meta' and a.get('name')=='robots':self.noindex='noindex' in a.get('content','')
 def handle_data(self,s):
  if self.inld:self.ld+=s
 def handle_endtag(self,t):
  if t=='script' and self.inld:self.jsonld.append(json.loads(self.ld));self.inld=False
pages={}
for file in D.rglob('*.html'):
 p=Page();p.feed(file.read_text());assert p.h1==1,(file,'H1');assert p.noindex,(file,'noindex');assert len(p.ids)==len(set(p.ids)),(file,'duplicate ids');assert '{{' not in file.read_text(),(file,'unresolved marker');pages[file]=p
for f,p in pages.items():
 for href in p.links:
  u=urlsplit(href)
  if u.path.startswith('/'):
   target=D/u.path.lstrip('/')/'index.html'
   assert target in pages,(f,href)
   if u.fragment:assert u.fragment in pages[target].ids,(f,href)
assert len(pages)==28
font=D/'fonts/fraunces-display.woff2';assert font.stat().st_size<100000
print('PASS: 28 pages, internal links/anchors/assets, unique IDs, single H1, valid JSON-LD, noindex, no template markers.')
print('Display font bytes:',font.stat().st_size)
