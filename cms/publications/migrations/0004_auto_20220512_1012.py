# Generated by Django 3.2.13 on 2022-05-12 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0003_toc'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='md_description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='publication',
            name='md_gateway_ref',
            field=models.TextField(blank=True, verbose_name='Gateway Ref'),
        ),
        migrations.AddField(
            model_name='publication',
            name='md_owner',
            field=models.TextField(blank=True, verbose_name='Owner'),
        ),
        migrations.AddField(
            model_name='publication',
            name='md_pac_reference',
            field=models.TextField(blank=True, verbose_name='PCC Reference'),
        ),
    ]
