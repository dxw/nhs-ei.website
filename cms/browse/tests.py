from bs4 import BeautifulSoup
from django.test import TestCase
from faker import Faker

# from selenium.webdriver.chrome.webdriver import WebDriver

from cms.browse.templatetags.browse_tags import (
    get_caption,
    url_for_link_page_id,
    menu_breadcrumb,
)
from cms.core.models import ExtendedMainMenuItem
from cms.pages.models import BasePage
from cms.settings.base import NHSEI_MAX_MENU_CAPTION_LENGTH


class TestBrowseUnit(TestCase):
    fixtures = ["fixtures/menu-fixtures.json"]

    def test_megamenu(self):
        response = self.client.get("/")
        soup = BeautifulSoup(response.content, "html.parser")

        burger = soup.find(id="toggle-menu")
        self.assertTrue(burger)

        menu = soup.find(id="mega-menu")
        self.assertTrue(menu)

        corporate = soup.find(class_="flat-menu corporate no_heading")
        self.assertTrue(corporate)
        corp_li = corporate.find_all("li")
        self.assertEqual(7, len(corp_li))

        main_menu = soup.find(class_="main-menu")
        self.assertTrue(main_menu)
        prog_li = main_menu.find_all("li")
        self.assertEqual(16, len(prog_li))

    def test_browse(self):
        response = self.client.get("/browse/")
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find(class_="browse__root-pane"))

        link_list = soup.findAll(class_="browse__link")
        self.assertEqual(16, len(link_list))

    def test_programme(self):
        response = self.client.get("/browse/cancer/")
        soup = BeautifulSoup(response.content, "html.parser")
        section = soup.find(id="section")
        self.assertIsNotNone(section)

        link_list = soup.find(id="section").find(class_="browse__list").find_all("li")
        self.assertEqual(8, len(link_list))

    def test_branch(self):
        response = self.client.get("/browse/cancer/cancer-level-2/")
        soup = BeautifulSoup(response.content, "html.parser")
        subsection = soup.find(id="subsection")
        self.assertIsNotNone(subsection)

        link_list = (
            soup.find(id="subsection").find(class_="browse__list").find_all("li")
        )
        self.assertEqual(2, len(link_list))

    def test_get_caption(self):
        page = BasePage.objects.get(title="About cancer")
        caption = get_caption(page.id)
        self.assertEqual("Lorem ipsum dolor sit amet, consectetur adipiscing", caption)

        caption_text = ""
        while len(caption_text) < NHSEI_MAX_MENU_CAPTION_LENGTH:
            caption_text += Faker().text()
        trimmed_caption = caption_text[0:NHSEI_MAX_MENU_CAPTION_LENGTH]

        page.excerpt = trimmed_caption
        page.save()
        caption = get_caption(page.id)
        self.assertEqual(trimmed_caption, caption)

        page.excerpt = caption_text
        page.save()
        caption = get_caption(page.id)
        self.assertEqual(caption_text[0:NHSEI_MAX_MENU_CAPTION_LENGTH], caption)

    def test_url_for(self):
        item = ExtendedMainMenuItem.objects.get(link_page_id=23)
        url = url_for_link_page_id(item)
        self.assertEqual("/browse/nursing-midwifery-care-staff/", url)

    def test_menu_breadcrumb(self):
        class FakeRequest:
            path = "/browse/"

        class FakeContext:
            request = FakeRequest()

        context = FakeContext()

        breadcrumbs = menu_breadcrumb(context)
        self.assertEqual(1, len(breadcrumbs["breadcrumbs"]))
        self.assertEqual("Home", breadcrumbs["breadcrumbs"][0]["label"])
        self.assertEqual("/browse/", breadcrumbs["breadcrumbs"][0]["href"])

        context.request.path = "/browse/cancer/"
        breadcrumbs = menu_breadcrumb(context)
        self.assertEqual(2, len(breadcrumbs["breadcrumbs"]))
        self.assertEqual("Home", breadcrumbs["breadcrumbs"][0]["label"])
        self.assertEqual("/browse/", breadcrumbs["breadcrumbs"][0]["href"])
        self.assertEqual("Cancer", breadcrumbs["breadcrumbs"][1]["label"])
        self.assertEqual("/browse/cancer/", breadcrumbs["breadcrumbs"][1]["href"])

        context.request.path = "/browse/cancer/nursing-midwifery-care-staff/"
        breadcrumbs = menu_breadcrumb(context)
        self.assertEqual(3, len(breadcrumbs["breadcrumbs"]))
        self.assertEqual("Home", breadcrumbs["breadcrumbs"][0]["label"])
        self.assertEqual("/browse/", breadcrumbs["breadcrumbs"][0]["href"])
        self.assertEqual("Cancer", breadcrumbs["breadcrumbs"][1]["label"])
        self.assertEqual("/browse/cancer/", breadcrumbs["breadcrumbs"][1]["href"])
        self.assertEqual(
            "Nursing, midwifery & care staff", breadcrumbs["breadcrumbs"][2]["label"]
        )
        self.assertEqual(
            "/browse/nursing-midwifery-care-staff/",
            breadcrumbs["breadcrumbs"][2]["href"],
        )


# class TestBrowseFunctional(TestCase):
#     selenium = None
#     fixtures = ["fixtures/menu-fixtures.json"]
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = WebDriver()
#         cls.selenium.implicitly_wait(300)
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()
#
#     def test_mega_menu(self):
#         self.selenium.get(self.live_server_url)
#
#         # get the burger menu
#         burger_menu = self.selenium.find_element_by_id("toggle-menu")
#         self.assertTrue(burger_menu)
#         # get the mega menu
#         mega_menu = self.selenium.find_element_by_id("mega-menu")
#         # is the mega menu hidden by default
#         self.assertFalse(mega_menu.is_displayed())
#         # click the burger
#         burger_menu.click()
#         # can we see the mega menu
#         self.assertTrue(mega_menu.is_displayed())
