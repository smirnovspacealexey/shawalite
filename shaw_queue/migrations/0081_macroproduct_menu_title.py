# Generated by Django 3.2.4 on 2023-11-06 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0080_auto_20231106_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='macroproduct',
            name='menu_title',
            field=models.CharField(default='', max_length=200, verbose_name='Название для меню'),
        ),
    ]