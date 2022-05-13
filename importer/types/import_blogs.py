import logging
import time
from abc import ABC

from dateutil import parser
from wagtail.models import Page

from cms.blogs.models import Blog, BlogIndexPage
from .importer_cls import Importer

from importer.utils import ImportCategoryMapper, create_category_relationships_for_page

logger = logging.getLogger("importer")


class BlogsImporter(Importer, ABC):

    category_mapper = ImportCategoryMapper()

    def __init__(self):
        super().__init__()
        blogs = Blog.objects.all()
        for page in blogs:
            self.cache[page.wp_id] = page

        try:
            self.blog_index_page = BlogIndexPage.objects.get(title="Blog Items Base")
        except Page.DoesNotExist:
            self.blog_index_page = BlogIndexPage(
                title="Blog Items Base",
                body="theres a place here for some text",
                show_in_menus=True,
                slug="blog-items-base",
            )
            self.staging_page.add_child(instance=self.blog_index_page)
            rev = self.blog_index_page.save_revision()
            rev.publish()
            logger.info("Created BlogIndexPage")

    def parse_results(self):
        # make a blog index page to use for now ...
        blogs = self.results  # this is json result set
        for blog in blogs:

            source = blog.get("source")
            modified = blog.get("modified")
            modified_time = parser.parse(modified)
            wp_id = int(blog.get("wp_id"))

            # cheap check first, is the file too old to be considered
            if self.check_is_too_old(modified_time, source):
                continue

            is_new = False

            if wp_id in self.cache:
                obj = self.cache[wp_id]
            else:
                obj = Blog(wp_id=wp_id, show_in_menus=True)
                obj.first_published_at = blog.get("date")
                is_new = True

            self("title", blog.get("title"), obj)
            self("body", blog.get("content"), obj)
            self("author", blog.get("author"), obj)
            self("source", blog.get("source"), obj)
            self("wp_slug", blog.get("slug"), obj)
            self("wp_link", blog.get("link"), obj)
            self("first_published_at", blog.get("date"), obj)
            self("last_published_at", blog.get("modified"), obj)
            self("latest_revision_created_at", blog.get("modified"), obj)

            if is_new:
                self.blog_index_page.add_child(instance=obj)
                logger.debug(
                    "Imported Blog wp_id=%s, title=%s" % (obj.wp_id, obj.title)
                )
            else:
                logger.debug("Updated Blog wp_id=%s, title=%s" % (obj.wp_id, obj.title))

            self.save(obj)

            # add the categories as related many to many, found this needs to
            # be after the save above
            if blog.get("categories") and is_new:  # some categories are blank
                category_ids = blog.get("categories").split(" ")  # list cat wp_id's
                for category_id in category_ids:
                    mapped_categories = (
                        self.category_mapper.get_mapped_categories_for_type_by_id(
                            "categories", category_id
                        )
                    )
                    create_category_relationships_for_page(obj, mapped_categories)

                logger.debug("Set categories to %s" % category_ids)

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Blog.objects.count(), self.count
