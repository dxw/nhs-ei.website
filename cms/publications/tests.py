from bs4 import BeautifulSoup
from django.test import TestCase

from cms.publications.models import Publication, PublicationIndexPage, TOC


class TestPublicationIndexPage(TestCase):

    # or load whichever file you piped it to
    fixtures = ["fixtures/testdata.json"]

    def test_first_heading(self):
        response = self.client.get("/publications-index-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        heading = soup.select_one("main h1")

        self.assertEqual(heading.text, "Publications Index Page")

    def test_first_paragrpah(self):
        response = self.client.get("/publications-index-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        heading = soup.select_one("main p")

        self.assertEqual(heading.text, "Publications index page content")

    def test_side_bar(self):
        # in the test data we have 2 of each of settings, regions and topics
        # check that all show up in a-z order and link to correct url
        response = self.client.get("/publications-index-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        publication_type_1 = soup.select_one('main a[href="?publication_type=1"]')
        publication_type_2 = soup.select_one('main a[href="?publication_type=2"]')

        self.assertEqual(publication_type_1.text, "Publication Type One")
        self.assertEqual(publication_type_1["href"], "?publication_type=1")
        self.assertEqual(publication_type_2.text, "Publication Type Two")
        self.assertEqual(publication_type_2["href"], "?publication_type=2")

    def test_publications_list(self):
        response = self.client.get("/publications-index-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        publication_newest = soup.select_one(
            "main .nhsuk-width-container:nth-child(1) .nhsuk-panel:nth-of-type(1)"
        )

        # heading
        self.assertEqual(
            publication_newest.select_one("h2").text.strip(), "Publication Two"
        )
        self.assertEqual(
            publication_newest.select_one("h2 a")["href"],
            "/publications-index-page/publication-two/",
        )

        # paragraph
        self.assertEqual(
            publication_newest.select_one("div.nhsuk-u-margin-bottom-3").text.strip(),
            "Publication two content",
        )

        # dates
        self.assertIn(
            publication_newest.select_one("p.nhsuk-body-s").text.strip()[:23],
            "Published:  04 Feb 2021 -",
        )

        # links
        self.assertEqual(
            publication_newest.select_one(
                "p.nhsuk-body-s a:nth-of-type(1)"
            ).text.strip(),
            "Publication Type Two",
        )
        self.assertEqual(
            publication_newest.select_one("p.nhsuk-body-s a:nth-of-type(1)")["href"],
            "?publication_type=2",
        )

        self.assertEqual(
            publication_newest.select_one(
                "p.nhsuk-body-s a:nth-of-type(2)"
            ).text.strip(),
            "Category Two",
        )
        self.assertEqual(
            publication_newest.select_one("p.nhsuk-body-s a:nth-of-type(2)")["href"],
            "?category=2",
        )

        publication_oldest = soup.select_one(
            "main .nhsuk-width-container:nth-child(1) .nhsuk-panel:nth-of-type(2)"
        )

        # heading
        self.assertEqual(
            publication_oldest.select_one("h2").text.strip(), "Publication One"
        )
        self.assertEqual(
            publication_oldest.select_one("h2 a")["href"],
            "/publications-index-page/publication-one/",
        )

        # paragraph
        self.assertEqual(
            publication_oldest.select_one("div.nhsuk-u-margin-bottom-3").text.strip(),
            "Publication one content",
        )

        # dates
        self.assertIn(
            publication_oldest.select_one("p.nhsuk-body-s").text.strip()[:23],
            "Published:  04 Feb 2021 -",
        )

        # links
        self.assertEqual(
            publication_oldest.select_one(
                "p.nhsuk-body-s a:nth-of-type(1)"
            ).text.strip(),
            "Publication Type One",
        )
        self.assertEqual(
            publication_oldest.select_one("p.nhsuk-body-s a:nth-of-type(1)")["href"],
            "?publication_type=1",
        )

        self.assertEqual(
            publication_oldest.select_one(
                "p.nhsuk-body-s a:nth-of-type(2)"
            ).text.strip(),
            "Category One",
        )
        self.assertEqual(
            publication_oldest.select_one("p.nhsuk-body-s a:nth-of-type(2)")["href"],
            "?category=1",
        )


class TestPublication(TestCase):

    # or load whichever file you piped it to
    fixtures = ["fixtures/testdata.json"]

    # theres a couple of pages worth testing

    def test_oldest_publication(self):
        # this page is using a PDF document link
        response = self.client.get("/publications-index-page/publication-one/")
        soup = BeautifulSoup(response.content, "html.parser")

        # page title
        title = soup.select_one("main h1").text.strip()
        self.assertEqual(title, "Publication One")

        # page content
        content = soup.select_one("#content p").text.strip()
        self.assertEqual(content, "Publication one content")

        # review date
        # better to test these actual date objects as unittest I think, one for later
        date_container = soup.select_one("main .nhsuk-review-date p")
        self.assertIn(date_container.text.strip()[:27], "Date published: 04 Feb 2021")

        # taxonomy links
        topic_1 = soup.select_one("main .nhsuk-u-reading-width a")
        self.assertEqual(topic_1["href"], "/publications-index-page/?category=1")
        self.assertEqual(topic_1.text.strip(), "Category One")

        publication_type_1 = soup.select_one("main a:nth-of-type(2)")
        self.assertEqual(
            publication_type_1["href"], "/publications-index-page/?publication_type=1"
        )
        self.assertEqual(publication_type_1.text.strip(), "Publication Type One")

        # document card
        title = soup.select_one("main .nhsuk-card h2.nhsuk-card__heading")
        self.assertEqual(title.text.strip(), "Document Title")
        self.assertEqual(
            title.select_one("a")["href"], "/documents/1/sample-pdf-file.pdf"
        )

        # i noticed that the h2 a has a p tag inside so do it this way
        file_size = soup.select_one(
            "main .nhsuk-card p:nth-child(2)"
        )  # its the first p tag of card
        self.assertIn(file_size.text.strip()[:10], "file size:")

        summary = soup.select_one("main .nhsuk-card .nhsuk-card__description p")
        self.assertEqual(summary.text.strip(), "Document Summary")

        svg = soup.select_one("main .nhsuk-card svg")
        self.assertEqual(svg.select_one("title").text.strip(), "PDF")

    def test_newset_publication(self):
        # this page is using a action link to a page
        response = self.client.get("/publications-index-page/publication-two/")
        soup = BeautifulSoup(response.content, "html.parser")

        # page title
        title = soup.select_one("main h1").text.strip()
        self.assertEqual(title, "Publication Two")

        # page content
        content = soup.select_one("#content p").text.strip()
        self.assertEqual(content, "Publication two content")

        # review date
        # better to test these actual date objects as unittest I think, one for later
        date_container = soup.select_one("main .nhsuk-review-date p")
        self.assertIn(date_container.text.strip()[:27], "Date published: 04 Feb 2021")

        # taxonomy links
        topic_1 = soup.select_one("main .nhsuk-u-reading-width a")
        self.assertEqual(topic_1["href"], "/publications-index-page/?category=2")
        self.assertEqual(topic_1.text.strip(), "Category Two")

        publication_type_1 = soup.select_one("main a:nth-of-type(2)")
        self.assertEqual(
            publication_type_1["href"], "/publications-index-page/?publication_type=2"
        )
        self.assertEqual(publication_type_1.text.strip(), "Publication Type Two")

        # document card
        title = soup.select_one("main .nhsuk-card h2.nhsuk-card__heading")
        self.assertEqual(title.text.strip(), "A Document With A Link To A Page")
        self.assertEqual(
            title.select_one("a")["href"],
            "/blog-index-page/",
        )

    def test_publication_pdf(self):
        """A publication can be downloaded as a PDF file"""
        response = self.client.get("/publications-index-page/publication-one/pdf/")
        self.assertEqual(response["content-type"], "application/pdf")
        self.assertEqual(
            response["content-disposition"],
            'attachment;filename="publication-one_2021-02-05.pdf"',
        )


class TestTocModelSave(TestCase):
    fixtures = ["fixtures/testdata.json"]

    def test_toc_links_on_webpage(self):
        # create a dummy content item
        parent = PublicationIndexPage.objects.first()
        page = Publication()
        page.body = '<h2 data-block-key="jaooc">a h2</h2><p data-block-key="47hga">not a h2</p><h2 data-block-key="4g0tt">another h2</h2><p data-block-key="1j3kd">still not a h2</p>'
        page.slug = "base-page"
        page.source = "root"
        page.title = "Test TOC Page"
        parent.add_child(instance=page)
        # save it (when we save, this will generate the table of contents and add ids to the h2 tags)
        page.save()

        response = self.client.get("/publications-index-page/base-page/")

        # load it again and check we have anchor tags
        body = str(response.content)
        soup = BeautifulSoup(body, "html.parser")
        h2s = [h2.get("id") for h2 in soup.find_all("h2")]
        self.assertIn("a-h2", h2s)
        self.assertIn("another-h2", h2s)

        # check the TOC table for anchors
        tocs = soup.select("#publication-toc a")
        self.assertEqual(2, len(tocs))
        self.assertEqual("#a-h2", tocs[0].attrs["href"])
        self.assertEqual("a h2", tocs[0].text)
        self.assertEqual("#another-h2", tocs[1].attrs["href"])
        self.assertEqual("another h2", tocs[1].text)

        # page content
        content = soup.select_one("#content p").text.strip()
        self.assertEqual(content, "not a h2")
