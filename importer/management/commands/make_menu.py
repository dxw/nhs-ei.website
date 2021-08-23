import logging

from django.core.management.base import BaseCommand
from importer.menu_structure import menu_structure, new_pages
from cms.pages.models import Page
from importer.preserve import preserve
from wagtail.core.models import Site
from wagtailmenus.conf import settings

import json

logger = logging.getLogger(__name__)


def restructure(menu):
    # menu_structure has the title of a list as an item, then the contents of that list as
    # a separate item in that list. We make it into a third entry on the original item.
    new_menu = []
    for item in menu:
        if type(item[0]) == str:
            if item[1] == "javascript:void(0);" and item[0] not in [
                "",
                "Open mobile menu",
            ]:
                item[1] = None
            new_menu.append([item[0], item[1], None])
        else:
            new_menu[-1][2] = restructure(item)
    return new_menu


def make_flat_menu(menu):
    # Given a nested menu, return a simple list of name/url pairs
    for item in menu:
        yield [item[0], item[1]]
        if item[2]:
            for item in list(make_flat_menu(item[2])):
                yield item


def get_pages(flat_menu):
    lookup = dict()
    root = Page.objects.get(slug="home")
    for item in flat_menu:
        name, url = item
        if url:
            url_bits = url.strip("/").split("/")
            page = root
            for bit in url_bits:
                try:
                    page = page.get_children().get(slug=bit)
                except Page.DoesNotExist:  # wagtail.core.models.DoesNotExist
                    print(bit)
                    raise
                else:
                    lookup[url] = page
    return lookup


def create_new_pages(pagenames):
    home_page = Page.objects.get(slug="home")
    for pagename in pagenames:
        if home_page.get_children().filter(slug=pagename):
            print(f"Not creating {pagename}, already exists")
            continue
        print(f"Creating {pagename}")
        page = Page(
            title=pagename,
            # wp_id=-10,
            # source="none",
            # wp_slug="none",
        )

        # making a new block as body is empty
        block = [
            {
                "type": "panel",
                "value": {
                    "label": "",
                    # this is the default, might want to change it...
                    "heding_level": "3",
                    # after it's been parsed for links
                    "body": f"<p>Placeholder text for {pagename}</p>",
                },
            }
        ]

        page.body = json.dumps(block)
        home_page.add_child(instance=page)
        preserve(page)


def add_root_menu_items(menu, lookup):
    # from https://github.com/rkhleics/wagtailmenus/blob/master/wagtailmenus/management/commands/autopopulate_main_menus.py
    # with a roundabout way of generating a queryset
    top_level_pages = [lookup[item[1]] for item in menu]
    page_ids = [x.id for x in top_level_pages]
    pages = Page.objects.filter(id__in=page_ids)
    assert len(pages) == len(page_ids)

    for site in Site.objects.all():
        menu_model = settings.models.MAIN_MENU_MODEL
        menu = menu_model.get_for_site(site)
        if not menu.get_menu_items_manager().exists():
            print(f"Adding {pages} to menu")
            menu.add_menu_items_for_pages(pages)
        else:
            print(f"Base menu already exists")


class Command(BaseCommand):
    help = "Make a menu structure suitable for wagtailmenus"

    def handle(self, *args, **options):
        # create new pages that might not exist to fill gaps in the menu structure
        create_new_pages(new_pages)
        # restructure the data from menu_structure to the right shape
        menu = restructure(menu_structure)
        # get a flattened version of that structure
        flat_menu = make_flat_menu(menu)
        # map existing pages to original URLs
        lookup = get_pages(flat_menu)
        print(lookup)
        # make menu have top level pages
        add_root_menu_items(menu, lookup)
