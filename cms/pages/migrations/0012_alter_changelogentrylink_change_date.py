# Generated by Django 3.2.13 on 2022-05-19 10:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_changelogentrylink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changelogentrylink',
            name='change_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='When the changes were made'),
        ),
    ]
