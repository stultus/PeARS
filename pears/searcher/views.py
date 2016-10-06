#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request, Blueprint
import requests, json
from ast import literal_eval

from . import searcher

from pears import best_pears
from pears import scorePages
from pears.utils import read_pears, query_distribution, load_entropies

def get_result_from_dht(query_dist):
    url = 'http://localhost:8080'
    headers = {'content-type': 'application/json', 'Accept-Charset':
            'UTF-8', 'Connection': 'close'}
    query_str  = ' '.join([each.strip('\n\[\]') for each in str(query_dist).split(' ')])
    r = requests.post(url, data=json.dumps(query_str), headers=headers)
    result = [r.text.split('\n')[-1]] if r else []
    return result

@searcher.route('/')
@searcher.route('/index')
def index():
    pages = []
    entropies_dict = load_entropies()
    query = request.args.get('q')
    if not query:
        return render_template("index.html")
    else:
        query_dist = query_distribution(query, entropies_dict)
        pears = get_result_from_dht(query_dist)
        pear_profiles = read_pears(pears)
        pear_details = best_pears.find_best_pears(query_dist, pear_profiles)
        if len(pear_details) == 0:
            pears = [['nopear',
                      'Sorry... no pears found :(',
                      './static/pi-pic.png']]
        else:
            pear_ips = pear_details.keys()
            pages = scorePages.runScript(query, query_dist, pear_ips)

        # '''remove the following lines after testing'''
        # pages = [['http://test.com', 'test']]

        return render_template('results.html', pears=pears,
                               query=query, results=pages)
