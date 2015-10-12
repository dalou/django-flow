# encoding: utf-8
from . import settings
from django.conf.urls import patterns, url
from . import views

if settings.FLOW_DISCONNECTED_ENABLED:
    urlpatterns = [
        #url(r'^__flow__/$', views.Flow.as_view(), name="flow"),
        url(r'^__flow__/receive/$', views.DisconnectedReceive.as_view(), name="django_flow_disconnected_receive"),
        url(r'^__flow__/send/$', views.DisconnectedSend.as_view(), name="django_flow_disconnected_send"),
    ]
