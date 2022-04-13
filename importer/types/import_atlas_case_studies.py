import logging
import time
from abc import ABC

from dateutil import parser
from wagtail.core.models import Page

from cms.publications.models import (
    Publication,
    PublicationIndexPage,
)
from .importer_cls import Importer

from importer.utils import ImportCategoryMapper, create_category_relationships_for_page

logger = logging.getLogger("importer")


class AtlasCaseStudiesImporter(Importer, ABC):
    atlas_case_study_index_page = None

    category_mapper = ImportCategoryMapper()

    def __init__(self):
        super().__init__()
        atlas_case_studies = Publication.objects.all()
        for case in atlas_case_studies:
            self.cache[case.wp_id] = case

        # make an atlas case study index page for the whole site, only one to
        # exist ...

        try:
            # a parent for all atlas case study pages
            self.atlas_case_study_index_page = PublicationIndexPage.objects.get(
                title="Atlas Case Study Items Base"
            )
        except Page.DoesNotExist:
            self.atlas_case_study_index_page = PublicationIndexPage(
                title="Atlas Case Study Items Base",
                body="theres a place here for some text",
                show_in_menus=True,
                slug="atlas-case-study-items-base",
            )
            self.home_page.add_child(instance=self.atlas_case_study_index_page)
            revision = self.atlas_case_study_index_page.save_revision()
            revision.publish()
            logger.info("Created Atlas Case Study Items Base")

    def parse_results(self):
        atlas_case_studies = self.results

        atlas_categories = [
            self.category_mapper.get_category_for_slug("atlas"),
            self.category_mapper.get_category_for_slug("nursing"),
        ]

        imported_count = 0

        for atlas_case_study in atlas_case_studies:

            imported_count = imported_count + 1

            modified = atlas_case_study.get("modified")
            modified_time = parser.parse(modified)
            wp_id = int(atlas_case_study.get("wp_id"))

            # cheap check first, is the file too old to be considered
            if self.check_is_too_old(modified_time, wp_id):
                continue

            is_new = False

            if wp_id in self.cache:
                obj = self.cache[wp_id]
            else:

                obj = Publication(wp_id=wp_id, show_in_menus=True)
                obj.first_published_at = atlas_case_study.get("date")
                is_new = True

            page_title = atlas_case_study.get("title")
            if not page_title:
                page_title = "page has no title"
                logger.warning(
                    "Page with wp_id %s has no title", atlas_case_study.get("wp_id")
                )
            elif len(page_title) > 250:
                logger.warning("Long page_title, %s", page_title)

            self("title", page_title, obj)
            self("body", atlas_case_study.get("content"), obj)
            self("wp_slug", atlas_case_study.get("slug"), obj)
            self("wp_link", atlas_case_study.get("link"), obj)
            self("last_published_at", atlas_case_study.get("modified"), obj)
            self("latest_revision_created_at", atlas_case_study.get("modified"), obj)

            if is_new:
                self.atlas_case_study_index_page.add_child(instance=obj)
                logger.debug(
                    "Created Publication, wp_id=%s, title=%s" % (obj.wp_id, obj.title)
                )
            else:
                logger.debug(
                    "Updated Publication, wp_id=%s, title=%s" % (obj.wp_id, obj.title)
                )

            self.save(obj)

            if is_new:

                # Tag the Atlas Case Studies as such.
                create_category_relationships_for_page(obj, atlas_categories)

                # add the categories as related many to many, found this
                # needs to be after the save above some categories are blank
                if atlas_case_study.get("categories"):
                    category_ids = atlas_case_study.get("categories").split(" ")
                    for category_id in category_ids:
                        mapped_categories = (
                            self.category_mapper.get_mapped_categories_for_type_by_id(
                                "categories", category_id
                            )
                        )
                        create_category_relationships_for_page(obj, mapped_categories)
                    logger.debug(
                        "Creating link to categories, cat ids = %s" % category_ids
                    )

                # add the regions as related many to many, found this needs
                # to be
                # after the save above
                # some regions are blank
                if atlas_case_study.get("regions"):
                    regions = atlas_case_study.get("regions").split(
                        " "
                    )  # list of category wp_id's

                    for region_id in regions:
                        mapped_regions = (
                            self.category_mapper.get_mapped_categories_for_type_by_id(
                                "regions", region_id
                            )
                        )
                        create_category_relationships_for_page(obj, mapped_regions)
                    logger.debug("Creating link to regions, region ids = %s" % regions)

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return imported_count, self.count
