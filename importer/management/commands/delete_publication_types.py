import sys

from django.core.management.base import BaseCommand
from cms.categories.models import PublicationType
from cms.publications.models import Publication


class Command(BaseCommand):
    help = "Deletes publicaton types (bulk action)"

    def handle(self, *args, **options):
        """remove publications first"""
        publications = Publication.objects.all()
        if publications:
            sys.stdout.write(
                "⚠️ Please delete publications before running this commend\n"
            )
            sys.exit()

        publication_types = PublicationType.objects.all()
        if not publication_types.count():
            sys.stdout.write("✅ Publication Types is empty\n")
        else:

            publication_types_length = len(publication_types)

            sys.stdout.write(
                "Publication Types to delete: {}\n".format(publication_types_length)
            )

            for publication_type in publication_types:
                sys.stdout.write("-")
                publication_type.delete()
                publication_types_length -= 1

            sys.stdout.write("\n")

            sys.stdout.write("✅ Complete\n")
