# Generated by Django 3.2.12 on 2022-03-28 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('pages', '0004_auto_20210825_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='TOC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anchor', models.TextField()),
                ('text', models.TextField()),
                ('page_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toc', to='wagtailcore.page')),
            ],
        ),
    ]