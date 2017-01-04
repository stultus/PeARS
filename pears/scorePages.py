""" Compares the query to each document
Called by ./mkQueryPage.py
"""

import os, requests, ipgetter
import re
import sys
import urllib
import webbrowser
from operator import itemgetter
from pears import db
import socket
import math
import numpy

import getUrlOverlap
from .utils import query_distribution, cosine_similarity, print_timing
from .models import Urls
import cStringIO


def scoreDS(query_dist, pear_urls):
    """ Get distributional score """
    DS_scores = {}
    wordclouds = {}
    titles = {}
    for val in pear_urls:
        url = val['url']
        doc_dist = val['dists']
        d = cStringIO.StringIO(str(doc_dist))
        vector = numpy.loadtxt(d)
        wordclouds[url] = val['wordclouds']
        titles[url] = val['title']
        if vector.all():
            score = cosine_similarity(vector, query_dist)
            if score > 0.3:  # Doc must be good enough
                DS_scores[url] = score
        else:
            Urls.query.filter_by(url=url).delete()
            db.session.commit()
    return DS_scores, wordclouds, titles


def scoreURL(query, pear_urls):
    """ Get url overlap score """
    URL_scores = {}
    for val in pear_urls:
      url = val['url']
      URL_scores[url] = getUrlOverlap.runScript(query, url)
    return URL_scores


def scoreDocs(query, query_dist, pear_urls):
    """ Score documents for a pear """
    document_scores = {}  # Document scores
    DS_scores, wordclouds, titles = scoreDS(query_dist, pear_urls)
    URL_scores = scoreURL(query, pear_urls)
    for val in pear_urls:
      v = val['url']
      if v in DS_scores and v in URL_scores:
        # If URL overlap high (0.2 because of averag e length of
        # query=4 -- see getUrlOverlap --  and similarity okay
        if URL_scores[v] > 0.7 and DS_scores[v] > 0.2:
          document_scores[v] = DS_scores[v] + URL_scores[v] * 0.2  # Boost DS score by a maximum of 0.2
        else:
          document_scores[v] = DS_scores[v]
        if math.isnan(document_scores[v]):  # Check for potential NaN -- messes up with sorting in bestURLs.
          document_scores[v] = 0
    return document_scores, wordclouds, titles


def bestURLs(doc_scores):
    best_urls = []
    c = 0
    for w in sorted(doc_scores, key=doc_scores.get, reverse=True):
        if c < 50:
          best_urls.append(w)
          c += 1
        else:
            break
    return best_urls


def ddg_redirect(query):
    print "No suitable pages found."
    duckquery = ""
    for w in query.rstrip('\n').split():
        duckquery = duckquery + w + "+"
    webbrowser.open_new_tab(
            "https://duckduckgo.com/?q=" +
            duckquery.rstrip('+'))
    return

def output(best_urls, url_titles, url_wordclouds):
    results = []
    # If documents matching the query were found on the pear network...
    if len(best_urls) > 0:
        for u in best_urls:
            results.append([u, url_titles[u], url_wordclouds[u]])

    # Otherwise, open duckduckgo and send the query there
    else:
        results = []
    return results


def get_pear_urls(ip):
    my_ip = ipgetter.myip()
    if ip == my_ip:
        urls = Urls.query.all()
        return [u.__dict__ for u in urls]
    else:
        return requests.get("http://{}:5000/api/urls".format(ip)).text

def runScript(query, query_dist, pears):
    url_wordclouds = {}
    url_titles = {}
    best_urls = []
    for pear in pears:
        pear_urls = get_pear_urls(pear)
        document_scores, wordclouds, titles = scoreDocs(query, query_dist, pear_urls)	#with URL overlap
        #document_scores, wordclouds = scoreDS(query_dist, pear_urls)  # without URL overlap
        url_wordclouds.update(wordclouds)
        url_titles.update(titles)
        best_urls = bestURLs(document_scores)
    return output(best_urls, url_titles, url_wordclouds)


if __name__ == '__main__':
    runScript(sys.argv[1], sys.argv[2], sys.argv[3])
