from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver


class TestBrowseUnit(TestCase):
    def test_browse(self):
        pass

    def test_browse_programme(self):
        pass

    def test_browse_branch(self):
        pass

    def test_browse(self):
        pass


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
