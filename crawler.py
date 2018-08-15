# work with python2.7
from bs4 import BeautifulSoup
import urllib2
import os
import json
import sys
import re
import shutil

root_dir = "resources"

import requests

def recreate_dir(path):
    """recreate dir: if exists, then purge, if not, then create"""
    print("re-create directory: ", path)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def download_file(url, local_filename):
    # NOTE the stream=True parameter
    # credit: https://blog.csdn.net/winterto1990/article/details/51220307
    r = requests.get(url, stream=True, timeout=100)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                


course_url = "http://web.stanford.edu/class/cs142"
crawl_url="http://web.stanford.edu/class/cs142/lectures.html"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(crawl_url,headers=header)),'html.parser')


seq_num = 1
for x in soup.find_all(name="a"):
    for y in re.findall("href=\".+?\"", str(x)):
        post_url = y.replace("href=\"", '').replace("\"", '')
        if post_url.endswith(".pdf"):
            file_name = os.path.join("Lectures", "{}_{}".format(seq_num, post_url.split('/')[-1]))
            down_url = course_url + '/' +post_url
            print("downloading {} to {}".format(down_url, file_name))
            download_file(down_url, file_name)
            seq_num += 1