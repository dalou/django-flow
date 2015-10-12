# encoding: utf-8
from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    url(r'^flow/$', views.Flow.as_view(), name="flow"),
]
