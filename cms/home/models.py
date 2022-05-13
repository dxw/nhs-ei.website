from cms.core.blocks import CoreBlocks
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import StreamFieldPanel
from wagtailnhsukfrontend.mixins import HeroMixin


class HomePage(HeroMixin, Page):
    max_num = 1
    body = StreamField(CoreBlocks, blank=True)
    content_panels = (
        Page.content_panels + HeroMixin.content_panels + [StreamFieldPanel("body")]
    )
