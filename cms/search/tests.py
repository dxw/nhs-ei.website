from socket import PACKET_BROADCAST
from bs4 import BeautifulSoup
from django.test import TestCase
from wagtail.contrib.search_promotions.models import SearchPromotion
from wagtail.search.models import Query
import lxml.html

from cms.search.views import parse_date

from cms.pages.models import Page, BasePage


class TestDateHandling(TestCase):
    def test_dates(self):
        self.assertEqual(parse_date(year='', month='', day='', before=True), None)
        self.assertEqual(parse_date(year='2000', month='badger', day='3', before=True), None)
        self.assertEqual(parse_date(year='badger', month='3', day='3', before=True), None)
        self.assertEqual(parse_date(year='2000', month='2', day='', before=False).day, 29)
        self.assertEqual(parse_date(year='2000', month='2' ,day='', before=True).day, 1)
        self.assertEqual(parse_date(year='2000', month='', day='', before=False).month, 12)
        self.assertEqual(parse_date(year='2000', month='', day='', before=True).month, 1)
        self.assertEqual(parse_date(year='2000', month='', day='', before=False).day, 31)
        self.assertEqual(parse_date(year='2000', month='', day='', before=True).day, 1)

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

    def test_negative_page(self):
        response = self.client.get("/search/?query=e&page=-2")
        self.assertContains(response, "Showing 21 to 30 of 48 results")

    def test_date_range(self):
        response = self.client.get("/search/?query=e")
        self.assertContains(response, "Showing 1 to 10 of 48 results")

        response = self.client.get(
            "/search/?query=e&content_type=all&date_from=2021-01-01&date_to=2021-12-31"
        )
        self.assertContains(response, "Showing 1 to 10 of 14 results")

        response = self.client.get("/search/?query=e&date_from=&date_to=2021-06-01")
        self.assertContains(response, "Showing 1 to 10 of 40 results")

        response = self.client.get(
            "/search/?query=e&content_type=all&date_from=2021-06-07"
        )
        self.assertContains(response, "Showing 1 to 7 of 7 results")

    def test_type_filters(self):
        response = self.client.get("/search/?query=e&content_type=pages")
        self.assertContains(response, "Showing 1 to 10 of 10 results")

        response = self.client.get("/search/?query=e&content_type=news")
        self.assertContains(response, "Showing 1 to 10 of 10 results")

        response = self.client.get("/search/?query=e&content_type=blogs")
        self.assertContains(response, "Showing 1 to 9 of 9 results")

        response = self.client.get("/search/?query=e&content_type=publications")
        self.assertContains(response, "Showing 1 to 8 of 8 results")

    def test_type_and_date_filters(self):
        response = self.client.get(
            "/search/?query=e&content_type=pages&date_from=2021-06-01&date_to=2021-12-31"
        )
        self.assertContains(response, "Showing 1 to 4 of 4 results")

        # TODO filter and date range without start/end dates, see test above

    def test_sort_orders(self):
        response = self.client.get("/search/?query=e&order=first_published_at")
        self.assertContains(response, "Abiogenesis corneal diagnostician")
        response = self.client.get("/search/?query=e&order=-first_published_at")
        self.assertNotContains(response, "Abiogenesis corneal diagnostician")

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
        self.assertEqual([''], root.xpath('//input[@id="search"]/@value'))
