# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 01:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0002_auto_20171027_0131'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='Joe', max_length=255),
            preserve_default=False,
        ),
    ]