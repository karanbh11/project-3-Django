# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_commentmodel_likemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='session_token',
            name='last_request_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
