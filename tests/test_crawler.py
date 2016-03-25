from unittest import TestCase
from crawler.crawler import Crawler

class CrawlerTest(TestCase):
    def setUp(self):
        self.crawler = Crawler()
        self.base_url = 'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591'

    def test_get_page_returns_html(self):
        page = self.crawler.get_request(self.base_url)
        self.assertIn('</html>', page)

    def test_soupify_response(self):
        page = self.crawler.get_request(self.base_url)
        soup = self.crawler.soupify(page)
        self.assertEquals(str(type(soup)), "<class 'bs4.BeautifulSoup'>")

    def test_get_pages_returns_url_list(self):
        page = self.crawler.get_request(self.base_url)
        soup = self.crawler.soupify(page)
        url_list = self.crawler.get_links(soup)
        self.assertIs(type(url_list), list)
        self.assertEqual(len(url_list), 8)

    def test_to_csv(self):
        id_1 = 87120
        id_2 = 871233
        name_1 = "Rick"
        name_2 = "Chuck"
        date_1 = "Mon Sep 24, 2012 4:53 pm"
        date_2 = "Mon Sep 23, 2012 4:53 pm"
        msg = "Tonight, 8pm, might be worth a look...?\n\nRJ".encode('unicode_escape')
        data = [
            [id_1, name_1, date_1, msg.decode("utf-8")],
            [id_2, name_1, date_2, msg.decode("utf-8")]
        ]
        csv = self.crawler.to_csv(data, "forum")
        self.assertEqual(data, csv)

