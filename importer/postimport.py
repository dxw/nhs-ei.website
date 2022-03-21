import ast
import json
import logging
import re
from html import unescape

from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.db import DataError
from wagtail.images.models import Image

from cms.atlascasestudies.models import AtlasCaseStudy
from cms.blogs.models import Blog
from cms.core.models import ParseList
from cms.pages.models import BasePage, ComponentsPage, LandingPage
from cms.posts.models import Post
from cms.publications.models import Publication
from importer.richtextbuilder import RichTextBuilder
from importer.types import trim_long_text

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


def parse_all_updated():
    # TODO For now we separate the post parsing so we can run it easily
    # later we will merge it up to do_refresh

    # call_command("parse_stream_fields", "prod")
    # call_command("parse_stream_fields_component_pages", "prod")
    # call_command("make_documents_list")

    page_parser = Parser()

    process_list = ParseList.objects.all()
    logger.info("Parsing %d new or updated pages" % len(process_list))
    for process_candidate in process_list:
        if not process_candidate.slug_fixed:
            fix_slug(process_candidate)
        if not process_candidate.html_parsed:
            page_parser.parse(process_candidate)

        # check state and clear if completed
        if process_candidate.slug_fixed and process_candidate.html_parsed:
            process_candidate.delete()


class Parser:
    def __init__(self):
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

        self.block_builder = RichTextBuilder(self.url_map)

    def parse(self, process_candidate):
        page = process_candidate.target.specific_class.objects.get(
            id=process_candidate.target.id
        )
        if isinstance(page, Blog):
            logger.info("⌛️ Skipping Blog page %s" % page.__class__)
            process_candidate.html_parsed = True
            process_candidate.save()
            return
        if isinstance(page, Post):
            logger.info("⌛️ Skipping Post page %s" % page.__class__)
            process_candidate.html_parsed = True
            process_candidate.save()
            return
        if isinstance(page, Publication):
            logger.info("⌛️ Skipping Publication page %s" % page.__class__)
            process_candidate.html_parsed = True
            process_candidate.save()
            return

        logger.info(f"⌛️ {page} processing ")
        # keep the dates as when imported
        # if page.title == 'Join the NHS COVID-19 vaccine team':
        first_published_at = page.first_published_at
        last_published_at = page.last_published_at
        latest_revision_created_at = page.latest_revision_created_at

        body = []  # the stream field
        # get this to make a stream field
        raw_content = page.raw_content

        # deal first with wysiwyg from wordpress
        # """ cant deal with forms, needs investigating """
        if raw_content and "<form action=" in raw_content:
            logger.critical("FORM FOUND: %s | %s | %s", page, page.id, page.wp_link)
        if raw_content:
            # line breaks mess up bs4 parsing, we dont need them anyway :)
            raw_content = raw_content.replace("\n", "")
            raw_content_block = self.make_text_block(raw_content, page)

            for row in raw_content_block:
                body.append(row)

        # then add any content fields if a field block has been used
        # AFAIK these are always after the body
        if page.content_fields:
            content_fields = ast.literal_eval(page.content_fields)
            for field in content_fields:
                keys = field.keys()
                for key in keys:
                    if (
                        key == "default_template_hidden_text_blocks"
                        and field["default_template_hidden_text_blocks"] != "False"
                    ):
                        # if len(page.content_fields) > 0:
                        content_fields = self.make_expander_group_block(
                            page.content_fields, page
                        )
                        for content_field in content_fields:
                            body.append(content_field)

                        # body.append(content_blocks)

        # print(body)
        # sys.exit()
        page.body = json.dumps(body)

        # dealing with unicode in title
        page.title = unescape(page.title)

        rev = page.save_revision()
        page.first_published_at = first_published_at
        page.last_published_at = last_published_at
        page.latest_revision_created_at = latest_revision_created_at
        page.save()
        rev.publish()
        process_candidate.html_parsed = True

    def make_text_block(self, content, page):
        # here need to see whats in there and pull out specials like tables
        # and so on
        # into their own block type
        # so far TABLE https://service-manual.nhs.uk/design-system/components
        # /table

        block_group = self.find_content_types_to_make_blocks(
            content, page
        )  # all the elements pulled out as we find them

        return block_group

    def find_content_types_to_make_blocks(self, content, page):

        TAGS_TO_BLOCKS = ["table", "iframe"]

        REMOVE_ATTRIBUTES = [
            "lang",
            "language",
            "onmouseover",
            "onmouseout",
            "script",
            "style",
            "font",
            "dir",
            "face",
            "size",
            "color",
            "style",
            "class",
            "width",
            "height",
            "hspace",
            "border",
            "valign",
            "align",
            "background",
            "bgcolor",
            "text",
            "link",
            "vlink",
            "alink",
            "cellpadding",
            "cellspacing",
        ]

        soup = BeautifulSoup(content, "lxml", exclude_encodings=True)

        iframes = soup.find_all("iframe")

        # '[document]' means leave it alone
        IFRAME_POSSIBLE_PARENTS = ["p", "div", "span"]

        for iframe in iframes:
            parent = iframe.previous_element
            if parent.name in IFRAME_POSSIBLE_PARENTS:
                # print(parent)
                parent.replaceWith(iframe)

        for attribute in REMOVE_ATTRIBUTES:
            for tag in soup.find_all(attrs={attribute: True}):
                del tag[attribute]

        soup = soup.find("body").findChildren(recursive=False)

        blocks = []
        block_value = ""
        counter = 0

        for tag in soup:

            counter += 1

            """
            the process here loops though each soup tag to discover the block
            type to use
            there's a table and iframe block to deal with if they exist
            """

            # print(tag.name)
            if not tag.name in TAGS_TO_BLOCKS:

                images = tag.find_all("img")

                # img.replaceWith(new_image)
                # it's a simple text field so concat all text
                # self.block_builder.extract_img(str(tag), page)
                self.block_builder.extract_links(str(tag), page)
                linked_html = str(tag)
                for link in self.block_builder.change_links:
                    linked_html = linked_html.replace(str(link[0]), str(link[1]))

                # replace any img elements with str.replace, problem
                # uploading image
                # as cant get correct src so missing images are marked and
                # logged
                for img in images:
                    img_string = str(img)
                    src = (
                        "original_images/" + img.get("src").split("/")[-1]
                    )  # need the last part
                    alt = img.get("alt")
                    new_image = None
                    try:
                        image = Image.objects.get(file=src)
                        new_image = self.block_builder.make_image_embed(
                            image.id, alt, "fullwidth"
                        )
                        linked_html = linked_html.replace(img_string, new_image)
                    except Image.DoesNotExist:
                        logger.warning(
                            "Missing image: %s | %s | %s", img["src"], page, page.id
                        )
                    if not new_image:
                        linked_html = (
                            linked_html + '<h3 style="color:red">missing ' "image</h3>"
                        )
                block_value += linked_html

            if tag.name == "table":

                if len(block_value) > 0:
                    blocks.append({"type": "text", "value": block_value})
                    block_value = ""
                blocks.append({"type": "html", "value": str(tag)})

            if tag.name == "iframe":

                if len(block_value) > 0:
                    blocks.append({"type": "text", "value": block_value})
                    block_value = ""
                blocks.append(
                    {
                        "type": "html",
                        "value": '<div class="core-custom"><div class="responsive-iframe">{}</div></div>'.format(
                            str(tag)
                        ),
                    }
                )

            if counter == len(soup) and len(block_value) > 0:
                # when we reach the end and somehing is in the
                # block_value just output and clear

                blocks.append({"type": "text", "value": block_value})
                block_value = ""

        return blocks

    def make_expander_group_block(self, content, page):
        content = ast.literal_eval(content)
        if len(content) and "default_template_hidden_text_section_title" in content[0]:
            title = content[0]["default_template_hidden_text_section_title"]
        else:
            title = "Unknown title"
            logger.warn("Missing title: %s | %s", page, page.id)

        if (
            len(content) > 0
            and "default_template_hidden_text_section_title" in content[1]
        ):
            expander_list = content[1]  # (a list of expanders)
            expanders = ast.literal_eval(
                expander_list["default_template_hidden_text_blocks"]
            )
        else:
            expanders = []
            logger.warning("Empty expander list: %s | %s", page, page.id)

        """
        {
            'type': 'expander_group',
            'value': {
                'expanders': [
                    {'title': 'asdfasf', 'body': [
                        {'type': 'richtext', 'value': '<p>asdfsadfa</p>'}
                    ]
                    },
                    {'title': 'asdfasdfa', 'body': [
                        {'type': 'richtext', 'value': '<p>asdfasdfasdfsa</p>'}
                    ]
                    },
                    {'title': 'asdfasdfafasdf asd', 'body': [
                        {'type': 'richtext', 'value': '<p>asdf dfs asdfa</p>'}
                    ]
                    }
                ]
            },
        }
        """

        block_title = {"type": "text", "value": ""}

        block_group = {
            "type": "expander_group",
            "value": {"expanders": []},
        }

        for expander in expanders:
            summary = expander["default_template_hidden_text_summary"]
            details = expander["default_template_hidden_text_details"]

            if not details:
                details = "<p></p>"
                logger.warn(
                    "Empty details expander given an empty paragraph tag on "
                    "%s (%s): summary %s",
                    page.title,
                    page.wp_id,
                    repr(summary),
                )
            # for item in field['items']:
            item_detail = details
            self.block_builder.extract_links(details, page)
            for link in self.block_builder.change_links:
                item_detail = item_detail.replace(str(link[0]), str(link[1]))
            block_item = {
                "title": summary,
                "body": [{"type": "richtext", "value": item_detail}],
            }
            block_group["value"]["expanders"].append(block_item)

        if title:
            block_title["value"] = "<h3>{}</h3>".format(title)
            return [block_title, block_group]
        else:
            return [block_group]

    def make_panel_block(self, content):
        """
        {
            'type': 'panel',
            'value': {
                'label': 'optional label',
                'body': 'required body'
            }
        }
        """
        # rich_text = self.block_builder.extract_links(content)
        self.block_builder.extract_links(content)
        for link in self.block_builder.change_links:
            content = content.replace(str(link[0]), str(link[1]))
        block = {
            "type": "panel",
            "value": {
                "label": "",
                # this is the default, might want to change it...
                "heding_level": "3",
                # after it's been parsed for links
                "body": content,
            },
        }

        return block
