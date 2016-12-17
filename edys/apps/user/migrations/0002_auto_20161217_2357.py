# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2016-12-17 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAssignedEditor',
            fields=[
            ],
            options={
                'verbose_name': 'Editor',
                'proxy': True,
                'verbose_name_plural': 'Editors',
            },
            bases=('user.user',),
        ),
        migrations.CreateModel(
            name='UserDefault',
            fields=[
            ],
            options={
                'verbose_name': 'Default',
                'proxy': True,
                'verbose_name_plural': 'Defaults',
            },
            bases=('user.user',),
        ),
        migrations.CreateModel(
            name='UserEditor',
            fields=[
            ],
            options={
                'verbose_name': 'Editor',
                'proxy': True,
                'verbose_name_plural': 'Editors',
            },
            bases=('user.user',),
        ),
        migrations.CreateModel(
            name='UserReviewer',
            fields=[
            ],
            options={
                'verbose_name': 'Reviewer',
                'proxy': True,
                'verbose_name_plural': 'Reviewers',
            },
            bases=('user.user',),
        ),
        migrations.AddField(
            model_name='user',
            name='is_assigned_editor',
            field=models.BooleanField(default=False, verbose_name='Assigned Editor'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_editor',
            field=models.BooleanField(default=False, verbose_name='Editor'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_reviewer',
            field=models.BooleanField(default=False, verbose_name='Reviewer'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Default'), (1, 'Editor'), (2, 'Assigned Editor'), (3, 'Reviewer')], default=0, verbose_name='User Type'),
        ),
    ]
