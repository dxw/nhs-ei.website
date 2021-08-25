from django.template.defaultfilters import default, filesizeformat
from wagtail.core.blocks import (
    StructBlock,
    RawHTMLBlock,
    CharBlock,
    StreamBlock,
    ListBlock,
    ChooserBlock,
)
from wagtail.core.blocks.field_block import (
    BooleanBlock,
    ChoiceBlock,
    DecimalBlock,
    IntegerBlock,
    MultipleChoiceBlock,
    PageChooserBlock,
    RichTextBlock,
    URLBlock,
)
from wagtail.documents.blocks import DocumentChooserBlock

from wagtailnhsukfrontend.blocks import (
    ActionLinkBlock,
    CareCardBlock,
    DetailsBlock,
    DoBlock,
    DontBlock,
    ExpanderBlock,
    ExpanderGroupBlock,
    FlattenValueContext,
    CardFeatureBlock,
    InsetTextBlock,
    ImageBlock,
    CardGroupBlock,
    WarningCalloutBlock,
    CardImageBlock,
    SummaryListBlock,
)

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
        group="custom",
        help_text="""
            Use this block to add raw html
        """,
        template="blocks/html_block.html",
    )


class LinkListBlock(StructBlock):
    footer_links = ListBlock(
        StructBlock(
            [
                ("text", CharBlock()),
                ("page", PageChooserBlock()),
                ("external_link", URLBlock()),
            ]
        )
    )


class FooterBlocks(StreamBlock):
    footer_links = LinkListBlock(group="Custom")
