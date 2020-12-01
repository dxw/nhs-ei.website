# Generated by Django 3.1.2 on 2020-10-18 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_toppage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basepage',
            name='parent',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='basepage',
            name='wp_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='toppage',
            name='parent',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='toppage',
            name='wp_id',
            field=models.IntegerField(null=True),
        ),
    ]