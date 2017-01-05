#For people who want to play with local indexing of Wikipedia using XOWA


def local_to_www(url):
  '''A hack to deal with locally indexed Wikipedia pages'''
  if "http://localhost:8080/en.wikipedia.org/" in url:
    url = url.replace("http://localhost:8080/","http://")
  return url

def xowa_to_www_title(title):
  return title.replace(" - XOWA"," - Wikipedia")
