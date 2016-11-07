import sys
import sqlite3
from urllib2 import HTTPError
import requests
import csv
from bs4 import BeautifulSoup
import os
import re
import runDistSemWeighted
from pears.models import Urls
from pears import db


dm_dict = {}
drows = []
home_directory = os.path.expanduser('~')



def mk_ignore():
    #A small ignore list for sites that don't need indexing.
    ignore=["twitter", "google", "duckduckgo", "bing", "yahoo", "facebook",
            "mail.google.com", "whatsapp", "telegram", "localhost"]
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

    firefox_directory = in_dir + "/.mozilla/firefox"
    for files in os.walk(firefox_directory):
        # Build the filename
        if re.search('places.sqlite', str(os.path.join(files))):
            history_db = str(os.path.realpath(files[0]) + '/places.sqlite')
            # print history_db
            return history_db

    return None

def readDM():
    """ Read dm file """
    # Make dictionary with key=row, value=vector
    dmlines = [(each.word, each.vector) for each in
            OpenVectors.query.all()]
    for l in dmlines:
            vects = [float(each) for each in l[1].split(',')]
            dm_dict[l[0]] = normalise(vects)



def record_urls_to_process(db_urls, num_pages):
    '''Select and write urls that will be clustered.'''

    ignore_list = mk_ignore()
    urls_to_process = []
    i = 0
    for url_str in db_urls:
        url = url_str[1]
        if i <= num_pages:
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
                    if not db.session.query(Urls).filter(url==url,
                            url==url_with_www).first():
                        urls_to_process.append(url)
                        i += 1
        else:
          break


    return urls_to_process


def extract_from_url(url):
    '''From history info, extract url, title and body of page,
    cleaned with BeautifulSoup'''
    drows = []
    try:
        # TODO: Is there any issue in using redirects?
        try:
            req = requests.get(url, allow_redirects=True, timeout=20)
        except (requests.exceptions.SSLError or
                requests.exceptions.Timeout) as e:
            print "\nCaught the exception: {0}. Trying with http...\n".format(
                    str(e))
            url = url.replace("https", "http")
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

        bs_obj = BeautifulSoup(req.text,"lxml")

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
                    body = bs_obj.get_text()
                    pattern = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
                    body_str=re.sub(pattern," ",body)
                    drows = [title, url, body_str]

                if title is None:
                    title = u'Untitled'
            except HTTPError as error:
                title = u'Untitled'
            except None:
                title = u'Untitled'
        return drows
    # can't connect to the host
    except:
        error = sys.exc_info()[0]
        print "Error - %s" % error


def runScript(num_pages):
    # [TODO] Set the firefox path here via config file
    HISTORY_DB = get_firefox_history_db(home_directory)
    if HISTORY_DB is None:
        print 'Error - Cannot find the Firefox history database.\n\nExiting...'
        sys.exit(1)

    # connect to the sqlite history database
    db = sqlite3.connect(HISTORY_DB)
    cursor = db.cursor()

    # get the list of all visited places via firefox browser
    cursor.execute("SELECT * FROM 'moz_places' ORDER BY visit_count DESC")
    rows = cursor.fetchall()

    urls_to_process = record_urls_to_process(rows, num_pages)

    index_url(urls_to_process)
    db.close()

def index_url(urls_to_process):
    for url in urls_to_process:
        print "Indexing '{}'\n".format(url)
        drows = extract_from_url(url)
        if drows:
            u = Urls(url=unicode(url))
            u.title = unicode(drows[0]).encode("ascii", 'ignore')
            u.url = unicode(drows[1]).encode("ascii", 'ignore')
            u.body = unicode(drows[2]).encode("ascii", 'ignore')
            u.private = False
            db.session.add(u)
            db.session.commit()
    runDistSemWeighted.runScript(dm_dict)



if __name__ == '__main__':
    runScript(sys.argv[1])
