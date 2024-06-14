# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-09-23 05:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0030_auto_20180827_1716'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pausetracker',
            options={'permissions': (('view_statistics', 'User can view statistics pages.'),)},
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(default='Name not set', max_length=30, null=True, verbose_name='имя'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='note',
            field=models.CharField(blank=True, max_length=200, verbose_name='комментарий'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=20, verbose_name='телефон'),
        ),
        migrations.AlterField(
            model_name='deliveryorder',
            name='address',
            field=models.CharField(default='Address not set', max_length=250, verbose_name='адрес'),
        ),
        migrations.AlterField(
            model_name='deliveryorder',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shaw_queue.Customer', verbose_name='клиент'),
        ),
        migrations.AlterField(
            model_name='deliveryorder',
            name='delivered_timepoint',
            field=models.DateTimeField(blank=True, null=True, verbose_name='время доставки заказа'),
        ),
        migrations.AlterField(
            model_name='deliveryorder',
            name='delivery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shaw_queue.Delivery', verbose_name='доставка'),
        ),
        migrations.AlterField(
            model_name='deliveryorder',
            name='delivery_duration',
            field=models.DurationField(blank=True, default=datetime.timedelta(0), null=True, verbose_name='продолжительность доставки'),
        ),
        migrations.AlterField(
            model_name='deliveryorder',
            name='note',
            field=models.CharField(blank=True, help_text='Введите комментарий к заказу.', max_length=250, null=True, verbose_name='комментарий'),
        ),
        migrations.AlterField(
            model_name='deliveryorder',
            name='obtain_timepoint',
            field=models.DateTimeField(blank=True, null=True, verbose_name='время получения заказа'),
        ),
        migrations.AlterField(
            model_name='deliveryorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shaw_queue.Order', verbose_name='включеный заказ'),
        ),
        migrations.AlterField(
            model_name='deliveryorder',
            name='prep_start_timepoint',
            field=models.DateTimeField(blank=True, null=True, verbose_name='время начала готовки'),
        ),
        migrations.AlterField(
            model_name='deliveryorder',
            name='preparation_duration',
            field=models.DurationField(blank=True, default=datetime.timedelta(0), null=True, verbose_name='продолжительность готовки'),
        ),
    ]