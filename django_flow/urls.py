# encoding: utf-8
from . import settings
from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from . import views

if settings.FLOW_DISCONNECTED_ENABLED:
    urlpatterns = [
        #url(r'^__flow__/$', views.Flow.as_view(), name="flow"),
        url(r'^__flow__/receive/$', views.DisconnectedReceive.as_view(), name="django_flow_disconnected_receive"),
        url(r'^__flow__/send/$', views.DisconnectedSend.as_view(), name="django_flow_disconnected_send"),
        url(r'^__flow__/admin/initials/$', staff_member_required(views.AdminInitials.as_view()), name="django_flow_admin_initials"),
        url(r'^__flow__/admin/dashboard/$', staff_member_required(views.AdminDashboard.as_view()), name="django_flow_admin_dashboard"),
    ]
