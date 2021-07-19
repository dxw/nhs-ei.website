from cms.categories.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.fields.related import ForeignKey
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class PostIndexPage(Page):
    # title already in the Page class
    # slug already in the Page class
    subpage_types = ["posts.Post"]
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_latest_posts(num):
        return Post.objects.all().order_by("-first_published_at")[:num]

    def get_context(self, request, *args, **kwargs):
        post_ordering = "-first_published_at"
        context = super().get_context(request, *args, **kwargs)

        if request.GET.get("category"):
            context["chosen_category_id"] = int(request.GET.get("category"))
            posts = (
                Post.objects.child_of(self)
                .live()
                .order_by(post_ordering)
                .filter(
                    post_category_relationship__category=request.GET.get("category")
                )
            )
        else:
            posts = Post.objects.child_of(self).live().order_by(post_ordering)

        paginator = Paginator(posts, 16)

        try:
            items = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context["posts"] = items
        context["categories"] = Category.objects.all()

        return context


class PostCategoryRelationship(models.Model):
    post = ParentalKey(
        "posts.Post",
        related_name="post_category_relationship",
    )
    category = ForeignKey(
        "categories.Category",
        related_name="+",
        on_delete=models.CASCADE,
    )


class Post(Page):

    parent_page_types = ["posts.PostIndexPage"]
    """
    title already in the Page class
    slug already in the Page class
    going to need to parse the html here to extract the text
    """

    # going to need to parse the html here to extract the text
    body = RichTextField(blank=True)

    """ coming across form wordpress need to keep for now"""
    wp_id = models.PositiveIntegerField(null=True)
    source = models.CharField(null=True, max_length=100)
    wp_slug = models.TextField(null=True, blank=True)
    wp_link = models.TextField(null=True, blank=True)

    """i think we can do away with this field
    and use the text from body to create the exceprt"""
    # excerpt = RichTextField(blank=True)

    author = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        InlinePanel("post_category_relationship", label="Categories"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("wp_id"),
                FieldPanel("author"),
                FieldPanel("source"),
                FieldPanel("wp_slug"),
                FieldPanel("wp_link"),
            ],
            heading="wordpress data we dont need in the end",
            classname="collapsed collapsible",
        ),
    ]
