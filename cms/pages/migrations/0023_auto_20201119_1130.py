# Generated by Django 3.1.2 on 2020-11-19 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0022_auto_20201118_2211'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basepage',
            old_name='content_field_block',
            new_name='content_field_blocks',
        ),
    ]
