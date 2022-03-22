from django.db import models
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField
from wagtail.core.models import ClusterableModel, ParentalKey, Page
from wagtail.documents.models import Document
from wagtail.images.models import Image
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


"""
We tried to extend the abstract models for image and document and then change
the BASE_IMAGE/DOC values but this caused a foreign key to be created on the
custom_logo setting in wagtailnhsfrontend. That package is included as is and
if we update that model future model updates may beak because of that key.
"""


class ImageImportBridge(models.Model):
    """
    Temp model to track images as imported.
    TODO: factor out after launch
    """

    wp_id = models.CharField(max_length=32, null=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class DocImportBridge(models.Model):
    """
    Temp model to track files as imported.
    TODO: factor out after launch
    """

    wp_id = models.CharField(max_length=32, null=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)


class ParseList(models.Model):
    """
    This is a list of new pages that needs to be split into content blocks
    """

    target = models.ForeignKey(Page, on_delete=models.CASCADE)
    slug_fixed = models.BooleanField(default=False)
    html_parsed = models.IntegerField(default=False)
