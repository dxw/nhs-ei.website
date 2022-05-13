from cms.blogs.models import Blog
from cms.categories.models import (
    Category,
    PublicationType,
)
from cms.posts.models import Post
from cms.publications.models import Publication
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    PermissionHelper,
    modeladmin_register,
)

"""CATEGORIES"""


class CategoryPermissionHelper(PermissionHelper):
    def user_can_delete_obj(self, user, obj):
        posts = Post.objects.filter(categorypage_category_relationship__category=obj)
        blogs = Blog.objects.filter(categorypage_category_relationship__category=obj)
        publications = Publication.objects.filter(
            categorypage_category_relationship__category=obj
        )
        if not posts and not blogs and not publications:
            return True


class CategoriesAdmin(ModelAdmin):
    model = Category
    search_fields = ("name",)
    list_display = ("name", "get_category_usage")
    menu_icon = "folder-open-inverse"
    # removed by Dragon
    # list_filter = ("sub_site",)

    # to prevent deletion of a category if it's in use
    permission_helper_class = CategoryPermissionHelper

    panels = [
        FieldPanel("name"),
        # eventually hidden
        FieldPanel("slug"),
        FieldPanel("description"),
        FieldPanel("wp_id"),
        FieldPanel("source"),
    ]

    def get_category_usage(self, obj):
        posts = Post.objects.filter(categorypage_category_relationship__category=obj)
        blogs = Blog.objects.filter(categorypage_category_relationship__category=obj)
        # posts_count, blogs_count = Category.get_category_usage()
        return "Posts {} | Blogs {}".format(posts.count(), blogs.count())

    get_category_usage.short_description = "Usage"


# modeladmin_register(CategoriesAdmin)

"""PUBLICATION TYPES"""


class PublicationTypePermissionHelper(PermissionHelper):
    def user_can_delete_obj(self, user, obj):
        publication_types = Publication.objects.filter(
            publication_publication_type_relationship__publication_type=obj
        )
        if not publication_types:
            return True


class PublicationTypeAdmin(ModelAdmin):
    model = PublicationType
    search_fields = ("name",)
    list_display = ("name", "get_publication_type_usage")
    menu_icon = "folder-open-inverse"

    # to prevent deletion of a publiction type if it's in use
    permission_helper_class = PublicationTypePermissionHelper

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("description"),
        FieldPanel("wp_id"),
    ]

    def get_publication_type_usage(self, obj):
        publications = Publication.objects.filter(
            publication_publication_type_relationship__publication_type=obj
        )
        # blogs = Blog.objects.filter(categorypage_category_relationship__category=obj)
        # posts_count, blogs_count = Category.get_category_usage()
        return "Publications {}".format(publications.count())

    get_publication_type_usage.short_description = "Usage"


"""ADMIN GROUP"""


class CategoriesAdminGroup(ModelAdminGroup):
    menu_label = "Classification"
    menu_icon = "folder-open-1"
    items = (
        CategoriesAdmin,
        PublicationTypeAdmin,
    )


modeladmin_register(CategoriesAdminGroup)
