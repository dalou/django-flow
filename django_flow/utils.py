
# encoding: utf-8

import datetime
import operator

from django.db import models
from django.db.models import Q
from django.contrib import auth, messages
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from .models import *
from . import settings

def create_staff_notification(title, body=None, email_receivers=[], send_emails=True):

    StaffNotification.objects.create(
        title=title,
        body=body,
    )

    if not email_receivers:
        email_receivers = settings.settings.STAFF_EMAILS.values()

    send_templated_mail(
        u'[STAFF] %s' % title,
        settings.settings.DEFAULT_NO_REPLY_EMAIL,
        email_receivers,
        template="django_flow/admin/email/staff_notification.html",
        context= {
            'title': title,
            'body': body,
        }
    )

class HtmlTemplateEmail(EmailMultiAlternatives):

    def __init__(self, subject, html, sender, receivers, context={}, **kwargs):
        if type(receivers) == type(str()) or type(receivers) == type(unicode()):
            receivers = [receivers]

        text_template = strip_tags(html)
        super(HtmlTemplateEmail, self).__init__(subject, text_template, sender, receivers, **kwargs)
        self.attach_alternative(html, "text/html")


def send_html_mail(subject, sender, receivers, html='', context={}, **kwargs):
    message = HtmlTemplateEmail(subject, html, sender, receivers, context, **kwargs)
    return message.send()

def send_templated_mail(subject, sender, receivers, template=None, context={}, **kwargs):
    html_template = get_template(template)
    context = Context(context)
    html = html_template.render(context)
    return send_html_mail(subject, sender, receivers, html=html, context=context, **kwargs)


