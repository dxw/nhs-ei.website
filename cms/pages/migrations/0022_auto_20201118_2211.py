# Generated by Django 3.1.2 on 2020-11-18 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0021_auto_20201118_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='basepage',
            name='component_fields',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='basepage',
            name='content_field_block',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='basepage',
            name='content_fields',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='basepage',
            name='model_fields',
            field=models.TextField(blank=True, null=True),
        ),
    ]