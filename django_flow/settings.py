# -*- coding: utf-8 -*-
from django.conf import settings

"""
A boolean that allow Flow app debug printing
"""
FLOW_DISCONNECTED_ENABLED = bool(int(getattr(settings, 'FLOW_DISCONNECTED_ENABLED', "0")))

"""
A boolean that allow Flow app debug printing
"""
FLOW_DEBUG = bool(int(getattr(settings, 'FLOW_DEBUG', "1")))

"""
Signal modules tuple paths that receive secure users messages
"""
FLOW_SIGNALS = getattr(settings, 'FLOW_SIGNALS', (
    "django_flow.signals",
))

"""
For more security, we can prefix signals receivers
"""
FLOW_SIGNALS_PREFIX = getattr(settings, 'FLOW_SIGNALS_PREFIX', "flow")

"""
    Browser ativity delay before marked as idle, in seconds
"""
FLOW_ACTIVITY_DELAY = int(getattr(settings, 'FLOW_ACTIVITY_DELAY', 1000 * 60 * 5))

"""
    Initial url to fetch initials data
"""
FLOW_INITIAL_URL = getattr(settings, 'FLOW_INITIAL_URL', "/flow/")

"""
A boolean that allow Flow app debug printing
"""
FLOW_WS_ENABLED = bool(int(getattr(settings, 'FLOW_WS_ENABLED', "1")))

FLOW_WS_URL = getattr(settings, 'FLOW_WS_URL', '/ws/')

FLOW_WS_CONNECTION = getattr(settings, 'FLOW_WS_CONNECTION', {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': None,
})

"""
A string to prefix elements in the Redis datastore, to avoid naming conflicts with other services.
"""
FLOW_WS_PREFIX = getattr(settings, 'FLOW_WS_PREFIX', "flow")

"""
The time in seconds, items shall be persisted by the Redis datastore.
"""
FLOW_WS_EXPIRE = int(getattr(settings, 'FLOW_WS_EXPIRE', 3600))

"""
Replace the subscriber class by a customized version.
"""
FLOW_WS_SUBSCRIBER = getattr(settings, 'FLOW_WS_SUBSCRIBER', 'django_flow.pipe.Subscriber')

"""
This set the magic string to recognize heartbeat messages. If set, this message string is ignored
by the server and also shall be ignored on the client.

If FLOW_WS_HEARTBEAT is not None, the server sends at least every 4 seconds a heartbeat message.
It is then up to the client to decide, what to do with these messages.
"""
FLOW_WS_HEARTBEAT = getattr(settings, 'FLOW_WS_HEARTBEAT', '--heartbeat--')


"""
If set, this callback function is called right after the initialization of the Websocket.
This function can be used to restrict the subscription/publishing channels for the current client.
As its first parameter, it takes the current ``request`` object.
The second parameter is a list of desired subscription channels.
This callback function shall return a list of allowed channels or throw a ``PermissionDenied``
exception.
Remember that this function is not allowed to perform any blocking requests, such as accessing the
database!
"""
FLOW_WS_ALLOWED_CHANNELS = getattr(settings, 'FLOW_WS_ALLOWED_CHANNELS', None)

"""
If set, this callback function is called instead of the default process_request function in WebsocketWSGIServer.
This function can be used to enforce custom authentication flow. i.e. JWT
"""
FLOW_WS_PROCESS_REQUEST = getattr(settings, 'FLOW_WS_PROCESS_REQUEST', None)








