# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-02 18:22


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0011_auto_20171027_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='prepared_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='maker', to='shaw_queue.Staff'),
        ),
    ]
