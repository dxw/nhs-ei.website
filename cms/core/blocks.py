from wagtail.core.blocks import (
    RawHTMLBlock,
    StreamBlock,
    StructBlock,
    CharBlock,
    ListBlock,
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

from .acf_blocks import (
    TopicSectionBlock,
    VisitNhsukInfobarBlock,
    PrioritiesBlock,
    VideoBlock,
    ArticleBlock,
)
import cms.categories.blocks
from wagtail.core import blocks as core_blocks

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

    visit_nhsuk_infobar = VisitNhsukInfobarBlock(group="ACF")
    topic_section = TopicSectionBlock(group="ACF")
    priorities = PrioritiesBlock(group="ACF")
    video = VideoBlock(group="ACF")
    recent_posts = cms.categories.blocks.RecentPostsBlock(group="ACF")
    article = ArticleBlock(group="ACF")

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
