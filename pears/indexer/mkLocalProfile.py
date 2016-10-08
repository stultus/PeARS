""" Make user profiles by adding document vectors """

import os
import sys

import numpy as np
from scipy.spatial import distance
from pears.models import OpenVectors, Urls
import runDistSemWeighted
from pears.utils import normalise, cosine_similarity
from pears import db, profile

stopwords = ["", "i", "a", "about", "an", "and", "each", "are", "as", "at", "be", "are", "were", "being", "by", "do",
             "does", "did", "for", "from", "how", "in", "is", "it", "its", "make", "made", "of", "on", "or", "s",
             "that", "the", "this", "to", "was", "what", "when", "where", "who", "will", "with", "has", "had", "have",
             "he", "she", "one", "also", "his", "her", "their", "only", "both", "they", "however", "then", "later",
             "but", "never", "which", "many"]
num_dimensions = 400
dm_dict = {}


def readUsers(usernames_file):
    """ Read list of users """
    # print "Getting users..."
    users = []
    f = open(usernames_file, 'r')
    for l in f:
        l = l.rstrip('\n')
        users.append(l)
    f.close()
    return users



def readDM():
    """ Read dm file (but only top 10,000 words) """
    c = 0
    # Make dictionary with key=row, value=vector
    dmlines = [(each.word, each.vector) for each in
            OpenVectors.query.all()]
    for l in dmlines:
        if c < 10000:
            vects = [float(each) for each in l[1].split(',')]
            dm_dict[l[0]] = normalise(vects)
            c += 1
        else:
            break



def sim_to_matrix(vec, n):
    """ Compute similarities and return top n """
    cosines = {}
    for k, v in dm_dict.items():
        cos = cosine_similarity(np.array(vec), np.array(v))
        cosines[k] = cos

    topics = []
    topics_s = ""
    c = 0
    for t in sorted(cosines, key=cosines.get, reverse=True):
        if c < n:
            if t.isalpha() and t not in stopwords:
                # print t,cosines[t]
                topics.append(t)
                topics_s += t + " "
                c += 1
        else:
            break
    return topics, topics_s[:-1]


def coherence(vecs):
    coh = 0.0
    counter = 0
    if len(vecs) > 1:
        matrix = np.array(vecs)
        # print matrix
        dist_m = distance.cdist(matrix, matrix, 'cosine')
        # print dist_m
        for i in range(0, len(vecs) - 1):
            for j in range(i + 1, len(vecs)):
                cosine = 1 - dist_m[i][j]
                # print cosine
                coh += cosine
                counter += 1
        coh = float(coh) / float(counter)
    else:
        coh = 1
    # print coh
    return coh


def computePearDist(pear):
    vbase = np.zeros(num_dimensions)
    vecs_for_coh = []  # Store vectors for this user in order to compute coherence
    # Open document distributions file
    urls = Urls.query.all()
    for l in urls:
        doc_dist = filter(None, l.dists.split(' '))
        vdocdist = np.array([float(i) for i in doc_dist])
        vbase = vbase + vdocdist
        if np.linalg.norm(vdocdist) > 0.0:
            vecs_for_coh.append(vdocdist)

    vbase = normalise(vbase)
    # Make string version of distribution
    dist_str = ""
    for n in vbase:
        dist_str = dist_str + "%.6f" % n + " "
    dist_str = dist_str.rstrip(' ')

    # coh=0
    coh = coherence(vecs_for_coh)
    # print coh
    return vbase, dist_str, coh


def createProfileFile(pear, pear_dist, topics_s, coh):
    profile.topics = topics_s
    profile.coherence = str(coh)
    profile.vector = pear_dist
    db.session.add(profile)
    db.session.commit()


def runScript():
    readDM()
    runDistSemWeighted.runScript(dm_dict)
    print "Computing pear for local history..."
    user = profile.name
    v, print_v, coh = computePearDist(user)
    topics, topics_s = sim_to_matrix(v, 20)
    createProfileFile(user, print_v, topics_s, coh)


# PERHAPS PEAR NOT FOUND?

if __name__ == '__main__':
    # when executing as script
    runScript("./local-history/documents.txt")
