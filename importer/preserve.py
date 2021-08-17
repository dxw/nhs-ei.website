from cms.blogs.models import Blog, BlogIndexPage
from cms.pages.models import Page
from django.core.management.base import BaseCommand


def preserve(obj):
    """Save updates to obj (including first-write) without
    trashing the publication/revision dates"""
    fpa = obj.first_published_at
    lpa = obj.last_published_at
    lrca = obj.latest_revision_created_at
    rev = obj.save_revision()
    rev.publish()
    obj.first_published_at = fpa
    obj.last_published_at = lpa
    obj.latest_revision_created_at = lrca
    obj.save()


class Command(BaseCommand):
    help = "Creates a sample page"

    def handle(self, *args, **options):
        try:
            exblog = Blog.objects.get(title="Preserve")
        except Page.DoesNotExist:
            pass
        else:
            exblog.delete()
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
        first_published_at = "2111-01-01T01:01:01Z"
        last_published_at = "2222-02-02T02:02:02Z"
        latest_revision_created_at = "2333-03-03T03:03:03Z"
        blog_index_page = BlogIndexPage.objects.get(title="Blog Items Base")
        obj = Blog(
            title="Preserve",
            # excerpt = post.get('excerpt'),
            # dont preset the slug coming from wordpress some are too long
            body="Preserve",
            show_in_menus=True,
            wp_id="0",
            author="Author",
            source="Source",
            wp_slug="Slug",
            wp_link="Link",
        )
        blog_index_page.add_child(instance=obj)
        obj.first_published_at = first_published_at
        obj.last_published_at = last_published_at
        obj.latest_revision_created_at = latest_revision_created_at
        preserve(obj)
        # Check that we can update the object and not mangle the date
        obj = Blog.objects.get(title="Preserve")
        obj.body = "Well preserved"
        preserve(obj)
