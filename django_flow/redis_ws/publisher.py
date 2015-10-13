#-*- coding: utf-8 -*-
from redis import ConnectionPool, StrictRedis
from .. import settings
from .redis_store import RedisStore

redis_connection_pool = ConnectionPool(**settings.FLOW_WS_CONNECTION)


class RedisPublisher(RedisStore):
    def __init__(self, **kwargs):
        """
        Initialize the channels for publishing messages through the message queue.
        """
        connection = StrictRedis(connection_pool=redis_connection_pool)
        super(RedisPublisher, self).__init__(connection)
        for key in self._get_message_channels(**kwargs):
            self._publishers.add(key)

    def fetch_message(self, request, facility, audience='any'):
        """
        Fetch the first message available for the given ``facility`` and ``audience``, if it has
        been persisted in the Redis datastore.
        The current HTTP ``request`` is used to determine to whom the message belongs.
        A unique string is used to identify the bucket's ``facility``.
        Determines the ``audience`` to check for the message. Must be one of ``broadcast``,
        ``group``, ``user``, ``session`` or ``any``. The default is ``any``, which means to check
        for all possible audiences.
        """
        prefix = self.get_prefix()
        channels = []
        if audience in ('session', 'any',):
            if request and request.session:
                channels.append('{prefix}session:{0}:{facility}'.format(request.session.session_key, prefix=prefix, facility=facility))
        if audience in ('user', 'any',):
            if request and request.user and request.user.is_authenticated():
                channels.append('{prefix}user:{0}:{facility}'.format(request.user.pk, prefix=prefix, facility=facility))
        if audience in ('group', 'any',):
            try:
                if request.user.is_authenticated():
                    groups = request.session['flow_redis_ws:memberof']
                    channels.extend('{prefix}group:{0}:{facility}'.format(g, prefix=prefix, facility=facility)
                                for g in groups)
            except (KeyError, AttributeError):
                pass
        if audience in ('broadcast', 'any',):
            channels.append('{prefix}broadcast:{facility}'.format(prefix=prefix, facility=facility))
        for channel in channels:
            message = self._connection.get(channel)

            if message:
                return message


    def fetch_disconnected_message(self, request, facility, audience='any'):
        """
        Fetch the first message available for the given ``facility`` and ``audience``, if it has
        been persisted in the Redis datastore.
        The current HTTP ``request`` is used to determine to whom the message belongs.
        A unique string is used to identify the bucket's ``facility``.
        Determines the ``audience`` to check for the message. Must be one of ``broadcast``,
        ``group``, ``user``, ``session`` or ``any``. The default is ``any``, which means to check
        for all possible audiences.
        """
        prefix = self.get_prefix()
        channels = []
        if audience in ('session', 'any',):
            if request and request.session:
                channels.append('{prefix}session:{0}:{facility}'.format(request.session.session_key, prefix=prefix, facility=facility))
        if audience in ('user', 'any',):
            if request and request.user and request.user.is_authenticated():
                channels.append('{prefix}user:{0}:{facility}'.format(request.user.pk, prefix=prefix, facility=facility))
        if audience in ('group', 'any',):
            try:
                if request.user.is_authenticated():
                    groups = request.session['flow_redis_ws:memberof']
                    channels.extend('{prefix}group:{0}:{facility}'.format(g, prefix=prefix, facility=facility)
                                for g in groups)
            except (KeyError, AttributeError):
                pass
        if audience in ('broadcast', 'any',):
            channels.append('{prefix}broadcast:{facility}'.format(prefix=prefix, facility=facility))
        for channel in channels:
            message = self._connection.get(channel)

            if message:
                self._connection.delete(channel)
                return message
