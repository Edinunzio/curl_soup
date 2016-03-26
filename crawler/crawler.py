import csv, pycurl
from io import BytesIO
from bs4 import BeautifulSoup
"""
Write a scraper using Python 3 (ideally, or 2.7 optionally),
Pycurl and BeautifulSoup (bs4) to be used to collect all posts from all the pages of this thread in this forum: 
http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591

Required fields are: post id, name, date of the post (in text form or as is) and post body.

Output the results to a text file named forum.csv

An example of a single post in that file should look like the following:

87120;"Rick";"Mon Sep 24, 2012 4:53 pm";"Tonight, 8pm, might be worth a look...?\n\nRJ"
"""

class Crawler(object):
    def __init__(self):
        self.buffer = BytesIO()
        self.crl = pycurl.Curl()
        self.base_url = 'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591'
        self.fieldnames = ['ID', 'Name', 'Date', 'Content']
        self.posts = []
        self.post = []


    def get_request(self, url):
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
        links =  set(link['href'] for link in _links)
        return list(links)

    def get_post_id_list(self, soup):
        _post_ids = soup.select('.forumline .name a')
        return [int(_id['name']) for _id in _post_ids]

    def get_post_by_id(self, soup, post_id):
        tags = soup.select('.forumline .name a')
        for tag in tags:
            if tag['name']== str(post_id):
                return tag

    def get_user_by_post_id(self, tag, post_id):
        name = tag.next_element.text
        return name

    #def get_post_date(self, soup, post_id):
        #_post_id = soup.select('.forumline .name')

    def to_csv(self, posts, name):
        f = open('forum.csv', 'wt')
        writer = csv.writer(f, delimiter=';', lineterminator='\r\n', quotechar = '"', quoting=csv.QUOTE_NONNUMERIC)
        for post in posts:
            writer.writerow([post[0], post[1], post[2], post[3].decode('utf-8')])
        f.close()
        return posts

"""

# row should look like:
# 87120;"Rick";"Mon Sep 24, 2012 4:53 pm";"Tonight, 8pm, might be worth a look...?\n\nRJ"
# fieldnames: 
    * post id
    * name
    * date of the post (in text form or as is)  
    * post body
{"ID": 87120, "Name": "Rick", "Date": "Mon Sep 24, 2012 4:53 pm", "Content": "Tonight, 8pm, might be worth a look...?\n\nRJ"}
fieldnames = ['ID', 'Name', 'Date', 'Content']

def to_csv(scraped, name):
    f = open('forum.csv', 'wt')
    writer = csv.writer(f)
    writer.writeheader()
    for _, post in scraped.items():
        #writer.writerow(['ID', 'Name', 'Date', 'Content'])
        
        writer.writerow(post)
    f.close()


"""