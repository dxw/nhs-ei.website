import logging

from django import template
from wagtail.core.models import Page
from django.urls import reverse
from cms.settings.base import NHSEI_MAX_MENU_CAPTION_LENGTH

register = template.Library()
logger = logging.getLogger("general")


@register.filter
def get_caption(caption_item_id):
    try:
        item_id = int(caption_item_id)
        try:
            page = Page.objects.get(id=item_id)
            specific_page = page.specific_class.objects.get(id=item_id)
            if hasattr(specific_page, "excerpt"):
                excerpt = specific_page.excerpt
                if len(excerpt) > NHSEI_MAX_CATION_LENGTH:
                    return excerpt[0:NHSEI_MAX_CATION_LENGTH]
                else:
                    return excerpt
        except Page.DoesNotExist:
            logger.error("Unable to locate page for item_id = %d" % item_id)
    except:
        logger.warning(
            "ID passed to get caption was not a number: '%s'" % caption_item_id
        )

    return ""


@register.filter
def url_for(item):
    page = Page.objects.get(id=item.link_page_id)
    return reverse("browse", args={page.slug})


@register.inclusion_tag("browse/breadcrumb.html", takes_context=True)
def menu_breadcrumb(context):
    url_path = context.request.path
    if url_path[0:8] == "/browse/":
        breadcrumb_pages = [
            {
                "label": "Home",
                "href": "/browse/",
            }
        ]
        path_components = url_path.split("/")
        if path_components[1] == "browse":
            # make menu bread crumbs
            if path_components[2]:
                for component in path_components[2:]:
                    try:
                        page = Page.objects.get(slug=component)
                        item = {
                            "label": page.title,
                            "href": reverse("browse", args={page.slug}),
                        }
                        breadcrumb_pages.append(item)
                    except Page.DoesNotExist:
                        # Just in case there is a non-page item in the list
                        pass

        return {
            "breadcrumbs": breadcrumb_pages,
        }

    return {}
