import logging

from django.http import Http404
from django.shortcuts import render
from wagtail.core.models import Page

from cms.core.models import ExtendedMainMenuItem

logger = logging.getLogger("general")


def fetch_page_by_slug(slug):
    ###########
    # https://trello.com/c/47ZFPaJb/255-fix-non-unique-slugs-in-browse-pages
    # This should be a unique page slug
    # programme_page = Page.objects.get(slug=programme)
    # Also see browse_tags.py:~58
    #######
    # But we have multiples, so we need to guard against that.
    pages = Page.objects.filter(slug=slug).live()
    if len(pages) == 0:
        # Should not be reachable
        raise Http404
    return list(pages)[0]
    #####################


def browse(request, programme, branch):
    # we could get current site, query main menu for matching items and then
    # load the items but we _know_ that ExtendedMenuItems will have our list
    # in it. 4+ queries -> 1 query
    menu_items = ExtendedMainMenuItem.objects.all()
    programmes = []
    for item in menu_items:
        page = Page.objects.get(id=item.link_page_id)
        programmes.append(page)

    # now use the section (if set) get the top level page by slug
    branches = []
    leaves = []
    branch_title = ""
    leaf_title = ""

    if programme:
        programme_page = fetch_page_by_slug(programme)
        branch_title = programme_page.title
        branches.append(programme_page)
        branches += [branch for branch in programme_page.get_children()]

        if branch:
            branch_page = fetch_page_by_slug(branch)
            leaf_title = branch_page.title
            leaves.append(branch_page)
            leaves += [leaf for leaf in branch_page.get_children()]

    return render(
        request,
        "browse/browse.html",
        {
            "programme": programme,
            "branch": branch,
            "branch_title": branch_title,
            "leaf_title": leaf_title,
            "programmes": programmes,
            "branch_items": branches,
            "leaf_items": leaves,
        },
    )
