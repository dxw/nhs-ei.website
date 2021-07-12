import sys
import time

from cms.categories.models import Category

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


class CategoriesImporter(Importer):
    def __init__(self):
        categories = Category.objects.all()
        if categories:
            sys.stdout.write("⚠️  Run delete_categories before running this command\n")
            sys.exit()

    def parse_results(self):
        categories = self.results
        for r in categories:
            # if the subsite parent for this category does not exits make it once
            category = Category(
                name=r.get("name"),
                slug=r.get("slug"),
                description=r.get("description"),
                wp_id=r.get("wp_id"),
                source=r.get("source"),
            )
            category.save()
            sys.stdout.write(".")

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Category.objects.count(), self.count
