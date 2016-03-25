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

    def get_page(self):
        self.status_code = 200
        return self
        #request = {}
        #request['status_code'] = 200
        #return request


    """
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://pycurl.io/')
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    # Body is a byte string.
    # We have to know the encoding in order to print it to a text file
    # such as standard output.
    print(body.decode('iso-8859-1')
    """