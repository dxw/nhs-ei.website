import logging
import sys
import time
from abc import ABC

from dateutil import parser
from wagtail.core.models import Page

from cms.atlascasestudies.models import (
    AtlasCaseStudy,
    AtlasCaseStudyIndexPage,
    AtlasCaseStudySettingRelationship,
    AtlasCaseStudyRegionRelationship,
)
from cms.categories.models import (
    Category,
    Region,
    Setting,
    CategoryPageCategoryRelationship,
)
from importer.preserve import preserve
from .importer_cls import Importer

logger = logging.getLogger("importer")


class AtlasCaseStudiesImporter(Importer, ABC):
    categories = None
    settings = None
    regions = None
    atlas_case_study_index_page = None

    def __init__(self):
        super().__init__()
        atlas_case_studies = AtlasCaseStudy.objects.all()
        for case in atlas_case_studies:
            self.cache[case.wp_id] = case

        # we need categories to exist before importing atlas case studies
        self.categories = Category.objects.all()
        if not self.categories:
            sys.exit("\n😲Cannot continue... did you import the categories first?")

        # we need settings to exist before importing atlas case studies
        self.settings = Setting.objects.all()
        if not self.settings:
            sys.exit("\n😲Cannot continue... did you import the settings first?")

        # we need categories to exist before importing atlas case studies
        self.regions = Region.objects.all()
        if not self.regions:
            sys.exit("\n😲Cannot continue... did you import the regions first?")

        # make an atlas case study index page for the whole site, only one to
        # exist ...

        try:
            # a parent for all atlas case study pages
            self.atlas_case_study_index_page = AtlasCaseStudyIndexPage.objects.get(
                title="Atlas Case Study Items Base"
            )
        except Page.DoesNotExist:
            self.atlas_case_study_index_page = AtlasCaseStudyIndexPage(
                title="Atlas Case Study Items Base",
                body="theres a place here for some text",
                show_in_menus=True,
                slug="atlas-case-study-items-base",
            )
            self.staging_page.add_child(instance=self.atlas_case_study_index_page)
            revision = self.atlas_case_study_index_page.save_revision()
            revision.publish()
            logger.info("Created Atlas Case Study Items Base")

    def parse_results(self):
        atlas_case_studies = self.results

        for atlas_case_study in atlas_case_studies:

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

                obj = AtlasCaseStudy(wp_id=wp_id, show_in_menus=True)
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
                logger.info(
                    "Created AtlasCaseStudy, wp_id=%s, title=%s"
                    % (obj.wp_id, obj.title)
                )
            else:
                logger.info(
                    "Updated AtlasCaseStudy, wp_id=%s, title=%s"
                    % (obj.wp_id, obj.title)
                )

            preserve(obj)

            if is_new:
                # add the categories as related many to many, found this
                # needs to be after the save above some categories are blank
                if not not atlas_case_study.get("categories"):
                    category_ids = atlas_case_study.get("categories").split(" ")
                    # list of category wp_id's
                    for category in category_ids:
                        category_object = Category.objects.get(
                            source="categories",
                            wp_id=int(category),
                        )

                        CategoryPageCategoryRelationship.objects.create(
                            category_page=obj, category=category_object
                        )
                    logger.info(
                        "Creating link to categories, cat ids = %s" % category_ids
                    )

                # Tag the Atlas Case Studies as such.
                atlas_category, _ = Category.objects.get_or_create(
                    name="Atlas Case Studies",
                    slug="atlas-case-studies",
                    description="Atlas of Shared Learning: Case Studies",
                    wp_id=None,
                    source=None,
                )
                CategoryPageCategoryRelationship.objects.create(
                    category_page=obj, category=atlas_category
                )

                # add the settings as related many to many, found this needs to
                # be after the save above
                # some settings are blank
                if not not atlas_case_study.get("settings"):
                    settings = atlas_case_study.get("settings").split(
                        " "
                    )  # list of setting wp_id's
                    settings_objects = Setting.objects.filter(wp_id__in=settings)
                    for setting in settings_objects:
                        AtlasCaseStudySettingRelationship.objects.create(
                            atlas_case_study=obj, setting=setting
                        )
                    logger.info("Creating link to setting, setting ids = %s" % settings)

                # add the regions as related many to many, found this needs
                # to be
                # after the save above
                # some regions are blank
                if not not atlas_case_study.get("regions"):
                    regions = atlas_case_study.get("regions").split(
                        " "
                    )  # list of category wp_id's

                    regions_objects = Region.objects.filter(wp_id__in=regions)
                    for region in regions_objects:
                        AtlasCaseStudyRegionRelationship.objects.create(
                            atlas_case_study=obj, region=region
                        )
                    logger.info("Creating link to setting, region ids = %s" % regions)

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return AtlasCaseStudy.objects.count(), self.count
