# Generated by Django 3.2.4 on 2023-05-25 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sber', '0002_sbersettings_callback_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sbersettings',
            name='callback_token',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]