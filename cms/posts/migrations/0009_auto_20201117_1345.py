# Generated by Django 3.1.2 on 2020-11-17 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20201029_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='wp_link',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='wp_slug',
            field=models.TextField(blank=True, null=True),
        ),
    ]
