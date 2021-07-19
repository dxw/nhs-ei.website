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
    PageChooserBlock,
    RichTextBlock,
    URLBlock,
)
from wagtail.documents.blocks import DocumentChooserBlock


class JumpMenuBlock(StructBlock):
    # this block renders a list of indivual anchor links as a jump menu
    # used in conjunction with the Named Anchor block
    menu = ListBlock(StructBlock([("title", CharBlock()), ("menu_id", CharBlock())]))

    class Meta:
        icon = "order-down"
        template = "blocks/jump_menu_block.html"
        help_text = 'Add a list of named anchors that correspond to the Named achors below e.g. "document-name"'


class NamedAnchorBlock(StructBlock):
    # this block is to render a named anchor for the jump menu
    # you can also add the heading if required
    anchor_id = CharBlock()
    heading = CharBlock(required=False)

    class Meta:
        icon = "placeholder"
        template = "blocks/named_anchor_block.html"
        help_text = 'Add a named place holder to jump to e.g. "document-name" with an optional heading'


class DocumentBlock(StructBlock):
    title = RichTextBlock(required=False)
    document = DocumentChooserBlock()
    summary = RichTextBlock(required=False)

    class Meta:
        icon = "doc"
        template = "blocks/document_block.html"
        help_text = "Choose or upload a document"

    def get_context(self, value, parent_context):
        context = super().get_context(value, parent_context)
        context["file_ext"] = value["document"].file_extension
        context["file_size"] = filesizeformat(value["document"].get_file_size())

        return context


class DocumentLinkBlock(StructBlock):
    title = RichTextBlock(required=False)
    external_url = URLBlock(required=False)
    page = PageChooserBlock(required=False)
    summary = RichTextBlock(required=False)

    class Meta:
        icon = "doc"
        template = "blocks/document_link_block.html"
        help_text = "Choose or upload a document"


class DocumentEmbedBlock(StructBlock):
    title = RichTextBlock(required=False)
    html = RawHTMLBlock()

    class Meta:
        icon = "doc"
        template = "blocks/document_embed_block.html"
        help_text = "Choose or upload a document"


class DocumentGroupBlock(StreamBlock):
    document = DocumentBlock()
    document_link = DocumentLinkBlock()
    document_embed = DocumentEmbedBlock()
    free_text = RichTextBlock()

    class Meta:
        icon = "placeholder"
        help_text = "Add any number of related documents"
        template = "blocks/document_group_block.html"


class PublicationsBlocks(StreamBlock):
    document_group = DocumentGroupBlock(group="Custom")
    jump_menu = JumpMenuBlock(group="Custom")
    named_anchor = NamedAnchorBlock(group="Custom")
