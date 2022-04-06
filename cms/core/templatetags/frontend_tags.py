import logging

from django import template
from wagtail.core.models import Page

register = template.Library()
logger = logging.getLogger("general")


@register.inclusion_tag("tags/breadcrumb.html", takes_context=True)
def breadcrumb(context):
    """
    Generates an array of pages which are passed to the breadcrumb template.
    """
    page = context.get("page", None)
    if isinstance(page, Page):
        site = page.get_site()
        breadcrumb_pages = []

        # Traverse the page parents with get_parent() until we hit a site root
        while page.id != site.root_page_id and not page.is_root():
            page = page.get_parent()
            breadcrumb_pages = [page] + breadcrumb_pages

        return {
            "breadcrumb_pages": breadcrumb_pages,
        }

    return {}

    # else:
    #     raise Exception("'page' not found in template context")


@register.inclusion_tag("tags/content_type_tag.html", takes_context=True)
def get_content_type_tag(context, page):
    result_page = Page.objects.get(id=page.id)
    content_type = result_page.content_type
    CONTENT_TYPE_LABELS = {
        "post": "News",
        "blog": "Blog",
        "publication": "Publication",
    }
    if content_type.model in CONTENT_TYPE_LABELS.keys():
        return {"type": CONTENT_TYPE_LABELS[content_type.model]}
