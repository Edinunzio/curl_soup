from unittest import TestCase
from crawler import Crawler

class CrawlerTest(TestCase):
    def setUp(self):
        self.crawler = Crawler()
        self.base_url = 'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591'

    def test_get_page_returns_valid_request(self):
        page = self.crawler.get_page()
        self.assertEqual(page.status_code, 200)