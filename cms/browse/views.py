import logging

from django.shortcuts import render
from wagtail.core.models import Page

from cms.core.models import ExtendedMainMenuItem

logger = logging.getLogger("general")


def browse(request, programme, branch):
    # we could get current site, query main menu for matching items and then
    # load the items but we _know_ that ExtendedMenuItems will haveour list
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
        programme_page = Page.objects.get(slug=programme)
        branch_title = programme_page.title
        branches.append(programme_page)
        branches += [branch for branch in programme_page.get_children()]

        if branch:
            branch_page = Page.objects.get(slug=branch)
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
