# Generated by Django 3.2.4 on 2022-11-21 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shaw_queue', '0060_cookingtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='cookingtime',
            name='default',
            field=models.BooleanField(default=True, verbose_name='по умолчанию'),
        ),
    ]