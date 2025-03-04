# Generated by Django 3.2.4 on 2025-02-05 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iko', '0006_iikosettings_last_update_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='iikosettings',
            name='last_getting_live',
            field=models.IntegerField(default=1, verbose_name='время выжидания между запросами к iko'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='iikosettings',
            name='last_update_token_live',
            field=models.IntegerField(default=1, verbose_name='время жизни тоенна в миллисекундах'),
            preserve_default=False,
        ),
    ]
