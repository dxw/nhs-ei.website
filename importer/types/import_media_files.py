import logging
import time
from abc import ABC
from io import BytesIO

from dateutil import parser
from django.core.files import File
from django.core.files.images import ImageFile
from wagtail.core.models import Collection
from wagtail.documents import get_document_model
from wagtail.images import get_image_model

from cms.core.models import ImageImportBridge, DocImportBridge
from importer.httpcache import session
from .importer_cls import Importer

logger = logging.getLogger("importer")

Document = get_document_model()
Image = get_image_model()

# the indicators from wordpress aren't nice so map them to better titles
SOURCES = {
    "media": "NHS England & Improvement",
    "media-aac": "Accelerated Access Collaborative",
    "media-commissioning": "Commissioning",
    "media-coronavirus": "Coronavirus",
    "media-greenernhs": "Greener NHS",
    "media-improvement-hub": "Improvement Hub",
    "media-non-executive-opportunities": "Non-executive opportunities",
    "media-rightcare": "Right Care",
}


class MediaFilesImporter(Importer, ABC):
    def __init__(self):
        # we used to clear this list of collections, we will update it instead

        # make collections based on sources
        # this does make collection names unique, maybe we'll need to refactor
        super().__init__()
        collection_root = Collection.get_first_root_node()
        for key in SOURCES.keys():
            collection = Collection.objects.filter(name=SOURCES[key])
            if not len(collection):
                collection_root.add_child(name=SOURCES[key])

    def parse_results(self):
        media_files = self.results

        for r in media_files:

            sub_site = r.get("source")
            collection_name = SOURCES[sub_site]
            collection = Collection.objects.get(name=collection_name)
            source_url = r.get("source_url")
            media_type = r.get("media_type")
            wp_id = r.get("wp_id")
            modified = r.get("modified")

            modified_time = parser.parse(modified)

            # cheap check first, is the file too old to be considered
            if self.check_is_too_old(modified_time, source_url):
                continue

            media_name = source_url.split("/")[-1]
            response = session.get(source_url)
            title = r.get("title")  # if the title id blank it causes an error
            if not title:
                logger.warning("No title was available for %s, %s", source_url, r)
                title = "No title was available"

            is_new = False

            if response:

                if media_type == "file":
                    media_file = File(BytesIO(response.content), name=media_name)
                elif media_type == "image":
                    media_file = ImageFile(BytesIO(response.content), name=media_name)
                else:
                    logger.error(
                        "Got no response and no file has been saved: %s %s, "
                        "%s" % (title, source_url, r)
                    )
                    # exit loop early, no need to save a file
                    continue

                try:
                    if media_type == "file":
                        media_object = DocImportBridge.objects.get(wp_id=wp_id).document
                    else:
                        media_object = ImageImportBridge.objects.get(wp_id=wp_id).image
                except ImageImportBridge.DoesNotExist:
                    is_new = True
                    media_object = Image(
                        title=title, file=media_file, collection=collection
                    )
                except DocImportBridge.DoesNotExist:
                    is_new = True
                    media_object = Document(
                        title=title, file=media_file, collection=collection
                    )

                self.changed = False

                self("title", title, media_object)
                self("file", media_file, media_object)
                self("collection", collection, media_object)
                self("created_at", r.get("date"), media_object)

                self.save(media_object)

                if is_new:
                    if media_type == "file":
                        logger.info("Imported File wp_id=%s, title=%s" % (wp_id, title))
                        DocImportBridge(wp_id=wp_id, document=media_object).save()
                    else:
                        logger.info(
                            "Imported Image wp_id=%s, title=%s" % (wp_id, title)
                        )
                        ImageImportBridge(wp_id=wp_id, image=media_object).save()
                else:
                    if media_type == "file":
                        logger.info("Updated File wp_id=%s, title=%s" % (wp_id, title))
                    else:
                        logger.info("Updated Image wp_id=%s, title=%s" % (wp_id, title))

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Document.objects.count() + Image.objects.count(), 0
