# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-02 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issueview', '0002_auto_20161202_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='repository',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
