import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import urlretrieve
from urlparse import urlparse, urljoin

#TODO: issue when indexing top domain
#check http links in same domain


url = sys.argv[1]

def cache_file(url):
  url_parsed = urlparse(url)
  print "URL_PARSED:",url_parsed
  path_dirs = url_parsed.path.rstrip('/')[1:].split('/')
  print "PATH_DIRS:",path_dirs
  page = path_dirs[-1]
  print "PAGE:",page
  cached_netloc = "./html_cache/"+url_parsed.netloc
  cached_dir = cached_netloc+"/"+'/'.join(path_dirs[:-1])+"/"
  print "CACHED_DIR:",cached_dir
  if not os.path.isdir(cached_dir):
    os.makedirs(cached_dir)
  cached_page = cached_dir+page
  print "CACHED_PAGE:",cached_page
  if not os.path.exists(cached_page):
    urlretrieve(url, cached_page)

def get_images(url):
  """Downloads all the images at 'url' to cache"""
  req = requests.get(url, allow_redirects=True, timeout=20)
  soup = BeautifulSoup(req.text,"lxml")
  url_parsed = list(urlparse(url))
  for image in soup.findAll("img"):
    print "Image: %(src)s" % image
    if not image["src"].lower().startswith("http"):
      img_path = urljoin(url,image["src"])
      print img_path
      cache_file(img_path)

def get_css(url):
  """Downloads all the css to local cache"""
  req = requests.get(url, allow_redirects=True, timeout=20)
  soup = BeautifulSoup(req.text,"lxml")
  url_parsed = list(urlparse(url))
  for link in soup.findAll("link"):
    if link["rel"][0] == "stylesheet":
      print "Link: %(href)s" % link
      if not link["href"].lower().startswith("http"):
        css_path = urljoin(url,link["href"])
        print css_path
        cache_file(css_path)


cache_file(url)
get_images(url)
get_css(url)
