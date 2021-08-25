from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page

"""CATEGORIES work with content types a across the site"""


class CategoryPageCategoryRelationship(models.Model):
    """
    A table which describes which Categories a CategoryPage has.
    """

    category_page = ParentalKey(
        "categories.CategoryPage",
        related_name="categorypage_category_relationship",
    )
    category = models.ForeignKey(
        "categories.Category",
        related_name="+",
        on_delete=models.CASCADE,
    )


class CategoryPage(Page):
    """CategoryPages are pages which have categories, like Blogs and Publications."""

    pass


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    """ coming across from wordpress need to keep for now"""
    wp_id = models.PositiveIntegerField(null=True, blank=True)
    source = models.CharField(null=True, max_length=100, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    # prevent deleting a category if its in use
    # def delete(self, *args, **kwargs):
    #     Post = apps.get_model('posts.Post')
    #     posts_count = Post.objects.filter(
    #         categorypage_category_relationship__category=self)

    #     Blog = apps.get_model('blogs.Blog')
    #     blogs_count = Blog.objects.filter(
    #         categorypage_category_relationship__category=self)

    #     if posts_count or blogs_count:
    #         raise ValidationError('1244')
    #     else:
    #         super().delete(*args, **kwargs)


"""PUBLICATION TYPES work with publications (document) and across sub sites"""


class PublicationType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    """ coming across from wordpress need to keep for now"""
    wp_id = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Publication Type"
        verbose_name_plural = "Publication Types"

    def __str__(self):
        return self.name

    # prevent deleting a category if its in use
    # def delete(self, *args, **kwargs):
    #     Post = apps.get_model('posts.Post')
    #     posts_count = Post.objects.filter(categorypage_category_relationship__category=self)

    #     Blog = apps.get_model('blogs.Blog')
    #     blogs_count = Blog.objects.filter(categorypage_category_relationship__category=self)

    #     if posts_count or blogs_count:
    #         raise ValidationError('1244')
    #     else:
    #         super().delete(*args, **kwargs)


class Setting(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    """ coming across from wordpress need to keep for now"""
    wp_id = models.PositiveIntegerField(null=True, blank=True)
    # source = models.CharField(null=True, max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name = "Setting"
        verbose_name_plural = "Settings"

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    """ coming across from wordpress need to keep for now"""
    wp_id = models.PositiveIntegerField(null=True, blank=True)
    # source = models.CharField(null=True, max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name = "Region"
        verbose_name_plural = "Regions"

    def __str__(self):
        return self.name
