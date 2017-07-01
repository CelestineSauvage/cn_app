# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-29 07:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('git_url', models.URLField(unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('git_name', models.CharField(blank=True, max_length=200, null=True)),
                ('git_username', models.CharField(blank=True, max_length=200, null=True)),
                ('default_branch', models.CharField(blank=True, default='master', max_length=200, null=True)),
                ('last_compiled', models.DateTimeField(blank=True, null=True)),
                ('repo_synced', models.BooleanField(default=False)),
                ('show_feedback', models.BooleanField(default=False)),
                ('provider', models.URLField(blank=True, null=True)),
            ],
        ),
    ]