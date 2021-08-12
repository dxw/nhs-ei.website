from cms.categories.models import CategoryPage, Category
from django.forms import Select
import cms.posts.models
import cms.blogs.models
import cms.publications.models

from wagtail.core.blocks import ChooserBlock, StructBlock, CharBlock
from wagtail.core.blocks.field_block import (
    IntegerBlock,
    MultipleChoiceBlock,
    BooleanBlock,
)
from wagtailnhsukfrontend.blocks import FlattenValueContext


class CategoryBlock(ChooserBlock):
    # inspired by https://groups.google.com/g/wagtail/c/S26h5GP9_Fk/m/h2jeyhBnBAAJ
    target_model = Category
    widget = Select

    def value_from_form(self, value):
        # workaround for being passed an empty string instead of None
        # see https://github.com/wagtail/wagtail/issues/7344
        if value == "":
            return None
        else:
            return super().value_from_form(value)


class RecentPostsBlock(FlattenValueContext, StructBlock):
    """List recently modified CategoryPages"""

    title = CharBlock()
    type = MultipleChoiceBlock(
        choices=(
            ("post", "Post"),
            ("blog", "Blog"),
            ("publication", "Publications"),
            ("all", "All"),
        ),
        default=["post", "blog", "publication", "all"],
        help_text="All will get all pages that can have categories, regardless of other choices",
    )
    category = CategoryBlock(
        required=False, help_text="You may limit results to a single category"
    )
    num_posts = IntegerBlock(default=10, help_text="How many pages to show")
    see_all_link = BooleanBlock(
        required=False,
        default=True,
        blank=True,
        help_text="Link to full category page?",
    )

    class Meta:
        icon = "pick"
        template = "blocks/recent_posts_block.html"
        help_text = "Show recent pages of a particular category"

    def get_context(self, value, parent_context):
        context = super().get_context(value, parent_context=parent_context)
        num_to_show = int(value.get("num_posts"))
        page_types = value.get("type")
        page_type_lookup = {
            "post": cms.posts.models.Post,
            "blog": cms.blogs.models.Blog,
            "publication": cms.publications.models.Publication,
        }
        pages = CategoryPage.objects.live()
        category = value.get("category")
        if category:
            pages = pages.filter(categorypage_category_relationship__category=category)
        if "all" not in page_types:
            page_classes = [page_type_lookup[page_type] for page_type in page_types]
            pages = pages.type(*page_classes)
        limited_pages = pages.order_by("-last_published_at")[:num_to_show]
        page_data = [
            {
                "record": page,
                "tag": page.specific._meta.verbose_name.title(),
                "date": page.last_published_at,
            }
            for page in limited_pages
        ]
        context["queryset"] = {"posts": page_data}
        return context
