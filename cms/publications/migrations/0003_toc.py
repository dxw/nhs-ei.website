# Generated by Django 3.2.12 on 2022-03-30 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('publications', '0002_auto_20210825_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='TOC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anchor', models.TextField()),
                ('text', models.TextField()),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toc', to='wagtailcore.page')),
            ],
        ),
    ]
