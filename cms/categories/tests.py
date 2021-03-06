from bs4 import BeautifulSoup
from django.test import TestCase
from cms.blogs.models import Blog


class TestCategoryIndexPage(TestCase):

    fixtures = ["fixtures/testdata.json"]

    def test_heading(self):
        response = self.client.get("/categories/")
        soup = BeautifulSoup(response.content, "html.parser")

        heading = soup.select_one("main h1")

        self.assertEqual(heading.text, "All categories")

    def test_category_list(self):
        response = self.client.get("/categories/")
        soup = BeautifulSoup(response.content, "html.parser")

        listed_categories = soup.select("main ul li")

        self.assertEqual(listed_categories[0].text, "Category One")
        self.assertEqual(listed_categories[1].text, "Category Two")


class TestCategoryDetailPage(TestCase):

    fixtures = ["fixtures/testdata.json"]

    def test_heading(self):
        response = self.client.get("/categories/category-one")
        soup = BeautifulSoup(response.content, "html.parser")

        heading = soup.select_one("main h1")

        self.assertEqual(heading.text, "Category One")

    def test_description(self):
        response = self.client.get("/categories/category-one")
        soup = BeautifulSoup(response.content, "html.parser")

        heading = soup.select_one("main p")

        self.assertEqual(heading.text, "Category one description")

    def test_pages_list(self):
        response = self.client.get("/categories/category-one")
        soup = BeautifulSoup(response.content, "html.parser")

        table_rows = soup.select("main table tr")
        # the most recently changed page should be top of this list
        self.assertEqual(table_rows[1].select("td")[0].text, "Post Two")
        self.assertEqual(table_rows[1].select("td")[1].text, "News")
        self.assertEqual(table_rows[1].select("td")[2].text, "25 Aug 2021")

        self.assertEqual(table_rows[2].select("td")[0].text, "Post One")
        self.assertEqual(table_rows[2].select("td")[1].text, "News")
        self.assertEqual(table_rows[2].select("td")[2].text, "25 Aug 2021")


class TestBlurb(TestCase):
    fixtures = ["fixtures/testdata.json"]

    def test_blurb(self):
        page = Blog.objects.specific().get(slug="blog-post-one")
        # words after the cut off don't appear
        self.assertIn("scelerisque", page.body, 93)
        self.assertNotIn("scelerisque", page.blurb(93))
        # it cuts off where we expect and puts an ellipsis at the end
        self.assertTrue(page.blurb(93).endswith(" id li\u2026"))
