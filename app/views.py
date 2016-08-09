#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, request

import best_pears
import scorePages
from app import app
from app.utils import read_pears, query_distribution, load_entropies


@app.route('/')
@app.route('/index')
def index():
    pages = []
    entropies_dict = load_entropies()
    query = request.args.get('q')
    if not query:
        return render_template("index.html")
    else:
        query_dist = query_distribution(query, entropies_dict)
        pears_ids = read_pears()
        pears = best_pears.find_best_pears(query_dist, pears_ids)
        if len(pears) == 0:
            pears = [['nopear',
                      'Sorry... no pears found :(',
                      './static/pi-pic.png']]
            print pears
        else:
            pear_names = []
            for p in pears:
                pear_names.append(p[0])
                print p
                pages = scorePages.runScript(query, query_dist, pear_names)

        # '''remove the following lines after testing'''
        # pages = [['http://test.com', 'test']]

        return render_template('results.html', pears=pears,
                               query=query, results=pages)
