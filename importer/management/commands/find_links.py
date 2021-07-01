from importer.importer_cls import Importer
from django.core.management.base import BaseCommand
from importer.websites import SCRAPY
import lxml.html


class Command(BaseCommand):
    """Discover hardlinks within england.nhs.uk might be broken."""

    # TODO: only does posts at the moment
    # NOTE: this command isn't plumbed into anything, probably won't ever be
    # FURTHER WORK: consider exporting as a CSV rather than printing to terminal

    help = "Report broken links thoughout the website"

    def handle(self, *args, **options):
        url = SCRAPY + "api/posts/"
        linkfinder = LinkFinder()
        linkfinder.fetch_all(url)
        linkfinder.parse_results()


class LinkFinder(Importer):
    def parse_results(self):
        pages = self.results
        count_bad = 0
        for page in pages:
            try:
                root = lxml.html.fromstring(page["content"])
            except KeyError:
                print("no body", page.keys())
            all_links = root.xpath("//a/@href")
            bad_links = [
                link
                for link in all_links
                if "england.nhs.uk" in link or link.startswith("/")
            ]
            if bad_links:
                count_bad = count_bad + 1
                print(page["source"], page["slug"], bad_links)
        print(f"{count_bad}/{len(pages)}, {count_bad*100/len(pages)}%")
