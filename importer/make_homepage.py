from django.contrib.contenttypes.models import ContentType
from cms.home.models import HomePage
from wagtail.core.models import Page, Site


"""A reimplementation of cms/home/migrations/0002_create_homepage.py"""


def create_homepage():
    print("Creating home page.")

    # Delete the default homepage
    # If migration is run multiple times, it may have already been deleted
    Page.objects.filter(id=2).delete()

    # Create content type for homepage model
    homepage_content_type, __ = ContentType.objects.get_or_create(
        model="homepage", app_label="home"
    )

    # Create a new homepage
    homepage = HomePage.objects.create(
        title="Home",
        draft_title="Home",
        slug="home",
        content_type=homepage_content_type,
        path="00010001",
        depth=2,
        numchild=0,
        url_path="/home/",
        hero_heading="Home",
        hero_text="Home",
    )

    # Create a site with the new homepage set as the root
    Site.objects.create(hostname="localhost", root_page=homepage, is_default_site=True)
