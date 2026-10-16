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
if __name__=='__main__':unittest.main()
