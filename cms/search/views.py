from datetime import datetime

from django.conf import settings

from cms.publications.models import Publication
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.core.models import Page
from wagtail.search.models import Query

from cms.posts.models import Post
from cms.blogs.models import Blog
from cms.pages.models import BasePage

import calendar

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

def parse_date(day, month, year, before):
    """Given user-generated strings probably containing a date, get a datetime for them.
    If it's just a year or year and month, choose the end of that datetime."""
    try:
        year_num = as_int(year)
        if not year_num:
            return None
        month_num = as_int(month) or (1 if before else 12)
        _, last_day_of_month = calendar.monthrange(year_num, month_num)
        day_num = as_int(day) or (1 if before else last_day_of_month)
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
    order=pub_date_asc&
    content_type=pages&
    date_from=2020-11-01&
    date_to=2020-11-29
    """



    def get_date(before=True):
        when = "before" if before else "after"
        return parse_date(
            day = request.GET.get(f"published-{when}-day"),
            month = request.GET.get(f"published-{when}-month"),
            year = request.GET.get(f"published-{when}-year"),
            before = before,
        )

    query_string = request.GET.get("query", "")
    search_ordering = validated_sort_order(request.GET.get("order", None))
    search_type = request.GET.get("content_type", "")
    date_from = get_date(before=True)
    date_to = get_date(before=False)
    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")

    page = int(request.GET.get("page", 1))
    search_results_count = 0

    def search(_class):

        start_date = date_from or "1900-01-01"
        end_date = date_to or datetime.max

        queryset = _class.objects.live()

        if search_ordering:
            queryset = queryset.order_by(search_ordering)

        if date_from and date_to:
            queryset = queryset.filter(
                latest_revision_created_at__range=[
                    start_date,
                    end_date,
                ]
            )
        elif date_from:
            queryset = queryset.filter(
                latest_revision_created_at__range=[start_date, end_date]
            )
        elif date_to:
            queryset = queryset.filter(
                latest_revision_created_at__range=[
                    start_date,
                    end_date,
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

    search_params = "&query={}&order={}&content_type={}&date_from={}&date_to={}".format(
        query_string, search_ordering, search_type, date_from, date_to
    )

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
        },
    )
