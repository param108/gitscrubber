# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-07 13:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issueview', '0005_auto_20161207_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issueview.Board'),
        ),
        migrations.AlterField(
            model_name='repository',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issueview.Board'),
        ),
    ]