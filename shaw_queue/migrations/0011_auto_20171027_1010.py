# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-27 05:10


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0010_menucategory_weidht'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menucategory',
            old_name='weidht',
            new_name='weight',
        ),
    ]