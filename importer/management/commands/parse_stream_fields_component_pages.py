import ast
import logging
from cms.publications.models import Publication
from cms.atlascasestudies.models import AtlasCaseStudy
from cms.posts.models import Post
from cms.blogs.models import Blog
import json
from html import unescape

from django.core.management.base import BaseCommand
from cms.pages.models import BasePage, ComponentsPage, LandingPage
from importer.types.importer_cls import ComponentsBuilder

logger = logging.getLogger("importer:parse_stream_fields_component_pages")

# https://www.caktusgroup.com/blog/2019/09/12/wagtail-data-migrations/

# <a id="3" linktype="page">link</a> link to a page
# <a id="1" linktype="document">link</a> link to a doc
# <a href="mailto:nick@nick.com">link</a> email link
# <a href="tel:01212">0121</a> phone link
# tables show ok but disapear after any save in the admin

# Super big note:
# after the pages are all imported plus all other content we need to move page content into blocks
# everything is a stream field, has to be that way for imported pages, possibly posts and blogs too...
# LINKS during this parsing and rich text fields need to be altered to consider internal liks to page types
# need to find the page link id for the stream field anchor
# DOWNLOADS and docs, and anythiong else that pops up
# need to get and upload documents
# IMAGES they too need to be uploaded to image manager and linked accordingly, well set everything to left align for now
########


class Command(BaseCommand):
    help = "parsing stream fields component pages"

    def __init__(self):
        super().__init__()
        models = [
            BasePage,
            ComponentsPage,
            Blog,
            Post,
            AtlasCaseStudy,
            Publication,
            LandingPage,
        ]

        self.url_map = {}  # cached

        for model in models:
            pages = model.objects.all()
            for page in pages:
                self.url_map[page.url] = {
                    "id": page.id,
                    "slug": page.slug,
                    "title": page.title,
                }

        # self.rich_text_builder = RichTextBuilder(self.url_map)

    def add_arguments(self, parser):
        parser.add_argument(
            "mode", type=str, help="Run as development with reduced recordsets"
        )

    def handle(self, *args, **options):
        pages = []
        if options["mode"] == "dev":
            """# dev get a small set of pages"""
            # components_parent = BasePage.objects.get(wp_id=62659, source='pages')
            components_parent = ComponentsPage.objects.get(wp_id=78673, source="pages")
            pages = ComponentsPage.objects.descendant_of(
                components_parent, inclusive=True
            )
            # base_pages_under_components_page = BasePage.objects.descendant_of(components_parent, inclusive=True)
            # pages = []
            # for page in base_pages:
            #     pages.append(page)
            # for page in base_pages_under_components_page:
            #     pages.append(page)

        if options["mode"] == "prod":
            """get all the pages"""
            pages = ComponentsPage.objects.all()
        # pages = ComponentsPage.objects.all()
        component_types = []  # just for dev to check we have them all
        """
        [
            'promo_component', # parse
            'article_component', # parse
            'two_columns_section', # parse
            'topic_section_component', # parse
            'breadcrumbs', ###
            'visit_nhsuk_infobar',
            'priorities_component'
        """
        # loop though each page look for the content_fields with default_template_hidden_text_blocks
        for page in pages:
            logger.info("⌛️ {} processing...".format(page))
            # keep the dates as when imported
            first_published_at = page.first_published_at
            last_published_at = page.last_published_at
            latest_revision_created_at = page.latest_revision_created_at

            body = []

            # then add any content fields if a field block has been used

            if page.component_fields:
                print(page, page.id)
                components = ast.literal_eval(page.component_fields)[0]
                builder = ComponentsBuilder(
                    ast.literal_eval(components["components"]), self.url_map
                )
                blocks = builder.make_blocks()
                body = blocks

            page.body = json.dumps(body)

            # dealing with unicode in title
            page.title = unescape(page.title)

            rev = page.save_revision()
            page.first_published_at = first_published_at
            page.last_published_at = last_published_at
            page.latest_revision_created_at = latest_revision_created_at
            page.save()
            rev.publish()

            logger.info("✅ {} done".format(page))

            # if page.title == 'About us':
            #     sys.exit()
