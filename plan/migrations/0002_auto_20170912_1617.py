# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 14:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 9, 12, 14, 17, 38, 266144, tzinfo=utc)),
        ),
    ]
