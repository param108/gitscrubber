# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-07 14:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issueview', '0008_readpermissions_writepermissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='user',
        ),
    ]