# encoding: utf-8

from django import template
from django.utils import timezone
from django.utils.safestring import mark_safe
from .. import settings

register = template.Library()

from ..models import *

@register.inclusion_tag('django_flow/_init.html', takes_context=True)
def flow_init(context):
    request = context['request']
    protocol = request.is_secure() and 'wss://' or 'ws://'
    heartbeat_msg = settings.FLOW_WS_HEARTBEAT and '"{0}"'.format(settings.FLOW_WS_HEARTBEAT) or 'null'
    context.update({
        'STATIC_URL': settings.settings.STATIC_URL,
        'FLOW_WS_HEARTBEAT': mark_safe(heartbeat_msg),
        'FLOW_WS_URI': protocol + request.get_host() + settings.FLOW_WS_URL,
        'FLOW_WS_ENABLED': settings.FLOW_WS_ENABLED,
        'FLOW_DEBUG': settings.FLOW_DEBUG,
        'FLOW_ACTIVITY_DELAY': settings.FLOW_ACTIVITY_DELAY,
        'FLOW_INITIAL_URL': settings.FLOW_INITIAL_URL,
        'FLOW_DISCONNECTED_ENABLED': settings.FLOW_DISCONNECTED_ENABLED,
    })
    return context

