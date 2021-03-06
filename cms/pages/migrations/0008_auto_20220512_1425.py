# Generated by Django 3.2.13 on 2022-05-12 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_delete_toc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basepage',
            name='md_gateway_ref',
        ),
        migrations.RemoveField(
            model_name='basepage',
            name='md_pac_reference',
        ),
        migrations.AddField(
            model_name='basepage',
            name='md_pac_reference',
            field=models.TextField(blank=True, verbose_name='PAC Reference'),
        ),
        migrations.AlterField(
            model_name='basepage',
            name='md_description',
            field=models.TextField(blank=True, verbose_name='Description of content'),
        ),
        migrations.AlterField(
            model_name='basepage',
            name='md_owner',
            field=models.TextField(blank=True, verbose_name='Content Owner'),
        ),
    ]
