# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-06-23 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20160406_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='items',
            field=models.ManyToManyField(related_name='menu', to='menu.Item'),
        ),
    ]
