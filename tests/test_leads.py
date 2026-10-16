import io,json,os,pathlib,sys,tempfile,unittest
from unittest.mock import patch
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from server import leads
class LeadTests(unittest.TestCase):
 def valid(self):return dict(kind='enquiry',name='Test Person',email='test@example.com',company='Example',website='https://example.com',budget='Under $5,000',service='Search Engine Optimization',message='Test enquiry',fax='',marketing=False)
 def test_strict_validation(self):
  self.assertEqual(leads.validate(self.valid())['email'],'test@example.com')
  for update in [{'email':'bad'},{'name':'x'*101},{'website':'javascript:alert(1)'},{'fax':'bot'},{'extra':'value'},{'marketing':'yes'},{'marketing':True},{'email':'a@example.com\nBcc: x@y.com'},{'kind':'review','website':''},{'budget':'unknown'},{'service':'unknown'}]:
   with self.subTest(update=update),self.assertRaises(leads.Invalid):leads.validate({**self.valid(),**update})
 def test_rate_limit_and_expiry(self):
  with tempfile.TemporaryDirectory() as t:
   db=str(pathlib.Path(t)/'limits.sqlite')
   for i in range(5):self.assertTrue(leads.allowed('client',db,'secret',1000))
   self.assertFalse(leads.allowed('client',db,'secret',1001));self.assertTrue(leads.allowed('other',db,'secret',1001));self.assertTrue(leads.allowed('client',db,'secret',1900))
 def request(self,body=None,**changes):
  payload=json.dumps(self.valid() if body is None else body).encode();env=dict(PATH_INFO='/api/leads',REQUEST_METHOD='POST',HTTP_ORIGIN=leads.CONFIG['origin'],CONTENT_TYPE='application/json',CONTENT_LENGTH=str(len(payload)),REMOTE_ADDR='test');env['wsgi.input']=io.BytesIO(payload);env.update(changes);status=[]
  result=leads.application(env,lambda code,headers:status.append(code));return status[0],json.loads(b''.join(result))
 def test_endpoint_fail_closed_and_delivery(self):
  self.assertEqual(self.request(HTTP_ORIGIN='https://evil.example')[0],'403 Forbidden')
  self.assertEqual(self.request()[0],'503 Service Unavailable')
  with tempfile.TemporaryDirectory() as t,patch.dict(os.environ,{'RATE_LIMIT_SECRET':'test-secret','RATE_LIMIT_DB':str(pathlib.Path(t)/'rates.sqlite')}),patch.dict(leads.CONFIG['lead'],{'enabled':True}):
   with patch.object(leads,'send',side_effect=RuntimeError('unavailable')):self.assertEqual(self.request()[0],'502 Bad Gateway')
   with patch.object(leads,'send') as send:
    self.assertEqual(self.request(),('200 OK',{'accepted':True}));send.assert_called_once()
   self.assertEqual(self.request(CONTENT_LENGTH='20000')[0],'413 Payload Too Large')
   self.assertEqual(self.request(CONTENT_TYPE='text/plain')[0],'415 Unsupported Media Type')
 def test_smtp_encryption_modes_and_recipient_rejection(self):
  env={'SMTP_HOST':'smtp.example.com','SMTP_USER':'sender@example.com','SMTP_PASSWORD':'unit-test-only','SMTP_FROM':'sender@example.com','LEAD_TO':'recipient@example.com'}
  for mode in ['ssl','starttls']:
   with self.subTest(mode=mode),patch.dict(os.environ,{**env,'SMTP_SECURITY':mode},clear=True),patch.object(leads.smtplib,'SMTP_SSL') as secure,patch.object(leads.smtplib,'SMTP') as upgrade:
    smtp=(secure if mode=='ssl' else upgrade).return_value.__enter__.return_value
    smtp.send_message.return_value={}
    leads.send(self.valid())
    smtp.login.assert_called_once_with(env['SMTP_USER'],env['SMTP_PASSWORD'])
    if mode=='ssl':upgrade.assert_not_called();smtp.starttls.assert_not_called()
    else:secure.assert_not_called();smtp.starttls.assert_called_once()
    smtp.send_message.return_value={'recipient@example.com':(550,b'rejected')}
    with self.assertRaises(RuntimeError):leads.send(self.valid())
  with patch.dict(os.environ,{**env,'SMTP_SECURITY':'none'},clear=True),self.assertRaises(RuntimeError):leads.send(self.valid())
 def test_loopback_relay_needs_no_password_and_refuses_external_hosts(self):
  env={'SMTP_SECURITY':'local','SMTP_HOST':'localhost','SMTP_PORT':'25','SMTP_FROM':'sender@example.com','LEAD_TO':'recipient@example.com'}
  with patch.dict(os.environ,env,clear=True),patch.object(leads.smtplib,'SMTP') as client:
   smtp=client.return_value.__enter__.return_value;smtp.send_message.return_value={}
   leads.send(self.valid());smtp.login.assert_not_called();smtp.starttls.assert_not_called()
   for update in [{'SMTP_HOST':'external.example.com'},{'SMTP_PORT':'587'}]:
    with patch.dict(os.environ,update),self.assertRaises(RuntimeError):leads.send(self.valid())
 def test_passenger_exact_mount(self):
  import passenger_wsgi
  for path in ['', '/']:
   env={'SCRIPT_NAME':'/api/leads','PATH_INFO':path,'REQUEST_METHOD':'GET'};status=[]
   passenger_wsgi.application(env,lambda code,headers:status.append(code))
   self.assertEqual(status,['405 Method Not Allowed'])
  status=[]
  passenger_wsgi.application({'SCRIPT_NAME':'/other','PATH_INFO':'','REQUEST_METHOD':'GET'},lambda code,headers:status.append(code))
  self.assertEqual(status,['404 Not Found'])
if __name__=='__main__':unittest.main()
