# Generated by Django 3.1.2 on 2020-10-21 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_basepage_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basepage',
            name='template',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
