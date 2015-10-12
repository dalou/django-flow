# encoding: utf-8

import logging

from django.apps import apps
from django.conf import settings
from django.views import generic
from django.http import JsonResponse

logger = logging.getLogger(__name__)



class Load(generic.View):

    facility = 'flow'
    audience = {'broadcast': True}

    def get(self, request, *args, **kwargs):
        """
            Connect to WS and send initial data from apps models get_initial_flow method
        """

        user = request.user
        if not (user.is_authenticated()):
            raise Http404

        flow = []
        ctx = {}
        for app in apps.get_apps():
            if app.__name__.startswith('apps'):
                if hasattr(app, 'get_initial_flow'):
                    for type, data in app.get_initial_flow(request, ctx):
                        flow.append({
                            'type': type,
                            'data': data
                        })

        return JsonResponse(flow, safe=False)

class InitialsJson(generic.View):

    def get(self, request, *args, **kwargs):
        self.request = request
        user = request.user
        if not (user.is_authenticated()):
            raise Http404

        flow = []
        for type, data in self.get_initials():
            flow.append({
                'type': type,
                'data': data
            })
        return JsonResponse(flow, safe=False)

    def get_initials(self):

        raise NotImplementedError("""
            Not implemented
        """)
