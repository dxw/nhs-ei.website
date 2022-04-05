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

            try:
                mapped_categories = (
                    category_mapper.get_mapped_categories_for_type_by_id(
                        type=r.get("source"), id=r.get("wp_id")
                    )
                )

            except:
                raise Exception(
                    f"Category \"{r.get('name')}\" with ID {r.get('wp_id')} does not exist in CATEGORY_MAP. This needs manually mapping."
                )

            for category in mapped_categories:
                logger.debug("Imported Category name=%s" % category.name)

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Category.objects.count(), self.count
