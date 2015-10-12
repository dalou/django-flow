# -*- coding: utf-8 -*-
import re, json, six, importlib
from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from .redis_ws.subscriber import RedisSubscriber
from .redis_ws.publisher import RedisPublisher
from .redis_ws.redis_store import RedisMessage
from .signals import flow_user_disconnected
from . import settings

# Import signals clients receptors modules from settings.FLOW_SIGNALS
signals_modules = []
for signal_module in settings.FLOW_SIGNALS:

    try:
        mod = importlib.import_module(signal_module)
        signals_modules.append( mod )
    except ImportError, e:
        raise ImportError("Could not import settings '%s' "
               "(Is it on sys.path? Does it have syntax errors?):"
                "%s" % (signal_module, e))


class Subscriber(RedisSubscriber):
    """
    Customised RedisSubscriber class for flow app, used by the websocket code to listen for subscribed channels

    """
    subscription_channels = ['subscribe-session', 'subscribe-group', 'subscribe-user', 'subscribe-broadcast']
    publish_channels = ['publish-session', 'publish-group', 'publish-user', 'publish-broadcast']

    def publish_message(self, message, expire=None):
        data = json.loads(message)
        user_pk = self.get_user_pk_for_channel('flow')
        if user_pk:
            dispatch(user_pk=user_pk, data=data)
        super(Subscriber, self).publish_message(message, expire=expire)


    def release(self):
        """
        Simulate proper client disconnection from a brutal broken pipe
        """
        user_pk = self.get_user_pk_for_channel('flow', subscribed=True)
        if user_pk:
            flow_user_disconnected.send(sender=django_settings.AUTH_USER_MODEL, user_pk=user_pk)
        super(Subscriber, self).release()


def dispatch(user_pk, data, **kwargs):
    """
    Dispatch user data messages to receivers signals set at FLOW_SIGNALS
    """
    print user_pk, data
    if isinstance(data, dict):

        type = data.get('type', '')
        flow_type = 'flow_%s' % type
        data = data.get('data', None)
        for signals_module in signals_modules:
            if hasattr(signals_module, flow_type):
                signal = getattr(signals_module, flow_type)
                if settings.FLOW_DEBUG:
                    debug_traceback('', data, [user_pk], type=type, to=False, success=True)

                signal.send(sender=django_settings.AUTH_USER_MODEL, user_pk=user_pk, data=data, kwargs=kwargs)
            else:
                if settings.FLOW_DEBUG:
                    debug_traceback('unknow : ', data, [user_pk], type=type, to=False, success=False)
    else:
        if settings.FLOW_DEBUG:
            debug_traceback('unknow data type : ', data, [user_pk], to=False, success=False)


class Publisher(RedisPublisher):
    """
    Customised RedisPublisher class for flow app, used by the websocket code to write on subscribed channels

    """
    pass


def send(type, data={}, users=None):
    """
    Send a message to a set of users (list of user pk)
    """
    typed_data = {
        'type': type,
        #'from': 'PY',
        'data': data
    }

    if settings.FLOW_DEBUG:
        debug_traceback('', data, users, type=type, to=True, success=True)

    kwargs = {}
    if users:
        kwargs['users'] = users
    else:
        kwargs['broadcast'] = True


    publisher = Publisher(facility='flow', **kwargs)
    message = RedisMessage(typed_data)
    publisher.publish_message(message)




def debug_traceback(msg, data, user_pks, success=True, to=False, type=None):
    users = get_user_model().objects.filter(pk__in=user_pks)
    c = ('\033[92m' if to else '\033[94m' ) if success else '\033[91m'
    endc = '\033[0m'
    print c + '---- \033[1;36mFLOW ' + endc
    message = c + ('SEND ' if to else 'RECEIVE ') + endc
    message += c + msg + endc
    message += (("\033[0m\033[1;36m%s" %  type) if type else '')  + endc
    print  "\t" + message
    message = str(data)
    print '\t' + message
    message = c + ('TO: ' if to else 'FROM: ') + endc
    message += "\033[1;36m" + "\033[0m \033[1;36m".join([(user.email) for user in users]) + endc
    print '\t' + message
    print c + '---- ' + endc