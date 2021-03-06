import csv, pycurl
from io import BytesIO
from bs4 import BeautifulSoup

class Crawler(object):
    def __init__(self):
        self.base_url = 'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591'

    def get_request(self, url):
        self.buffer = BytesIO()
        self.crl = pycurl.Curl()
        self.crl.setopt(self.crl.URL, url)
        self.crl.setopt(self.crl.WRITEDATA, self.buffer)
        self.crl.perform()
        self.crl.close()

        body = self.buffer.getvalue()
        self.body = body.decode('iso-8859-1')
        return self.body

    def soupify(self, response):
        return BeautifulSoup(response, 'html.parser')

    def get_links(self, soup):
        _links = soup.select('.gensmall a')
        links =  [link['href'] for link in _links]
        return list(links[:-1])

    def get_post_id_list(self, soup):
        _post_ids = soup.select('.forumline .name a')
        return [int(_id['name']) for _id in _post_ids]

    def get_tag_by_id(self, soup, post_id):
        tags = soup.select('.forumline .name a')
        for tag in tags:
            if tag['name']== str(post_id):
                return tag

    def get_user_by_post_id(self, tag):
        name = tag.next_element.text
        return name

    def get_post_date(self, tag):
        post_date = tag.previous_element.previous_element.find_next_sibling('td').span.contents
        return post_date[0].strip('Posted: ')

    def get_post_msg(self, tag):
        post_msg = tag.previous_element.previous_element.find_next_sibling('td').table.tr.find_next_sibling('tr').find_next_sibling('tr').span
        if post_msg.text == '':
            post_msg = tag.previous_element.previous_element.find_next_sibling('td').table.tr.find_next_sibling('tr').find_next_sibling('tr')
            post_msg = post_msg.text.split('_________________')
            return post_msg[0]
        post_msg = post_msg.text.split('_________________')
        return post_msg[0]

    def build_post_data(self, soup, post_id):
        tag = self.get_tag_by_id(soup, post_id)
        name = self.get_user_by_post_id(tag)
        post_date = self.get_post_date(tag)
        msg = self.get_post_msg(tag)
        return [post_id, name, post_date, msg.encode('unicode_escape')]

    def to_csv(self, posts, name):
        f = open(name+'.csv', 'wt')
        writer = csv.writer(f, delimiter=';', lineterminator='\r\n', quotechar = '"', quoting=csv.QUOTE_NONNUMERIC)
        for post in posts:
            writer.writerow([post[0], post[1], post[2], post[3].decode('utf-8')])
        f.close()
        return posts

c = Crawler()
crawls = []
response = c.get_request('http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591')
init_soup = c.soupify(response)
links = c.get_links(init_soup)
init_post_ids = c.get_post_id_list(init_soup)
for _id in init_post_ids:
    crawls.append(c.build_post_data(init_soup, _id))
for link in links:
    _response = c.get_request('http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/'+link)
    _soup = c.soupify(_response)
    _post_ids = c.get_post_id_list(_soup)
    for _post_id in _post_ids:
        crawls.append(c.build_post_data(_soup, _post_id))
c.to_csv(crawls, 'forum')