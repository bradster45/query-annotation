# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-06 11:12
from __future__ import unicode_literals

from django.db import migrations
import public.models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hit',
            name='rating',
            field=public.models.RangeField(null=True),
        ),
    ]