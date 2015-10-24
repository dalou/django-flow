# encoding: utf-8

import logging
import json

from django.apps import apps
from django.conf import settings
from django.views import generic
from django.http import JsonResponse

logger = logging.getLogger(__name__)

from .pipe import dispatch, send,  disconnected_receive, debug_traceback
from .models import StaffNotification

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


"""
    Message receive from js GET (disconnected mode)
    Flush redis store
"""
class DisconnectedReceive(generic.View):

    def get(self, request, *args, **kwargs):
        self.request = request
        user = request.user
        if not (user.is_authenticated()):
            raise Http404

        flow = []
        for message in disconnected_receive(request):
            flow.append(message)
        return JsonResponse(flow, safe=False)

"""
    Message send from js GET (disconnected mode)
"""
class DisconnectedSend(DisconnectedReceive):

    def get(self, request, *args, **kwargs):
        self.request = request
        user = request.user
        if not (user.is_authenticated()):
            raise Http404

        data = json.loads(request.GET.get('msg'))
        dispatch(user.pk, data)

        return super(DisconnectedSend, self).get(request, *args, **kwargs)




class AdminDashboard(generic.TemplateView):

    template_name = "django_flow/admin/dashboard.html"


class AdminInitials(InitialsJson):

    def get(self, request, *args, **kwargs):
        if not (request.user.is_staff):
            raise Http404
        else:
            return super(AdminInitials, self).get(request, *args, **kwargs)

    def get_initials(self):

        for staff_notification in StaffNotification.objects.all()[0:100]:
            yield 'staff_notification_initial', staff_notification.to_json()








