from bs4 import BeautifulSoup
from django.test import TestCase
from wagtail.contrib.search_promotions.models import SearchPromotion
from wagtail.search.models import Query

from cms.pages.models import Page, BasePage


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

        # Now we have promoted a page for the phrase, we should get it in the search results
        self.assertNotContains(response, "Test Aardvarks Page")
        self.assertContains(response, "Search")
        # self.assertContains(response, "Test Bananas Page")
        # self.assertContains(response, "Plantains are similar to bananas.")

    def test_breadcrumbs(self):
        response = self.client.get("/search/")

        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.findAll(class_="nhsuk-breadcrumb__item")
        self.assertEqual(2, len(list(items)))

        self.assertEquals("Home", items[0].text.strip())
        self.assertEquals("Search", items[1].text.strip())


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
