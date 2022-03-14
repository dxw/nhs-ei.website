import logging
import time
from abc import ABC

from cms.categories.models import Region
from . import trim_long_text
from .importer_cls import Importer

# the indiators from wordpress aren't nice so map them to better titles
# SOURCES = {
#     'categories': 'NHS England & Improvement',
#     'categories-aac': 'Accelerated Access Collaborative',
#     'categories-commissioning': 'Commissioning',
#     'categories-coronavirus': 'Coronavirus',
#     'categories-greenernhs': 'Greener NHS',
#     'categories-improvement-hub': 'Improvement Hub',
#     'categories-non-executive-opportunities': 'Non-executive opportunities',
#     'categories-rightcare': 'Right Care',
# }

logger = logging.getLogger("importer")


class RegionsImporter(Importer, ABC):
    def __init__(self):
        super().__init__()
        regions = Region.objects.all()
        for region in regions:
            self.cache[region.wp_id] = region

    def parse_results(self):
        regions = self.results

        for r in regions:
            is_new = False
            wp_id = int(r.get("wp_id"))
            if wp_id in self.cache:
                region = self.cache[wp_id]
            else:
                is_new = True
                region = Region(wp_id=wp_id)

            self.changed = False

            self("name", r.get("name"), region)
            self("slug", trim_long_text(r.get("slug"), 200), region)
            self("description", r.get("description"), region)

            self.save(region)
            if is_new:
                logger.info("Imported Region name=%s" % region.name)
            else:
                logger.info("Updated Region name=%s" % region.name)

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Region.objects.count(), self.count
