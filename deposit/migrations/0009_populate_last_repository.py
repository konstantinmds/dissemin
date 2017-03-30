# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 19:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations

def do_nothing(apps, schema):
    pass

def populate_prefs(apps, schema):
    """
    Prefill user preferences with the last deposits made
    by a user
    """
    DepositRecord = apps.get_model('deposit', 'DepositRecord')
    UserPreferences = apps.get_model('deposit', 'UserPreferences')
    for record in DepositRecord.objects.all().order_by('date'):
        user = record.user
        userprefs, _ = UserPreferences.objects.get_or_create(user=user)
        userprefs.last_repository = record.repository
        userprefs.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deposit', '0008_userpreferences'),
    ]

    operations = [
        migrations.RunPython(populate_prefs, do_nothing),
    ]
