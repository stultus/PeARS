from pears.indexer import retrieve_raw_data,hierarchClustering,mkLocalProfile
import os, sys


def index_browser_history():
    num_pages=50
    retrieve_raw_data.runScript(num_pages)

if __name__=="__main__":
    index_browser_history()
    hierarchClustering.runScript(0.6)
    mkLocalProfile.runScript()
