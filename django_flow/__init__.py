default_app_config = 'django_flow.DefaultConfig'

from django.apps import AppConfig

class DefaultConfig(AppConfig):
    name = 'django_flow'
    verbose_name = u"Flow"

    user_presence = {}

    def ready(self):

        from . import signals
        from . import models


