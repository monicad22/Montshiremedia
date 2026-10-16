"""cPanel Passenger entry point mounted only at /api/leads."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
os.umask(0o077)
from server.leads import application as lead_application

def application(environ, start_response):
    # Passenger removes the app mount from PATH_INFO. Restore only this exact route.
    if environ.get('SCRIPT_NAME', '').rstrip('/') == '/api/leads' and environ.get('PATH_INFO', '') in ('', '/'):
        environ = dict(environ, PATH_INFO='/api/leads')
    return lead_application(environ, start_response)
