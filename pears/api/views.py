#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pears.models import Profile, Urls
from . import api


@api.route('/api/profile')
def get_profile():
    return Profile.query.first().vector

@api.route('/api/urls')
def get_urls():
    urls = Urls.query.all()
    return str([u.__dict__ for u in urls])
