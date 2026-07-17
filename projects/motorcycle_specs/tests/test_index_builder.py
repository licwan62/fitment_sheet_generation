from moto_dimension_crawler.index_builder import build_index


class FakeCrawler:
    def __init__(self, pages):
        self.pages = pages
        self.requested = []

    def fetch(self, url):
        self.requested.append(url)
        return self.pages.get(url), {}, False


def test_build_index_follows_brand_catalog_pagination_only():
    home = "https://www.motorcyclespecs.co.za/"
    bmw1 = "https://www.motorcyclespecs.co.za/bikes/bmw.html"
    bmw2 = "https://www.motorcyclespecs.co.za/bikes/bmw2.html"
    pages = {
        home: '<a href="/bikes/bmw.html">BMW</a>',
        bmw1: '<a href="bmw2.html">BMW page 2</a><a href="ducati.html">Ducati</a>',
        bmw2: '<a href="/model/bmw/bmw-f750gs-21.html">BMW F 750GS 2021</a>',
    }
    crawler = FakeCrawler(pages)
    index = build_index(crawler, home, {"BMW"})

    assert bmw2 in crawler.requested
    assert "https://www.motorcyclespecs.co.za/bikes/ducati.html" not in crawler.requested
    assert any(row["page_url"].endswith("bmw-f750gs-21.html") for row in index)
