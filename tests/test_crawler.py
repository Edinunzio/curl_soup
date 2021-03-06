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

    def test_get_post_id_list_returns_list(self):
        page = self.crawler.get_request(self.base_url)
        soup = self.crawler.soupify(page)
        post_ids = self.crawler.get_post_id_list(soup)
        self.assertIs(type(post_ids), list)
        self.assertIs(type(post_ids[0]), int)
        self.assertEqual(len(post_ids), 15)

    def test_get_tag_by_id_returns_id_tag(self):
        page = self.crawler.get_request(self.base_url)
        soup = self.crawler.soupify(page)
        tag = self.crawler.get_tag_by_id(soup, 87120)
        self.assertEquals(str(type(tag)), "<class 'bs4.element.Tag'>")

    def test_get_user_by_post_id(self):
        page = self.crawler.get_request(self.base_url)
        soup = self.crawler.soupify(page)
        tag_1 = self.crawler.get_tag_by_id(soup, 87120)
        user_1 = self.crawler.get_user_by_post_id(tag_1)
        self.assertIs(type(user_1), str)
        self.assertEqual(user_1, "Rick")
        tag_2 = self.crawler.get_tag_by_id(soup, 87131)
        user_2 = self.crawler.get_user_by_post_id(tag_2)
        self.assertIs(type(user_2), str)
        self.assertEqual(user_2, "pigtin")

    def test_get_post_date(self):
        page = self.crawler.get_request(self.base_url)
        soup = self.crawler.soupify(page)
        tag = self.crawler.get_tag_by_id(soup, 87120)
        post_date = self.crawler.get_post_date(tag)
        self.assertIs(type(post_date), str)
        self.assertNotIn(post_date, "Posted: ")

    def test_get_post_msg(self):
        page = self.crawler.get_request(self.base_url)
        soup = self.crawler.soupify(page)
        tag = self.crawler.get_tag_by_id(soup, 87120)
        post_msg = self.crawler.get_post_msg(tag)
        self.assertIs(type(post_msg), str)
        self.assertIn("Tonight, 8pm, might be worth a look", post_msg)

        tag_2 = self.crawler.get_tag_by_id(soup, 87131)
        post_msg_2 = self.crawler.get_post_msg(tag_2)
        self.assertIs(type(post_msg_2), str)
        self.assertIn("Oh dear! Just switched off", post_msg_2)
        self.assertNotIn("_________________", post_msg_2)

    def test_gets_next_msg_span_if_empty(self):
        page = self.crawler.get_request('http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591')
        soup = self.crawler.soupify(page)
        tag = self.crawler.get_tag_by_id(soup, 87140)
        post_msg = self.crawler.get_post_msg(tag)
        self.assertIs(type(post_msg), str)
        self.assertIn("i wouldn't bother", post_msg)

    def test_build_post_data(self):
        page = self.crawler.get_request(self.base_url)
        soup = self.crawler.soupify(page)
        data = self.crawler.build_post_data(soup, 87120)
        self.assertEqual(data[0:3], [87120, "Rick", "Mon Sep 24, 2012 4:53 pm"])

    def test_to_csv(self):
        id_1 = 87120
        id_2 = 871233
        name_1 = "Rick"
        name_2 = "Chuck"
        date_1 = "Mon Sep 24, 2012 4:53 pm"
        date_2 = "Mon Sep 23, 2012 4:53 pm"
        msg = "Tonight, 8pm, might be worth a look...?\n\nRJ".encode('unicode_escape')
        data = [
            [id_1, name_1, date_1, msg],
            [id_2, name_2, date_2, msg]
        ]
        csv = self.crawler.to_csv(data, "test_forum")
        self.assertEqual(data, csv)