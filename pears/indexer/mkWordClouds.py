###############################################
# Make word clouds for document vectors
###############################################

import os
import sys

import numpy as np
from scipy.spatial import distance
from pears.utils import sim_to_matrix
from pears import db
from pears.models import Urls

###########################################
# Compute profile
###########################################

def computeWordClouds():
    wordclouds = {}  # Store vectors for this user in order to compute coherence
    # Open document distributions file
    urls = Urls.query.all()
    for l in urls:
        url = l.url
        doc_dist = filter(None, l.dists.split(' '))
        vdocdist = np.array([float(i) for i in doc_dist])
        if np.linalg.norm(vdocdist) > 0.0:
            topics, topics_s = sim_to_matrix(vdocdist, 10)
            l.wordclouds = topics_s
        # print url, topics_s
    db.session.commit()


###################
# Entry point
###################
def runScript():
    print "Computing wordclouds for local user..."
    computeWordClouds()


if __name__ == '__main__':
    # when executing as script
    runScript()
