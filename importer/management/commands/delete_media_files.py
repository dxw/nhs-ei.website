import sys

from django.core.management.base import BaseCommand
from wagtail.images.models import Image
from wagtail.documents.models import Document
from wagtail.core.models import Collection

# the indiators from wordpress aren't nice so map them to better titles
SOURCES = {
    "media": "NHS England & Improvement",
    "media-aac": "Accelerated Access Collaborative",
    "media-commissioning": "Commissioning",
    "media-coronavirus": "Coronavirus",
    "media-greenernhs": "Greener NHS",
    "media-improvement-hub": "Improvement Hub",
    "media-non-executive-opportunities": "Non-executive opportunities",
    "media-rightcare": "Right Care",
    "media-north-east-yorkshire": "North East and Yorkshire",
    "media-south": "South West",
    "media-london": "London",
    "media-east-of-england": "East of England",
    "media-midlands": "Midlands",
    "media-north-west": "North West",
    "media-south-east": "South East",
}


class Command(BaseCommand):
    help = "Deletes media files (bulk action)"

    def handle(self, *args, **options):
        """removes all images and documents"""

        images = Image.objects.all()
        documents = Document.objects.all()
        # collections = Collection.objects.all()

        if images:
            images_length = images.count()
            sys.stdout.write("Images to delete: {}\n".format(images_length))

            for image in images:
                sys.stdout.write("-")
                image.delete()
                images_length -= 1
            sys.stdout.write("\n")
        else:
            sys.stdout.write("✅ There are no images to delete\n")

        if documents:
            documents_length = documents.count()
            sys.stdout.write("Documents to delete: {}\n".format(documents_length))

            for document in documents:
                sys.stdout.write("-")
                document.delete()
                documents_length -= 1
            sys.stdout.write("\n")
        else:
            sys.stdout.write("✅ There are no documents to delete\n")

        sys.stdout.write("✅ Removing collections\n")
        for key in SOURCES.keys():
            try:
                collection = Collection.objects.filter(name=SOURCES[key])
                for c in collection:
                    c.delete()
                    sys.stdout.write("-")
            except Collection.DoesNotExist:
                pass
        sys.stdout.write("\n✅ Complete\n")
