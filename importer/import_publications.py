import sys
import time
from urllib.parse import urlparse
import logging

from django.core.management import call_command
from django.utils.html import strip_tags
from cms.categories.models import (
    Category,
    PublicationType,
    CategoryPageCategoryRelationship,
)
from cms.pages.models import BasePage
from cms.publications.models import (
    Publication,
    PublicationIndexPage,
    PublicationPublicationTypeRelationship,
)
from wagtail.core.models import Page

from .importer_cls import Importer

logger = logging.getLogger("importer")

FAKE_SOURCE = "publications"

# so we can match the subsite categories for the publication index page
PUBLICATION_SOURCES_TO_PUBLICATION_TYPE_SOURCES = {
    "publications": "publication_types",
    "publications-aac": "publication_types-aac",
    "publications-commissioning": "publication_types-commissioning",
    "publications-coronavirus": "publication_types-coronavirus",
    "publications-greenernhs": "publication_types-greenernhs",
    "publications-improvement-hub": "publication_types-improvement-hub",
    "publications-non-executive-opportunities": "publication_types-non-executive-opportunities",
    "publications-rightcare": "publication_types-rightcare",
}

# so we can add publication to a sub site and build out sub site publication index pages
PUBLICATION_SOURCES = {
    "publications": "NHS England & Improvement",
    "publications-aac": "Accelerated Access Collaborative",
    "publications-commissioning": "Commissioning",
    "publications-coronavirus": "Coronavirus",
    "publications-greenernhs": "Greener NHS",
    "publications-improvement-hub": "Improvement Hub",
    "publications-non-executive-opportunities": "Non-executive opportunities",
    "publications-rightcare": "Right Care",
}

# so we can match the subsite categories for the publications pages
PUBLICATION_SOURCES_TO_CATEGORY_SOURCES = {
    "publications": "categories",
    "publications-aac": "categories-aac",
    "publications-commissioning": "categories-commissioning",
    "publications-coronavirus": "categories-coronavirus",
    "publications-greenernhs": "categories-greenernhs",
    "publications-improvement-hub": "categories-improvement-hub",
    "publications-non-executive-opportunities": "categories-non-executive-opportunities",
    "publications-rightcare": "categories-rightcare",
}


class PublicationsImporter(Importer):
    def __init__(self):
        publications = Publication.objects.all()
        if publications:
            sys.stdout.write(
                "⚠️  Run delete_publications before running this command\n"
            )
            sys.exit()

    def parse_results(self):
        # make a posts index page for the whole site, only one to exist, call is News ...
        publications = self.results
        home_page = Page.objects.filter(title="Home")[0]

        for publication in publications:
            # we need a sub_site_category to choose the publication types and categories
            source = publication.get("source")

            # lets make a publication index page if not already in place
            try:
                # we need a pretty unique name here as some imported page have the title as News
                # a parent for all publication item index pages
                publications_index_page = BasePage.objects.get(
                    title="Publication Items Base"
                )
            except Page.DoesNotExist:
                publications_index_page = BasePage(
                    title="Publication Items Base",
                    body="theres a place here for some text",
                    show_in_menus=True,
                    slug="publication-items-base",
                    wp_slug="auto-generated-publications-index",
                    wp_id=0,
                    source=FAKE_SOURCE,
                )
                home_page.add_child(instance=publications_index_page)
                revision = publications_index_page.save_revision()
                revision.publish()
                sys.stdout.write(".")

            try:
                sub_site_publication_index_page = PublicationIndexPage.objects.get(
                    title=PUBLICATION_SOURCES[FAKE_SOURCE]
                )
            except PublicationIndexPage.DoesNotExist:
                sub_site_publication_index_page = PublicationIndexPage(
                    title=PUBLICATION_SOURCES[FAKE_SOURCE],
                    body="",
                    show_in_menus=True,
                )
                publications_index_page.add_child(
                    instance=sub_site_publication_index_page
                )
                rev = sub_site_publication_index_page.save_revision()
                rev.publish()
                sys.stdout.write(".")

            # lets make the posts for each sub site, we're in a loop for each post here
            first_published_at = publication.get("date")
            last_published_at = publication.get("modified")
            latest_revision_created_at = publication.get("modified")

            page_title = publication.get("title")
            if not page_title:
                page_title = "page has no title"
                logger.warn("page %s has no title", publication)
            elif len(page_title) > 250:
                logger.warn("long page title: %s %s", page_title, publication)
                page_title = page_title[:250] + "..."
            obj = Publication(
                title=page_title,
                # excerpt = post.get('excerpt'),
                # dont preset the slug coming from wordpress some are too long
                body="",  # TODO populate later from field_57ed4101bec1c
                show_in_menus=True,
                wp_id=publication.get("wp_id"),
                author=publication.get("author"),
                wp_slug=publication.get("slug"),
                wp_link=publication.get("link"),
                component_fields=publication.get("component_fields"),
                source=FAKE_SOURCE,
            )
            sub_site_publication_index_page.add_child(instance=obj)
            rev = obj.save_revision()  # this needs to run here
            rev.publish()

            obj.first_published_at = first_published_at
            obj.last_published_at = last_published_at
            obj.latest_revision_created_at = latest_revision_created_at
            obj.save()
            rev.publish()
            sys.stdout.write(".")

            # add the publication types as related many to many, found this needs to be after the save above
            # some publication types can be blank
            if publication.get("publication_type"):

                types = publication.get("publication_type").split(
                    " "
                )  # list of category wp_id's

                publication_types = PublicationType.objects.filter(wp_id__in=types)

                for publication_type in publication_types:
                    rel = PublicationPublicationTypeRelationship.objects.create(
                        publication=obj, publication_type=publication_type
                    )

                sys.stdout.write(".")

            # Create source category
            source = publication.get("source")
            if source:
                source_category, _ = Category.objects.get_or_create(
                    name=f"source: {source}",
                    description=f"Content from the {source} subsite",
                    wp_id=None,
                    source=None,
                )
            CategoryPageCategoryRelationship.objects.create(
                category_page=obj, category=source_category
            )

            # add the categories (topics) as related many to many, found this needs to be after the save above
            # some categories can be blank

            if publication.get("categories"):

                category_id = publication.get("categories").split(
                    " "
                )  # list of category wp_id's

                for category in category_id:
                    # find matching category on id and sub_site
                    category_object = Category.objects.get(
                        source=PUBLICATION_SOURCES_TO_CATEGORY_SOURCES[source],
                        wp_id=int(category),
                    )

                    CategoryPageCategoryRelationship.objects.create(
                        category_page=obj, category=category_object
                    )

                sys.stdout.write(".")

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Publication.objects.count(), self.count
