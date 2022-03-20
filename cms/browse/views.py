import logging

from django.shortcuts import render

logger = logging.getLogger("general")


def browse(request):
    return render(request, "browse/browse.html")


def browse_branch(request, section):
    return render(request, "browse/browse.html", {"section": section})


def browse_leaf(request, section, branch):
    return render(request, "browse/browse.html", {"section": section, "branch": branch})
