from cms.core.blocks import CoreBlocks
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtailnhsukfrontend.mixins import HeroMixin


class HomePage(HeroMixin, Page):
    max_num = 1
    body = StreamField(CoreBlocks, blank=True)
    content_panels = (
        Page.content_panels + HeroMixin.content_panels + [StreamFieldPanel("body")]
    )
