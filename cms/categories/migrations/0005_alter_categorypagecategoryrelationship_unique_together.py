# Generated by Django 3.2.12 on 2022-03-29 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0004_alter_category_slug'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='categorypagecategoryrelationship',
            unique_together={('category_page', 'category')},
        ),
    ]
