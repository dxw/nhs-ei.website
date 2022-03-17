import logging

from nis import cat
from django.utils.text import slugify

from cms.categories.models import Category

logger = logging.getLogger("importer")


class URLParser:
    def __init__(self, url=None):
        self.url_parts = []
        if url:
            self.url_parts = url.strip("/").split("/")
        else:
            print("url is required!")

    def find_slug(self):
        return "".join(self.url_parts[-1:])


class ImportCategoryMapper:
    def __init__(self):

        self.cache = {}

        # Build a cache of all existing categories, so we can cut down on database hits to try find them
        existing_categories = Category.objects.all()
        for category in existing_categories:
            self.cache[category.slug] = category

    def get_slug_for_category_name(self, category_name):

        return slugify(category_name)

    def get_category_for_name(self, category_name):
        slug = self.get_slug_for_category_name(category_name)

        if slug in self.cache:
            category = self.cache[slug]
            logger.debug(
                f"Matched category {category.name} (with slug {category.slug}) from cache"
            )

        else:
            category = Category(name=category_name, slug=slug)
            self.cache[slug] = category
            logger.debug(
                f"Created new category {category.name} with slug {category.slug})"
            )

        return category
