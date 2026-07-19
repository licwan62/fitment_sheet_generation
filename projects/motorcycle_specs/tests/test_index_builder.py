from moto_dimension_crawler.index_builder import build_1000ps_index, build_bikedekho_index, build_bikez_index, build_index


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


def test_bikedekho_index_uses_specs_sitemap_and_filters_brand():
    sitemap = "https://www.bikedekho.com/ModelSpecifications.xml"
    pages = {
        sitemap: """<urlset>
          <url><loc>https://www.bikedekho.com/bmw-scooters/c-400-gt/specifications</loc></url>
          <url><loc>https://www.bikedekho.com/hi/bmw-scooters/c-400-gt/specifications</loc></url>
          <url><loc>https://www.bikedekho.com/honda/shine/specifications</loc></url>
        </urlset>""",
    }
    index = build_bikedekho_index(FakeCrawler(pages), "https://www.bikedekho.com/", {"BMW"})

    assert [row["page_url"] for row in index] == [
        "https://www.bikedekho.com/bmw-scooters/c-400-gt/specifications"
    ]
    assert index[0]["page_title"] == "BMW c 400 gt"
    assert index[0]["source_name"] == "bikedekho"


def test_1000ps_index_uses_brand_directory_and_keeps_multiple_models():
    brands = "https://www.1000ps.com/en-gb/brands"
    bmw = "https://www.1000ps.com/en-gb/brand/7/bmw"
    pages = {
        brands: '<a href="/en-gb/brand/7/bmw">BMW</a><a href="/en-gb/brand/2/honda">Honda</a>',
        bmw: '<a href="/en-gb/model/9553/bmw-c-400-gt">Details</a><a href="/en-gb/model/3723/bmw-s-1000-rr">Details</a>',
    }
    crawler = FakeCrawler(pages)
    index = build_1000ps_index(crawler, "https://www.1000ps.com/", {"BMW"}, 2)

    assert bmw in crawler.requested
    assert not any("/brand/2/honda" in url for url in crawler.requested)
    assert {row["page_title"] for row in index} == {"bmw c 400 gt", "bmw s 1000 rr"}
    assert all(row["source_name"] == "1000ps" and row["source_priority"] == 2 for row in index)


def test_bikez_index_follows_only_selected_brand_pages():
    brands = "https://bikez.com/brands/index.php"
    bmw = "https://bikez.com/brand/bmw_motorcycles.php"
    bmw2 = "https://bikez.com/brand/bmw_motorcycles.php?page=2"
    pages = {
        brands: '<a href="/brand/bmw_motorcycles.php">BMW motorcycles 100</a><a href="/brand/honda_motorcycles.php">Honda motorcycles 100</a>',
        bmw: '<a href="?page=2">Next</a><a href="/motorcycles/bmw_c_400_gt_2025.php">BMW C 400 GT</a>',
        bmw2: '<a href="/motorcycles/bmw_c_400_gt_2024.php">BMW C 400 GT</a>',
    }
    crawler = FakeCrawler(pages)
    index = build_bikez_index(crawler, "https://bikez.com/", {"BMW"}, 3)

    assert bmw2 in crawler.requested
    assert not any("honda_motorcycles" in url for url in crawler.requested)
    assert len(index) == 2
    assert all(row["source_priority"] == 3 for row in index)
