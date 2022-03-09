from cms.categories.models import Category, CategoryPage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class BlogIndexPage(Page):
    # title already in the Page class
    # slug already in the Page class
    subpage_types = ["blogs.Blog"]
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_latest_blogs(self, num):
        return Blog.objects.all().order_by("-latest_revision_created_at")[:num]

    def get_context(self, request, *args, **kwargs):
        blog_ordering = "-latest_revision_created_at"
        context = super().get_context(request, *args, **kwargs)

        if request.GET.get("category"):
            context["chosen_category_id"] = int(request.GET.get("category"))
            blogs = (
                Blog.objects.live()
                .order_by(blog_ordering)
                .filter(
                    categorypage_category_relationship__category=request.GET.get(
                        "category"
                    )
                )
            )
        else:
            blogs = Blog.objects.live().order_by(blog_ordering)

        paginator = Paginator(blogs, 16)

        try:
            items = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context["blogs"] = items
        # the categories context isn't used but is tested for and we'll
        # probably want to reinstate it.
        context["categories"] = Category.objects.all()
        return context


class Blog(CategoryPage):
    parent_page_types = ["blogs.BlogIndexPage"]
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

    """i think we can do away with this field
    and use the text from body to create the exceprt"""
    # excerpt = RichTextField(blank=True)

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
