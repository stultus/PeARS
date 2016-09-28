from flask import Blueprint

indexer = Blueprint('indexer', __name__)
import views

import retrieve_raw_data
