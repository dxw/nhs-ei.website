# Blocks designed to mimic the behaviour of existing NHS Advanced Custom Fields

from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from django.core.exceptions import ValidationError

# ===============================
# Looking for a RecentPostsBlock?
# It's in cms.categories.blocks
#
# Not added a PromoBlock -- might already be in Base?
# ===============================

NHS_UK_URL = "https://nhs.uk"


def validate_nhsuk_url(value):
    if not value.startswith(NHS_UK_URL):
        raise ValidationError(f"URL does not start with {NHS_UK_URL}")


class VisitNhsukInfobarBlock(blocks.StructBlock):
    """
    wp_name: visit_nhsuk_infobar
    Note that the wp version has no fields, but we're adding a name
    for the specific form of healthcare and a custom URL.
    """

    topic = blocks.CharBlock(
        help_text='Fills in the sentence: "For any medical advice relating to _____ please visit nhs.uk". May be blank.',
        required=False,
    )
    url = blocks.URLBlock(
        help_text=f"URL user is guided to. Must start {NHS_UK_URL} .",
        required=True,
        default=NHS_UK_URL,
        validators=[validate_nhsuk_url],
    )

    class Meta:
        icon = "user"
        template = "blocks/acf/visit_nhsuk_infobar_block.html"
        help_text = "Recommends users find medical advice at nhs.uk"


class TopicBlock(blocks.StructBlock):
    "wp's 'topic_section_component' is a list of these"
    title = blocks.CharBlock()  # topic_title in wp
    content = (
        blocks.CharBlock()
    )  # topic_content in wp; is <p>text</p> ... might be full HTML?
    page = blocks.PageChooserBlock()  # topic_url in wp

    class Meta:
        icon = "user"
        template = "blocks/acf/topic_block.html"
        help_text = "A topic."


class TopicSectionBlock(blocks.StructBlock):
    "wp: 'topic_section_component'"
    title = blocks.CharBlock()
    topics = blocks.ListBlock(child_block=TopicBlock)

    class Meta:
        icon = "user"
        template = "blocks/acf/topic_section_block.html"
        help_text = "Topics."


class PriorityBlock(blocks.StructBlock):
    "wp's 'priorities_component' is a list of these"
    highlight = blocks.BooleanBlock(required=False)  # nhsuk_highlight in wp
    title = blocks.CharBlock()  # priority_title in wp; contains stray HTML
    page = blocks.PageChooserBlock()  # priority_url in wp

    class Meta:
        icon = "user"
        template = "blocks/acf/priority_block.html"
        help_text = "A priority."


class PrioritiesBlock(blocks.StructBlock):
    "wp: 'priorities_component'"
    title = blocks.CharBlock()
    priorities = blocks.ListBlock(child_block=PriorityBlock)

    class Meta:
        icon = "user"
        template = "blocks/acf/priorities_block.html"
        help_text = "Priorities."


class VideoBlock(blocks.StructBlock):
    "wp: 'video_component'"
    title = blocks.CharBlock()  # wp: video_title
    # video_size: is_half_width
    # title_link: "" ???
    embed = EmbedBlock()  # wp: youtube_link
    content = blocks.RichTextBlock()  # wp: content, actual HTML (<a>) seen
    # video_background: false
    # video_background_colour: "" ???

    class Meta:
        icon = "user"
        template = "blocks/acf/video_block.html"
        help_text = "Video with description"


class ArticleBlock(blocks.StructBlock):
    "wp: 'article_component'"
    title = blocks.CharBlock()  # wp: article_title
    image = ImageChooserBlock()  # wp: article_image
    image_alignment = blocks.ChoiceBlock(
        [
            ["right", "right"],
            ["left", "left"],
        ],
        default="right",
    )  # wp: article_image_alignment; has-right-aligned-image
    image_size = blocks.ChoiceBlock(
        [
            ["half", "half width"],
            ["third", "one third width"],
            ["quarter", "one quarter width"],
        ],
        default="third",
    )  # wp:article_image_size; has-third-width-image
    # background # wp:article_background; false
    # background-colour #wp:article_background_colour: "#e8edee"
    content = blocks.RichTextBlock()  # wp: article_content; full HTML
    page = blocks.PageChooserBlock()  # wp: article_url, optional

    class Meta:
        icon = "user"
        template = "blocks/acf/article_block.html"
        help_text = (
            "A third-of-a-screen article about a page, either this one or another"
        )
