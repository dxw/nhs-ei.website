from cms.categories.models import Category, Region, Setting, CategoryPage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class AtlasCaseStudyIndexPage(Page):
    # title already in the Page class
    # slug already in the Page class
    subpage_types = ["atlascasestudies.AtlasCaseStudy"]
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_latest_atlas_case_studies(self, num):
        return AtlasCaseStudy.objects.all().order_by("-latest_revision_created_at")[
            :num
        ]

    def get_context(self, request, *args, **kwargs):
        atlas_case_study_ordering = "-latest_revision_created_at"
        context = super().get_context(request, *args, **kwargs)

        if request.GET.get("setting"):
            context["chosen_setting_id"] = int(request.GET.get("setting"))
            atlas_case_studies = (
                AtlasCaseStudy.objects.live()
                .order_by(atlas_case_study_ordering)
                .filter(
                    atlas_case_study_setting_relationship__setting=request.GET.get(
                        "setting"
                    )
                )
            )
        elif request.GET.get("region"):
            context["chosen_region_id"] = int(request.GET.get("region"))
            atlas_case_studies = (
                AtlasCaseStudy.objects.live()
                .order_by(atlas_case_study_ordering)
                .filter(
                    atlas_case_study_region_relationship__region=request.GET.get(
                        "region"
                    )
                )
            )
        elif request.GET.get("category"):
            context["chosen_category_id"] = int(request.GET.get("category"))
            atlas_case_studies = (
                AtlasCaseStudy.objects.live()
                .order_by(atlas_case_study_ordering)
                .filter(
                    categorypage_category_relationship__category=request.GET.get(
                        "category"
                    )
                )
            )
        else:
            atlas_case_studies = AtlasCaseStudy.objects.live().order_by(
                atlas_case_study_ordering
            )

        paginator = Paginator(atlas_case_studies, 16)

        try:
            items = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context["atlas_case_studies"] = items

        context["categories"] = Category.objects.all()

        context["setting"] = Setting.objects.all()

        context["regions"] = Region.objects.all()

        # an experiment to get only categories that are used by blogs
        # blog_pages_ids = [x.id for x in Blog.objects.all()]
        # print(blog_pages_ids)
        # print(Category.objects.filter(blog_categories__in=blog_pages_ids))
        # context['categories'] = Category.objects.filter(blog_categories__in=blog_pages_ids)
        return context


class AtlasCaseStudySettingRelationship(models.Model):
    atlas_case_study = ParentalKey(
        "atlascasestudies.AtlasCaseStudy",
        related_name="atlas_case_study_setting_relationship",
    )
    setting = models.ForeignKey(
        "categories.Setting",
        related_name="+",
        on_delete=models.CASCADE,
    )


class AtlasCaseStudyRegionRelationship(models.Model):
    atlas_case_study = ParentalKey(
        "atlascasestudies.AtlasCaseStudy",
        related_name="atlas_case_study_region_relationship",
    )
    region = models.ForeignKey(
        "categories.Region",
        related_name="+",
        on_delete=models.CASCADE,
    )


class AtlasCaseStudy(CategoryPage):
    parent_page_types = ["atlascasestudies.AtlasCaseStudyIndexPage"]
    """
    title already in the Page class
    slug already in the Page class
    going to need to parse the html here to extract the text
    """

    # going to need to parse the html here to extract the text
    body = RichTextField(blank=True)

    """ coming across form wordpress need to keep for now"""
    wp_id = models.PositiveIntegerField(null=True, blank=True)
    wp_slug = models.TextField(null=True, blank=True)
    wp_link = models.TextField(null=True, blank=True)

    content_panels = Page.content_panels + [
        InlinePanel("atlas_case_study_setting_relationship", label="Settings"),
        InlinePanel("atlas_case_study_region_relationship", label="Regions"),
        InlinePanel("categorypage_category_relationship", label="Categories"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("wp_id"),
                FieldPanel("wp_slug"),
                FieldPanel("wp_link"),
            ],
            heading="wordpress data we dont need in the end",
            classname="collapsed collapsible",
        ),
    ]
