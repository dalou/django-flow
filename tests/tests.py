from __future__ import absolute_import, unicode_literals

from unittest import TestCase as UnitTestCase

import django
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import connection
from django.test import TestCase, TransactionTestCase
from django.test.utils import override_settings
from django.utils.encoding import force_text