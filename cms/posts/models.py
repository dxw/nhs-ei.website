from cms.categories.models import Category, CategoryPage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class PostIndexPage(Page):
    # title and slug come from the Page class
    subpage_types = ["posts.Post"]
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_latest_posts(num):
        return Post.objects.all().order_by("-latest_revision_created_at")[:num]

    def get_context(self, request, *args, **kwargs):
        post_ordering = "-latest_revision_created_at"
        context = super().get_context(request, *args, **kwargs)

        if request.GET.get("category"):
            context["chosen_category_id"] = int(request.GET.get("category"))
            posts = (
                Post.objects.child_of(self)
                .live()
                .order_by(post_ordering)
                .filter(
                    categorypage_category_relationship__category=request.GET.get(
                        "category"
                    )
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


class Post(CategoryPage):
    class Meta:
        verbose_name = "News"

    parent_page_types = ["posts.PostIndexPage"]
    """
    title already in the Page class
    slug already in the Page class
    going to need to parse the html here to extract the text
    """

    # going to need to parse the html here to extract the text
    body = RichTextField(blank=True)

    """ coming across form wordpress need to keep for now"""
    wp_id = models.PositiveIntegerField(null=True, blank=True)
    source = models.CharField(null=True, max_length=100, blank=True)

    wp_slug = models.TextField(null=True, blank=True)
    wp_link = models.TextField(null=True, blank=True)

    author = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        InlinePanel("categorypage_category_relationship", label="Categories"),
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
