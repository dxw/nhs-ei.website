from django import template
from cms.publications.models import PublicationIndexPage, TOC

register = template.Library()


@register.simple_tag
def get_lastest_publications_columns(num):
    return [
        PublicationIndexPage.get_latest_publications(num)[:2],
        PublicationIndexPage.get_latest_publications(num)[2:],
    ]


@register.inclusion_tag("publications/toc.html")
def get_toc(obj):
    toc_items = []
    if obj:
        toc_items = TOC.objects.filter(page=obj)

    return {"toc_items": toc_items}
