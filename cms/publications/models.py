from urllib.parse import urlparse

from cms.categories.models import Category, PublicationType, CategoryPage
from cms.publications.blocks import PublicationsBlocks
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.fields.related import ForeignKey
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page


class PublicationIndexPage(Page):
    # title already in the Page class
    # slug already in the Page class
    subpage_types = ["publications.Publication"]
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Publications Index Page"
        verbose_name_plural = "Publications Index Pages"

    def get_latest_publications(num):
        return Publication.objects.all().order_by("-latest_revision_created_at")[:num]

    def get_context(self, request, *args, **kwargs):
        """
        Publications can have one or more categories (topics) or publications (publication_type).
        At the moment, you can only choose one or the other. I think that's best to avoid lots of empty
        result sets but we will need a decision made on that. TODO.
        """
        context = super().get_context(request, *args, **kwargs)
        publication_ordering = request.GET.get("order") or "-latest_revision_created_at"

        if request.GET.get("publication_type"):
            context["publication_type_id"] = int(request.GET.get("publication_type"))
            publications = (
                Publication.objects.live()
                .order_by(publication_ordering)
                .filter(
                    publication_publication_type_relationship__publication_type=request.GET.get(
                        "publication_type"
                    )
                )
            )
        # NOTE: filtering by category was commented out but I want see if it works -- Dragon.
        elif request.GET.get("category"):
            context["category_id"] = int(request.GET.get("category"))
            publications = (
                Publication.objects.live()
                .order_by(publication_ordering)
                .filter(
                    categorypage_category_relationship__category=request.GET.get(
                        "category"
                    )
                )
            )
        # NOTE: end block for previous note -- Dragon.
        else:
            publications = Publication.objects.live().order_by(publication_ordering)

        paginator = Paginator(publications, 16)

        try:
            items = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context["publications"] = items
        context["publication_types"] = PublicationType.objects.all()
        # categories isn't exposed on the webpage at all, and contains a lot of empty categories.
        context["categories"] = Category.objects.all()
        context["order"] = publication_ordering

        return context

    def get_wp_api_link(self):
        # TODO: Pretty sure this is a debug feature that should be removed.
        return f"https://www.england.nhs.uk/wp-json/wp/v2/documents/{self.wp_id}"

    def get_wp_live_link(self):
        # TODO: Pretty sure this is a debug feature that should be removed.
        self_url_path = self.url
        live_url_path = urlparse(self.wp_link).path
        live_url = "https://www.england.nhs.uk{}".format(live_url_path)
        print(self_url_path)
        print(live_url_path)
        return live_url


class PublicationPublicationTypeRelationship(models.Model):
    publication = ParentalKey(
        "publications.Publication",
        related_name="publication_publication_type_relationship",
    )
    publication_type = ForeignKey(
        "categories.PublicationType",
        related_name="+",
        on_delete=models.CASCADE,
    )


class Publication(CategoryPage):

    parent_page_types = ["publications.PublicationIndexPage"]
    """
    title already in the Page class
    slug already in the Page class
    going to need to parse the html here to extract the text
    """

    # going to need to parse the html here to extract the text
    body = RichTextField(blank=True)
    documents = StreamField(PublicationsBlocks, blank=True)

    """ coming across form wordpress need to keep for now"""
    wp_id = models.PositiveIntegerField(null=True, blank=True)
    source = models.CharField(null=True, max_length=100, blank=True)

    wp_slug = models.TextField(null=True, blank=True)
    wp_link = models.TextField(null=True, blank=True)
    component_fields = models.TextField(null=True, blank=True)

    """i think we can do away with this field
    and use the text from body to create the exceprt"""
    # excerpt = RichTextField(blank=True)

    author = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        InlinePanel(
            "publication_publication_type_relationship", label="Publication Types"
        ),
        InlinePanel(
            "categorypage_category_relationship", label="Publication Categories"
        ),
        FieldPanel("body"),
        StreamFieldPanel("documents"),
        MultiFieldPanel(
            [
                FieldPanel("wp_id"),
                FieldPanel("author"),
                FieldPanel("source"),
                FieldPanel("wp_slug"),
                FieldPanel("wp_link"),
                FieldPanel("component_fields"),
            ],
            heading="wordpress data we dont need in the end",
            classname="collapsed collapsible",
        ),
    ]

    def get_wp_api_link(self):
        wp_source = self.source.replace("pages-", "")
        wp_id = self.wp_id
        if wp_source != "pages":
            api_url = "https://www.england.nhs.uk/{}/wp-json/wp/v2/documents/{}".format(
                wp_source, wp_id
            )
        else:
            api_url = "https://www.england.nhs.uk/wp-json/wp/v2/documents/{}".format(
                wp_id
            )
        return api_url

    def get_wp_live_link(self):
        self_url_path = self.url
        live_url_path = urlparse(self.wp_link).path
        live_url = "https://www.england.nhs.uk{}".format(live_url_path)
        print(self_url_path)
        print(live_url_path)
        return live_url
