# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-02 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escapad_formulaire', '0003_auto_20170502_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='projet',
            name='url_home',
            field=models.CharField(default='default', max_length=30),
            preserve_default=False,
        ),
    ]
