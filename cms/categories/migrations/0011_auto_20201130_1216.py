# Generated by Django 3.1.3 on 2020-11-30 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0010_auto_20201130_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='wp_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]