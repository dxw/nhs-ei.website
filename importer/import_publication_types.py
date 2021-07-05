import sys
import time

from django.core.management import call_command
from cms.categories.models import PublicationType

from .importer_cls import Importer


# the indiators from wordpress aren't nice so map them to better titles
SOURCES = {
    "publication_types": "NHS England & Improvement",
    "publication_types-aac": "Accelerated Access Collaborative",
    "publication_types-commissioning": "Commissioning",
    "publication_types-coronavirus": "Coronavirus",
    "publication_types-greenernhs": "Greener NHS",
    "publication_types-improvement-hub": "Improvement Hub",
    "publication_types-non-executive-opportunities": "Non-executive opportunities",
    "publication_types-rightcare": "Right Care",
}


class PublicationTypesImporter(Importer):
    def __init__(self):
        publication_type = PublicationType.objects.all()
        if publication_type:
            sys.stdout.write(
                "⚠️  Run delete_publication_types before running this command\n"
            )
            sys.exit()

    def parse_results(self):
        publication_types = self.results
        for r in publication_types:
            publication_type = PublicationType(
                name=r.get("name"),
                slug=r.get("slug"),
                description=r.get("description"),
                wp_id=r.get("wp_id"),
                source=r.get("source"),
            )
            publication_type.save()
            sys.stdout.write(".")

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return PublicationType.objects.count(), self.count
