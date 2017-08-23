# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-01 16:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0004_auto_20170801_1743'),
    ]

    operations = [
        migrations.RenameField(
            model_name='race',
            old_name='seaon_id',
            new_name='season_id',
        ),
        migrations.AlterField(
            model_name='plan',
            name='annualHours',
            field=models.PositiveIntegerField(default=200, verbose_name='Annual hours'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='planEnd',
            field=models.DateField(default=datetime.date(2018, 7, 31), verbose_name='End of Plan'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='planStart',
            field=models.DateField(default=datetime.date(2017, 8, 1), verbose_name='Start of Plan'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='typeOfPlan',
            field=models.CharField(choices=[('normal', 'Normal'), ('reversed', 'Reversed')], default='normal', max_length=20, verbose_name='Type of Plan'),
        ),
        migrations.AlterField(
            model_name='race',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 8, 1, 16, 21, 40, 349932, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='race',
            name='name',
            field=models.CharField(default='', max_length=80),
        ),
        migrations.AlterField(
            model_name='race',
            name='priority',
            field=models.PositiveIntegerField(choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High')], default='1', verbose_name='Priority'),
        ),
        migrations.AlterField(
            model_name='race',
            name='time',
            field=models.TimeField(verbose_name=datetime.time(0, 0)),
        ),
        migrations.AlterField(
            model_name='season',
            name='year',
            field=models.PositiveIntegerField(default=2017, verbose_name='Season'),
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(default=18, verbose_name='Age'),
        ),
        migrations.AlterField(
            model_name='user',
            name='cp60',
            field=models.PositiveIntegerField(default=100, verbose_name='CP60 (W)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='maxHR',
            field=models.PositiveIntegerField(default=180, verbose_name='Maximum Heart Rate (bpm)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='strong1',
            field=models.CharField(choices=[('endurance', 'Endurance'), ('force', 'Force'), ('speedSkills', 'Speed Skills'), ('eForce', 'Endurance Force'), ('aEndurance', 'Anaerobic Endurance'), ('maxPower', 'Maximum Power')], default='endurance', max_length=30, verbose_name='Strongest skill'),
        ),
        migrations.AlterField(
            model_name='user',
            name='strong2',
            field=models.CharField(choices=[('endurance', 'Endurance'), ('force', 'Force'), ('speedSkills', 'Speed Skills'), ('eForce', 'Endurance Force'), ('aEndurance', 'Anaerobic Endurance'), ('maxPower', 'Maximum Power')], default='endurance', max_length=30, verbose_name='Second strongest skill'),
        ),
        migrations.AlterField(
            model_name='user',
            name='weak1',
            field=models.CharField(choices=[('endurance', 'Endurance'), ('force', 'Force'), ('speedSkills', 'Speed Skills'), ('eForce', 'Endurance Force'), ('aEndurance', 'Anaerobic Endurance'), ('maxPower', 'Maximum Power')], default='endurance', max_length=30, verbose_name='Weakest skills'),
        ),
        migrations.AlterField(
            model_name='user',
            name='weak2',
            field=models.CharField(choices=[('endurance', 'Endurance'), ('force', 'Force'), ('speedSkills', 'Speed Skills'), ('eForce', 'Endurance Force'), ('aEndurance', 'Anaerobic Endurance'), ('maxPower', 'Maximum Power')], default='endurance', max_length=30, verbose_name='Second weakest skill'),
        ),
        migrations.AlterField(
            model_name='user',
            name='yearsOfExperience',
            field=models.PositiveIntegerField(default=0, verbose_name='Years of Experience'),
        ),
    ]
