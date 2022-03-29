from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from faker import Faker as fk
from selenium.webdriver.chrome.webdriver import WebDriver

from cms.browse.templatetags.browse_tags import get_caption, url_for, menu_breadcrumb
from cms.core.models import ExtendedMainMenuItem
from cms.pages.models import BasePage
from cms.settings.base import NHSEI_MAX_CATION_LENGTH


class TestBrowseUnit(TestCase):
    fixtures = ["fixtures/menu-fixtures.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.faker = fk()

    def test_get_caption(self):
        page = BasePage.objects.get(title="About cancer")
        caption = get_caption(page.id)
        self.assertEqual("Lorem ipsum dolor sit amet, consectetur adipiscing", caption)

        caption_text = ""
        while len(caption_text) < NHSEI_MAX_CATION_LENGTH:
            caption_text += self.faker.text()
        trimmed_caption = caption_text[0:NHSEI_MAX_CATION_LENGTH]

        page.excerpt = trimmed_caption
        page.save()
        caption = get_caption(page.id)
        self.assertEqual(trimmed_caption, caption)

        page.excerpt = caption_text
        page.save()
        caption = get_caption(page.id)
        self.assertEqual(caption_text[0:NHSEI_MAX_CATION_LENGTH], caption)

    def test_url_for(self):
        item = ExtendedMainMenuItem.objects.get(link_page_id=23)
        url = url_for(item)
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


class TestBrowseFunctional(StaticLiveServerTestCase):
    selenium = None
    fixtures = ["fixtures/testdata.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_mega_menu(self):
        self.selenium.get(self.live_server_url)

        # get the burger menu
        burger_menu = self.selenium.find_element_by_id("toggle-menu")
        self.assertTrue(burger_menu)
        # get the mega menu
        mega_menu = self.selenium.find_element_by_id("mega-menu")
        # is the mega menu hidden by default
        self.assertFalse(mega_menu.is_displayed())
        # click the burger
        burger_menu.click()
        # can we see the mega menu
        self.assertTrue(mega_menu.is_displayed())
        # Check we can see corporate menu without caption
        # Check we can see programmes with captions
        # check clicking a programme takes you to the browse pages

    def test_browse(self):
        self.selenium.get("%s/%s" % (self.live_server_url, "/browse"))

    def test_programme(self):
        pass

    def test_branch(self):
        pass

    def test_leaf(self):
        pass
