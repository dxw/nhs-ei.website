from bs4 import BeautifulSoup
from django.test import TestCase


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

        self.assertEqual(table_rows[1].select("td")[0].text, "Publication One")
        self.assertEqual(table_rows[1].select("td")[1].text, "Publication")
        self.assertEqual(table_rows[1].select("td")[2].text, "05 Feb 2021")

        self.assertEqual(table_rows[2].select("td")[0].text, "Post Two")
        self.assertEqual(table_rows[2].select("td")[1].text, "News")
        self.assertEqual(table_rows[2].select("td")[2].text, "04 Feb 2021")
