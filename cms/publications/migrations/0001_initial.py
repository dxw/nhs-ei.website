# Generated by Django 3.1.2 on 2020-11-16 15:31

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0052_pagelogentry'),
        ('categories', '0008_publicationtype_publicationtypesubsite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('wp_id', models.PositiveSmallIntegerField(null=True)),
                ('source', models.CharField(max_length=100, null=True)),
                ('author', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PublicationPublicationTypeRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='categories.publicationtype')),
                ('publication', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='publication_publication_type_relationship', to='publications.publication')),
            ],
        ),
        migrations.CreateModel(
            name='PublicationIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('sub_site_publication_types', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='publication_type_sub_site', to='categories.publicationtypesubsite')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]