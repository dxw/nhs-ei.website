from datetime import datetime, timedelta, timezone
from django.conf import settings

from cms.publications.models import Publication
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.core.models import Page
from wagtail.search.models import Query

from cms.posts.models import Post
from cms.blogs.models import Blog
from cms.pages.models import BasePage
from cms.publications.models import PublicationType

from urllib.parse import urlparse, parse_qsl, urlencode

import calendar


def pageless_query(url):
    """Return the query part of the URL without the page
    e.g. 'http://server/search/?page=3&query=e'
    returns &query=e

    We prepend a & because this is going to get appended to search/?page=4 or similar
    You may use request.build_absolute_uri() to get the URL
    """
    url_query = parse_qsl(urlparse(url).query)
    url_query = [fragment for fragment in url_query if fragment[0] != "page"]
    return "&" + urlencode(url_query)


acceptable_sort_orders = [
    "latest_revision_created_at",
    "-latest_revision_created_at",
    "first_published_at",
    "-first_published_at",
    "last_published_at",
    "-last_published_at",
    # "go_live_at", # worth considering for future use.
    # "-go_live_at",
]


class NotANumberError(Exception):
    """Only catch when we can't parse dates, not other ValueErrors"""

    pass


def as_int(i):
    """Get a number for a number-like string, but:
    * tolerate no value
    * raise a custom error for easier trapping downstream"""
    try:
        if i:
            return int(i)
        return None
    except ValueError as ex:
        raise NotANumberError from ex


def parse_date(year, month, day, before):
    """Given user-generated strings probably containing a date, get a datetime for them.
    If it's just a year or year and month, choose the end of that datetime."""
    try:
        year_num = as_int(year)
        if not year_num:
            return None
        month_num = as_int(month) or (12 if before else 1)
        _, last_day_of_month = calendar.monthrange(year_num, month_num)
        day_num = as_int(day) or (last_day_of_month if before else 1)
        return datetime(year=year_num, month=month_num, day=day_num)

    except NotANumberError:
        return None


def validated_sort_order(sort_order):
    if sort_order and sort_order.lower() in acceptable_sort_orders:
        return sort_order.lower()
    return None


def search(request):
    """
    sample query
    ?
    query=nursing&
    order=first_published_at&
    content_type=pages&
    before-year=2020&before_month=11&before_day=1&
    after-year=2011&after_month=6&before_day=17
    """

    def get_date(before=True):
        when = "before" if before else "after"
        return parse_date(
            day=request.GET.get(f"{when}-day"),
            month=request.GET.get(f"{when}-month"),
            year=request.GET.get(f"{when}-year"),
            before=before,
        )

    query_string = request.GET.get("query", "")
    search_ordering = validated_sort_order(request.GET.get("order", None))
    search_type = request.GET.get("content_type", "")
    publication_types = request.GET.getlist("publication_type")
    date_from = get_date(before=False)
    date_to = get_date(before=True)

    page = int(request.GET.get("page", 1))
    search_results_count = 0

    def search(_class):

        start_date = date_from or datetime.min
        end_date = date_to or datetime.max - timedelta(days=7)

        queryset = _class.objects.live()

        if search_ordering:
            queryset = queryset.order_by(search_ordering)

        if date_from or date_to:
            queryset = queryset.filter(
                # The time zone is set to suppress 'naive datetime' warnings
                first_published_at__range=[
                    start_date.replace(tzinfo=timezone.utc),
                    end_date.replace(tzinfo=timezone.utc) + timedelta(days=1),
                ]
            )
        return queryset.search(query_string)

    # Search
    if query_string:
        if search_type == "news":
            search_results = search(Post)
        elif search_type == "blogs":
            search_results = search(Blog)
        elif search_type == "pages":
            search_results = search(BasePage)
        elif search_type == "publications":
            search_results = search(Publication)
        else:
            search_results = search(Page)

        search_results_count = search_results.count()

        query = Query.get(query_string)
        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, settings.SEARCH_RESULTS_PER_PAGE)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    search_params = pageless_query(request.build_absolute_uri())

    # figure out the page results from - to numbers
    if page > 0:
        min_result_index = min(
            1 + ((page - 1) * settings.SEARCH_RESULTS_PER_PAGE), search_results_count
        )
        max_result_index = min(
            page * settings.SEARCH_RESULTS_PER_PAGE, search_results_count
        )
    else:
        # 0 and negative numbers count down from the last result
        abs_min_result_index = (
            (paginator.num_pages - 1) * settings.SEARCH_RESULTS_PER_PAGE
        ) + (page * settings.SEARCH_RESULTS_PER_PAGE)
        min_result_index = max(1, abs_min_result_index + 1)
        max_result_index = min(
            search_results_count,
            min_result_index + settings.SEARCH_RESULTS_PER_PAGE - 1,
        )

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "query_string": query_string,
            "search_results": search_results,
            "results_count": search_results_count,
            "page": page,
            "search_params": search_params,
            "content_type": search_type,
            "order": search_ordering,
            "date_from": date_from,
            "date_to": date_to,
            "min_result_index": min_result_index,
            "max_result_index": max_result_index,
            "publication_types": PublicationType.objects.all(),
            "publication_types_checked": publication_types,
        },
    )
