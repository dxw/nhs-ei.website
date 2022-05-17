from bs4 import BeautifulSoup
from django.test import TestCase
from wagtail.contrib.search_promotions.models import SearchPromotion
from wagtail.search.models import Query
import lxml.html
import re

from cms.search.views import pageless_query, parse_date

from cms.pages.models import Page, BasePage


class TestSearchDescription(TestCase):
    def test_search_description_in_search(self):
        """Search description is present and isn't shortened"""
        BasePage.objects.create(
            title="a page",
            slug="a_page",
            depth=1,
            path="/a_page",
            search_description="stuff " * 100 + "has a search_description",
            body="blah blah blah",
        )
        response = self.client.get("/search/?query=e")
        self.assertContains(response, "search_description")
        self.assertNotContains(response, "blah")


class TestPagelessQuery(TestCase):
    def test_pageless_query(self):
        self.assertEqual(
            pageless_query(
                "http://example/search/?kitten=yes&repeated=yes&repeated=yes&page=5&ocelot=no"
            ),
            "&kitten=yes&repeated=yes&repeated=yes&ocelot=no",
        )


# # Disabled this class of tests in order to see if this helps ElasticSearch
# class PublicationFilters():
#     fixtures = ["fixtures/publication_types.json"]

#     def test_a_publication_filter(self):
#         """Publication filters include Publications that are of the right type, even if they have other types"""
#         response = self.client.get(
#             "/search/?query=e&content_type=publications&publication_type=ocelot"
#         )
#         self.assertContains(response, "Ocelot Kitten")
#         self.assertNotContains(response, "Panther Kitten")
#         self.assertNotContains(response, "Puppies")
#         self.assertContains(response, "Panthelot")

#     def test_no_publication_filter(self):
#         "All publications appear if there is no publication type specified"
#         response = self.client.get(
#             "/search/?query=e&content_type=publications&publication_type="
#         )
#         self.assertContains(response, "Ocelot Kitten")
#         self.assertContains(response, "Panther Kitten")
#         self.assertContains(response, "Puppies")
#         self.assertContains(response, "Panthelot")

#     def test_malformed_publication_filter(self):
#         "All publications appear if there are no valid publication types"
#         response = self.client.get(
#             "/search/?query=e&content_type=publications&publication_type=stegosaurus"
#         )
#         self.assertContains(response, "Ocelot Kitten")
#         self.assertContains(response, "Panther Kitten")
#         self.assertContains(response, "Puppies")
#         self.assertContains(response, "Panthelot")

#     def test_combo_publication_filter(self):
#         "Both ocelots and panthers appear if selected, but not puppies"
#         response = self.client.get(
#             "/search/?query=e&content_type=publications&publication_type=ocelot&publication_type=panther"
#         )
#         self.assertContains(response, "Ocelot Kitten")
#         self.assertContains(response, "Panther Kitten")
#         self.assertNotContains(response, "Puppies")
#         self.assertContains(response, "Panthelot")

#     def test_publications_and_dates(self):
#         "Combining different search fields works correctly."
#         response = self.client.get(
#             "/search/?query=e&content_type=publications&publication_type=ocelot&before-year=2000"
#         )
#         self.assertNotContains(response, "Ocelot Kitten")
#         self.assertNotContains(response, "Panther Kitten")
#         self.assertContains(response, "Old Ocelot")


class TestDateHandling(TestCase):
    def test_dates(self):
        self.assertEqual(parse_date(year="", month="", day="", before=True), None)
        self.assertEqual(
            parse_date(year="2000", month="badger", day="3", before=True), None
        )
        self.assertEqual(
            parse_date(year="badger", month="3", day="3", before=True), None
        )
        # TODO self.assertEqual(parse_date(year='2000', month='2', day='31', before=True), None)
        self.assertEqual(
            parse_date(year="2000", month="2", day="", before=True).day, 29
        )
        self.assertEqual(
            parse_date(year="2000", month="2", day="", before=False).day, 1
        )
        self.assertEqual(
            parse_date(year="2000", month="", day="", before=True).month, 12
        )
        self.assertEqual(
            parse_date(year="2000", month="", day="", before=False).month, 1
        )
        self.assertEqual(parse_date(year="2000", month="", day="", before=True).day, 31)
        self.assertEqual(parse_date(year="2000", month="", day="", before=False).day, 1)


class TestSearch(TestCase):
    def test_simple_search(self):
        root = Page.get_first_root_node()

        test_aardvarks_page = BasePage(
            title="Test Aardvarks Page",
            slug="test-page-aardvarks",
        )

        test_bananas_page = BasePage(
            title="Test Bananas Page",
            slug="test-page-bananas",
        )

        root.add_child(instance=test_aardvarks_page)
        root.add_child(instance=test_bananas_page)

        response = self.client.get("/search/?query=aardvarks")

        self.assertContains(response, "Test Aardvarks Page")
        self.assertNotContains(response, "Test Bananas Page")

    def test_promoted_search(self):

        root = Page.get_first_root_node()

        test_aardvarks_page = BasePage(
            title="Test Aardvarks Page",
            slug="test-page-aardvarks",
        )

        test_bananas_page = BasePage(
            title="Test Bananas Page",
            slug="test-page-bananas",
        )

        root.add_child(instance=test_aardvarks_page)
        root.add_child(instance=test_bananas_page)

        response = self.client.get("/search/?query=plantains")

        # At this point there is no promoted search, no results should appear
        self.assertNotContains(response, "Suggested result")
        self.assertNotContains(response, "Test Aardvarks Page")
        self.assertNotContains(response, "Test Bananas Page")

        SearchPromotion.objects.create(
            query=Query.get("plantains"),
            page_id=test_bananas_page.id,
            sort_order=0,
            description="Plantains are similar to bananas.",
        )

        response = self.client.get("/search/?query=plantains")

        # Now we have promoted a page for the phrase, we should get it in the
        # search results
        self.assertNotContains(response, "Test Aardvarks Page")
        self.assertContains(response, "Search")
        self.assertContains(response, "Test Bananas Page")
        self.assertContains(response, "Plantains are similar to bananas.")

    def test_breadcrumbs(self):
        response = self.client.get("/search/")

        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.findAll(class_="nhsuk-breadcrumb__item")
        self.assertEqual(2, len(list(items)))

        self.assertEquals("Home", items[0].text.strip())
        self.assertEquals("Search", items[1].text.strip())


class TestSearchWithFilters(TestCase):
    fixtures = ["fixtures/loadsa-pages.json"]

    def assertResultsRangeSummaryEquals(self, response, min, max, total):
        expected = f"Showing {min} to {max} of {total} results"
        match = re.search(
            r"Showing (?:\d+ to \d+ of \d+|no) results", response.rendered_content
        )
        if match:
            self.assertEquals(match.group(0), expected)
        else:
            self.assertEquals("<<No results text found.>>", expected)

    def test_negative_page(self):
        response = self.client.get("/search/?query=e&page=-2")
        self.assertResultsRangeSummaryEquals(response, min=21, max=30, total=48)

    def test_date_range(self):
        response = self.client.get("/search/?query=e")
        self.assertResultsRangeSummaryEquals(response, min=1, max=10, total=48)

        response = self.client.get(
            "/search/?query=e&content_type=all&after-year=2021&after-month=1&after-day=1&before-year=2021&before-month=12&before_day=31"
        )
        self.assertResultsRangeSummaryEquals(response, min=1, max=10, total=14)

        response = self.client.get(
            "/search/?query=e&before-year=2021&before-month=06&before-day=01"
        )
        self.assertResultsRangeSummaryEquals(response, min=1, max=10, total=40)

        response = self.client.get(
            "/search/?query=e&content_type=all&after-year=2021&after-month=6&after-day=07"
        )
        self.assertResultsRangeSummaryEquals(response, min=1, max=7, total=7)

    def test_date_range_remembers_full_date(self):
        """Confirm that all the date fragments correctly correspond to each other"""
        response = self.client.get(
            "/search/?query=e&content_type=all&after-day=2&after-month=3&after-year=2004&before-day=5&before-month=6&before-year=2007"
        )
        root = lxml.html.fromstring(response.rendered_content)
        self.assertEqual(root.xpath("//input[@id='after-year']/@value"), ["2004"])
        self.assertEqual(root.xpath("//input[@id='after-month']/@value"), ["3"])
        self.assertEqual(root.xpath("//input[@id='after-day']/@value"), ["2"])
        self.assertEqual(root.xpath("//input[@id='before-year']/@value"), ["2007"])
        self.assertEqual(root.xpath("//input[@id='before-month']/@value"), ["6"])
        self.assertEqual(root.xpath("//input[@id='before-day']/@value"), ["5"])

    def test_date_range_remembers_partial_date(self):
        """If the dates were filled in before the user clicked the search button,
        we fill in the dates afterwards. (Also demonstrates the differing date ranges)"""
        response = self.client.get(
            "/search/?query=e&content_type=all&after-year=2021&before-year=2022"
        )
        root = lxml.html.fromstring(response.rendered_content)
        self.assertEqual(root.xpath("//input[@id='after-year']/@value"), ["2021"])
        self.assertEqual(root.xpath("//input[@id='after-month']/@value"), ["1"])
        self.assertEqual(root.xpath("//input[@id='after-day']/@value"), ["1"])
        self.assertEqual(root.xpath("//input[@id='before-year']/@value"), ["2022"])
        self.assertEqual(root.xpath("//input[@id='before-month']/@value"), ["12"])
        self.assertEqual(root.xpath("//input[@id='before-day']/@value"), ["31"])

    def test_type_filters(self):
        response = self.client.get("/search/?query=e&content_type=pages")
        self.assertResultsRangeSummaryEquals(response, min=1, max=10, total=10)

        response = self.client.get("/search/?query=e&content_type=news")
        self.assertResultsRangeSummaryEquals(response, min=1, max=10, total=10)

        response = self.client.get("/search/?query=e&content_type=blogs")
        self.assertResultsRangeSummaryEquals(response, min=1, max=9, total=9)

        response = self.client.get("/search/?query=e&content_type=publications")
        self.assertResultsRangeSummaryEquals(response, min=1, max=8, total=8)

    def test_type_and_date_filters(self):
        response = self.client.get(
            "/search/?query=e&content_type=pages&after-year=2021&after-month=6&before-year=2021"
        )
        self.assertResultsRangeSummaryEquals(response, min=1, max=4, total=4)

        response = self.client.get(
            "/search/?query=e&content_type=pages&after-year=&after-month=&after-day=&before-year=&before-month=&before-day="
        )
        self.assertResultsRangeSummaryEquals(response, min=1, max=10, total=10)

    def test_same_day(self):
        response = self.client.get(
            "/search/?query=e&content_type=all&"
            + "after-year=2021&after-month=11&after-day=13&"
            + "before-year=2021&before-month=11&before-day=13"
        )
        self.assertResultsRangeSummaryEquals(response, min=1, max=1, total=1)

    def test_sort_orders(self):
        response = self.client.get("/search/?query=e&order=first_published_at")
        self.assertContains(response, "Cerebrum cerebrum acrocyanosis")

        response = self.client.get("/search/?query=e&order=-first_published_at")
        self.assertNotContains(response, "Cerebrum cerebrum acrocyanosis")

    def test_invalid_sort_order(self):
        # passing an invalid order should be just like no order
        response = self.client.get("/search/?query=e&order=not_a_valid_order")
        self.assertContains(response, "Abiogenesis corneal diagnostician")


class TestPagination(TestCase):
    fixtures = ["fixtures/menu-fixtures.json"]

    def test_no_pagination(self):
        response = self.client.get("/search/?query=no-results")
        self.assertNotContains(response, "Previous")
        self.assertNotContains(response, "Next")

    def test_no_next(self):
        response = self.client.get("/search/?page=3&query=e")
        self.assertContains(response, "Previous")
        self.assertNotContains(response, "Next")

    def test_no_prev(self):
        response = self.client.get("/search/?query=e")
        self.assertNotContains(response, "Previous")
        self.assertContains(response, "Next")

    def test_prev_and_next(self):
        response = self.client.get("/search/?page=2&query=e")
        self.assertContains(response, "Previous")
        self.assertContains(response, "Next")


class TestSearchBox(TestCase):
    def test_no_query(self):
        # If no query is provided, the search bar is empty (not None)
        response = self.client.get("/search/")
        root = lxml.html.fromstring(response.rendered_content)
        self.assertEqual([""], root.xpath('//input[@id="search"]/@value'))
