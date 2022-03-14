import logging
import time
from abc import ABC

from cms.categories.models import Setting
from . import trim_long_text
from .importer_cls import Importer

logger = logging.getLogger("importer")

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


class SettingsImporter(Importer, ABC):
    def __init__(self):
        super().__init__()
        settings = Setting.objects.all()
        for setting in settings:
            self.cache[setting.wp_id] = setting

    def parse_results(self):
        settings = self.results

        for r in settings:
            is_new = False
            wp_id = int(r.get("wp_id"))
            if wp_id in self.cache:
                setting = self.cache[wp_id]
            else:
                is_new = True
                setting = Setting(wp_id=wp_id)

            self.changed = False

            self("name", r.get("name"), setting)
            self("slug", trim_long_text(r.get("slug"), 200), setting)
            self("description", r.get("description"), setting)

            self.save(setting)
            if is_new:
                logger.info("Imported Setting name=%s" % setting.name)
            else:
                logger.info("Updated Setting name=%s" % setting.name)

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Setting.objects.count(), self.count
