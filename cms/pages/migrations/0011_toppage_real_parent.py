# Generated by Django 3.1.2 on 2020-10-22 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_basepage_wp_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='toppage',
            name='real_parent',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]