import logging
import sys

from django.core.management.base import BaseCommand
from wagtail.core.models import Page

from cms.pages.models import BasePage

# some pages are autogenerated so for now lets ignore them
from importer.types.importer_cls import Importer

logger = logging.getLogger("importer:page_mover")

MOVE_PAGE_IGNORE = [
    "news-items-base",
    "blog-items-base",
    "atlas-case-study-items-base",
    "publication-items-base",
]


def _get_parent(id):
    parents = BasePage.objects.filter(wp_id=id)
    if len(parents) == 0:
        logger.warning("Cannot find parent page for id %d" % id)
        return None
    elif len(parents) > 1:
        logger.warning(
            "Multiple parents found for id %d, %s"
            % (
                id,
                map(
                    lambda page: "%d:%s:%s " % (page.id, page.title, page.parent_type),
                    parents,
                ),
            )
        )
    return parents.first()


class Command(BaseCommand):
    """
    the purpose of this module is to move pages under the correct parent
    according to worpress.
    """

    help = (
        "Moves pages into position indicated by the parent field (the "
        "wordpress page id)"
    )

    def handle(self, *args, **options):
        staging = BasePage.objects.get(wp_id=Importer.STAGING_PAGE_WP_ID)
        pages = staging.get_children()
        logger.info("⚠️Got %d pages" % len(pages))

        home_page = Page.objects.filter(title="Home")[0]
        logger.info("⚠️Got Home page")

        try:
            for page in pages:
                _page = BasePage.objects.get(id=page.id)
                logger.info("⚠ Processing page %s" % page.title)
                if _page.real_parent:
                    parents = BasePage.objects.filter(wp_id=_page.real_parent)
                    parent = parents.first()
                elif _page.parent:
                    parents = BasePage.objects.filter(wp_id=_page.parent)
                    parent = parents.first()
                else:
                    parent = home_page

                if parent:
                    logger.info(
                        "  Moving '%s' to be a child of '%s'"
                        % (_page.title, parent.title)
                    )
                    _page.move(parent, pos="last-child")
        except Exception as ex:
            logger.error(" ️Error: %s for '%s'" % (ex, page))

        if not pages:
            logger.error("⚠️  Run `runimport pages` before running this command")
            sys.exit()

        logger.info("✅  All pages moved")
