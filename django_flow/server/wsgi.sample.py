import os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.dev")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
#from django.core.wsgi import get_wsgi_application
from django.conf import settings
from ..redis_ws.wsgi_runserver import WebsocketWSGIServer


#_django_app = get_wsgi_application()
_websocket_app = WebsocketWSGIServer()

def application(environ, start_response):
    if environ.get('PATH_INFO').startswith(settings.WEBSOCKET_URL):
        return _websocket_app(environ, start_response)