# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-23 17:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0003_auto_20170912_1618'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='season_id',
            new_name='parent_season',
        ),
        migrations.RenameField(
            model_name='planweek',
            old_name='plan_id',
            new_name='parent_plan',
        ),
        migrations.RenameField(
            model_name='planweekday',
            old_name='week_id',
            new_name='parent_week',
        ),
        migrations.RenameField(
            model_name='race',
            old_name='season_id',
            new_name='parent_season',
        ),
        migrations.RenameField(
            model_name='season',
            old_name='user_id',
            new_name='parent_user',
        ),
        migrations.AlterField(
            model_name='plan',
            name='planEnd',
            field=models.DateField(default=datetime.date(2018, 9, 22), verbose_name='End of Plan'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='planStart',
            field=models.DateField(default=datetime.date(2017, 9, 23), verbose_name='Start of Plan'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='strong1',
            field=models.CharField(choices=[('Endurance', 'Endurance'), ('Force', 'Force'), ('Speed Skills', 'Speed Skills'), ('Endurance Force', 'Endurance Force'), ('Anaerobic Endurance', 'Anaerobic Endurance'), ('Maximum Power', 'Maximum Power')], default='endurance', max_length=30, verbose_name='Strongest skill'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='strong2',
            field=models.CharField(choices=[('Endurance', 'Endurance'), ('Force', 'Force'), ('Speed Skills', 'Speed Skills'), ('Endurance Force', 'Endurance Force'), ('Anaerobic Endurance', 'Anaerobic Endurance'), ('Maximum Power', 'Maximum Power')], default='endurance', max_length=30, verbose_name='Second strongest skill'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weak1',
            field=models.CharField(choices=[('Endurance', 'Endurance'), ('Force', 'Force'), ('Speed Skills', 'Speed Skills'), ('Endurance Force', 'Endurance Force'), ('Anaerobic Endurance', 'Anaerobic Endurance'), ('Maximum Power', 'Maximum Power')], default='endurance', max_length=30, verbose_name='Weakest skills'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weak2',
            field=models.CharField(choices=[('Endurance', 'Endurance'), ('Force', 'Force'), ('Speed Skills', 'Speed Skills'), ('Endurance Force', 'Endurance Force'), ('Anaerobic Endurance', 'Anaerobic Endurance'), ('Maximum Power', 'Maximum Power')], default='endurance', max_length=30, verbose_name='Second weakest skill'),
        ),
        migrations.AlterField(
            model_name='race',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 9, 23, 17, 35, 54, 195660, tzinfo=utc)),
        ),
    ]
