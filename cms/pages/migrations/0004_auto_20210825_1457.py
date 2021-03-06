# Generated by Django 3.1.13 on 2021-08-25 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20210825_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basepage',
            name='source',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='basepage',
            name='wp_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='basepage',
            name='wp_slug',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='componentspage',
            name='source',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='componentspage',
            name='wp_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='componentspage',
            name='wp_slug',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='source',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='wp_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='wp_slug',
            field=models.TextField(blank=True, null=True),
        ),
    ]
