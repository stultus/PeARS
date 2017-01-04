#Detect whether page is under CC license and a snippet can be extracted from it.

from bs4 import BeautifulSoup
import requests
import sys
import re


def open_site(url):
  '''Checking for wikipedia or SO page'''
  for i in ["wikipedia.org","stackoverflow.com"]:
    if i in url:
      return True
  return False

def cc(bs_obj):
  '''Checking for CC logo'''
  imgs = bs_obj.find_all('img')
  for img in imgs:
    src = img['src']
    for i in ["creativecommons.org","cc-by"]:
      if i in src:
        return True
  return False

def get_snippet(bs_obj):
  body = bs_obj.get_text()
  pattern = re.compile('(^[\s]+)|([\s]+$)|([\s][\s]+)', re.MULTILINE)
  body_str=re.sub(pattern," ",body)
  i=0
  snippet = ""
  for l in body_str.split('\n'):
    '''Only choose informative lines, not first in Wikipedia'''
    if len(l) > 100 and i < 2 and "Jump to:" not in l and "XOWA" not in l:
      snippet+=l.rstrip('\n')
      i+=1
  snippet = ' '.join(snippet.split(' ')[:50])
  return snippet

def try_snippet(url, bs_obj):
  '''If page is CC-licensed, get snippet'''
  snippet = ""
  is_open = False

  if open_site(url) or cc(bs_obj):
    snippet = get_snippet(bs_obj)

  return snippet
