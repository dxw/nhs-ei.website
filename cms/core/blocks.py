from wagtail.core.blocks import (
    RawHTMLBlock,
    StreamBlock,
    StructBlock,
    CharBlock,
    ListBlock,
    URLBlock,
)
from wagtail.core.blocks.field_block import (
    RichTextBlock,
    PageChooserBlock,
)

from wagtail.images.blocks import (
    ImageChooserBlock,
)

from wagtailnhsukfrontend.blocks import (
    ActionLinkBlock,
    CareCardBlock,
    DetailsBlock,
    DoBlock,
    DontBlock,
    ExpanderBlock,
    ExpanderGroupBlock,
    CardFeatureBlock,
    InsetTextBlock,
    ImageBlock,
    CardGroupBlock,
    WarningCalloutBlock,
    CardImageBlock,
    SummaryListBlock,
)

from django.core.exceptions import ValidationError

import cms.categories.blocks

RICHTEXT_FEATURES_ALL = [
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "bold",
    "italic",
    "ol",
    "ul",
    "hr",
    "link",
    "document-link",
    "image",
    "embed",
    "code",
    "superscript",
    "subscript",
    "strikethrough",
    "blockquote",
]

NHS_UK_URL = "https://nhs.uk/"


def validate_nhsuk_url(value):
    if not value.startswith(NHS_UK_URL):
        raise ValidationError(f"URL does not start with {NHS_UK_URL}")


class VisitNhsukInfobarBlock(StructBlock):
    """
    wp_name: visit_nhsuk_infobar
    Note that the wp version has no fields, but we're adding a name
    for the specific form of healthcare and a custom URL.
    """

    topic = CharBlock(
        help_text='Fills in the sentence: "For any medical advice relating to _____ please visit nhs.uk". May be blank.',
        required=False,
    )
    url = URLBlock(
        help_text=f"URL user is guided to. Must start {NHS_UK_URL} .",
        required=True,
        default=NHS_UK_URL,
        validators=[validate_nhsuk_url],
    )

    class Meta:
        icon = "user"
        template = "blocks/visit_nhsuk_infobar_block.html"
        help_text = "Recommends users find medical advice at nhs.uk"


class PageHeadingBlock(StructBlock):
    text = RichTextBlock()
    image = ImageChooserBlock(required=False)

    class Meta:
        template = "blocks/page_heading_block.html"


class PromotedLinkBlock(StructBlock):
    title = CharBlock()
    image = ImageChooserBlock()
    link = PageChooserBlock()


class PromotedLinksBlock(StructBlock):
    links = ListBlock(PromotedLinkBlock())

    class Meta:
        template = "blocks/promo_links_block.html"


class CoreBlocks(StreamBlock):
    action_link = ActionLinkBlock(group="Base")
    care_card = CareCardBlock(group="Base")
    details = DetailsBlock(group="Base")
    do_list = DoBlock(group="Base")
    dont_list = DontBlock(group="Base")
    expander = ExpanderBlock(group="Base")
    expander_group = ExpanderGroupBlock(group="Base")
    inset_text = InsetTextBlock(group="Base")
    image = ImageBlock(group="Base")
    panel = CardFeatureBlock(group="Base")
    panel_list = CardGroupBlock(group="Base")
    # panel_with_image = PanelBlockWithImage(group='Base')
    warning_callout = WarningCalloutBlock(group="Base")
    summary_list = SummaryListBlock(group="Base")
    promo = CardImageBlock(group="Base")
    promo_group = CardGroupBlock(group="Base")
    page_heading = PageHeadingBlock(group="Custom")
    promoted_links = PromotedLinksBlock(group="Custom")
    visit_nhsuk = VisitNhsukInfobarBlock(group="Custom")

    recent_posts = cms.categories.blocks.RecentPostsBlock(group="Custom")
    text = RichTextBlock(
        group="Custom",
        help_text="""
            Use this block to add formatted text into a page e.g.
            paragraph with heading and/or links and images
        """,
        template="blocks/text_block.html",
        features=RICHTEXT_FEATURES_ALL,
    )
    html = RawHTMLBlock(
        group="Custom",
        help_text="""
            Use this block to add raw html
        """,
        template="blocks/html_block.html",
    )
