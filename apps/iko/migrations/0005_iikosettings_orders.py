# Generated by Django 3.2.4 on 2025-02-05 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iko', '0004_ikoorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='iikosettings',
            name='orders',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
