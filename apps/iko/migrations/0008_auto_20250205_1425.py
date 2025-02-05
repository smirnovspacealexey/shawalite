# Generated by Django 3.2.4 on 2025-02-05 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iko', '0007_auto_20250205_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iikosettings',
            name='last_getting_live',
            field=models.IntegerField(default=20000, verbose_name='время выжидания между запросами к iko'),
        ),
        migrations.AlterField(
            model_name='iikosettings',
            name='last_update_token_live',
            field=models.IntegerField(default=1800000, verbose_name='время жизни тоенна в миллисекундах'),
        ),
    ]
