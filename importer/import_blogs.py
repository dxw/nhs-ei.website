import sys
import time

from cms.blogs.models import Blog, BlogIndexPage, BlogCategoryRelationship
from cms.categories.models import Category
from wagtail.core.models import Page
from django.core.management import call_command

from .importer_cls import Importer

# blogs are not from a subsite so rewrite the source blogs to posts
# they use the same categories

# these are used for matching to subsite because there is only one subsite.
CATEGORY_SOURCE_NAME = "categories"
POST_SOURCE = "NHS England & Improvement"


class BlogsImporter(Importer):
    def __init__(self):
        blogs = Blog.objects.all()
        if blogs:
            sys.stdout.write("⚠️  Run delete_blogs before running this command\n")
            sys.exit()

    def parse_results(self):
        # make a blog index page to use for now ...
        blog_index_page = None
        home_page = Page.objects.filter(title="Home")[0]

        try:
            blog_index_page = BlogIndexPage.objects.get(title="Blog Items Base")
        except Page.DoesNotExist:
            blog_index_page = BlogIndexPage(
                title="Blog Items Base",
                body="theres a place here for some text",
                show_in_menus=True,
                slug="blog-items-base",
            )
            home_page.add_child(instance=blog_index_page)
            rev = blog_index_page.save_revision()
            rev.publish()
            sys.stdout.write(".")

        blogs = self.results  # this is json result set
        for blog in blogs:
            first_published_at = blog.get("date")
            last_published_at = blog.get("modified")
            latest_revision_created_at = blog.get("modified")

            obj = Blog(
                title=blog.get("title"),
                # excerpt = post.get('excerpt'),
                # dont preset the slug coming from wordpress some are too long
                body=blog.get("content"),
                show_in_menus=True,
                wp_id=blog.get("wp_id"),
                author=blog.get("author"),
                source=blog.get("source"),
                wp_slug=blog.get("slug"),
                wp_link=blog.get("link"),
            )
            blog_index_page.add_child(instance=obj)
            rev = obj.save_revision()  # this needs to run here

            obj.first_published_at = first_published_at
            obj.last_published_at = last_published_at
            obj.latest_revision_created_at = latest_revision_created_at
            # probably not the best way to do this but need to update the dates on the page record.
            obj.save()
            rev.publish()

            # Create source category
            source = blog.get("source")
            if source:
                source_category, _ = Category.objects.get_or_create(
                    name=f"source: {source}",
                    description=f"Content from the {source} subsite",
                    wp_id=None,
                    source=None,
                )
            BlogCategoryRelationship.objects.create(blog=obj, category=source_category)

            # add the categories as related many to many, found this needs to be after the save above
            if blog.get("categories"):  # some categories are blank
                cat_ids = blog.get("categories").split(" ")  # list of category wp_id's
                for cat_id in cat_ids:
                    # find matching category on id and sub_site
                    category_object = Category.objects.get(
                        source=CATEGORY_SOURCE_NAME,
                        wp_id=int(cat_id),
                    )

                    BlogCategoryRelationship.objects.create(
                        blog=obj, category=category_object
                    )

            sys.stdout.write(".")

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Blog.objects.count(), self.count
