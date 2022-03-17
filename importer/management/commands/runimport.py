import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand

from importer.postimport import parse_all_updated
from importer.types.import_atlas_case_studies import AtlasCaseStudiesImporter
from importer.types.import_blogs import BlogsImporter
from importer.types.import_categories import CategoriesImporter
from importer.types.import_media_files import MediaFilesImporter
from importer.types.import_pages import PagesImporter
from importer.types.import_posts import PostsImporter
from importer.types.import_publication_types import PublicationTypesImporter
from importer.types.import_publications import PublicationsImporter
from importer.types.import_regions import RegionsImporter
from importer.types.import_settings import SettingsImporter
from importer.websites import SCRAPY

logger = logging.getLogger("importer")


def get_api_url(app):
    if app == "categories":
        return SCRAPY + "api/categories/"
    if app == "publication_types":
        return SCRAPY + "api/publication_types/"
    if app == "settings":
        return SCRAPY + "api/settings/"
    if app == "regions":
        return SCRAPY + "api/regions/"
    if app == "tags":
        return SCRAPY + "api/tags/"
    if app == "pages":
        return SCRAPY + "api/pages/"
    if app == "posts":
        return SCRAPY + "api/posts/"
    if app == "publications":
        return SCRAPY + "api/publications/"
    if app == "atlas_case_studies":
        return SCRAPY + "api/atlas_case_studies/"
    if app == "blogs":
        return SCRAPY + "api/blogs/"
    if app == "media":
        return SCRAPY + "api/media_files"


def do_low_impact():
    """
    These all run really quickly ~20s so group them
    """
    import_categories(get_api_url("categories"))
    import_publication_types(get_api_url("publication_types"))
    import_settings(get_api_url("settings"))
    import_regions(get_api_url("regions"))


def do_refresh():
    """
    This can be run repeatedly, it tags changed objects in the ParseList model
    """
    import_pages(get_api_url("pages"))
    import_posts(get_api_url("posts"))
    import_blogs(get_api_url("blogs"))
    import_publications(get_api_url("publications"))
    import_atlas_case_studies(get_api_url("atlas_case_studies"))

    # only runs on child pages of import staging page
    call_command("page_mover")

    # These are fast we can run them every time
    call_command("dedupe_pubtypes")
    call_command("dedupe_categories")


class Command(BaseCommand):
    help = (
        "Imports an apps records from the API. \ available apps: "
        "categories, publication_types, settings, regions, pages, posts, "
        "blogs, publications, atlascasestudies "
    )

    def add_arguments(self, parser):
        parser.add_argument("app", type=str, help="The APP to import")

    def handle(self, *args, **options):

        # the magic happens here e.g. getting initial api url then looping
        # through items and parsing the results. There's no other models
        # involved except the one for each app might we want to log it?

        if options["app"] == "venti":
            import_media_files(get_api_url("media"))
            do_low_impact()
            do_refresh()
            parse_all_updated()

        elif options["app"] == "low_impact":
            do_low_impact()
        elif options["app"] == "refresh":
            do_refresh()
        elif options["app"] == "parse":
            parse_all_updated()

        elif options["app"] == "posts":
            import_posts(get_api_url("posts"))
        elif options["app"] == "publications":
            import_publications(get_api_url("publications"))
        elif options["app"] == "atlas_case_studies":
            import_atlas_case_studies(get_api_url("atlas_case_studies"))
        elif options["app"] == "pages":
            import_pages(get_api_url("pages"))
        elif options["app"] == "blogs":
            import_blogs(get_api_url("blogs"))
        elif options["app"] == "media":
            import_media_files(get_api_url("media"))
        elif options["app"] == "documents":
            call_command("make_documents_list")
        else:
            print("❌ runimport subcommand not recognised")


def import_media_files(url):
    if not url:
        raise Exception("url error")
    media_files_importer = MediaFilesImporter()
    fetch = media_files_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = media_files_importer.parse_results()

    logger.info(
        "✅ %d Media Files imported, api count (%d)" % (completed_count, api_count)
    )


def import_categories(url):
    if not url:
        raise Exception("url error")
    categories_importer = CategoriesImporter()
    fetch = categories_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = categories_importer.parse_results()

    logger.info(
        "✅ %d Categories processed, api count (%d)" % (completed_count, api_count)
    )


def import_publication_types(url):
    if not url:
        raise Exception("url error")
    publication_types_importer = PublicationTypesImporter()
    fetch = publication_types_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = publication_types_importer.parse_results()

    logger.info(
        "✅ %d Publication Types processed, api count (%d)"
        % (completed_count, api_count)
    )


def import_atlas_case_studies(url):
    if not url:
        raise Exception("url error")
    atlas_case_studies_importer = AtlasCaseStudiesImporter()
    fetch = atlas_case_studies_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = atlas_case_studies_importer.parse_results()

    logger.info(
        "✅ %d Atals Case Studies processed, api count (%d)"
        % (completed_count, api_count)
    )


def import_settings(url):
    if not url:
        raise Exception("url error")
    settings_importer = SettingsImporter()
    fetch = settings_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = settings_importer.parse_results()

    logger.info("✅ {} Settings processed".format(completed_count))


def import_regions(url):
    if not url:
        raise Exception("url error")
    regions_importer = RegionsImporter()
    fetch = regions_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = regions_importer.parse_results()

    logger.info("✅ %d Regions processed, api count (%d)" % (completed_count, api_count))


def import_posts(url):
    if not url:
        raise Exception("url error")
    posts_importer = PostsImporter()
    fetch = posts_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = posts_importer.parse_results()

    logger.info("✅ %d Posts imported, api count (%d)" % (completed_count, api_count))


def import_publications(url):
    if not url:
        raise Exception("url error")
    publications_importer = PublicationsImporter()
    fetch = publications_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = publications_importer.parse_results()

    logger.info(
        "✅ %d Publications imported, api count (%d)" % (completed_count, api_count)
    )


def import_blogs(url):
    if not url:
        raise Exception("url error")
    blogs_importer = BlogsImporter()
    fetch = blogs_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = blogs_importer.parse_results()

    logger.info("✅ %d Blogs imported, api count (%d)" % (completed_count, api_count))


def import_pages(url):
    if not url:
        raise Exception("url error")
    pages_all_importer = PagesImporter()
    fetch = pages_all_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = pages_all_importer.parse_results()

    logger.info("✅ %d Pages imported, api count (%d)" % (completed_count, api_count))
