import logging
import time
from abc import ABC

from dateutil import parser
from wagtail.core.models import Page

from cms.categories.models import (
    PublicationType,
)
from cms.pages.models import BasePage
from cms.publications.models import (
    Publication,
    PublicationIndexPage,
    PublicationPublicationTypeRelationship,
)
from .importer_cls import Importer

from importer.utils import ImportCategoryMapper, create_category_relationships_for_page

logger = logging.getLogger("importer")

FAKE_SOURCE = "publications"

# so we can add publication to a sub site and build out sub site publication
# index pages
PUBLICATION_SOURCES = {
    "publications": "NHS England & Improvement",
    "publications-aac": "Accelerated Access Collaborative",
    "publications-commissioning": "Commissioning",
    "publications-coronavirus": "Coronavirus",
    "publications-greenernhs": "Greener NHS",
    "publications-improvement-hub": "Improvement Hub",
    "publications-non-executive-opportunities": "Non-executive opportunities",
    "publications-rightcare": "Right Care",
    "publications-north-east-yorkshire": "North East and Yorkshire",
    "publications-south": "South West",
    "publications-london": "London",
    "publications-east-of-england": "East of England",
    "publications-midlands": "Midlands",
    "publications-north-west": "North West",
    "publications-south-east": "South East",
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


class PublicationsImporter(Importer, ABC):

    category_mapper = ImportCategoryMapper()

    def __init__(self):
        super().__init__()
        publications = Publication.objects.all()
        for page in publications:
            self.cache[page.wp_id] = page

        # lets make a publication index page if not already in place
        try:
            # we need a pretty unique name here as some imported page have
            # the title as News
            # a parent for all publication item index pages
            self.publications_index_page = BasePage.objects.get(
                title="Publication Items Base"
            )
        except Page.DoesNotExist:
            self.publications_index_page = BasePage(
                title="Publication Items Base",
                body="theres a place here for some text",
                show_in_menus=True,
                slug="publication-items-base",
                wp_slug="auto-generated-publications-index",
                wp_id=0,
                source=FAKE_SOURCE,
            )

            self.staging_page.add_child(instance=self.publications_index_page)
            revision = self.publications_index_page.save_revision()
            revision.publish()
            logger.info("Created publications_index_page")

    def parse_results(self):
        # make a posts index page for the whole site, only one to exist,
        # call is News ...
        publications = self.results

        for publication in publications:
            # we need a sub_site_category to choose the publication types and
            # categories

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
                self.publications_index_page.add_child(
                    instance=sub_site_publication_index_page
                )
                rev = sub_site_publication_index_page.save_revision()
                rev.publish()
                logger.debug(
                    "Created PublicationIndexPage title=%s"
                    % PUBLICATION_SOURCES[FAKE_SOURCE]
                )

            # lets make the posts for each sub site, we're in a loop for each
            # post here

            page_title = publication.get("title")
            if not page_title:
                page_title = "page has no title"
                logger.warning("page %s has no title", publication)
            elif len(page_title) > 250:
                logger.warning("long page title: %s %s", page_title, publication)
                page_title = page_title[:250] + "..."

            modified = publication.get("modified")
            modified_time = parser.parse(modified)
            wp_id = int(publication.get("wp_id"))

            # cheap check first, is the file too old to be considered
            if self.check_is_too_old(modified_time, wp_id):
                continue

            is_new = False

            if wp_id in self.cache:
                obj = self.cache[wp_id]
            else:
                obj = Publication(wp_id=wp_id, show_in_menus=True, source=FAKE_SOURCE)
                obj.first_published_at = publication.get("date")
                is_new = True

            self("title", page_title, obj)
            self("body", "", obj)
            self("author", publication.get("author"), obj)
            self("wp_slug", publication.get("slug"), obj)
            self("wp_link", publication.get("link"), obj)
            self("component_fields", publication.get("component_fields"), obj)
            self("first_published_at", publication.get("date"), obj)
            self("last_published_at", publication.get("modified"), obj)
            self("latest_revision_created_at", publication.get("modified"), obj)

            if is_new:
                sub_site_publication_index_page.add_child(instance=obj)
                logger.debug(
                    "Imported Publication wp_id=%d, title=%s" % (obj.wp_id, obj.title)
                )
            else:
                logger.debug(
                    "Updated Publication wp_id=%d, title=%s" % (obj.wp_id, obj.title)
                )

            self.save(obj)

            # add the publication types as related many to many, found this
            # needs to be after the save above
            # some publication types can be blank
            if publication.get("publication_type"):

                types = publication.get("publication_type").split(
                    " "
                )  # list of category wp_id's

                publication_types = PublicationType.objects.filter(wp_id__in=types)

                for publication_type in publication_types:
                    PublicationPublicationTypeRelationship.objects.create(
                        publication=obj, publication_type=publication_type
                    )

                logger.debug("Associated publication with %s" % publication_types)

            source = publication.get("source")

            # add the categories (topics) as related many to many, found this
            # needs to be after the save above
            # some categories can be blank

            if publication.get("categories") and is_new:

                category_ids = publication.get("categories").split(
                    " "
                )  # list of category wp_id's

                for category_id in category_ids:

                    mapped_categories = (
                        self.category_mapper.get_mapped_categories_for_type_by_id(
                            PUBLICATION_SOURCES_TO_CATEGORY_SOURCES[source], category_id
                        )
                    )
                    create_category_relationships_for_page(obj, mapped_categories)

                logger.debug("Set categories to %s" % category_ids)

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Publication.objects.count(), self.count
