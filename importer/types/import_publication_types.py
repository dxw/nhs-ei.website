import logging
import time
from abc import ABC

from cms.categories.models import PublicationType
from .importer_cls import Importer

logger = logging.getLogger("importer")

# the indiators from wordpress aren't nice so map them to better titles
SOURCES = {
    "publication_types": "NHS England & Improvement",
    "publication_types-aac": "Accelerated Access Collaborative",
    "publication_types-commissioning": "Commissioning",
    "publication_types-coronavirus": "Coronavirus",
    "publication_types-greenernhs": "Greener NHS",
    "publication_types-improvement-hub": "Improvement Hub",
    "publication_types-non-executive-opportunities": "Non-executive " "opportunities",
    "publication_types-rightcare": "Right Care",
}


class PublicationTypesImporter(Importer, ABC):
    def __init__(self):
        super().__init__()
        pubs = PublicationType.objects.all()
        for pub in pubs:
            self.cache[pub.wp_id] = pub

    def parse_results(self):
        publication_types = self.results
        for r in publication_types:

            is_new = False
            wp_id = int(r.get("wp_id"))
            if wp_id in self.cache:
                publication_type = self.cache[wp_id]
            else:
                is_new = True
                publication_type = PublicationType(wp_id=wp_id)

            self.changed = False

            self("name", r.get("name"), publication_type)
            self("slug", r.get("slug"), publication_type)
            self("description", r.get("description"), publication_type)

            self.save(publication_type)
            if is_new:
                logger.info(
                    "Imported PublicationType wp_id=%s, title=%s"
                    % (publication_type.wp_id, publication_type.name)
                )
            else:
                logger.info(
                    "Updated PublicationType wp_id=%s, title=%s"
                    % (publication_type.wp_id, publication_type.name)
                )

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return PublicationType.objects.count(), self.count
