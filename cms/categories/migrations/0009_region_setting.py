# Generated by Django 3.1.2 on 2020-11-17 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0008_publicationtype_publicationtypesubsite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True)),
                ('wp_id', models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True)),
                ('wp_id', models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                'verbose_name': 'Setting',
                'verbose_name_plural': 'Settings',
                'ordering': ['name'],
            },
        ),
    ]
