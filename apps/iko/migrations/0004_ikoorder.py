# Generated by Django 3.2.4 on 2025-01-28 09:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('iko', '0003_iikosettings_last_getting'),
    ]

    operations = [
        migrations.CreateModel(
            name='IkoOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ikoid', models.CharField(blank=True, max_length=200, null=True)),
                ('number', models.CharField(blank=True, max_length=200, null=True)),
                ('is_voiced', models.BooleanField(default=False, verbose_name='Is Voiced')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата, время')),
            ],
        ),
    ]
