from unittest import TestCase
from crawler.crawler import Crawler

class CrawlerTest(TestCase):
    def setUp(self):
        self.crawler = Crawler()
        self.base_url = 'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591'

    def test_get_page_returns_html(self):
        page = self.crawler.get_request(self.base_url)
        self.assertIn('</html>', page)

    def test_get_pages_returns_url_list(self):
        url_list = self.crawler.get_pages(self.base_url)
        self.assertIs(type(url_list), list)

