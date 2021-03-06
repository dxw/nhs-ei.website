# Generated by Django 3.2.12 on 2022-03-03 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0012_uploadeddocument'),
        ('wagtailimages', '0023_add_choose_permissions'),
        ('core', '0002_extendedmainmenuitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageImportBridge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wp_id', models.CharField(max_length=32)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailimages.image')),
            ],
        ),
        migrations.CreateModel(
            name='DocImportBridge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wp_id', models.CharField(max_length=32)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtaildocs.document')),
            ],
        ),
    ]
