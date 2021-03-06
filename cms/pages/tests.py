from bs4 import BeautifulSoup
from django.test import TestCase


class TestComponentsPage(TestCase):

    # or load whichever file you piped it to
    fixtures = ["fixtures/testdata.json"]

    def test_first_heading(self):
        response = self.client.get("/component-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        heading = soup.select_one("main h1")

        self.assertEqual(heading.text, "Component Page")

    def test_recent_panel(self):
        response = self.client.get("/component-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        panel = soup.select_one("main .category-latest")

        heading = panel.select_one("h2")
        self.assertEqual(heading.text, "Recent Posts")

        items = panel.find_all("div", class_="item-card")

        first_item = items[0]
        first_item_link = first_item.select_one("a")

        self.assertEqual(first_item_link["href"], "/post-index-page/post-two/")
        self.assertEqual(first_item_link.text.strip(), "Post Two")

        second_item = items[1]
        second_item_link = second_item.select_one("a")

        self.assertEqual(second_item_link["href"], "/post-index-page/post-one/")
        self.assertEqual(second_item_link.text.strip(), "Post One")

    def test_all_common_blocks(self):
        response = self.client.get("/base-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        # Action links
        action_links = soup.find_all("div", "nhsuk-action-link")
        self.assertEqual(len(action_links), 3)
        self.assertEqual(
            action_links[0].find("span", "nhsuk-action-link__text").string,
            "Example Link",
        )
        self.assertEqual(
            action_links[1].find("span", "nhsuk-action-link__text").string,
            "Example Link New Window",
        )
        self.assertEqual(
            action_links[1].find("a", "nhsuk-action-link__link")["target"], "_blank"
        )
        self.assertEqual(
            action_links[2].find("span", "nhsuk-action-link__text").string,
            "Example expander group block action link, opens a new window",
        )
        self.assertEqual(
            action_links[2].find("a", "nhsuk-action-link__link")["target"], "_blank"
        )

        # Do don't list
        do_dont_lists = soup.find_all("div", "nhsuk-do-dont-list")
        self.assertEqual(len(do_dont_lists), 2)

        do_list = do_dont_lists[0]
        dont_list = do_dont_lists[1]

        self.assertEqual(len(do_list.find("ul", "nhsuk-list").find_all("li")), 2)
        self.assertEqual(len(dont_list.find("ul", "nhsuk-list").find_all("li")), 2)

        self.assertTrue("nhsuk-list--tick" in do_list.find("ul", "nhsuk-list")["class"])
        self.assertTrue(
            "nhsuk-list--cross" in dont_list.find("ul", "nhsuk-list")["class"]
        )

        # Inset text
        inset_text_block = soup.find("div", "nhsuk-inset-text")
        self.assertEqual(inset_text_block.find("p").string, "Inset text block")

        # Image block
        image_block = soup.find("figure", "nhsuk-image")
        self.assertTrue(image_block.find("img", "nhsuk-image__img"))
        self.assertTrue(image_block.find("figcaption", "nhsuk-image__caption"))
        self.assertEqual(
            image_block.find("figcaption", "nhsuk-image__caption").string.strip(),
            "Image block",
        )

        panel_group = soup.find("ul", "nhsuk-card-group")
        self.assertEqual(len(panel_group.find_all("li", "nhsuk-card-group__item")), 2)

        # Warning
        warning_callout = soup.find("div", "nhsuk-warning-callout")
        self.assertEqual(
            warning_callout.find("h3", "nhsuk-warning-callout__label").string.strip(),
            "Warning callout block",
        )
        self.assertEqual(
            warning_callout.find("p").string, "Warning callout block content"
        )

    def test_nhsuk_banner(self):
        response = self.client.get("/base-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        banner = soup.select_one(".nhs-banner")
        self.assertEquals(
            "For any medical advice relating to kittens please visit NHS.uk",
            banner.text.strip(),
        )
        self.assertIn("https://nhs.uk/kittens", str(banner))
