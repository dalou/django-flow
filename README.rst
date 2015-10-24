django-flow
==============

This framework allow to create bidirectional real time (or not) pipeline between client browsers and server application.
Through a robuste redis connection, the connected mode works only with uwsgi and browsers compatible with websockets.
The disconnected mode works with all configuration.
The framework can be configured to allow or disallow both of them.
If connected mode and disconnected mode are actived and the browser doesn't accept websockets, the disconnected mode is used by default.
If connected mode is the one actived and the browser doesn't accept websockets, the frameworks doesn't not work and be silent.
If disconnected mode is the one actived, it's works without websocket and they will never be used.

## Installation

1. Install `django_flow`

        pip install django-flow

2. Add `django_flow` to your `INSTALLED_APPS` in your project settings.

3. Add `django_flow` to your urlconf if you use disconnected mode.

        url(r'^what_ever_you_want/', include('django_flow.urls')),

4. Optionnaly add `django_flow`  to your urlconf if you use disconnected mode.

        url(r'^what_ever_you_want/', include('django_flow.urls')),

Usage
=====

Add ``'flow'`` to your INSTALLED_APPS



