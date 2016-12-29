import os, cStringIO
import time, requests, ipgetter, numpy
from sqlalchemy.types import PickleType
import getpass
import socket

from numpy import linalg, array, dot, sqrt, math

from .models import OpenVectors, Profile
from pears import db

stopwords = ["", "(", ")", "a", "about", "an", "and", "are", "around", "as", "at", "away", "be", "become", "became",
             "been", "being", "by", "did", "do", "does", "during", "each", "for", "from", "get", "have", "has", "had",
             "her", "his", "how", "i", "if", "in", "is", "it", "its", "made", "make", "many", "most", "of", "on", "or",
             "s", "some", "that", "the", "their", "there", "this", "these", "those", "to", "under", "was", "were",
             "what", "when", "where", "who", "will", "with", "you", "your"]

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def readDM():
    """ Read dm file (but only top 10,000 words) """
    c = 0
    dm_dict = {}
    # Make dictionary with key=row, value=vector
    profile = Profile.query.first()
    if not profile:
        user = getpass.getuser()
        profile = Profile(name=unicode(user))
    dmlines = [(each.word, each.vector) for each in
            OpenVectors.query.all()]
    for l in dmlines:
        if c < 10000:
            vects = [float(each) for each in l[1].split(',')]
            dm_dict[l[0]] = normalise(vects)
            c += 1
        else:
            break
    return dm_dict

def sim_to_matrix(vec, n):
    """ Compute similarities and return top n """
    dm_dict = readDM()
    cosines = {}
    for k, v in dm_dict.items():
        cos = cosine_similarity(numpy.array(vec), numpy.array(v))
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

def normalise(v):
    norm = linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def cosine_similarity(peer_v, query_v):
    if len(peer_v) != len(query_v):
        raise ValueError("Peer vector and query vector must be "
                         " of same length")
    num = dot(peer_v, query_v)
    den_a = dot(peer_v, peer_v)
    den_b = dot(query_v, query_v)
    return num / (sqrt(den_a) * sqrt(den_b))


def load_entropies(entropies_file='demo/ukwac.entropy.txt'):
    entropies_dict = {}
    with open(entropies_file, "r") as entropies:
        for line in entropies:
            word, score = line.split('\t')
            word = word.lower()
            # Must have this cos lower() can match two instances of the same word in the list
            if word.isalpha() and word not in entropies_dict:
                entropies_dict[word] = float(score)

    return entropies_dict


def query_distribution(query, entropies):
    """ Make distribution for query """
    words = query.rstrip('\n').split()

    # Only retain arguments which are in the distributional semantic space
    vecs_to_add = []
    for word in words:
        word_db = OpenVectors.query.filter(OpenVectors.word == word).first()
        if word_db:
            vecs_to_add.append(word_db)
        else:
            word = word[0].upper() + word[1:]  # Did user carelessly forget to capitalise a proper noun?
            word_db = OpenVectors.query.filter(OpenVectors.word == word).first()
            if word_db:
                vecs_to_add.append(word_db)

    vbase = array([])
    # Add vectors together
    if vecs_to_add:
        # Take first word in vecs_to_add to start addition
        vbase = array([float(i) for i in vecs_to_add[0].vector.split(',')])
        for vec in vecs_to_add[1:]:
            if vec.word in entropies and math.log(entropies[vec.word] + 1) > 0:
                weight = float(1) / float(math.log(entropies[vec.word] + 1))
                vbase = vbase + weight * array([float(i) for i in vec.vector.split(',')])
            else:
                vbase = vbase + array([float(i) for i in vec.vector.split(',')])

    vbase = normalise(vbase)
    return vbase


def read_pears(pears):
    profile = Profile.query.first()
    my_ip = ipgetter.myip()
    # my_ip =  ([l for l in ([ip for ip in
        # socket.gethostbyname_ex(socket.gethostname())[2] if not
        # ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
            # s.getsockname()[0], s.close()) for s in
            # [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]])
        # if l][0][0])
    pears_dict = {}
    if not pears:
      p = profile.vector
      val = cStringIO.StringIO(str(p))
      pears_dict[my_ip] = numpy.loadtxt(val)
    else:
      for ip in pears:
        if ip == my_ip:
          p = profile.vector
        else:
          p = requests.get("http://{}:5000/api/profile".format(ip)).text
          val =      cStringIO.StringIO(str(p))
          pears_dict[ip] = numpy.loadtxt(val)
    return pears_dict

def print_timing(func):
    """ Timing function, just to know how long things take """
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s in scorePages took %0.3f ms' % (func.func_name, (t2 - t1) * 1000.0)
        return res

    return wrapper
