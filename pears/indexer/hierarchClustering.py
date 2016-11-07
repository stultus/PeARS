####################################################################
####################################################################
import scipy.cluster.hierarchy as hac
from operator import itemgetter, attrgetter
import numpy as np
import sys
import os
import re
from pears.models import Urls
from pears import db


dm_dict={}    #Dictionary to store dm file

############################################
# Cosine similarity
############################################

def cosine_similarity(peer_v, query_v):
  if len(peer_v) != len(query_v):
    raise ValueError("Peer vector and query vector must be "
                   " of same length")
  num = dot(peer_v, query_v)
  den_a = dot(peer_v, peer_v)
  den_b = dot(query_v, query_v)
  return num / (sqrt(den_a) * sqrt(den_b))

#################################################
# Read dm file
#################################################

def readDM():
  urls = Urls.query.all()
  for l in urls:
    url = l.url
    doc_dist = filter(None, l.dists.split(' '))
    vdocdist = np.array([float(i) for i in doc_dist])
    dm_dict[url]=vdocdist


##################################################
# Delete from DB
##################################################

def delete_from_db(url):
  db.session.query(Urls).filter_by(url=url).delete()
  db.session.commit()


##################################################
# Set private/public flag
##################################################

def set_privacy_flag(url,private_bool):
  matches = db.session.query(Urls).filter_by(url=url).all()
  for m in matches:
    m.private = private_bool
    db.session.add(m)
  db.session.commit()


##################################################
# Process lemmatised file
##################################################

def processFile(threshold):
  i=0                             #Iterator
  matrix=[]
  urls=[]

  for k,v in dm_dict.items():
    if np.linalg.norm(v) != 0:
      matrix.append(v)
      urls.append(k)

  z = hac.linkage(np.array(matrix), metric='cosine', method='complete')
  z=z.clip(0)
  clusters=hac.fcluster(z, threshold, criterion="distance")
  #clusters=hac.fcluster(z, 2, 'maxclust')

  readable_clusters={}
  i=0
  for c in clusters:
    if c in readable_clusters:
      readable_clusters[c].append(urls[i])
    else:
      readable_clusters[c]=[urls[i]]
    i+=1
  print len(readable_clusters),"clusters found!"
  for c,v in readable_clusters.items():
    print "CLUSTER"
    for item in v:
      print item
    user_input = raw_input("Keep? (y/n) ")
    if user_input == "y":
      for item in v:
        set_privacy_flag(item,True)



def runScript(threshold):
  readDM()    #Load the semantic space
  clusters=processFile(threshold)

  remaining_urls = [(each.url,each.private) for each in Urls.query.all()]
  for r in remaining_urls:
    print r


  # when executing as script
if __name__ == '__main__':
    runScript(sys.argv[1])
