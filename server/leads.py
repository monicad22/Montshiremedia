"""Optional same-origin WSGI lead endpoint. Not deployed by the static Sites manifest.
Run behind a production WSGI server and HTTPS reverse proxy; see server/README.md.
"""
import hashlib,hmac,json,os,pathlib,re,smtplib,sqlite3,ssl,time
from email.message import EmailMessage
from urllib.parse import urlparse
ROOT=pathlib.Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/'content.json').read_text())
SHARED=json.loads((ROOT/'content/shared.json').read_text())
SERVICES=json.loads((ROOT/'content/services.json').read_text())
LIMITS={'kind':10,'name':100,'email':254,'company':150,'website':300,'budget':100,'service':100,'message':5000,'fax':200}
class Invalid(ValueError): pass

def validate(data):
 if not isinstance(data,dict) or set(data)-set(LIMITS)-{'marketing'}:raise Invalid('Invalid fields')
 if any(not isinstance(data.get(k,''),str) or len(data.get(k,''))>limit for k,limit in LIMITS.items()):raise Invalid('Invalid field length or type')
 if not isinstance(data.get('marketing',False),bool):raise Invalid('Invalid consent')
 clean={k:data.get(k,'').strip() for k in LIMITS};clean['marketing']=data.get('marketing',False)
 if clean['fax']:raise Invalid('Rejected')
 if clean['kind'] not in ['enquiry','review']:raise Invalid('Invalid enquiry type')
 for k in ['name','email','company','message']:
  if not clean[k]:raise Invalid('Required field')
 for k,v in clean.items():
  if isinstance(v,str) and (re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]',v) or (k!='message' and ('\r' in v or '\n' in v))):raise Invalid('Invalid characters')
 if not re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,63}",clean['email']):raise Invalid('Invalid email')
 if clean['kind']=='review' and not clean['website']:raise Invalid('Website required')
 if clean['website']:
  u=urlparse(clean['website'])
  if u.scheme not in ['http','https'] or not u.hostname or u.username or u.password or any(c.isspace() for c in clean['website']):raise Invalid('Invalid website')
 if clean['budget'] not in SHARED['form']['budgets'][1:]+([''] if clean['kind']=='review' else []):raise Invalid('Invalid budget')
 if clean['service'] not in [SHARED['form']['service_default']]+[s['name'] for s in SERVICES]:raise Invalid('Invalid service')
 lead=CONFIG['lead']
 if clean['marketing'] and not (lead['marketing_enabled'] and all(lead.get(k) for k in ['sender_name','postal_address','contact_email','unsubscribe_url'])):raise Invalid('Marketing consent unavailable')
 return clean

def allowed(client,db_path,secret,now=None):
 """Atomic fixed-window limit: 5 requests/15 min; expiring HMAC keys only."""
 now=int(time.time() if now is None else now);key=hmac.new(secret.encode(),client.encode(),hashlib.sha256).hexdigest()
 with sqlite3.connect(db_path,timeout=5) as db:
  db.execute('CREATE TABLE IF NOT EXISTS limits (client TEXT PRIMARY KEY, start INTEGER NOT NULL, count INTEGER NOT NULL)')
  db.execute('BEGIN IMMEDIATE')
  db.execute('DELETE FROM limits WHERE start <= ?', (now-900,))
  row=db.execute('SELECT count FROM limits WHERE client=?',(key,)).fetchone()
  if row and row[0]>=5:return False
  db.execute('INSERT INTO limits(client,start,count) VALUES(?,?,1) ON CONFLICT(client) DO UPDATE SET count=count+1',(key,now))
 return True

def send(data):
 required=['SMTP_HOST','SMTP_USER','SMTP_PASSWORD','SMTP_FROM','LEAD_TO']
 if not all(os.environ.get(k) for k in required):raise RuntimeError('Delivery unavailable')
 msg=EmailMessage();msg['Subject']='Montshire Media — '+('Site review request' if data['kind']=='review' else 'Project enquiry')
 msg['From']=os.environ['SMTP_FROM'];msg['To']=os.environ['LEAD_TO'];msg['Reply-To']=data['email']
 # Plain-text email only; user content is never evaluated as HTML or used in subject headers.
 msg.set_content('\n\n'.join(f'{k.upper()}: {data[k]}' for k in ['kind','name','email','company','website','budget','service','message'])+'\n\nMARKETING CONSENT: '+str(data['marketing'])+'\nCONSENT TEXT VERSION: 2026-10-v2\nUTC RECEIVED: '+time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
 with smtplib.SMTP(os.environ['SMTP_HOST'],int(os.getenv('SMTP_PORT','587')),timeout=10) as smtp:
  smtp.ehlo();smtp.starttls(context=ssl.create_default_context());smtp.ehlo();smtp.login(os.environ['SMTP_USER'],os.environ['SMTP_PASSWORD']);refused=smtp.send_message(msg)
  if refused:raise RuntimeError('Recipient rejected')

def application(environ,start_response):
 def respond(code,obj):
  body=json.dumps(obj).encode();start_response(code,[('Content-Type','application/json'),('Content-Length',str(len(body))),('Cache-Control','no-store'),('X-Content-Type-Options','nosniff'),('Referrer-Policy','no-referrer')]);return [body]
 if environ.get('PATH_INFO')!='/api/leads':return respond('404 Not Found',{'accepted':False})
 if environ.get('REQUEST_METHOD')!='POST':return respond('405 Method Not Allowed',{'accepted':False})
 # Exact Origin allowlist; do not trust Host or client-supplied forwarding headers.
 if environ.get('HTTP_ORIGIN')!=os.getenv('SITE_ORIGIN',CONFIG['origin']):return respond('403 Forbidden',{'accepted':False})
 if environ.get('CONTENT_TYPE','').split(';')[0].strip()!='application/json':return respond('415 Unsupported Media Type',{'accepted':False})
 try:size=int(environ.get('CONTENT_LENGTH','0'))
 except ValueError:return respond('400 Bad Request',{'accepted':False})
 if size<2 or size>16384:return respond('413 Payload Too Large',{'accepted':False})
 if not CONFIG['lead']['enabled'] or not os.getenv('RATE_LIMIT_SECRET') or not os.getenv('RATE_LIMIT_DB'):return respond('503 Service Unavailable',{'accepted':False})
 try:
  if not allowed(environ.get('REMOTE_ADDR','unknown'),os.environ['RATE_LIMIT_DB'],os.environ['RATE_LIMIT_SECRET']):return respond('429 Too Many Requests',{'accepted':False})
  data=validate(json.loads(environ['wsgi.input'].read(size)))
 except (Invalid,ValueError,UnicodeDecodeError):return respond('400 Bad Request',{'accepted':False})
 except Exception:return respond('503 Service Unavailable',{'accepted':False})
 try:send(data)
 except Exception:return respond('502 Bad Gateway',{'accepted':False})
 return respond('200 OK',{'accepted':True})
