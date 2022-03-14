import logging
import time
from abc import ABC

from cms.categories.models import Category
from . import trim_long_text
from .importer_cls import Importer

# the indiators from wordpress aren't nice so map them to better titles
SOURCES = {
    "categories": "NHS England & Improvement",
    "categories-aac": "Accelerated Access Collaborative",
    "categories-commissioning": "Commissioning",
    "categories-coronavirus": "Coronavirus",
    "categories-greenernhs": "Greener NHS",
    "categories-improvement-hub": "Improvement Hub",
    "categories-non-executive-opportunities": "Non-executive opportunities",
    "categories-rightcare": "Right Care",
}

logger = logging.getLogger("importer")


class CategoriesImporter(Importer, ABC):
    def __init__(self):
        # load all existsing cats to cut down on DB hits
        super().__init__()
        cats = Category.objects.all()
        for cat in cats:
            self.cache[cat.wp_id] = cat

    def parse_results(self):
        categories = self.results
        for r in categories:
            # if the subsite parent for this category does not exist make it
            # once

            is_new = False
            wp_id = int(r.get("wp_id"))
            if wp_id in self.cache:
                category = self.cache[wp_id]
            else:
                category = Category(wp_id=wp_id)
                is_new = True

            self.changed = False

            self("name", r.get("name"), category)
            self("slug", trim_long_text(r.get("slug"), 50), category)
            self("description", r.get("description"), category)
            self("source", r.get("source"), category)

            self.save(category)
            if is_new:
                logger.debug("Imported Category name=%s" % category.name)
            else:
                logger.debug("Updated Category name=%s" % category.name)

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Category.objects.count(), self.count
