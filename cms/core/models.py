from django.db import models
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField
from wagtail.core.models import ClusterableModel, ParentalKey
from wagtailmenus.models import AbstractMainMenuItem


@register_setting
class CoreSettings(BaseSetting, ClusterableModel):
    alert_banner = RichTextField()
    is_visible = models.BooleanField(default=False, blank=True)

    header_extra = models.TextField(blank=True, null=True)
    footer_extra = models.TextField(blank=True, null=True)

    panels = [
        MultiFieldPanel(
            [FieldPanel("alert_banner"), FieldPanel("is_visible")],
            heading="Alert Banner",
        ),
        MultiFieldPanel(
            [
                FieldPanel("header_extra"),
                FieldPanel("footer_extra"),
            ],
            heading="Extra header and footer code",
            help_text="You can add valid html code snippets here such as "
            "analytics code or other scripts",
        ),
    ]


class ExtendedMainMenuItem(AbstractMainMenuItem):

    menu = ParentalKey(
        "wagtailmenus.MainMenu",
        on_delete=models.CASCADE,
        related_name="extended_menu_items",
    )

    caption = models.CharField(
        max_length=250,
        blank=True,
        help_text="Additional explanatory text which appears alongside this menu item",
    )

    panels = (
        PageChooserPanel("link_page"),
        FieldPanel("link_url"),
        FieldPanel("url_append"),
        FieldPanel("link_text"),
        FieldPanel("caption"),
        FieldPanel("allow_subnav"),
    )
