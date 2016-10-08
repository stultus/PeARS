#!/usr/bin/env python

from flask import Flask, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
import getpass

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('config')

from .models import Profile
user = getpass.getuser()
profiles = Profile.query.all()
if profiles:
    profile = profiles[0]
else:
    profile = Profile(name=user)

from pears import models, searcher, indexer, api

app.register_blueprint(searcher.searcher)
app.register_blueprint(indexer.indexer)
app.register_blueprint(api.api)

@app.teardown_appcontext
def teardown_db(exception):
    if db is not None:
        db.session.close()
