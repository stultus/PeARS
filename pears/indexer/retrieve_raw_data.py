import os
import re
import sys
import csv
import sqlite3
import requests
import numpy as np
from urllib2 import HTTPError
from bs4 import BeautifulSoup
import runDistSemWeighted
from pears.models import Urls,OpenVectors
from pears import db


dm_dict = {}
drows = []
home_directory = os.path.expanduser('~')

def local_to_www(url):
  '''A hack to deal with locally indexed Wikipedia pages'''
  if "http://localhost:8080/en.wikipedia.org/" in url:
    url = url.replace("http://localhost:8080/","http://")
  return url


def mk_ignore():
    #A small ignore list for sites that don't need indexing.
    ignore=["twitter", "google", "duckduckgo", "bing", "yahoo", "facebook",
            "mail.google.com", "whatsapp", "telegram"]
    '''Make ignore list'''
    s = []
    for i in ignore:
        s.append("www."+i)
        s.append("://"+i)
    return s


def get_firefox_history_db(in_dir):
  """Given a home directory it will search it for the places.sqlite file
  in Mozilla Firefox and return the path. This should work on Windows/
  Linux"""
  print "Finding Firefox DB history..."
  firefox_directory = in_dir + "/.mozilla/firefox"
  for files in os.walk(firefox_directory):
    # Build the filename
    if re.search('places.sqlite', str(os.path.join(files))):
      history_db = str(os.path.realpath(files[0]) + '/places.sqlite')
      # print history_db
      return history_db
  return None

def normalise(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def readDM():
    """ Read dm file """
    print "Reading vectors..."
    dmlines = [(each.word, each.vector) for each in
            OpenVectors.query.all()]
    c = 0
    for l in dmlines:
      #if c < 10000:
      vects = [float(each) for each in l[1].split(',')]
      dm_dict[l[0]] = normalise(vects)
      c+=1
    print "Finished! Read",c,"vectors..."

def record_urls_to_process(db_urls, num_pages):
    '''Select and write urls that will be clustered.'''
    print "Now writing the",num_pages,"pages to process..."
    ignore_list = mk_ignore()
    urls_to_process = []
    i = 0
    for url_str in db_urls:

        url = unicode(url_str[1])
        if i < num_pages:
            if not any( i in url for i in ignore_list):
                if not url.startswith('http'):
                    continue
                url = url.replace('http://', 'https://').rstrip('/')
                if url not in urls_to_process:
                    if "www" not in url:
                        url_with_www = url.replace("https://", "https://www.")
                        if url_with_www in urls_to_process:
                            continue
                    else:
                        url_with_www = url
                    if not db.session.query(Urls).filter_by(url=url).all():
                      urls_to_process.append(url)
                      print "...writing",url,"..."
                      i+=1
                    else:
                      print url,"is already known..."
        else:
          print "Recorded",len(urls_to_process),"urls..."
          break

    return urls_to_process


def extract_from_url(url):
    '''From history info, extract url, title and body of page,
    cleaned with BeautifulSoup'''
    drows = []
    try:
        # TODO: Is there any issue in using redirects?
        try:
            req = requests.get(unicode(url), allow_redirects=True, timeout=20)
        except (requests.exceptions.SSLError or
                requests.exceptions.Timeout) as e:
            print "\nCaught the exception: {0}. Trying with http...\n".format(
                    str(e))
            url = unicode(url.replace("https", "http"))
            req = requests.get(url, allow_redirects=True)
        except requests.exceptions.RequestException as e:
            print "Ignoring {0} because of error {1}\n".format(url,
                    str(e))
            return
        except requests.exceptions.HTTPError as err:
            print str(err)
            return
        req.encoding = 'utf-8'

        if req.status_code is not 200:
            print "Warning: "  + str(req.url) + ' has a status code of: ' \
                + str(req.status_code) + ' omitted from database.\n'

        bs_obj = BeautifulSoup(unicode(req.text),"lxml")

        if hasattr(bs_obj.title, 'string') \
                & (req.status_code == requests.codes.ok):
            try:
                title = unicode(bs_obj.title.string)
                if url.startswith('http'):
                    if title is None:
                        title = u'Untitled'
                    checks = ['script', 'style', 'meta', '<!--']
                    for chk in bs_obj.find_all(checks):
                        chk.extract()
                    body = unicode(bs_obj.get_text())
                    pattern = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
                    body_str=re.sub(pattern," ",body)
                    www_url = local_to_www(url)
                    drows = [title, www_url, body_str]

                if title is None:
                    title = u'Untitled'
            except HTTPError as error:
                title = u'Untitled'
            except None:
                title = u'Untitled'
        #print "Processed",url,"..."
        return drows
    # can't connect to the host
    except:
        error = sys.exc_info()[0]
        print "Error - %s" % error

def index_url(urls_to_process):
    for url in urls_to_process:
        print "Indexing '{}'\n".format(url)
        drows = extract_from_url(url)
        if drows:
            u = Urls(url=unicode(url))
            u.title = unicode(drows[0])
            u.url = unicode(drows[1])
            u.body = unicode(drows[2])
            u.private = False
            db.session.add(u)
            db.session.commit()
    runDistSemWeighted.runScript()

def index_history(num_pages):
  # [TODO] Set the firefox path here via config file
  HISTORY_DB = get_firefox_history_db(home_directory)
  if HISTORY_DB is None:
    print 'Error - Cannot find the Firefox history database.\n\nExiting...'
    sys.exit(1)

  # connect to the sqlite history database
  firefox_db = sqlite3.connect(HISTORY_DB)
  cursor = firefox_db.cursor()

  # get the list of all visited places via firefox browser
  cursor.execute("SELECT * FROM 'moz_places' ORDER BY visit_count DESC")
  rows = cursor.fetchall()

  urls_to_process = record_urls_to_process(rows, int(num_pages))
  firefox_db.close()
  return urls_to_process


def index_from_file(filename):
  f = open(filename,'r')
  urls_to_process = []
  for url in f:
    url = url.rstrip('\n')
    www_url = local_to_www(url)
    if not db.session.query(Urls).filter_by(url=www_url).all():
      urls_to_process.append(url)
      print "...writing",url,"..."
    else:
      print url,"is already known..."
  return urls_to_process


def runScript(switch, arg):
  '''Run script, either by indexing part of history or by indexing the urls
  provided by the user'''
  readDM()
  urls_to_process = []

  if switch == "history":
    urls_to_process = index_history(arg)

  if switch == "file":
    urls_to_process = index_from_file(arg)

  index_url(urls_to_process)

if __name__ == '__main__':
  runScript(sys.argv[1], sys.argv[2])
