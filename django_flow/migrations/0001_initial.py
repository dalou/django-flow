# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaffNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('title', models.CharField(max_length=254, verbose_name=b'Title')),
                ('body', models.TextField(null=True, verbose_name=b'Body', blank=True)),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
    ]
