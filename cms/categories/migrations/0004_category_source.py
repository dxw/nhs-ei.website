# Generated by Django 3.1.2 on 2020-10-21 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_category_wp_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='source',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
