import logging
import re
import sys

from django.core.exceptions import ValidationError
from django.core.validators import slug_re
from django.db import DataError
from django.utils.html import strip_tags
from wagtail.core.models import Page

from cms.core.models import ParseList
from cms.pages.models import ComponentsPage, BasePage
from importer.types import trim_long_text
from importer.utils import URLParser

logger = logging.getLogger("parser")


def strip_chars(text):
    return re.sub(r"\W+", "-", text)


def save_slug(page):
    try:
        page.save()
        return True
    except ValidationError as e:
        print(e)
        return False
    except DataError as e:
        return False


def fix_slug(process_candidate):
    page = process_candidate.target
    logger.debug("Fixing slug for %s" % page)
    # There are a _lot_ of name clashes, we'll build a slug based and increment it if needed
    base_slug = strip_chars(trim_long_text(strip_chars(page.title), 251))
    slug = base_slug
    counter = 1
    while counter < 100:
        page.slug = slug
        try:
            page.save()
            process_candidate.slug_fixed = True
            process_candidate.save()
            logger.debug("Updated slug to '%s' for '%s'" % (page.slug, page))
            return
        except ValidationError as e:
            slug = base_slug + "-" + "%02d" % counter
            counter += 1
        except DataError as e:
            logger.error(page, e)
            return
    logger.error("Could not find a slug for %s" % page)


def fix_html(process_candidate):
    page = process_candidate.target
    # at this point it could be a Basepage or a Component page, we need to try for each


def parse_all_updated():
    # TODO For now we separate the post parsing so we can run it easily
    # later we will merge it up to do_refresh

    # call_command("parse_stream_fields", "prod")
    # call_command("parse_stream_fields_component_pages", "prod")
    # call_command("make_documents_list")

    process_list = ParseList.objects.all()
    logger.info("Parsing %d new or updated pages" % len(process_list))
    for process_candidate in process_list:
        if not process_candidate.slug_fixed:
            fix_slug(process_candidate)
        if not process_candidate.html_parsed:
            fix_html(process_candidate)

        # check state and clear if completed
        if process_candidate.slug_fixed and process_candidate.html_parsed:
            process_candidate.delete()


# class Parser:
#     home_page = None
#
#     def __init__(self):
#         self.home_page = Page.objects.get(title="Home")
