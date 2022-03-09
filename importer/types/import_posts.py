import logging
import time
from abc import ABC

from dateutil import parser
from wagtail.core.models import Page

from cms.categories.models import Category, CategoryPageCategoryRelationship
from cms.pages.models import BasePage
from cms.posts.models import Post, PostIndexPage
from importer.preserve import preserve
from .importer_cls import Importer

logger = logging.getLogger("importer:posts")

# so we can match the subsite categories for the post index page
POST_SOURCES_TO_CATEGORY_SOURCES = {
    "posts": "categories",
    "posts-aac": "categories-aac",
    "posts-commissioning": "categories-commissioning",
    "posts-coronavirus": "categories-coronavirus",
    "posts-greenernhs": "categories-greenernhs",
    "posts-improvement-hub": "categories-improvement-hub",
    "posts-non-executive-opportunities": "categories-non-executive" "-opportunities",
    "posts-rightcare": "categories-rightcare",
}

# so we can a post to a sub site and build out sub site post index pages
POST_SOURCES = {
    "posts": "NHS England & Improvement",
    "posts-aac": "Accelerated Access Collaborative",
    "posts-commissioning": "Commissioning",
    "posts-coronavirus": "Coronavirus",
    "posts-greenernhs": "Greener NHS",
    "posts-improvement-hub": "Improvement Hub",
    "posts-non-executive-opportunities": "Non-executive opportunities",
    "posts-rightcare": "Right Care",
}


class PostsImporter(Importer, ABC):
    news_index_page = None

    def __init__(self):
        super().__init__()
        posts = Post.objects.all()
        for page in posts:
            self.cache[page.wp_id] = page

        try:
            # we need a pretty unique name here as some imported page have
            # the title as News
            # a parent for all news item index pages
            self.news_index_page = BasePage.objects.get(title="News Items Base")
        except Page.DoesNotExist:
            self.news_index_page = BasePage(
                title="News Items Base",
                body="theres a place here for some text",
                show_in_menus=True,
                slug="news-items-base",
                wp_slug="auto-generated-news-index",
                wp_id=0,
                source="auto-generated-news-index",
            )
            self.staging_page.add_child(instance=self.news_index_page)
            revision = self.news_index_page.save_revision()
            revision.publish()
            logger.info("Created News Items Base")

    def parse_results(self):
        # make a posts index page for the whole site, only one to exist,
        # call is News ...
        posts = self.results

        for post in posts:
            # we need a sub_site_category for the news index page
            source = post.get("source")
            modified = post.get("modified")
            modified_time = parser.parse(modified)
            wp_id = int(post.get("wp_id"))

            # cheap check first, is the file too old to be considered
            if self.check_is_too_old(modified_time, source):
                continue

            try:
                sub_site_news_index_page = PostIndexPage.objects.get(
                    title=POST_SOURCES[post.get("source")]
                )
            except PostIndexPage.DoesNotExist:
                sub_site_news_index_page = PostIndexPage(
                    title=POST_SOURCES[post.get("source")],
                    body="",
                    show_in_menus=True,
                )
                self.news_index_page.add_child(instance=sub_site_news_index_page)
                rev = sub_site_news_index_page.save_revision()
                rev.publish()
                logger.info("Created post index, %s" % POST_SOURCES[post.get("source")])

            # let's make the posts for each sub site, we're in a loop for each
            # post here

            is_new = False

            if wp_id in self.cache:
                obj = self.cache[wp_id]
            else:
                obj = Post(wp_id=wp_id, show_in_menus=True)
                obj.first_published_at = post.get("date")
                is_new = True

            self.changed = False

            self("title", post.get("title"), obj)
            # excerpt = post.get('excerpt'),
            # dont preset the slug coming from wordpress some are too long
            self("body", post.get("content"), obj)
            self("author", post.get("author"), obj)
            self("source", post.get("source"), obj)
            self("wp_slug", post.get("slug"), obj)
            self("wp_link", post.get("link"), obj)
            self("last_published_at", post.get("modified"), obj)
            self("latest_revision_created_at", post.get("modified"), obj)

            if is_new:
                sub_site_news_index_page.add_child(instance=obj)
                logger.info("Imported Post wp_id=%d, title=%s" % (obj.wp_id, obj.title))
            else:
                logger.info("Updated Post wp_id=%d, title=%s" % (obj.wp_id, obj.title))

            preserve(obj)

            # Create source category
            source = post.get("source")
            if source and is_new:
                source_category, _ = Category.objects.get_or_create(
                    name=f"source: {source}",
                    description=f"Content from the {source} subsite",
                    wp_id=None,
                    source=None,
                )
                CategoryPageCategoryRelationship.objects.create(
                    category_page=obj, category=source_category
                )

            # add the categories as related many to many, found this needs to
            # be after the save above
            if post.get("categories") and is_new:  # some categories are blank
                category_ids = post.get("categories").split(
                    " "
                )  # list of category wp_id's

                ###
                for category_id in category_ids:
                    # find matching category on id and sub_site
                    try:
                        category_object = Category.objects.get(
                            source=POST_SOURCES_TO_CATEGORY_SOURCES[source],
                            wp_id=int(category_id),
                        )

                        CategoryPageCategoryRelationship.objects.create(
                            category_page=obj, category=category_object
                        )
                    except Exception as ex:
                        logger.warning(
                            "Unable to locate category for wp_id=%s, "
                            "source=%s" % (category_id, source)
                        )

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Post.objects.count(), self.count
