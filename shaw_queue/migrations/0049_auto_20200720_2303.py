# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2020-07-20 18:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0048_auto_20200720_2244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productoption',
            name='product_variant',
        ),
        migrations.AddField(
            model_name='productoption',
            name='product_variants',
            field=models.ManyToManyField(to='shaw_queue.ProductVariant', verbose_name='Вариант товара'),
        ),
    ]
