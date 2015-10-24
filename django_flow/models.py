# encoding: utf-8

from . import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import formats
from django.contrib.auth import get_user_model
# encoding: utf-8

from .signals import flow_user_disconnected
from .pipe import send



class StaffNotification(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, db_index=True)

    title = models.CharField("Title", max_length=254)
    body = models.TextField("Body", null=True, blank=True)

    class Meta:
        ordering = ('-date_created', )

    def to_json(self, extra={}):
        json = {
            'pk': self.pk,
            "created_date": formats.date_format(self.date_created, "SHORT_DATETIME_FORMAT"),
            "title": self.title,
            "body": self.body,
        }
        json.update(extra)
        return json

"""
LISTENED APP EVENTS BY FLOW
"""
@receiver(post_save, sender=StaffNotification)
def handle_staff_notification_post_save(sender, instance, created, **kwargs):
    if created:
        User = get_user_model()
        users = list(set(User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).values_list("pk", flat=True)))

        send('staff_notification_created', instance.to_json(), users=users)
    # else:
    #     send('staff_notification_changed', instance.to_json(), users=users)