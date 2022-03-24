import logging

from django import template
from wagtail.core.models import Page

from cms.settings.base import NHSEI_MAX_CATION_LENGTH

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
                    return excerpt[0:NHSEI_MAX_CATION_LENGTH] + "..."
                else:
                    return excerpt
        except Page.DoesNotExist:
            logger.error("Unable to locate page for item_id = %d" % item_id)
    except:
        logger.warning(
            "ID passed to get caption was not a number: '%s'" % caption_item_id
        )

    return ""


from django.urls import reverse, path


@register.filter
def url_for(item):
    page = Page.objects.get(id=item.link_page_id)
    return reverse("browse", args={page.slug})
