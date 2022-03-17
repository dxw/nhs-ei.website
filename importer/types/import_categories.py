import logging
import time
from abc import ABC

from cms.categories.models import Category
from .importer_cls import Importer

from importer.utils import ImportCategoryMapper

logger = logging.getLogger("importer")

category_mapper = ImportCategoryMapper()


class CategoriesImporter(Importer, ABC):
    def parse_results(self):
        categories = self.results
        for r in categories:

            category = category_mapper.get_category_for_name(r.get("name"))
            logger.debug("Imported Category name=%s" % category.name)

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Category.objects.count(), self.count
