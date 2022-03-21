import logging
import time
from abc import ABC

from dateutil import parser
from django.core.validators import slug_re
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags

from cms.pages.models import BasePage, ComponentsPage
from importer.utils import URLParser
from . import trim_long_text
from .importer_cls import Importer

logger = logging.getLogger("importer")


class PagesImporter(Importer, ABC):
    def __init__(self):
        # uniqufy urls to start with so we can deal with altering them later
        # all pages initially come in at the top level under home page
        # so urls can get changed to keep them unique (Wagtail action)
        super().__init__()
        self.random_strings = []

        base_pages = BasePage.objects.all()
        for page in base_pages:
            self.cache[page.wp_id] = page

    def parse_results(self):

        pages = self.results  # this is json result set

        for page in pages:

            modified = page.get("modified")
            modified_time = parser.parse(modified)
            wp_id = int(page.get("wp_id"))

            # cheap check first, is the file too old to be considered
            if self.check_is_too_old(modified_time, wp_id):
                continue

            is_new = False

            if wp_id in self.cache:
                obj = self.cache[wp_id]
            else:
                obj = BasePage(wp_id=wp_id, show_in_menus=True)
                if page.get("page-components.php") or page.get("page-blog-landing.php"):
                    obj = ComponentsPage(wp_id=wp_id, show_in_menus=True)
                else:
                    obj = BasePage(wp_id=wp_id, show_in_menus=True)
                is_new = True

            self.changed = False

            """
            Process: We need to import the pages at the top level under the
            home page as we don't know the
            page sitemap structure until all pages have been imported.

            Problem: using the wordpress slugs here means wagtail wrangles
            them to be unique at the top level

            Solution: we need to be able to fix these slugs later on still
            run into slugs we are again
            duplicating so lets set our own unique slug here so we can change
            back later without
            issue.
            """
            # these are fields that are meta data to be saved
            model_fields = {
                "owner": "",
                "description": "",
                "gateway_ref": "",
                "pcc_reference": "",
            }
            for item in page.get("model_fields"):
                for k, v in item.items():
                    model_fields[k] = v

            self("title", page.get("title"), obj)
            self("slug", "%d----%s" % (hash(page.get("slug")), page.get("wp_id")), obj)
            self("excerpt", trim_long_text(strip_tags(page.get("excerpt")), 250), obj)
            self("raw_content", page.get("content"), obj)
            self("raw_content", page.get("content"), obj)
            self("author", page.get("author"), obj)
            self("md_owner", model_fields["owner"], obj)
            self("md_description", model_fields["description"], obj)
            self("md_gateway_ref", model_fields["gateway_ref"], obj)
            self("md_pcc_reference", model_fields["pcc_reference"], obj)

            # start wordpress fields we can delete later
            self("parent", page.get("parent"), obj)
            self("source", page.get("source"), obj)
            self("wp_template", page.get("template"), obj)
            self("wp_slug", page.get("slug"), obj)
            self("real_parent", page.get("real_parent") or 0, obj)
            self("wp_link", page.get("wp_link"), obj)
            self("model_fields", page.get("model_fields"), obj)
            self("content_fields", page.get("content_fields"), obj)
            self("content_field_blocks", page.get("content_field_blocks"), obj)
            self("component_fields", page.get("component_fields"), obj)

            if is_new:
                self.staging_page.add_child(instance=obj)
                logger.debug(
                    "Imported %s wp_id=%s, title=%s"
                    % (obj.__class__, obj.wp_id, obj.title)
                )
            else:
                logger.debug(
                    "Updated %s wp_id=%s, title=%s"
                    % (obj.__class__, obj.wp_id, obj.title)
                )

            self("first_published_at", page.get("date"), obj)
            self("last_published_at", page.get("modified"), obj)
            self("latest_revision_created_at", page.get("modified"), obj)

            self.save(obj)

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return (
            BasePage.objects.live().descendant_of(self.staging_page).count(),
            self.count,
        )
