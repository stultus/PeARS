import re
import sys


def jaccard(a, b):
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def dice(a, b):
    c = a.intersection(b)
    return float(2 * len(c)) / (len(a) + len(b))


def score_url_overlap(query, url):
    url = url.rstrip('/')  # Strip last backslash if there is one
    m = re.search('.*/([^/]+)', url)  # Get last element in url
    if m:
        url = m.group(1)

    # print jaccard(set(query.lower()), set(url.lower()))
    return dice(set(query.lower()), set(url.lower()))

def generic_overlap(i1,i2):
  '''Generic overlap calculation between two strings'''
  return dice(set(i1.lower()), set(i2.lower()))


