import sys

from django.core.management.base import BaseCommand
from cms.categories.models import Category
from cms.posts.models import Post
from cms.blogs.models import Blog


class Command(BaseCommand):
    help = "Deletes categories (bulk action)"

    def handle(self, *args, **options):
        """remove categories first"""
        posts = Post.objects.all()
        blogs = Blog.objects.all()
        if posts or blogs:
            sys.stdout.write(
                "⚠️ Please delete posts and blogs before running this commend\n"
            )
            sys.exit()

        categories = Category.objects.all()
        if not categories.count():
            sys.stdout.write("✅ Categories is empty\n")
        else:

            categories_length = len(categories)

            sys.stdout.write("Categories to delete: {}\n".format(categories_length))

            for category in categories:
                sys.stdout.write("-")
                category.delete()
                categories_length -= 1

            sys.stdout.write("\n✅ Complete\n")
