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


    def get_request(self, url):
        self.crl.setopt(self.crl.URL, url)
        self.crl.setopt(self.crl.WRITEDATA, self.buffer)
        self.crl.perform()
        self.crl.close()

        body = self.buffer.getvalue()
        self.body = body.decode('iso-8859-1')
        return self.body

    def get_pages(self, base_url):
        return ['a', 'b', 'c', 'd']

"""
# row should look like:
# 87120;"Rick";"Mon Sep 24, 2012 4:53 pm";"Tonight, 8pm, might be worth a look...?\n\nRJ"
# fieldnames: 
    * post id
    * name
    * date of the post (in text form or as is)  
    * post body

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