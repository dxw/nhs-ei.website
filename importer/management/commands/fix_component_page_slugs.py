import logging

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from cms.pages.models import ComponentsPage
from importer.types import trim_long_text

logger = logging.getLogger("importer")

# some pages are autogenerated so for now lets ignore them
# when we have auto generate nav is shouldnt matter...
FIX_SLUGS_IGNORE = [
    "news-items-base",
    "blog-items-base",
    "atlas-case-study-items-base",
    "publication-items-base",
]


class Command(BaseCommand):
    """
    the purpose of this module is to fix pages slugs.
    during the first import they get incremented by wagtail to make the slugs unique
    once moved into place by movepages.py they can be corrected to the slug
    in SCRAPY
    """

    help = "Fixes component page slugs"

    def handle(self, *args, **options):
        """
        we need to loop through every component page model and get the original slug
        updated to be the same as the slug in SCRAPY
        """

        pages = ComponentsPage.objects.all().order_by("-depth")

        for page in pages:
            if page.slug not in FIX_SLUGS_IGNORE:
                first_published = page.first_published_at
                last_published = page.last_published_at
                latest_revision_created = page.latest_revision_created_at

                if "----" not in page.slug:
                    # Already processed
                    continue

                page.slug = trim_long_text(page.slug.split("----")[0], 254)
                logger.info("⚙️ {} SLUG updated".format(page))

                """
                running save_revision() as it seems like a good idea to not break page paths
                just to be safe...
                try to keep revision dates to match whats in wordpress as our
                revisions reset that at the save()
                """
                try:
                    rev = page.save_revision()
                    page.first_published_at = first_published
                    page.last_published_at = last_published
                    page.latest_revision_created_at = latest_revision_created
                    page.save()
                    rev.publish()
                except ValidationError:
                    logger.warning(
                        "Slug for component page %s cannot be updated.", page
                    )

        logger.info("✅  All slugs fixed")
